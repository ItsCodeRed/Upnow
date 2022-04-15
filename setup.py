from cx_Freeze import setup, Executable

setup(name = "Upnow",
    version = "1.0",
    description = "Reminds you to stand.",
    executables = [Executable("reminders.py", base = "Win32GUI")])

# to build the app, run the following command:
# python setup.py build