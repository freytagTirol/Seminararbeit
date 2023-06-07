import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar

from main import main

# Initialize the Tkinter application
root = tk.Tk()
root.title("Script GUI")

# Global variables
selected_folder = ""
ai_option = tk.BooleanVar()
cut_option = tk.BooleanVar()
test_option = tk.BooleanVar()
progress_value = tk.DoubleVar()


# Function to select a folder
def select_folder():
    global selected_folder
    selected_folder = filedialog.askdirectory()
    folder_label.config(text=selected_folder)


# Function to start the script
def start_script():
    global selected_folder
    global ai_option
    global cut_option
    global test_option

    if not selected_folder:
        messagebox.showwarning("Warning", "Please select a folder.")
        return

    # Set the options
    ai = ai_option.get()
    cut = cut_option.get()
    test = test_option.get()

    # Disable the start button
    start_button.config(state="disabled")

    # Call the main script function
    main(ai, cut, test)

    # Enable the start button
    start_button.config(state="normal")

    # Show completion message
    messagebox.showinfo("Script Completed", "The script has finished running.")


# Function to update the progress bar
def update_progress(progress):
    progressbar["value"] = progress


# Function to exit the application
def exit_app():
    root.destroy()


# Create the GUI elements
folder_button = tk.Button(root, text="Select Folder", command=select_folder)
folder_button.pack(pady=10)

folder_label = tk.Label(root, text="")
folder_label.pack()

ai_checkbox = tk.Checkbutton(root, text="AI", variable=ai_option)
ai_checkbox.pack()
ai_checkbox.select()

cut_checkbox = tk.Checkbutton(root, text="Cut", variable=cut_option)
cut_checkbox.pack()
cut_checkbox.select()

cut_checkbox = tk.Checkbutton(root, text="Test", variable=test_option)
cut_checkbox.pack()

start_button = tk.Button(root, text="Start", command=start_script)
start_button.pack(pady=10)

progressbar = Progressbar(root, orient=tk.HORIZONTAL, length=200, mode='determinate', variable=progress_value)
progressbar.pack(pady=10)

exit_button = tk.Button(root, text="Exit", command=exit_app)
exit_button.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()


if __name__ == '__main__':
    start_script()
