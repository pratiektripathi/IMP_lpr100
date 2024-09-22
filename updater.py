import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import requests
import os

def download_file():
    url = url_entry.get()
    save_path = filedialog.asksaveasfilename(title="Save File As", initialfile=os.path.basename(url))
    
    if not url or not save_path:
        messagebox.showerror("Error", "URL or save path not provided.")
        return

    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Check if the request was successful
        
        # Get the total file size
        total_size = int(response.headers.get('content-length', 0))
        progress_bar['maximum'] = total_size
        
        with open(save_path, 'wb') as file:
            downloaded_size = 0
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:  # Filter out keep-alive new chunks
                    file.write(chunk)
                    downloaded_size += len(chunk)
                    progress_bar['value'] = downloaded_size
                    root.update_idletasks()
                    
        messagebox.showinfo("Success", f"File downloaded successfully and saved to {save_path}.")
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Failed to download file: {e}")
    finally:
        progress_bar['value'] = 0

# Set up the GUI
root = tk.Tk()
root.title("File Downloader")

tk.Label(root, text="File URL:").pack(pady=5)
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

download_button = tk.Button(root, text="Download", command=download_file)
download_button.pack(pady=20)

progress_bar = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
progress_bar.pack(pady=10)

root.mainloop()