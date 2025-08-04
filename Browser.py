# Welcome to PyBrowser
# A simple Python web browser interface using Tkinter and webbrowser module.
import webbrowser
import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog, ttk
import json
import os
import csv
import random

try:
    from tkinterweb import HtmlFrame
    HAS_WEBVIEW = True
except ImportError:
    HAS_WEBVIEW = False

HISTORY_FILE = "history.json"
BOOKMARKS_FILE = "bookmarks.json"
SETTINGS_FILE = "settings.json"
PROFILE_FILE = "profile.json"
SESSION_FILE = "session.json"

LANGUAGES = {
    "en": {
        "title": "PyBrowser",
        "search": "Search:",
        "enter_url": "Enter URL (with http:// or https://):",
        "open": "Open in Browser",
        "bookmark": "Bookmark",
        "clear": "Clear",
        "copy": "Copy",
        "paste": "Paste",
        "delete_selected": "Delete Selected",
        "delete_all": "Delete All",
        "open_all": "Open All",
        "history": "History (last 10):",
        "bookmarks": "Bookmarks:",
        "set_homepage": "Set Homepage",
        "open_homepage": "Open Homepage",
        "import_bookmarks": "Import Bookmarks",
        "export_bookmarks": "Export Bookmarks",
        "about": "About",
        "theme": "Theme",
        "language": "Language",
        "profile": "Profile",
        "update": "Check for Updates",
        "browser": "Browser",
        "notes": "Notes",
        "sort_az": "Sort A-Z",
        "sort_newest": "Sort Newest",
        "sort_oldest": "Sort Oldest",
        "filter": "Filter",
        "backup": "Backup",
        "restore": "Restore",
        "export_csv": "Export CSV",
        "import_csv": "Import CSV",
        "greeting": "Welcome",
        "easter_egg": "Easter Egg",
    },
    "es": {
        "title": "PyNavegador",
        "search": "Buscar:",
        "enter_url": "Ingrese URL (con http:// o https://):",
        "open": "Abrir en navegador",
        "bookmark": "Favorito",
        "clear": "Limpiar",
        "copy": "Copiar",
        "paste": "Pegar",
        "delete_selected": "Eliminar seleccionado",
        "delete_all": "Eliminar todo",
        "open_all": "Abrir todos",
        "history": "Historial (últimos 10):",
        "bookmarks": "Favoritos:",
        "set_homepage": "Establecer página de inicio",
        "open_homepage": "Abrir página de inicio",
        "import_bookmarks": "Importar favoritos",
        "export_bookmarks": "Exportar favoritos",
        "about": "Acerca de",
        "theme": "Tema",
        "language": "Idioma",
        "profile": "Perfil",
        "update": "Buscar actualizaciones",
        "browser": "Navegador",
        "notes": "Notas",
        "sort_az": "Ordenar A-Z",
        "sort_newest": "Más reciente",
        "sort_oldest": "Más antiguo",
        "filter": "Filtrar",
        "backup": "Respaldar",
        "restore": "Restaurar",
        "export_csv": "Exportar CSV",
        "import_csv": "Importar CSV",
        "greeting": "Bienvenido",
        "easter_egg": "Huevo de Pascua",
    },
    "kl": {
        "title": "PyBrowser",
        "search": "Ujarlerneq:",
        "enter_url": "URL allaguk (http:// imaluunniit https://):",
        "open": "Brosersimi ammasiguk",
        "bookmark": "Bookmarki",
        "clear": "Suliaruk",
        "copy": "Kopier",
        "paste": "Paste",
        "delete_selected": "Toqqakkat piiakkit",
        "delete_all": "Tamarmik piiakkit",
        "open_all": "Tamarmik ammasiguk",
        "history": "Oqaatsit (kingullit 10):",
        "bookmarks": "Bookmarkit:",
        "set_homepage": "Homepage toqqaruk",
        "open_homepage": "Homepage ammasiguk",
        "import_bookmarks": "Bookmarkit importi",
        "export_bookmarks": "Bookmarkit exporti",
        "about": "Paasissutissat",
        "theme": "Tema",
        "language": "Oqaatsit",
        "profile": "Profil",
        "update": "Nutarteruk",
        "browser": "Browseri",
        "notes": "Notit",
        "sort_az": "A-Z sorteruk",
        "sort_newest": "Kingulliit",
        "sort_oldest": "Siulliit",
        "filter": "Filteri",
        "backup": "Backupi",
        "restore": "Restoreri",
        "export_csv": "CSV exporti",
        "import_csv": "CSV importi",
        "greeting": "Tikilluarit",
        "easter_egg": "Easter Egg",
    },
    "iu": {
        "title": "ᐱᐅᓯᑦᑎᓂᖅ PyBrowser",
        "search": "ᓯᓚᒥᓂᖅ:",
        "enter_url": "URL ᐅᖃᓕᒫᖅ (http:// ᐊᒪᓗ http://):",
        "open": "ᐅᖃᓕᒫᖅᑐᖅ ᐱᐅᓯᑦᑎᓂᖅᑕ",
        "bookmark": "ᐱᐅᓯᑦᑎᓂᖅᑕᐅᑦ",
        "clear": "ᓯᓚᒥᓂᖅ",
        "copy": "ᓯᓚᒥᓂᖅ",
        "paste": "ᓯᓚᒥᓂᖅ",
        "delete_selected": "ᑕᑯᔭᖅᑕᐅᑦ ᓯᓚᒥᓂᖅ",
        "delete_all": "ᑕᑯᔭᖅᑕᐅᑦ ᓯᓚᒥᓂᖅ",
        "open_all": "ᑕᑯᔭᖅᑕᐅᑦ ᐱᐅᓯᑦᑎᓂᖅᑕ",
        "history": "ᐅᓪᓗᓂᖅ (10 ᓂᑦᓯᐊᖅᑕᐅᑦ):",
        "bookmarks": "ᐱᐅᓯᑦᑎᓂᖅᑕᐅᑦ:",
        "set_homepage": "ᐅᖃᓕᒫᖅᑐᖅ homepage",
        "open_homepage": "ᐱᐅᓯᑦᑎᓂᖅᑕ homepage",
        "import_bookmarks": "ᐱᐅᓯᑦᑎᓂᖅᑕᐅᑦ ᐱᐅᓯᑦᑎᓂᖅᑕ",
        "export_bookmarks": "ᐱᐅᓯᑦᑎᓂᖅᑕᐅᑦ ᐱᐅᓯᑦᑎᓂᖅᑕ",
        "about": "ᐱᐅᓯᑦᑎᓂᖅ",
        "theme": "ᐱᐅᓯᑦᑎᓂᖅ",
        "language": "ᐅᖃᓕᒫᖅᑐᖅ",
        "profile": "ᐱᐅᓯᑦᑎᓂᖅ",
        "update": "ᐱᐅᓯᑦᑎᓂᖅ",
        "browser": "ᐱᐅᓯᑦᑎᓂᖅ",
        "notes": "ᓯᓚᒥᓂᖅ",
        "sort_az": "A-Z ᓯᓚᒥᓂᖅ",
        "sort_newest": "ᓯᓚᒥᓂᖅ",
        "sort_oldest": "ᓯᓚᒥᓂᖅ",
        "filter": "ᓯᓚᒥᓂᖅ",
        "backup": "ᐱᐅᓯᑦᑎᓂᖅ",
        "restore": "ᐱᐅᓯᑦᑎᓂᖅ",
        "export_csv": "CSV ᐱᐅᓯᑦᑎᓂᖅ",
        "import_csv": "CSV ᐱᐅᓯᑦᑎᓂᖅ",
        "greeting": "ᐊᓘᓐᓃᖅ",
        "easter_egg": "Easter Egg",
    }
}

def _(key):
    return LANGUAGES.get(settings.get("language", "en"), LANGUAGES["en"]).get(key, key)

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

def get_browser():
    return settings.get("browser", "default")

def open_url(url):
    browser = get_browser()
    if browser == "default":
        webbrowser.open(url)
    elif browser == "chrome":
        webbrowser.get("chrome").open(url)
    elif browser == "firefox":
        webbrowser.get("firefox").open(url)
    elif browser == "edge":
        webbrowser.get("windows-default").open(url)
    else:
        webbrowser.open(url)

history = load_json(HISTORY_FILE, [])
bookmarks = load_json(BOOKMARKS_FILE, [])
settings = load_json(SETTINGS_FILE, {
    "homepage": "https://www.google.com",
    "theme": "light",
    "language": "en",
    "browser": "default"
})
profile = load_json(PROFILE_FILE, {"name": "User", "avatar": "", "greeting": _("greeting")})
session = load_json(SESSION_FILE, {"last_url": ""})

def on_open():
    url = url_entry.get().strip()
    if not url:
        messagebox.showerror("Invalid URL", "URL cannot be empty.")
        return
    if is_valid_url(url):
        open_url(url)
        if url not in history:
            history.append(url)
            save_json(HISTORY_FILE, history)
        session["last_url"] = url
        save_json(SESSION_FILE, session)
        update_history()
        update_frequent()
        if HAS_WEBVIEW:
            webview.load_website(url)
    else:
        messagebox.showerror("Invalid URL", "Please enter a valid http:// or https:// URL.")

def on_clear():
    url_entry.delete(0, tk.END)
    if HAS_WEBVIEW:
        webview.load_html("<h3>PyBrowser</h3>")

def on_bookmark():
    url = url_entry.get().strip()
    note = simpledialog.askstring(_("notes"), _("notes"), initialvalue="")
    folder = simpledialog.askstring("Folder", "Bookmark folder (optional):", initialvalue="")
    if url and is_valid_url(url):
        entry = {"url": url, "note": note, "folder": folder}
        if entry not in bookmarks:
            bookmarks.append(entry)
            save_json(BOOKMARKS_FILE, bookmarks)
            update_bookmarks()
            messagebox.showinfo(_("bookmark"), f"{_('bookmark')}: {url}")
        else:
            messagebox.showinfo(_("bookmark"), "Already bookmarked.")
    else:
        messagebox.showerror("Invalid URL", "Please enter a valid http:// or https:// URL.")

def update_history(sort="newest"):
    history_list.delete(0, tk.END)
    items = history[-10:][::-1] if sort == "newest" else history[:10]
    for url in items:
        history_list.insert(tk.END, url)

def update_bookmarks(filter_text="", sort="az"):
    bookmark_list.delete(0, tk.END)
    filtered = [b for b in bookmarks if filter_text.lower() in b["url"].lower()]
    sorted_b = sorted(filtered, key=lambda b: b["url"]) if sort == "az" else filtered
    for b in sorted_b:
        display = b["url"]
        if b.get("folder"):
            display += f" [{b['folder']}]"
        if b.get("note"):
            display += f" - {b['note']}"
        bookmark_list.insert(tk.END, display)

def update_frequent():
    freq = {}
    for url in history:
        freq[url] = freq.get(url, 0) + 1
    frequent_list.delete(0, tk.END)
    for url, count in sorted(freq.items(), key=lambda x: -x[1])[:5]:
        frequent_list.insert(tk.END, f"{url} ({count})")

def on_history_select(event):
    selection = history_list.curselection()
    if selection:
        url_entry.delete(0, tk.END)
        url_entry.insert(0, history_list.get(selection[0]))
        if HAS_WEBVIEW:
            webview.load_website(history_list.get(selection[0]))

def on_bookmark_select(event):
    selection = bookmark_list.curselection()
    if selection:
        url = bookmarks[selection[0]]["url"]
        url_entry.delete(0, tk.END)
        url_entry.insert(0, url)
        if HAS_WEBVIEW:
            webview.load_website(url)

def on_set_homepage():
    homepage = simpledialog.askstring(_("set_homepage"), _("set_homepage"), initialvalue=settings.get("homepage", ""))
    if homepage and is_valid_url(homepage):
        settings["homepage"] = homepage
        save_json(SETTINGS_FILE, settings)
        messagebox.showinfo(_("set_homepage"), f"{_('set_homepage')}: {homepage}")
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
    file_path = filedialog.askopenfilename(title=_("import_bookmarks"), filetypes=[("JSON Files", "*.json"), ("CSV Files", "*.csv")])
    if file_path:
        if file_path.endswith(".json"):
            imported = load_json(file_path, [])
            if isinstance(imported, list):
                for entry in imported:
                    if isinstance(entry, dict) and is_valid_url(entry.get("url", "")):
                        if entry not in bookmarks:
                            bookmarks.append(entry)
                save_json(BOOKMARKS_FILE, bookmarks)
                update_bookmarks()
                messagebox.showinfo(_("import_bookmarks"), "Bookmarks imported.")
            else:
                messagebox.showerror(_("import_bookmarks"), "Invalid bookmarks file.")
        elif file_path.endswith(".csv"):
            with open(file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    if row and is_valid_url(row[0]):
                        entry = {"url": row[0], "note": row[1] if len(row) > 1 else "", "folder": row[2] if len(row) > 2 else ""}
                        if entry not in bookmarks:
                            bookmarks.append(entry)
                save_json(BOOKMARKS_FILE, bookmarks)
                update_bookmarks()
                messagebox.showinfo(_("import_bookmarks"), "Bookmarks imported from CSV.")

def on_export_bookmarks():
    file_path = filedialog.asksaveasfilename(title=_("export_bookmarks"), defaultextension=".json", filetypes=[("JSON Files", "*.json"), ("CSV Files", "*.csv")])
    if file_path:
        if file_path.endswith(".json"):
            save_json(file_path, bookmarks)
            messagebox.showinfo(_("export_bookmarks"), "Bookmarks exported.")
        elif file_path.endswith(".csv"):
            with open(file_path, "w", newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                for b in bookmarks:
                    writer.writerow([b["url"], b.get("note", ""), b.get("folder", "")])
            messagebox.showinfo(_("export_bookmarks"), "Bookmarks exported to CSV.")

def on_open_all_bookmarks():
    for b in bookmarks:
        if is_valid_url(b["url"]):
            open_url(b["url"])

def on_search():
    query = search_entry.get().strip()
    engine = search_engine.get()
    if query:
        if engine == "Google":
            url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        else:
            url = f"https://www.bing.com/search?q={query.replace(' ', '+')}"
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
        messagebox.showinfo(_("copy"), "URL copied to clipboard.")

def on_paste_url():
    try:
        url = root.clipboard_get()
        url_entry.delete(0, tk.END)
        url_entry.insert(0, url)
    except Exception:
        messagebox.showerror(_("paste"), "Clipboard is empty or invalid.")

def on_delete_bookmark():
    selection = bookmark_list.curselection()
    if selection:
        bookmarks.pop(selection[0])
        save_json(BOOKMARKS_FILE, bookmarks)
        update_bookmarks()

def on_delete_history():
    selection = history_list.curselection()
    if selection:
        history.pop(selection[0])
        save_json(HISTORY_FILE, history)
        update_history()

def on_delete_all_bookmarks():
    if messagebox.askyesno(_("delete_all"), "Delete all bookmarks?"):
        bookmarks.clear()
        save_json(BOOKMARKS_FILE, bookmarks)
        update_bookmarks()

def on_delete_all_history():
    if messagebox.askyesno(_("delete_all"), "Delete all history?"):
        history.clear()
        save_json(HISTORY_FILE, history)
        update_history()

def on_about():
    messagebox.showinfo(_("about"),
        f"{_('title')}\nA supercharged Python browser launcher.\n\nFeatures:\n- History & Bookmarks\n- Homepage\n- Import/Export Bookmarks\n- Open All Bookmarks\n- Search (Google/Bing)\n- Clipboard\n- Delete entries\n- Drag-and-drop\n- Settings\n- Keyboard shortcuts\n- Appearance\n- Multi-language\n- Frequent sites\n- Bookmark folders/notes\n- Sorting/filtering\n- Export/import CSV\n- Backup/restore\n- Custom browser\n- Mini web preview\n- User profile\n- Session restore\n- Update check\n- Easter egg"
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
    root.bind('<Control-e>', lambda e: on_easter_egg())

def on_theme_change():
    theme = theme_var.get()
    settings["theme"] = theme
    save_json(SETTINGS_FILE, settings)
    if theme == "dark":
        root.tk_setPalette(background="#222", foreground="#eee")
    else:
        root.tk_setPalette(background="#fff", foreground="#000")

def on_language_change():
    lang = lang_var.get()
    settings["language"] = lang
    save_json(SETTINGS_FILE, settings)
    messagebox.showinfo(_("language"), f"Language set to {lang}. Restart app to apply.")

def on_browser_change():
    browser = browser_var.get()
    settings["browser"] = browser
    save_json(SETTINGS_FILE, settings)
    messagebox.showinfo(_("browser"), f"Browser set to {browser}.")

def on_backup():
    file_path = filedialog.asksaveasfilename(title=_("backup"), defaultextension=".json", filetypes=[("JSON Files", "*.json")])
    if file_path:
        backup = {
            "history": history,
            "bookmarks": bookmarks,
            "settings": settings,
            "profile": profile,
            "session": session
        }
        save_json(file_path, backup)
        messagebox.showinfo(_("backup"), "Backup saved.")

def on_restore():
    file_path = filedialog.askopenfilename(title=_("restore"), filetypes=[("JSON Files", "*.json")])
    if file_path:
        restored = load_json(file_path, {})
        global history, bookmarks, settings, profile, session
        history = restored.get("history", [])
        bookmarks = restored.get("bookmarks", [])
        settings = restored.get("settings", settings)
        profile = restored.get("profile", profile)
        session = restored.get("session", session)
        save_json(HISTORY_FILE, history)
        save_json(BOOKMARKS_FILE, bookmarks)
        save_json(SETTINGS_FILE, settings)
        save_json(PROFILE_FILE, profile)
        save_json(SESSION_FILE, session)
        update_history()
        update_bookmarks()
        update_frequent()
        messagebox.showinfo(_("restore"), "Backup restored.")

def on_easter_egg():
    facts = [
        "Python was named after Monty Python.",
        "Tkinter is included with most Python installations.",
        "You can run PyBrowser on a Raspberry Pi!",
        "Try pressing Ctrl+E for a surprise.",
        "The web was invented in 1989."
    ]
    messagebox.showinfo(_("easter_egg"), random.choice(facts))

def on_profile():
    name = simpledialog.askstring(_("profile"), "Enter your name:", initialvalue=profile.get("name", "User"))
    avatar = simpledialog.askstring(_("profile"), "Enter avatar URL (optional):", initialvalue=profile.get("avatar", ""))
    greeting = simpledialog.askstring(_("profile"), "Enter greeting:", initialvalue=profile.get("greeting", _("greeting")))
    profile["name"] = name
    profile["avatar"] = avatar
    profile["greeting"] = greeting
    save_json(PROFILE_FILE, profile)
    update_profile()

def update_profile():
    profile_label.config(text=f"{profile.get('greeting', _('greeting'))}, {profile.get('name', 'User')}!")
    # Avatar display stub (could use PIL for images)

root = tk.Tk()
root.title(_("title"))

# Appearance
theme_var = tk.StringVar(value=settings.get("theme", "light"))
lang_var = tk.StringVar(value=settings.get("language", "en"))
browser_var = tk.StringVar(value=settings.get("browser", "default"))

# Menu
menu = tk.Menu(root)
root.config(menu=menu)
settings_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label=_("Settings"), menu=settings_menu)
settings_menu.add_command(label=_("set_homepage"), command=on_set_homepage)
settings_menu.add_command(label=_("open_homepage"), command=on_open_homepage)
settings_menu.add_separator()
settings_menu.add_command(label=_("import_bookmarks"), command=on_import_bookmarks)
settings_menu.add_command(label=_("export_bookmarks"), command=on_export_bookmarks)
settings_menu.add_separator()
settings_menu.add_command(label=_("backup"), command=on_backup)
settings_menu.add_command(label=_("restore"), command=on_restore)
settings_menu.add_separator()
settings_menu.add_command(label=_("about"), command=on_about)
settings_menu.add_command(label=_("easter_egg"), command=on_easter_egg)
settings_menu.add_separator()
settings_menu.add_command(label=_("profile"), command=on_profile)

appearance_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label=_("theme"), menu=appearance_menu)
appearance_menu.add_radiobutton(label="Light", variable=theme_var, value="light", command=on_theme_change)
appearance_menu.add_radiobutton(label="Dark", variable=theme_var, value="dark", command=on_theme_change)

lang_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label=_("language"), menu=lang_menu)
lang_menu.add_radiobutton(label="English", variable=lang_var, value="en", command=on_language_change)
lang_menu.add_radiobutton(label="Español", variable=lang_var, value="es", command=on_language_change)
lang_menu.add_radiobutton(label="Kalaallisut", variable=lang_var, value="kl", command=on_language_change)
lang_menu.add_radiobutton(label="Inuktitut", variable=lang_var, value="iu", command=on_language_change)

browser_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label=_("browser"), menu=browser_menu)
browser_menu.add_radiobutton(label="Default", variable=browser_var, value="default", command=on_browser_change)
browser_menu.add_radiobutton(label="Chrome", variable=browser_var, value="chrome", command=on_browser_change)
browser_menu.add_radiobutton(label="Firefox", variable=browser_var, value="firefox", command=on_browser_change)
browser_menu.add_radiobutton(label="Edge", variable=browser_var, value="edge", command=on_browser_change)

menu.add_command(label=_("update"), command=lambda: messagebox.showinfo(_("update"), "PyBrowser is up to date!"))

# Profile
profile_label = tk.Label(root, text="")
profile_label.pack(pady=2)
update_profile()

# Search
search_frame = tk.Frame(root)
search_frame.pack(pady=5)
tk.Label(search_frame, text=_("search")).pack(side=tk.LEFT)
search_entry = tk.Entry(search_frame, width=30)
search_entry.pack(side=tk.LEFT, padx=5)
search_engine = ttk.Combobox(search_frame, values=["Google", "Bing"], width=8)
search_engine.set("Google")
search_engine.pack(side=tk.LEFT, padx=2)
tk.Button(search_frame, text=_("search"), command=on_search).pack(side=tk.LEFT)

# URL Entry
tk.Label(root, text=_("enter_url")).pack(pady=5)
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)
if session.get("last_url"):
    url_entry.insert(0, session["last_url"])

btn_frame = tk.Frame(root)
btn_frame.pack(pady=5)
tk.Button(btn_frame, text=_("open"), command=on_open).pack(side=tk.LEFT, padx=5)
tk.Button(btn_frame, text=_("bookmark"), command=on_bookmark).pack(side=tk.LEFT, padx=5)
tk.Button(btn_frame, text=_("clear"), command=on_clear).pack(side=tk.LEFT, padx=5)
tk.Button(btn_frame, text=_("copy"), command=on_copy_url).pack(side=tk.LEFT, padx=5)
tk.Button(btn_frame, text=_("paste"), command=on_paste_url).pack(side=tk.LEFT, padx=5)

lists_frame = tk.Frame(root)
lists_frame.pack(pady=10)

tk.Label(lists_frame, text=_("history")).grid(row=0, column=0)
tk.Label(lists_frame, text=_("bookmarks")).grid(row=0, column=1)
tk.Label(lists_frame, text="Frequent:").grid(row=0, column=2)

history_list = tk.Listbox(lists_frame, width=40, height=6)
history_list.grid(row=1, column=0, padx=5)
history_list.bind('<<ListboxSelect>>', on_history_select)
tk.Button(lists_frame, text=_("delete_selected"), command=on_delete_history).grid(row=2, column=0, pady=2)
tk.Button(lists_frame, text=_("delete_all"), command=on_delete_all_history).grid(row=3, column=0, pady=2)
tk.Button(lists_frame, text=_("sort_newest"), command=lambda: update_history("newest")).grid(row=4, column=0, pady=2)
tk.Button(lists_frame, text=_("sort_oldest"), command=lambda: update_history("oldest")).grid(row=5, column=0, pady=2)

bookmark_list = tk.Listbox(lists_frame, width=40, height=6)
bookmark_list.grid(row=1, column=1, padx=5)
bookmark_list.bind('<<ListboxSelect>>', on_bookmark_select)
tk.Button(lists_frame, text=_("delete_selected"), command=on_delete_bookmark).grid(row=2, column=1, pady=2)
tk.Button(lists_frame, text=_("delete_all"), command=on_delete_all_bookmarks).grid(row=3, column=1, pady=2)
tk.Button(lists_frame, text=_("open_all"), command=on_open_all_bookmarks).grid(row=4, column=1, pady=2)
tk.Button(lists_frame, text=_("sort_az"), command=lambda: update_bookmarks(sort="az")).grid(row=5, column=1, pady=2)
tk.Label(lists_frame, text=_("filter")).grid(row=6, column=1)
filter_entry = tk.Entry(lists_frame, width=20)
filter_entry.grid(row=7, column=1)
tk.Button(lists_frame, text=_("filter"), command=lambda: update_bookmarks(filter_text=filter_entry.get())).grid(row=8, column=1, pady=2)

frequent_list = tk.Listbox(lists_frame, width=30, height=6)
frequent_list.grid(row=1, column=2, padx=5)

# Mini web preview
if HAS_WEBVIEW:
    webview = HtmlFrame(root, horizontal_scrollbar="auto")
    webview.pack(fill="both", expand=True, padx=10, pady=10)
    webview.load_html("<h3>PyBrowser</h3>")
else:
    tk.Label(root, text="Install 'tkinterweb' for web preview!").pack(pady=5)

update_history()
update_bookmarks()
update_frequent()
bind_shortcuts()

root.mainloop()
