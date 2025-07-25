# Welcome to PyBrowser
# A simple Python web browser interface using Tkinter and webbrowser module.
import webbrowser
import tkinter as tk
from tkinter import messagebox
import json
import os

HISTORY_FILE = "history.json"
BOOKMARKS_FILE = "bookmarks.json"

def load_json(filename):
    if os.path.exists(filename):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_json(filename, data):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f)
    except Exception as e:
        messagebox.showerror("Save Error", f"Could not save {filename}: {e}")

history = load_json(HISTORY_FILE)
bookmarks = load_json(BOOKMARKS_FILE)

def on_open():
    url = url_entry.get().strip()
    if not url:
        messagebox.showerror("Invalid URL", "URL cannot be empty.")
        return
    if url.startswith("https://") or url.startswith("http://"):
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
    if url and (url.startswith("https://") or url.startswith("http://")):
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
    for url in history[-10:][::-1]:  # Show last 10, newest first
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

root = tk.Tk()
root.title("PyBrowser")

tk.Label(root, text="Enter URL (with http:// or https://):").pack(pady=5)
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

btn_frame = tk.Frame(root)
btn_frame.pack(pady=5)
tk.Button(btn_frame, text="Open in Browser", command=on_open).pack(side=tk.LEFT, padx=5)
tk.Button(btn_frame, text="Bookmark", command=on_bookmark).pack(side=tk.LEFT, padx=5)
tk.Button(btn_frame, text="Clear", command=on_clear).pack(side=tk.LEFT, padx=5)

lists_frame = tk.Frame(root)
lists_frame.pack(pady=10)

tk.Label(lists_frame, text="History (last 10):").grid(row=0, column=0)
tk.Label(lists_frame, text="Bookmarks:").grid(row=0, column=1)

history_list = tk.Listbox(lists_frame, width=40, height=6)
history_list.grid(row=1, column=0, padx=5)
history_list.bind('<<ListboxSelect>>', on_history_select)

bookmark_list = tk.Listbox(lists_frame, width=40, height=6)
bookmark_list.grid(row=1, column=1, padx=5)
bookmark_list.bind('<<ListboxSelect>>', on_bookmark_select)

update_history()
update_bookmarks()

root.mainloop()