import subprocess
import sys
import os
import shutil
import threading
import tkinter as tk
from tkinter import messagebox
from pathlib import Path

user_profile = Path(os.environ["USERPROFILE"])
base_dir = user_profile / "NedroGraph"
project_dir = base_dir / "NedroGraph_repo"
windows_folder = project_dir / "Windows version"
linux_folder = project_dir / "Linux version"
min_ver = (3, 9)
max_ver = (3, 12)
choice = None
create_shortcut = False
shortcut_var = None
version_accept = False
install = False
REPO_URL = "https://github.com/zgorov41-design/NedroGraph.git"
BASE_DIR = str(windows_folder)
DIR_APP = str(windows_folder / "app.py")
DIR_GUI = str(windows_folder / "GUI_Nedrograph.py")
ICON_SERVER_PATH = str(windows_folder / "images" / "server.ico")
ICON_PATH = str(windows_folder / "images" / "icon.ico")

command1 = ('$s=(New-Object -ComObject WScript.Shell).CreateShortcut('
           '[Environment]::GetFolderPath("Desktop")+"\\Server.lnk"); '
           f'$s.TargetPath="{DIR_APP}"; $s.WorkingDirectory="{BASE_DIR}"; '
           f'$s.IconLocation="{ICON_SERVER_PATH}"; $s.Save()')

command2 = ('$s=(New-Object -ComObject WScript.Shell).CreateShortcut('
           '[Environment]::GetFolderPath("Desktop")+"\\NedroGraph.lnk"); '
           f'$s.TargetPath="{DIR_GUI}"; $s.WorkingDirectory="{BASE_DIR}"; '
           f'$s.IconLocation="{ICON_PATH}"; $s.Save()')


root = tk.Tk()
root.title("NedroGraph — install")
root.geometry("400x350")

label = tk.Label(root, text="Choose action", font=("Arial", 14))
label.pack(pady=30)

status = tk.Label(root, text="", font=("Arial", 12), fg="gray", width=40, anchor="center")
status.pack(pady=5)

def set_status(text):
    root.after(0, lambda: status.config(text=text))

def find_system_python():
    for cmd in ("py", "python", "python3"):
        if shutil.which(cmd) is None:
            continue
        try:
            proc = subprocess.run([cmd, "--version"], capture_output=True, text=True, shell=True)
            out = ((proc.stdout or "") + (proc.stderr or "")).strip()
            if "Python" in out:
                parts = out.replace("Python ", "").strip().split(".")
                if len(parts) >= 2 and parts[0].isdigit() and parts[1].isdigit():
                    return cmd, (int(parts[0]), int(parts[1])), f"{parts[0]}.{parts[1]}.{parts[2] if len(parts) > 2 else '0'}"
        except Exception:
            continue
    return None, None, None

def get_python_version():
    if getattr(sys, "frozen", False):
        return find_system_python()
    full = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    py_cmd = sys.executable
    return py_cmd, (sys.version_info.major, sys.version_info.minor), full

def install_python_312():
    set_status("Installing python 3.12...")
    try:
        subprocess.run("winget install --id Python.Python.3.12 -e --accept-package-agreements --scope machine", shell=True, check=True)
        messagebox.showinfo("NedroGraph", "Python 3.12 installed.\nRestart the installer — PATH will be updated only in a new session.")
    except Exception as e:
        messagebox.showerror("Installation error", f"Failed to install Python:\n{e}")
    root.destroy()

def ask_install_python(reason):
    def do_ask():
        answer = messagebox.askyesno("Python", reason)
        if answer:
            threading.Thread(target=install_python_312, daemon=True).start()
        else:
            status.config(text="Installing is cancelled")
            root.after(1200, root.destroy)
    root.after(0, do_ask)

def install_requirements(py_cmd):
    set_status("Installing requirements...")
    try:
        subprocess.run(f'"{py_cmd}" -m pip install Flask==2.3.3 Werkzeug==2.3.7 Flask-SocketIO==5.3.6 gevent==24.2.1 gevent-websocket==0.10.1', shell=True, check=True, capture_output=True, text=True)
        set_status("Requirements installed")
    except subprocess.CalledProcessError as e:
        err = e.stderr or str(e)
        root.after(0, lambda: messagebox.showerror("Installation error", f"Error installing dependencies:\n{err}"))
        raise

def install_worker():
    global version_accept, install
    try:
        set_status("Checking Python version...")
        py_cmd, ver_tuple, full = get_python_version()

        if ver_tuple is None:
            root.after(0, lambda: ask_install_python("Python isn't installed. Install 3.12.10?"))
            return

        set_status(f"Detected: Python {full}")

        if min_ver <= ver_tuple <= max_ver:
            version_accept = True
        else:
            root.after(0, lambda: ask_install_python(f"Python {full} isn't acceptable. Install 3.12.10?"))
            return

        install = True
        if version_accept and install:
            install_requirements(py_cmd)
            set_status("Cloning repository...")
            base_dir.mkdir(parents=True, exist_ok=True)
            if not project_dir.exists():
                subprocess.run(["git", "clone", REPO_URL, str(project_dir)], capture_output=True, text=True, check=True)
            if choice == "win":
                if windows_folder.exists() and linux_folder.exists():
                    shutil.rmtree(linux_folder)
                if create_shortcut:
                    subprocess.run(["powershell", "-NoProfile", "-Command", command1], check=True)
                    subprocess.run(["powershell", "-NoProfile", "-Command", command2], check=True)
            elif choice == "linux":
                if linux_folder.exists() and windows_folder.exists():
                    shutil.rmtree(windows_folder)
                if create_shortcut:
                    subprocess.run(["powershell", "-NoProfile", "-Command", command1], check=True)
                    subprocess.run(["powershell", "-NoProfile", "-Command", command2], check=True)
            root.after(0, show_final_window)
    except subprocess.CalledProcessError as e:
        msg = f"Command failed:\n{e.stderr or e}"
        root.after(0, lambda: messagebox.showerror("Installation error", msg))
        root.after(0, root.destroy)
    except Exception as e:
        msg = str(e)
        root.after(0, lambda: messagebox.showerror("Installation error", msg))
        root.after(0, root.destroy)

def show_version_buttons():
    global btn_install, shortcut_var
    btn_install.pack_forget()
    label.config(text="Choose version:", fg="black")
    shortcut_var = tk.BooleanVar(value=True)
    tk.Checkbutton(root, text="Create shortcut?", variable=shortcut_var, font=("Arial", 12)).pack(pady=5)
    tk.Button(root, text="Windows version", command=lambda: set_choice("win"), width=25, height=2, bg="#3498eb", fg="white").pack(pady=10)
    tk.Button(root, text="Linux version", command=lambda: set_choice("linux"), width=25, height=2, bg="#c26819", fg="white").pack(pady=10)

def run_install():
    threading.Thread(target=install_worker, daemon=True).start()

def show_final_window():
    label.config(text="")
    set_status("")
    final = tk.Toplevel(root)
    final.title("NedroGraph")
    final.geometry("300x160")
    final.grab_set()
    tk.Label(final, text="Process is final", font=("Arial", 14)).pack(pady=30)
    tk.Button(final, text="OK", width=12, command=root.destroy).pack(pady=5)

def set_choice(value):
    global choice, create_shortcut
    create_shortcut = shortcut_var.get()
    choice = value
    label.config(text="Processing...", fg="black")
    root.after(500, run_install)

def on_install_click():
    show_version_buttons()

btn_install = tk.Button(root, text="Install program?", command=on_install_click, width=25, height=2, bg="#4CAF50", fg="white")
btn_install.pack(pady=10)

root.mainloop()
