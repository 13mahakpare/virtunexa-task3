import markdown
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import webbrowser
import time

# Create a default folder to save HTML files
SAVE_FOLDER = "converted_files"
os.makedirs(SAVE_FOLDER, exist_ok=True)

# Function to read Markdown file
def read_markdown_file(filename):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return None

# Function to convert Markdown to HTML
def convert_markdown_to_html(md_content):
    return markdown.markdown(md_content)

# Function to generate full HTML
def generate_full_html(html_content):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Converted Markdown</title>
</head>
<body style="font-family: Arial, sans-serif; margin: 20px;">
    {html_content}
</body>
</html>"""

# Function to simulate progress
def update_progress():
    for i in range(1, 101, 10):
        progress_bar["value"] = i
        root.update_idletasks()
        time.sleep(0.1)
    progress_bar["value"] = 100

# Function to save temporary HTML file for preview
def save_html_temp(html_content):
    temp_filename = "temp_preview.html"
    full_html = generate_full_html(html_content)
    with open(temp_filename, "w", encoding="utf-8") as file:
        file.write(full_html)
    return temp_filename

# Function to select a Markdown file
def select_file():
    global output_filepath
    filepath = filedialog.askopenfilename(filetypes=[("Markdown Files", "*.md")])

    if not filepath:
        return

    file_label.config(text=f"Selected File: {os.path.basename(filepath)}", fg="green")

    md_content = read_markdown_file(filepath)

    if md_content:
        # Start progress
        update_progress()
        
        html_output = convert_markdown_to_html(md_content)
        temp_file = save_html_temp(html_output)
        output_filepath = None

        view_button.config(state=tk.NORMAL)

        choice = messagebox.askyesno("Save File?", "Do you want to save the converted HTML file?")
        if choice:
            save_html_file(html_output, filepath)
    else:
        messagebox.showerror("Error", "Invalid Markdown file.")

# Function to save HTML file in default folder
def save_html_file(html_content, input_filepath):
    global output_filepath
    base_name = os.path.basename(input_filepath).replace(".md", ".html")
    output_filepath = os.path.join(SAVE_FOLDER, base_name)

    full_html = generate_full_html(html_content)
    with open(output_filepath, "w", encoding="utf-8") as file:
        file.write(full_html)
    
    messagebox.showinfo("Success", f"HTML file saved: {output_filepath}")
    download_button.config(state=tk.NORMAL)

# Function to download file to custom location
def download_file():
    if output_filepath:
        save_path = filedialog.asksaveasfilename(defaultextension=".html",
                                                 filetypes=[("HTML Files", "*.html")])
        if save_path:
            os.rename(output_filepath, save_path)
            messagebox.showinfo("Success", f"File saved as: {save_path}")

# Function to view file
def view_file():
    temp_file = "temp_preview.html"
    if os.path.exists(temp_file):
        webbrowser.open(temp_file)
    elif output_filepath and os.path.exists(output_filepath):
        webbrowser.open(output_filepath)
    else:
        messagebox.showerror("Error", "No converted file available to view.")

# Creating GUI
root = tk.Tk()
root.title("Markdown to HTML Converter")
root.geometry("500x450")
root.configure(bg="#2C3E50")


from PIL import Image, ImageTk  # Import Pillow

# Load and resize the icon
try:
    img = Image.open("markicon.png")  # Load the image
    img = img.resize((100, 100), Image.LANCZOS)  
    icon = ImageTk.PhotoImage(img)

    icon_label = tk.Label(root, image=icon, bg="#f5f5f5")
    icon_label.pack(pady=5)
except Exception as e:
    print("Error loading image:", e)


label = tk.Label(root, text="Markdown to HTML Converter", font=("verdana", 18, "bold"), bg="#2C3E50", fg="white")
label.pack(pady=30)  # Increased padding to move everything down

desc_label = tk.Label(root, text="Select a Markdown file and convert it into an HTML document.", font=("verdana", 14), bg="#2C3E50", fg="white")
desc_label.pack(pady=5)

file_label = tk.Label(root, text="No file selected", font=("Arial", 11), bg="#f5f5f5", fg="red")
file_label.pack(pady=5)

progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
progress_bar.pack(pady=5)

select_button = tk.Button(root, text="Choose File", command=select_file, font=("Arial", 12), bg="#3498db", fg="white", width=20)
select_button.pack(pady=5)

view_button = tk.Button(root, text="View HTML File", command=view_file, font=("Arial", 12), bg="#f39c12", fg="white", width=20, state=tk.DISABLED)
view_button.pack(pady=5)

download_button = tk.Button(root, text="Download HTML File", command=download_file, font=("Arial", 12), bg="#27ae60", fg="white", width=20, state=tk.DISABLED)
download_button.pack(pady=5)

exit_button = tk.Button(root, text="Exit", command=root.quit, font=("Arial", 12), bg="#e74c3c", fg="white", width=20)
exit_button.pack(pady=10)

# Run the GUI
root.mainloop()
