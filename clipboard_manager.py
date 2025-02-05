import rumps
from AppKit import NSPasteboard, NSStringPboardType
import json
import os

class ClipboardManagerApp(rumps.App):
    def __init__(self):
        super(ClipboardManagerApp, self).__init__("📎 Clippy")
        self.history = []
        self.history_file = os.path.expanduser("~/.clipboard_history.json")
        self.load_history()
        self.menu = self.build_menu()

        # Add static menu items (only once)
        self.menu.clear()  # Clear the default menu
        self.menu.add(rumps.MenuItem("Clear History", callback=self.clear_history))
        self.menu.add(rumps.separator)  # Add a separator line
        self.update_history_menu()  # Add clipboard history items

    def build_menu(self):
        return []  # Return an empty menu 

    def update_history_menu(self):
        # Remove existing history items
        for item in list(self.menu.values()):  # Use list to avoid modifying while iterating
            if hasattr(item, "title") and item.title not in ["Clear History", "Quit"]:  # Skip static items
                self.menu.pop(str(item.title))  # Convert title to string

        # Add updated history items
        for item in self.history:
            self.menu.add(rumps.MenuItem(item, callback=self.copy_to_clipboard))

    def load_history(self):
        if os.path.exists(self.history_file):
            with open(self.history_file, "r") as f:
                self.history = json.load(f)

    def save_history(self):
        with open(self.history_file, "w") as f:
            json.dump(self.history, f)

    def add_to_history(self, text):
        if text and text not in self.history:
            self.history.append(text)
            if len(self.history) > 20:  # Limit history size
                self.history.pop(0)
            self.save_history()
            self.update_history_menu()  # Update the menu with new history

    def clear_history(self, _):
        self.history = []
        self.save_history()
        self.update_history_menu()  # Update the menu after clearing history

    def copy_to_clipboard(self, sender):
        pasteboard = NSPasteboard.generalPasteboard()
        pasteboard.clearContents()
        pasteboard.setString_forType_(sender.title, NSStringPboardType)

    @rumps.timer(1)  # Check clipboard every second
    def check_clipboard(self, _):
        pasteboard = NSPasteboard.generalPasteboard()
        clipboard_content = pasteboard.stringForType_(NSStringPboardType)
        if clipboard_content and (not self.history or clipboard_content != self.history[-1]):
            self.add_to_history(clipboard_content)

if __name__ == "__main__":
    app = ClipboardManagerApp()
    app.run()