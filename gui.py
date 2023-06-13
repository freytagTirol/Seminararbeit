import os.path
import tkinter as tk
from tkinter import filedialog, messagebox
from idlelib.tooltip import Hovertip

from main import main

selected_folder = None
selected_excel = None
ai_option = None
cut_option = None
folder_label = None
excel_label = None
api_key_entry = None
start_button = None


def start_gui():
    global selected_folder
    global selected_excel
    global ai_option
    global cut_option
    global folder_label
    global excel_label
    global api_key_entry
    global start_button

    # Initialize the Tkinter application
    root = tk.Tk()
    root.title("Seminararbeit")
    # root.geometry("200x230")
    root.geometry("600x300")
    # root.resizable(False, False)

    # Global variables
    selected_folder = ""
    selected_excel = ""
    ai_option = tk.BooleanVar()
    cut_option = tk.BooleanVar()

    # test_option = tk.BooleanVar()
    # progress_value = tk.DoubleVar()

    # Create the GUI elements

    api_key_label = tk.Label(root, text="API Key")
    api_key_label.grid(row=0)
    api_key_entry = tk.Entry(root)
    api_key_entry.grid(pady=10, row=0, column=1)
    api_key_tt_text = "Enter your OpenAI API key here"
    Hovertip(api_key_label, text=api_key_tt_text)
    Hovertip(api_key_entry, text=api_key_tt_text)

    folder_button = tk.Button(root, text="Select Folder", command=select_folder)
    folder_button.grid(pady=10, columnspan=2)
    Hovertip(folder_button, text="Select source folder containing the MD&A .txt files")

    folder_label = tk.Label(root, text="")
    folder_label.grid(columnspan=2)

    excel_button = tk.Button(root, text="Select Excel", command=select_excel)
    excel_button.grid(pady=10, columnspan=2)
    Hovertip(excel_button, text="Select the Excel file containing the litigation data")

    excel_label = tk.Label(root, text="")
    excel_label.grid(columnspan=2)

    ai_checkbox = tk.Checkbutton(root, text="AI", variable=ai_option)
    ai_checkbox.grid(columnspan=2)
    ai_checkbox.select()
    Hovertip(ai_checkbox, text="Uncheck this box to use the keyword analysis instead of AI")

    cut_checkbox = tk.Checkbutton(root, text="Cut", variable=cut_option)
    cut_checkbox.grid(columnspan=2)
    cut_checkbox.select()
    Hovertip(cut_checkbox, text="Check this box to cut the MD&A texts instead of creating summaries")

    # test_checkbox = tk.Checkbutton(root, text="Test", variable=test_option)
    # test_checkbox.grid(columnspan=2)

    start_button = tk.Button(root, text="Start", command=start_script)
    start_button.grid(pady=20, columnspan=2)

    # progressbar = Progressbar(root, orient=tk.HORIZONTAL, length=200, mode='determinate', variable=progress_value)
    # progressbar.grid(columnspan=2)

    # exit_button = tk.Button(root, text="Exit", command=exit_app)
    # exit_button.grid(columnspan=2)

    # Start the Tkinter event loop
    root.mainloop()


# Function to select a folder
def select_folder():
    global selected_folder
    global folder_label
    selected_folder = filedialog.askdirectory()
    folder_label.config(text=selected_folder)


# Function to select the Excel table
def select_excel():
    global selected_excel
    global excel_label
    selected_excel = filedialog.askopenfilename(filetypes=[("Excel files", ".xlsx .xls")])
    excel_label.config(text=selected_excel)


# Function to start the script
def start_script():
    global selected_folder
    global selected_excel
    global ai_option
    global cut_option
    global api_key_entry
    global start_button

    print("DEBUG: We are in start_script")

    # Set the options
    ai = ai_option.get()
    cut = cut_option.get()
    # test = test_option.get()
    api_key = api_key_entry.get()

    if not selected_folder:
        messagebox.showwarning("Warning", "Please select a folder.")
    if not api_key:
        messagebox.showwarning("Warning", "Please enter your API Key.")
    if not selected_excel:
        messagebox.showwarning("Warning", "Please select an Excel table.")

    print(f'DEBUG: selected_folder: "{selected_folder}"')
    print(f'DEBUG: api_key: "{api_key}"')
    print(f'DEBUG: selected_excel: "{selected_excel}"')
    if not selected_folder or not selected_excel or not api_key_entry:
        return

    print("DEBUG: We are about to disable the button")
    # Disable the start button
    start_button.config(state="disabled")

    # Call the main script function
    main(src=selected_folder,
         excel_path=selected_excel,
         ai=ai,
         cut=cut,
         api_key=api_key)

    # Enable the start button
    start_button.config(state="normal")

    # Show completion message
    messagebox.showinfo("Success",
                        f'All files have been analyzed. Find the results in {selected_folder}/res')


# # Function to update the progress bar
# def update_progress(progress):
#     progressbar["value"] = progress


# # Function to exit the application
# def exit_app():
#     root.destroy()


if __name__ == '__main__':
    start_gui()
