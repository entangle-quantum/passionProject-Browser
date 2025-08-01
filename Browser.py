# Welcome to PyBrowser
# A simple Python web browser interface using Tkinter and webbrowser module.
import webbrowser
import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog
import json
import os

HISTORY_FILE = "history.json"
BOOKMARKS_FILE = "bookmarks.json"
SETTINGS_FILE = "settings.json"

def load_json(filename, default=None):
    if os.path.exists(filename):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return default if default is not None else []
    return default if default is not None else []

def save_json(filename, data):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f)
    except Exception as e:
        messagebox.showerror("Save Error", f"Could not save {filename}: {e}")

def is_valid_url(url):
    return url.startswith("https://") or url.startswith("http://")

history = load_json(HISTORY_FILE, [])
bookmarks = load_json(BOOKMARKS_FILE, [])
settings = load_json(SETTINGS_FILE, {"homepage": "https://www.google.com"})

def on_open():
    url = url_entry.get().strip()
    if not url:
        messagebox.showerror("Invalid URL", "URL cannot be empty.")
        return
    if is_valid_url(url):
        webbrowser.open(url)
        if url not in history:
            history.append(url)
            save_json(HISTORY_FILE, history)
        update_history()
    else:
        messagebox.showerror("Invalid URL", "Please enter a valid http:// or https:// URL.")

def on_clear():
    url_entry.delete(0, tk.END)

def on_bookmark():
    url = url_entry.get().strip()
    if url and is_valid_url(url):
        if url not in bookmarks:
            bookmarks.append(url)
            save_json(BOOKMARKS_FILE, bookmarks)
            update_bookmarks()
            messagebox.showinfo("Bookmarked", f"Bookmarked: {url}")
        else:
            messagebox.showinfo("Already Bookmarked", "URL is already bookmarked.")
    else:
        messagebox.showerror("Invalid URL", "Please enter a valid http:// or https:// URL.")

def update_history():
    history_list.delete(0, tk.END)
    for url in history[-10:][::-1]:
        history_list.insert(tk.END, url)

def update_bookmarks():
    bookmark_list.delete(0, tk.END)
    for url in bookmarks:
        bookmark_list.insert(tk.END, url)

def on_history_select(event):
    selection = history_list.curselection()
    if selection:
        url_entry.delete(0, tk.END)
        url_entry.insert(0, history_list.get(selection[0]))

def on_bookmark_select(event):
    selection = bookmark_list.curselection()
    if selection:
        url_entry.delete(0, tk.END)
        url_entry.insert(0, bookmark_list.get(selection[0]))

def on_set_homepage():
    homepage = simpledialog.askstring("Set Homepage", "Enter homepage URL:", initialvalue=settings.get("homepage", ""))
    if homepage and is_valid_url(homepage):
        settings["homepage"] = homepage
        save_json(SETTINGS_FILE, settings)
        messagebox.showinfo("Homepage Set", f"Homepage set to: {homepage}")
    else:
        messagebox.showerror("Invalid URL", "Please enter a valid http:// or https:// URL.")

def on_open_homepage():
    homepage = settings.get("homepage", "")
    if homepage and is_valid_url(homepage):
        url_entry.delete(0, tk.END)
        url_entry.insert(0, homepage)
        on_open()
    else:
        messagebox.showerror("No Homepage", "No valid homepage set.")

def on_import_bookmarks():
    file_path = filedialog.askopenfilename(title="Import Bookmarks", filetypes=[("JSON Files", "*.json")])
    if file_path:
        imported = load_json(file_path, [])
        if isinstance(imported, list):
            for url in imported:
                if is_valid_url(url) and url not in bookmarks:
                    bookmarks.append(url)
            save_json(BOOKMARKS_FILE, bookmarks)
            update_bookmarks()
            messagebox.showinfo("Import", "Bookmarks imported.")
        else:
            messagebox.showerror("Import Error", "Invalid bookmarks file.")

def on_export_bookmarks():
    file_path = filedialog.asksaveasfilename(title="Export Bookmarks", defaultextension=".json", filetypes=[("JSON Files", "*.json")])
    if file_path:
        save_json(file_path, bookmarks)
        messagebox.showinfo("Export", "Bookmarks exported.")

def on_open_all_bookmarks():
    if bookmarks:
        for url in bookmarks:
            if is_valid_url(url):
                webbrowser.open(url)
    else:
        messagebox.showinfo("No Bookmarks", "No bookmarks to open.")

def on_search():
    query = search_entry.get().strip()
    if query:
        url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        url_entry.delete(0, tk.END)
        url_entry.insert(0, url)
        on_open()
    else:
        messagebox.showerror("Empty Search", "Please enter a search query.")

def on_copy_url():
    url = url_entry.get().strip()
    if url:
        root.clipboard_clear()
        root.clipboard_append(url)
        messagebox.showinfo("Copied", "URL copied to clipboard.")

def on_paste_url():
    try:
        url = root.clipboard_get()
        url_entry.delete(0, tk.END)
        url_entry.insert(0, url)
    except Exception:
        messagebox.showerror("Paste Error", "Clipboard is empty or invalid.")

def on_delete_bookmark():
    selection = bookmark_list.curselection()
    if selection:
        url = bookmark_list.get(selection[0])
        bookmarks.remove(url)
        save_json(BOOKMARKS_FILE, bookmarks)
        update_bookmarks()

def on_delete_history():
    selection = history_list.curselection()
    if selection:
        url = history_list.get(selection[0])
        history.remove(url)
        save_json(HISTORY_FILE, history)
        update_history()

def on_delete_all_bookmarks():
    if messagebox.askyesno("Delete All", "Delete all bookmarks?"):
        bookmarks.clear()
        save_json(BOOKMARKS_FILE, bookmarks)
        update_bookmarks()

def on_delete_all_history():
    if messagebox.askyesno("Delete All", "Delete all history?"):
        history.clear()
        save_json(HISTORY_FILE, history)
        update_history()

def on_about():
    messagebox.showinfo("About PyBrowser",
        "PyBrowser\nA simple Python browser launcher.\n\nFeatures:\n- History & Bookmarks\n- Homepage\n- Import/Export Bookmarks\n- Open All Bookmarks\n- Search\n- Clipboard\n- Delete entries\n- Drag-and-drop\n- Settings\n- Keyboard shortcuts"
    )

def on_drag(event):
    url_entry.delete(0, tk.END)
    url_entry.insert(0, event.data)

def bind_shortcuts():
    root.bind('<Control-o>', lambda e: on_open())
    root.bind('<Control-b>', lambda e: on_bookmark())
    root.bind('<Control-h>', lambda e: on_open_homepage())
    root.bind('<Control-c>', lambda e: on_copy_url())
    root.bind('<Control-v>', lambda e: on_paste_url())
    root.bind('<Control-q>', lambda e: root.quit())

root = tk.Tk()
root.title("PyBrowser")

# Menu
menu = tk.Menu(root)
root.config(menu=menu)
settings_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Settings", menu=settings_menu)
settings_menu.add_command(label="Set Homepage", command=on_set_homepage)
settings_menu.add_command(label="Open Homepage", command=on_open_homepage)
settings_menu.add_separator()
settings_menu.add_command(label="Import Bookmarks", command=on_import_bookmarks)
settings_menu.add_command(label="Export Bookmarks", command=on_export_bookmarks)
settings_menu.add_separator()
settings_menu.add_command(label="About", command=on_about)

# Search
search_frame = tk.Frame(root)
search_frame.pack(pady=5)
tk.Label(search_frame, text="Search:").pack(side=tk.LEFT)
search_entry = tk.Entry(search_frame, width=30)
search_entry.pack(side=tk.LEFT, padx=5)
tk.Button(search_frame, text="Search", command=on_search).pack(side=tk.LEFT)

# URL Entry
tk.Label(root, text="Enter URL (with http:// or https://):").pack(pady=5)
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

btn_frame = tk.Frame(root)
btn_frame.pack(pady=5)
tk.Button(btn_frame, text="Open in Browser", command=on_open).pack(side=tk.LEFT, padx=5)
tk.Button(btn_frame, text="Bookmark", command=on_bookmark).pack(side=tk.LEFT, padx=5)
tk.Button(btn_frame, text="Clear", command=on_clear).pack(side=tk.LEFT, padx=5)
tk.Button(btn_frame, text="Copy", command=on_copy_url).pack(side=tk.LEFT, padx=5)
tk.Button(btn_frame, text="Paste", command=on_paste_url).pack(side=tk.LEFT, padx=5)

lists_frame = tk.Frame(root)
lists_frame.pack(pady=10)

tk.Label(lists_frame, text="History (last 10):").grid(row=0, column=0)
tk.Label(lists_frame, text="Bookmarks:").grid(row=0, column=1)

history_list = tk.Listbox(lists_frame, width=40, height=6)
history_list.grid(row=1, column=0, padx=5)
history_list.bind('<<ListboxSelect>>', on_history_select)
tk.Button(lists_frame, text="Delete Selected", command=on_delete_history).grid(row=2, column=0, pady=2)
tk.Button(lists_frame, text="Delete All", command=on_delete_all_history).grid(row=3, column=0, pady=2)

bookmark_list = tk.Listbox(lists_frame, width=40, height=6)
bookmark_list.grid(row=1, column=1, padx=5)
bookmark_list.bind('<<ListboxSelect>>', on_bookmark_select)
tk.Button(lists_frame, text="Delete Selected", command=on_delete_bookmark).grid(row=2, column=1, pady=2)
tk.Button(lists_frame, text="Delete All", command=on_delete_all_bookmarks).grid(row=3, column=1, pady=2)
tk.Button(lists_frame, text="Open All", command=on_open_all_bookmarks).grid(row=4, column=1, pady=2)

update_history()
update_bookmarks()
bind_shortcuts()

root.mainloop()
