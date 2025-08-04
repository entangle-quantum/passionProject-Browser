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
    },
    "fr": {
        "title": "PyNavigateur",
        "search": "Recherche :",
        "enter_url": "Entrez l'URL (avec http:// ou https://) :",
        "open": "Ouvrir dans le navigateur",
        "bookmark": "Favori",
        "clear": "Effacer",
        "copy": "Copier",
        "paste": "Coller",
        "delete_selected": "Supprimer la sélection",
        "delete_all": "Tout supprimer",
        "open_all": "Tout ouvrir",
        "history": "Historique (10 derniers) :",
        "bookmarks": "Favoris :",
        "set_homepage": "Définir la page d'accueil",
        "open_homepage": "Ouvrir la page d'accueil",
        "import_bookmarks": "Importer les favoris",
        "export_bookmarks": "Exporter les favoris",
        "about": "À propos",
        "theme": "Thème",
        "language": "Langue",
        "profile": "Profil",
        "update": "Vérifier les mises à jour",
        "browser": "Navigateur",
        "notes": "Notes",
        "sort_az": "Trier A-Z",
        "sort_newest": "Trier par plus récent",
        "sort_oldest": "Trier par plus ancien",
        "filter": "Filtrer",
        "backup": "Sauvegarder",
        "restore": "Restaurer",
        "export_csv": "Exporter CSV",
        "import_csv": "Importer CSV",
        "greeting": "Bienvenue",
        "easter_egg": "Œuf de Pâques",
    },
    "de": {
        "title": "PyBrowser",
        "search": "Suche:",
        "enter_url": "URL eingeben (mit http:// oder https://):",
        "open": "Im Browser öffnen",
        "bookmark": "Lesezeichen",
        "clear": "Löschen",
        "copy": "Kopieren",
        "paste": "Einfügen",
        "delete_selected": "Auswahl löschen",
        "delete_all": "Alles löschen",
        "open_all": "Alle öffnen",
        "history": "Verlauf (letzte 10):",
        "bookmarks": "Lesezeichen:",
        "set_homepage": "Startseite festlegen",
        "open_homepage": "Startseite öffnen",
        "import_bookmarks": "Lesezeichen importieren",
        "export_bookmarks": "Lesezeichen exportieren",
        "about": "Über",
        "theme": "Thema",
        "language": "Sprache",
        "profile": "Profil",
        "update": "Nach Updates suchen",
        "browser": "Browser",
        "notes": "Notizen",
        "sort_az": "Sortieren A-Z",
        "sort_newest": "Neueste zuerst",
        "sort_oldest": "Älteste zuerst",
        "filter": "Filtern",
        "backup": "Backup",
        "restore": "Wiederherstellen",
        "export_csv": "CSV exportieren",
        "import_csv": "CSV importieren",
        "greeting": "Willkommen",
        "easter_egg": "Osterei",
    },
    "it": {
        "title": "PyBrowser",
        "search": "Cerca:",
        "enter_url": "Inserisci URL (con http:// o https://):",
        "open": "Apri nel browser",
        "bookmark": "Segnalibro",
        "clear": "Cancella",
        "copy": "Copia",
        "paste": "Incolla",
        "delete_selected": "Elimina selezionato",
        "delete_all": "Elimina tutto",
        "open_all": "Apri tutto",
        "history": "Cronologia (ultimi 10):",
        "bookmarks": "Segnalibri:",
        "set_homepage": "Imposta homepage",
        "open_homepage": "Apri homepage",
        "import_bookmarks": "Importa segnalibri",
        "export_bookmarks": "Esporta segnalibri",
        "about": "Informazioni",
        "theme": "Tema",
        "language": "Lingua",
        "profile": "Profilo",
        "update": "Controlla aggiornamenti",
        "browser": "Browser",
        "notes": "Note",
        "sort_az": "Ordina A-Z",
        "sort_newest": "Ordina per più recente",
        "sort_oldest": "Ordina per più vecchio",
        "filter": "Filtra",
        "backup": "Backup",
        "restore": "Ripristina",
        "export_csv": "Esporta CSV",
        "import_csv": "Importa CSV",
        "greeting": "Benvenuto",
        "easter_egg": "Uovo di Pasqua",
    },
    "ru": {
        "title": "PyBrowser",
        "search": "Поиск:",
        "enter_url": "Введите URL (с http:// или https://):",
        "open": "Открыть в браузере",
        "bookmark": "Закладка",
        "clear": "Очистить",
        "copy": "Копировать",
        "paste": "Вставить",
        "delete_selected": "Удалить выбранное",
        "delete_all": "Удалить все",
        "open_all": "Открыть все",
        "history": "История (последние 10):",
        "bookmarks": "Закладки:",
        "set_homepage": "Установить домашнюю страницу",
        "open_homepage": "Открыть домашнюю страницу",
        "import_bookmarks": "Импорт закладок",
        "export_bookmarks": "Экспорт закладок",
        "about": "О программе",
        "theme": "Тема",
        "language": "Язык",
        "profile": "Профиль",
        "update": "Проверить обновления",
        "browser": "Браузер",
        "notes": "Заметки",
        "sort_az": "Сортировать A-Z",
        "sort_newest": "Сначала новые",
        "sort_oldest": "Сначала старые",
        "filter": "Фильтр",
        "backup": "Резервная копия",
        "restore": "Восстановить",
        "export_csv": "Экспорт CSV",
        "import_csv": "Импорт CSV",
        "greeting": "Добро пожаловать",
        "easter_egg": "Пасхальное яйцо",
    },
    "zh": {
        "title": "Py浏览器",
        "search": "搜索：",
        "enter_url": "输入网址（含 http:// 或 https://）：",
        "open": "在浏览器中打开",
        "bookmark": "书签",
        "clear": "清除",
        "copy": "复制",
        "paste": "粘贴",
        "delete_selected": "删除选中项",
        "delete_all": "全部删除",
        "open_all": "全部打开",
        "history": "历史记录（最近10条）：",
        "bookmarks": "书签：",
        "set_homepage": "设置主页",
        "open_homepage": "打开主页",
        "import_bookmarks": "导入书签",
        "export_bookmarks": "导出书签",
        "about": "关于",
        "theme": "主题",
        "language": "语言",
        "profile": "个人资料",
        "update": "检查更新",
        "browser": "浏览器",
        "notes": "备注",
        "sort_az": "按A-Z排序",
        "sort_newest": "按最新排序",
        "sort_oldest": "按最旧排序",
        "filter": "筛选",
        "backup": "备份",
        "restore": "恢复",
        "export_csv": "导出CSV",
        "import_csv": "导入CSV",
        "greeting": "欢迎",
        "easter_egg": "彩蛋",
    },
    "ja": {
        "title": "Pyブラウザ",
        "search": "検索：",
        "enter_url": "URLを入力（http://またはhttps://）：",
        "open": "ブラウザで開く",
        "bookmark": "ブックマーク",
        "clear": "クリア",
        "copy": "コピー",
        "paste": "貼り付け",
        "delete_selected": "選択を削除",
        "delete_all": "すべて削除",
        "open_all": "すべて開く",
        "history": "履歴（最新10件）：",
        "bookmarks": "ブックマーク：",
        "set_homepage": "ホームページを設定",
        "open_homepage": "ホームページを開く",
        "import_bookmarks": "ブックマークをインポート",
        "export_bookmarks": "ブックマークをエクスポート",
        "about": "情報",
        "theme": "テーマ",
        "language": "言語",
        "profile": "プロフィール",
        "update": "アップデートを確認",
        "browser": "ブラウザ",
        "notes": "ノート",
        "sort_az": "A-Zで並べ替え",
        "sort_newest": "新しい順",
        "sort_oldest": "古い順",
        "filter": "フィルター",
        "backup": "バックアップ",
        "restore": "復元",
        "export_csv": "CSVエクスポート",
        "import_csv": "CSVインポート",
        "greeting": "ようこそ",
        "easter_egg": "イースターエッグ",
    },
    "ar": {
        "title": "باي براوزر",
        "search": "بحث:",
        "enter_url": "أدخل الرابط (http:// أو https://):",
        "open": "افتح في المتصفح",
        "bookmark": "إشارة مرجعية",
        "clear": "مسح",
        "copy": "نسخ",
        "paste": "لصق",
        "delete_selected": "حذف المحدد",
        "delete_all": "حذف الكل",
        "open_all": "افتح الكل",
        "history": "السجل (آخر 10):",
        "bookmarks": "الإشارات المرجعية:",
        "set_homepage": "تعيين الصفحة الرئيسية",
        "open_homepage": "افتح الصفحة الرئيسية",
        "import_bookmarks": "استيراد الإشارات المرجعية",
        "export_bookmarks": "تصدير الإشارات المرجعية",
        "about": "حول",
        "theme": "السمة",
        "language": "اللغة",
        "profile": "الملف الشخصي",
        "update": "تحقق من التحديثات",
        "browser": "المتصفح",
        "notes": "ملاحظات",
        "sort_az": "ترتيب A-Z",
        "sort_newest": "الأحدث أولاً",
        "sort_oldest": "الأقدم أولاً",
        "filter": "تصفية",
        "backup": "نسخ احتياطي",
        "restore": "استعادة",
        "export_csv": "تصدير CSV",
        "import_csv": "استيراد CSV",
        "greeting": "مرحبا",
        "easter_egg": "بيضة عيد الفصح",
    },
    "pt": {  # Portuguese
        "title": "PyNavegador",
        "search": "Pesquisar:",
        "enter_url": "Digite o URL (com http:// ou https://):",
        "open": "Abrir no navegador",
        "bookmark": "Favorito",
        "clear": "Limpar",
        "copy": "Copiar",
        "paste": "Colar",
        "delete_selected": "Excluir selecionado",
        "delete_all": "Excluir tudo",
        "open_all": "Abrir todos",
        "history": "Histórico (últimos 10):",
        "bookmarks": "Favoritos:",
        "set_homepage": "Definir página inicial",
        "open_homepage": "Abrir página inicial",
        "import_bookmarks": "Importar favoritos",
        "export_bookmarks": "Exportar favoritos",
        "about": "Sobre",
        "theme": "Tema",
        "language": "Idioma",
        "profile": "Perfil",
        "update": "Verificar atualizações",
        "browser": "Navegador",
        "notes": "Notas",
        "sort_az": "Ordenar A-Z",
        "sort_newest": "Mais recentes",
        "sort_oldest": "Mais antigos",
        "filter": "Filtrar",
        "backup": "Backup",
        "restore": "Restaurar",
        "export_csv": "Exportar CSV",
        "import_csv": "Importar CSV",
        "greeting": "Bem-vindo",
        "easter_egg": "Easter Egg",
    },
    "hi": {  # Hindi
        "title": "पाइब्राउज़र",
        "search": "खोजें:",
        "enter_url": "URL दर्ज करें (http:// या https://):",
        "open": "ब्राउज़र में खोलें",
        "bookmark": "बुकमार्क",
        "clear": "साफ करें",
        "copy": "कॉपी",
        "paste": "पेस्ट",
        "delete_selected": "चयनित हटाएँ",
        "delete_all": "सभी हटाएँ",
        "open_all": "सभी खोलें",
        "history": "इतिहास (अंतिम 10):",
        "bookmarks": "बुकमार्क:",
        "set_homepage": "मुखपृष्ठ सेट करें",
        "open_homepage": "मुखपृष्ठ खोलें",
        "import_bookmarks": "बुकमार्क आयात करें",
        "export_bookmarks": "बुकमार्क निर्यात करें",
        "about": "के बारे में",
        "theme": "थीम",
        "language": "भाषा",
        "profile": "प्रोफ़ाइल",
        "update": "अपडेट जांचें",
        "browser": "ब्राउज़र",
        "notes": "नोट्स",
        "sort_az": "A-Z क्रमबद्ध करें",
        "sort_newest": "नवीनतम पहले",
        "sort_oldest": "पुराने पहले",
        "filter": "फ़िल्टर",
        "backup": "बैकअप",
        "restore": "पुनर्स्थापित करें",
        "export_csv": "CSV निर्यात करें",
        "import_csv": "CSV आयात करें",
        "greeting": "स्वागत है",
        "easter_egg": "ईस्टर एग",
    },
    "tr": {  # Turkish
        "title": "PyTarayıcı",
        "search": "Ara:",
        "enter_url": "URL girin (http:// veya https://):",
        "open": "Tarayıcıda aç",
        "bookmark": "Yer imi",
        "clear": "Temizle",
        "copy": "Kopyala",
        "paste": "Yapıştır",
        "delete_selected": "Seçiliyi sil",
        "delete_all": "Hepsini sil",
        "open_all": "Hepsini aç",
        "history": "Geçmiş (son 10):",
        "bookmarks": "Yer imleri:",
        "set_homepage": "Ana sayfa ayarla",
        "open_homepage": "Ana sayfayı aç",
        "import_bookmarks": "Yer imlerini içe aktar",
        "export_bookmarks": "Yer imlerini dışa aktar",
        "about": "Hakkında",
        "theme": "Tema",
        "language": "Dil",
        "profile": "Profil",
        "update": "Güncellemeleri kontrol et",
        "browser": "Tarayıcı",
        "notes": "Notlar",
        "sort_az": "A-Z sırala",
        "sort_newest": "En yeni",
        "sort_oldest": "En eski",
        "filter": "Filtrele",
        "backup": "Yedekle",
        "restore": "Geri yükle",
        "export_csv": "CSV dışa aktar",
        "import_csv": "CSV içe aktar",
        "greeting": "Hoşgeldiniz",
        "easter_egg": "Easter Egg",
    },
    "ko": {  # Korean
        "title": "파이브라우저",
        "search": "검색:",
        "enter_url": "URL 입력 (http:// 또는 https://):",
        "open": "브라우저에서 열기",
        "bookmark": "북마크",
        "clear": "지우기",
        "copy": "복사",
        "paste": "붙여넣기",
        "delete_selected": "선택 삭제",
        "delete_all": "전체 삭제",
        "open_all": "전체 열기",
        "history": "기록 (최근 10개):",
        "bookmarks": "북마크:",
        "set_homepage": "홈페이지 설정",
        "open_homepage": "홈페이지 열기",
        "import_bookmarks": "북마크 가져오기",
        "export_bookmarks": "북마크 내보내기",
        "about": "정보",
        "theme": "테마",
        "language": "언어",
        "profile": "프로필",
        "update": "업데이트 확인",
        "browser": "브라우저",
        "notes": "노트",
        "sort_az": "A-Z 정렬",
        "sort_newest": "최신순",
        "sort_oldest": "오래된순",
        "filter": "필터",
        "backup": "백업",
        "restore": "복원",
        "export_csv": "CSV 내보내기",
        "import_csv": "CSV 가져오기",
        "greeting": "환영합니다",
        "easter_egg": "이스터에그",
    },
    "pl": {  # Polish
        "title": "PyPrzeglądarka",
        "search": "Szukaj:",
        "enter_url": "Wpisz URL (z http:// lub https://):",
        "open": "Otwórz w przeglądarce",
        "bookmark": "Zakładka",
        "clear": "Wyczyść",
        "copy": "Kopiuj",
        "paste": "Wklej",
        "delete_selected": "Usuń zaznaczone",
        "delete_all": "Usuń wszystko",
        "open_all": "Otwórz wszystko",
        "history": "Historia (ostatnie 10):",
        "bookmarks": "Zakładki:",
        "set_homepage": "Ustaw stronę główną",
        "open_homepage": "Otwórz stronę główną",
        "import_bookmarks": "Importuj zakładki",
        "export_bookmarks": "Eksportuj zakładki",
        "about": "O programie",
        "theme": "Motyw",
        "language": "Język",
        "profile": "Profil",
        "update": "Sprawdź aktualizacje",
        "browser": "Przeglądarka",
        "notes": "Notatki",
        "sort_az": "Sortuj A-Z",
        "sort_newest": "Najnowsze",
        "sort_oldest": "Najstarsze",
        "filter": "Filtruj",
        "backup": "Kopia zapasowa",
        "restore": "Przywróć",
        "export_csv": "Eksportuj CSV",
        "import_csv": "Importuj CSV",
        "greeting": "Witamy",
        "easter_egg": "Easter Egg",
    },
    # Add more languages here as needed!
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
lang_menu.add_radiobutton(label="Français", variable=lang_var, value="fr", command=on_language_change)
lang_menu.add_radiobutton(label="Deutsch", variable=lang_var, value="de", command=on_language_change)
lang_menu.add_radiobutton(label="Italiano", variable=lang_var, value="it", command=on_language_change)
lang_menu.add_radiobutton(label="Русский", variable=lang_var, value="ru", command=on_language_change)
lang_menu.add_radiobutton(label="中文", variable=lang_var, value="zh", command=on_language_change)
lang_menu.add_radiobutton(label="日本語", variable=lang_var, value="ja", command=on_language_change)
lang_menu.add_radiobutton(label="العربية", variable=lang_var, value="ar", command=on_language_change)
lang_menu.add_radiobutton(label="Português", variable=lang_var, value="pt", command=on_language_change)
lang_menu.add_radiobutton(label="हिन्दी", variable=lang_var, value="hi", command=on_language_change)
lang_menu.add_radiobutton(label="Türkçe", variable=lang_var, value="tr", command=on_language_change)
lang_menu.add_radiobutton(label="한국어", variable=lang_var, value="ko", command=on_language_change)
lang_menu.add_radiobutton(label="Polski", variable=lang_var, value="pl", command=on_language_change)

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
