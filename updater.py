import tkinter as tk
import zipfile
import io
import os
import shutil
import json
import aiohttp
import asyncio
import requests

class MainApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Updater")
        xcord = (self.winfo_screenwidth() / 2) - 150
        ycord = (self.winfo_screenheight() / 2) - 75
        self.ucd = 0
        self.geometry("300x150" + "+" + str(int(xcord)) + "+" + str(int(ycord)))
        self.dot = tk.StringVar()
        self.resizable(False, False)

        self.frame1 = tk.Frame(self, bg="#ADD8E0")
        self.label1 = tk.Label(self.frame1, text="Checking For Update", font=("Arquitecta", 12), bg="#ADD8E0")
        self.label1.grid(row=0, column=0, pady=5)

        self.label2 = tk.Label(self.frame1, textvariable=self.dot, font=("Arquitecta", 16), fg="red", bg="#ADD8E0")
        self.dot.set("")
        self.label2.grid(row=1, column=0, pady=5)

        self.button1 = tk.Button(self.frame1, text="Download & Update", font=("Arquitecta", 12), bg="#ADD8E0",
                                 command=self.start_download)
        self.button1.grid(row=2, column=0, pady=5)
        self.button1.grid_remove()
        self.frame1.pack(fill="both", expand=True)

        self.check()

    def check(self):
        self.ucd += 1
        cup = False
        if self.ucd > 5:
            cup = self.update_check()

        if self.ucd < 20 and not cup:
            if len(self.dot.get()) < 5:
                self.dot.set(self.dot.get() + "*")
            else:
                self.dot.set("")
            self.after(500, self.check)

        elif self.ucd < 20 and cup:
            self.dot.set("update available")
            self.button1.grid()
        else:
            self.dot.set("update not available")

    def start_download(self):
        # Schedule the async download task
        self.dot.set("downloading")
        self.button1.grid_remove()
        self.update_idletasks()
        asyncio.run(self.download())

    async def download(self):
        await self.do_update()

    async def download_github_repo(self, zip_url, extract_to="temp_repo"):
        async with aiohttp.ClientSession() as session:
            async with session.get(zip_url) as response:
                if response.status == 200:
                    data = await response.read()
                    with zipfile.ZipFile(io.BytesIO(data)) as zip_ref:
                        zip_ref.extractall(extract_to)
                else:
                    self.dot.set(f"Failed to download repository: {response.status}")

    def update_files(self, source_folder, destination_folder):
        if not os.path.exists(source_folder):
            self.dot.set(f"Source folder '{source_folder}' does not exist.")
            return

        for root, dirs, files in os.walk(source_folder):
            relative_path = os.path.relpath(root, source_folder)
            dest_dir = os.path.join(destination_folder, relative_path)
            os.makedirs(dest_dir, exist_ok=True)

            for file in files:
                source_file = os.path.join(root, file)
                dest_file = os.path.join(dest_dir, file)
                shutil.copy2(source_file, dest_file)

        print(f"All files from '{source_folder}' have been updated to '{destination_folder}'.")

    def update_check(self):
        url = "https://raw.githubusercontent.com/pratiektripathi/lpr100exe/main/version.json"
        old = json.load(open('version.json'))
        try:
            response = requests.get(url)
            if response.status_code == 200:
                content = response.content.decode('utf-8')
                version_info = json.loads(content)
                if old['version'] < version_info['version']:
                    return True
            else:
                return False
        except:
            return False

    async def do_update(self):
        try:
            repo_url = "https://github.com/pratiektripathi/lpr100exe/archive/refs/heads/main.zip"
            extract_folder = "temp_repo/lpr100exe-main"
            destination_folder = os.getcwd()

            await self.download_github_repo(repo_url)
            self.update_files(extract_folder, destination_folder)
            
            self.dot.set("update complete")
        except:
            self.dot.set("update failed")
            
        shutil.rmtree("temp_repo")

if __name__ == '__main__':
    app = MainApp()
    app.mainloop()
