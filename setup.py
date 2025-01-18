import sys
from cx_Freeze import setup, Executable

# Dependencies
build_exe_options = {
    "packages": ["tkinter", "customtkinter"],
    "excludes": [],
    "include_files": []
}

# Base for GUI applications
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="SRTeew",
    version="1.0",
    description="SRT Subtitle Editor with Easy Workflow",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py", base=base, target_name="SRTeew.exe", icon="image.ico")]
) 