import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import os

from services.validator_service import process_file

selected_file = None


def browse_file():
    global selected_file

    selected_file = filedialog.askopenfilename(
        title="Select Catalogue Excel",
        filetypes=[
            ("Excel Files", "*.xlsx *.xlsm")
        ]
    )

    if selected_file:
        file_label.config(text=os.path.basename(selected_file))


def validate():
    if not selected_file:
        messagebox.showwarning(
            "No File",
            "Please select an Excel file."
        )
        return

    status.config(text="Validating... Please wait")

    def run():
        try:
            result = process_file(selected_file)

            status.config(text="Validation Complete!")

            messagebox.showinfo(
                "Success",
                result
            )

        except Exception as e:
            messagebox.showerror(
                "Error",
                str(e)
            )

    threading.Thread(target=run).start()


root = tk.Tk()
root.title("Catalogue Validation Tool")
root.geometry("500x250")

tk.Label(
    root,
    text="Catalogue Validation Tool",
    font=("Arial", 18, "bold")
).pack(pady=20)

file_label = tk.Label(
    root,
    text="No file selected"
)
file_label.pack()

tk.Button(
    root,
    text="Browse Excel",
    command=browse_file,
    width=20
).pack(pady=10)

tk.Button(
    root,
    text="Validate",
    command=validate,
    width=20
).pack()

status = tk.Label(
    root,
    text=""
)
status.pack(pady=20)

root.mainloop()