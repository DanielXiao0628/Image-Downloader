import os
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from tkinter import Tk, Label, Entry, Button, filedialog, messagebox, StringVar, N, S, E, W
from tkinter.ttk import Progressbar
import threading

def download_images(url, folder_path, progress_var, update_progress, notify_completion):
    try:
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception("Failed to retrieve the webpage")
        
        soup = BeautifulSoup(response.text, 'html.parser')
        img_tags = soup.find_all('img')
        urls = [img.get('src') for img in img_tags if img.get('src')]

        if not urls:
            raise Exception("No images found on the webpage")

        for i, img_url in enumerate(urls):
            img_url = urljoin(url, img_url)
            try:
                img_data = requests.get(img_url).content
                img_name = f'image_{i+1}.jpg'
                with open(os.path.join(folder_path, img_name), 'wb') as f:
                    f.write(img_data)

                update_progress(progress_var, i + 1, len(urls))
            except Exception as e:
                print(f"Error downloading {img_url}: {e}")

        notify_completion("Success", "Images downloaded successfully")
    except Exception as e:
        notify_completion("Error", f"An error occurred: {e}")

def start_download_thread():
    url = url_entry.get()
    folder_path = folder_entry.get()
    if not url or not folder_path:
        messagebox.showinfo("Info", "Please enter both URL and folder path")
        return

    progress_var.set(0)  # Reset progress bar
    download_thread = threading.Thread(target=download_images, args=(url, folder_path, progress_var, update_progress, lambda title, message: messagebox.showinfo(title, message)))
    download_thread.start()

def update_progress(progress_var, current, total):
    progress = int((current / total) * 100)
    progress_var.set(progress)
    root.update_idletasks()

root = Tk()
root.title("Image Downloader")
root.geometry("450x150")  # Adjust window size

# Variables
progress_var = StringVar(value="0")

# Layout adjustments
Label(root, text="Webpage URL:").grid(row=0, column=0, sticky=W, padx=10, pady=5)
url_entry = Entry(root, width=40)
url_entry.grid(row=0, column=1, padx=10, pady=5)

Label(root, text="Save to folder:").grid(row=1, column=0, sticky=W, padx=10, pady=5)
folder_entry = Entry(root, width=40)
folder_entry.grid(row=1, column=1, padx=10, pady=5)
Button(root, text="Browse", command=lambda: folder_entry.insert(0, filedialog.askdirectory())).grid(row=1, column=2, sticky=E, padx=10, pady=5)

Button(root, text="Download Images", command=start_download_thread).grid(row=2, column=0, columnspan=3, padx=10, pady=5)

progress_bar = Progressbar(root, length=300, variable=progress_var, mode='determinate')
progress_bar.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky=E+W)

root.mainloop()
