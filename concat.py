import os
import subprocess
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from natsort import natsorted

class VideoConcatenatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MP4 Concatenator")
        self.root.geometry("500x300")

        # Input folder selection
        tk.Label(root, text="Select Input Folder:").pack(pady=5)
        self.input_entry = tk.Entry(root, width=50)
        self.input_entry.pack(pady=5)
        tk.Button(root, text="Browse", command=self.select_input_folder).pack(pady=5)

        # Output file selection
        tk.Label(root, text="Select Output File:").pack(pady=5)
        self.output_entry = tk.Entry(root, width=50)
        self.output_entry.pack(pady=5)
        tk.Button(root, text="Browse", command=self.select_output_file).pack(pady=5)

        # Start button
        self.start_button = tk.Button(root, text="Start Concatenation", command=self.start_concatenation)
        self.start_button.pack(pady=10)

        # Progress bar
        self.progress = ttk.Progressbar(root, length=400, mode="indeterminate")
        self.progress.pack(pady=10)

    def select_input_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, folder)

    def select_output_file(self):
        file = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 Files", "*.mp4")])
        if file:
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, file)

    def start_concatenation(self):
        input_folder = self.input_entry.get()
        output_file = self.output_entry.get()

        if not input_folder or not output_file:
            messagebox.showerror("Error", "Please select both input folder and output file.")
            return

        self.start_button.config(state=tk.DISABLED)
        self.progress.start()

        threading.Thread(target=self.concatenate_videos, args=(input_folder, output_file), daemon=True).start()

    def concatenate_videos(self, input_folder, output_file):
        try:
            # Find all MP4 files
            mp4_files = []
            for folder, _, files in sorted(os.walk(input_folder)):
                for file in files:
                    if file.lower().endswith(".mp4"):
                        mp4_files.append(os.path.join(folder, file))

            mp4_files = natsorted(mp4_files)

            if not mp4_files:
                messagebox.showerror("Error", "No MP4 files found in the selected folder.")
                return

            # Write file list for FFmpeg
            list_file = "file_list.txt"
            with open(list_file, "w") as f:
                for file in mp4_files:
                    f.write(f"file '{file}'\n")

            # Run FFmpeg
            subprocess.run(["ffmpeg", "-f", "concat", "-y", "-safe", "0", "-i", list_file, "-vcodec", "copy", "-an", output_file])

            # Clean up
            os.remove(list_file)

            messagebox.showinfo("Success", f"Videos concatenated successfully:\n{output_file}")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{e}")

        finally:
            self.start_button.config(state=tk.NORMAL)
            self.progress.stop()

# Run the GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = VideoConcatenatorApp(root)
    root.mainloop()
