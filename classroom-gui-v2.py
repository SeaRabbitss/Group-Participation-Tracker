import tkinter as tk
from tkinter import ttk, messagebox
import csv
import random

class ClassroomGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Classroom Participation Tracker")
        
        # Set window size and make it non-resizable
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        
        # Define color scheme
        self.colors = {
            'bg': '#f0f0f0',  # Light gray background
            'button': '#4a90e2',  # Pleasant blue for buttons
            'frame': '#ffffff',  # White for frames
            'text': '#333333'  # Dark gray for text
        }
        
        # Configure root window background
        self.root.configure(bg=self.colors['bg'])
        
        # Configure style
        self.style = ttk.Style()
        self.style.configure('TFrame', background=self.colors['frame'])
        self.style.configure('TLabelframe', background=self.colors['frame'])
        self.style.configure('TLabelframe.Label', background=self.colors['frame'])
        self.style.configure('TButton', 
                           padding=5,
                           background=self.colors['button'],
                           foreground=self.colors['text'])
        self.style.configure('Desk.TButton',
                           padding=10,
                           width=15,
                           font=('Arial', 10))
        
        # Store student desks
        self.students = {}  # Dictionary to store student name: participation count
        
        # Create main frame with padding and background
        self.main_frame = ttk.Frame(root, padding="20", style='TFrame')
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create left control panel
        self.create_control_panel()
        
        # Create classroom display area
        self.create_classroom_display()

    def create_control_panel(self):
        # Left panel frame
        control_frame = ttk.Frame(self.main_frame, padding="10")
        control_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10)
        
        # Export to CSV button
        ttk.Button(control_frame, text="Export to CSV", command=self.export_csv).grid(row=0, column=0, pady=5, sticky='ew')
        
        # Reset buttons
        ttk.Button(control_frame, text="Reset Tracking", command=self.reset_tracking).grid(row=1, column=0, pady=5, sticky='ew')
        ttk.Button(control_frame, text="Reset Classroom", command=self.reset_classroom).grid(row=2, column=0, pady=5, sticky='ew')
        
        # Add/Remove student controls
        add_frame = ttk.LabelFrame(control_frame, text="Add Student", padding="10")
        add_frame.grid(row=3, column=0, pady=10, sticky='ew')
        self.add_student_entry = ttk.Entry(add_frame)
        self.add_student_entry.grid(row=0, column=0, pady=5, padx=5, sticky='ew')
        ttk.Button(add_frame, text="Add Student", command=self.add_student).grid(row=1, column=0, pady=5, sticky='ew')
        
        remove_frame = ttk.LabelFrame(control_frame, text="Remove Student", padding="10")
        remove_frame.grid(row=4, column=0, pady=10, sticky='ew')
        self.remove_student_entry = ttk.Entry(remove_frame)
        self.remove_student_entry.grid(row=0, column=0, pady=5, padx=5, sticky='ew')
        ttk.Button(remove_frame, text="Remove Student", command=self.remove_student).grid(row=1, column=0, pady=5, sticky='ew')
        
        # Select student frame
        select_frame = ttk.LabelFrame(control_frame, text="Select Student", padding="10")
        select_frame.grid(row=5, column=0, pady=10, sticky='ew')
        self.selected_student_var = tk.StringVar()
        ttk.Label(select_frame, textvariable=self.selected_student_var).grid(row=0, column=0, pady=5)
        ttk.Button(select_frame, text="Select Student", command=self.select_random_student).grid(row=1, column=0, pady=5, sticky='ew')

    def create_classroom_display(self):
        # Classroom display frame
        self.classroom_frame = ttk.Frame(self.main_frame, padding="10")
        self.classroom_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10)
        self.update_classroom_display()

    def update_classroom_display(self):
        # Clear existing display
        for widget in self.classroom_frame.winfo_children():
            widget.destroy()
        
        # Create student desk buttons
        row = 0
        col = 0
        for student, count in self.students.items():
            desk = ttk.Button(self.classroom_frame, 
                            text=f"{student}\n{count}",
                            style='Desk.TButton',
                            command=lambda s=student: self.increment_participation(s))
            desk.grid(row=row, column=col, padx=10, pady=10)
            col += 1
            if col > 2:  # 3 desks per row
                col = 0
                row += 1

    def export_csv(self):
        try:
            with open('classroom.csv', 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=['name', 'participation'])
                writer.writeheader()
                for student, count in self.students.items():
                    writer.writerow({'name': student, 'participation': count})
            messagebox.showinfo("Success", "Classroom exported successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export classroom: {str(e)}")

    def reset_tracking(self):
        for student in self.students:
            self.students[student] = 0
        self.update_classroom_display()
        messagebox.showinfo("Success", "Participation counts reset to 0!")

    def reset_classroom(self):
        self.students.clear()
        self.update_classroom_display()
        messagebox.showinfo("Success", "Classroom reset!")

    def add_student(self):
        name = self.add_student_entry.get().strip()
        if name:
            if name in self.students:
                messagebox.showerror("Error", "Student already exists!")
            else:
                self.students[name] = 0
                self.update_classroom_display()
                self.add_student_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Please enter a student name!")

    def remove_student(self):
        name = self.remove_student_entry.get().strip()
        if name:
            if name in self.students:
                del self.students[name]
                self.update_classroom_display()
                self.remove_student_entry.delete(0, tk.END)
            else:
                messagebox.showerror("Error", "Student not found!")
        else:
            messagebox.showerror("Error", "Please enter a student name!")

    def select_random_student(self):
        if self.students:
            # Find the minimum participation count
            min_count = min(self.students.values())
            
            # Get all students with the minimum count
            min_students = [student for student, count in self.students.items() 
                        if count == min_count]
            
            # Select the alphabetically first student
            selected = min(min_students)
            
            self.selected_student_var.set(selected)
            # Increment participation count for selected student
            self.increment_participation(selected)
        else:
            messagebox.showerror("Error", "No students in classroom!")

    def increment_participation(self, student):
        self.students[student] += 1
        self.update_classroom_display()

if __name__ == "__main__":
    root = tk.Tk()
    app = ClassroomGUI(root)
    app.update_classroom_display()
    root.mainloop()