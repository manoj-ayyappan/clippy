from setuptools import setup

APP = ["clipboard_manager.py"]
DATA_FILES = ["clipboard_history.json"]  # Add any required files here
OPTIONS = {
    "argv_emulation": True,
    "plist": {
        "LSUIElement": True,
        "CFBundleName": "ClipboardManager",
        "CFBundleDisplayName": "Clipboard Manager",
        "CFBundleIdentifier": "com.yourname.clipboardmanager",
        "CFBundleVersion": "1.0.0",
        "CFBundleShortVersionString": "1.0.0",
    },
    "packages": ["rumps", "pyobjc", "AppKit"],  # Explicitly include pyobjc and AppKit
    "includes": ["pyobjc"],  # Ensure pyobjc is included
    "excludes": ["Carbon"],  # Exclude Carbon framework (if not needed)
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={"py2app": OPTIONS},
    setup_requires=["py2app"],
)