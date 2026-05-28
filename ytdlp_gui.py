import os
import locale
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import time
import tkinter as tk
from tkinter import filedialog, messagebox, ttk


BG = "#20222b"
SURF = "#303442"
SURF_2 = "#3b4050"
ACCENT = "#4f8cff"
ACCENT_H = "#6da0ff"
TEXT = "#f1f3f8"
DIM = "#a6adbb"
GREEN = "#54c58a"
RED = "#ff6b6b"
ORANGE = "#f3b45b"
BORDER = "#454b5f"
FONT = ("Segoe UI", 10)
FNSM = ("Segoe UI", 9)
FNLG = ("Segoe UI", 12, "bold")
FNMONO = ("Consolas", 9)
FMTS = ["mp4", "mkv", "webm", "mov", "avi", "mp3", "aac", "ogg", "m4a", "flac", "wav"]
AUDIO_FORMATS = {"mp3", "aac", "ogg", "m4a", "flac", "wav"}
CONSOLE_ENCODING = locale.getpreferredencoding(False) or "utf-8"


I18N = {
    "tr": {
        "app_title": "yt-dlp GUI",
        "tagline": "YouTube ve 1000+ site",
        "language": "Dil",
        "url": "Video URL",
        "paste": "Yapıştır",
        "fetch_formats": "Formatları Getir",
        "quality": "Kalite / Format",
        "start": "Başlangıç",
        "end": "Bitiş",
        "time_hint": "örn. 27:50 veya 01:02:03",
        "output_format": "Çıktı Formatı",
        "cut_method": "Kesme Yöntemi",
        "direct": "Direkt kes (hızlı, bazen keyframe'e kayar)",
        "post": "Tam indir → kes (hızlı kopya)",
        "reencode": "Tam indir → yeniden kodla (en doğru)",
        "codec": "Video Codec (yeniden kodlama modunda)",
        "h264": "h264 - uyumlu",
        "h265": "h265 - küçük dosya",
        "copy": "copy - yeniden kodlama yok",
        "reencode_size": "Yeniden Kodlama Çözünürlüğü",
        "size_source": "Orijinal",
        "size_1080": "1080p",
        "size_720": "720p - hızlı",
        "size_480": "480p - en hızlı",
        "twitter_tip": "MP4 paylaşımı için yeniden kodla + h264 en güvenli seçenek.",
        "folder": "Kayıt Klasörü",
        "choose": "Seç",
        "download": "İndir",
        "cancel": "İptal",
        "ready": "Hazır",
        "missing_deps": "Eksik bağımlılık - log'a bakın",
        "deps_ready": "yt-dlp ve ffmpeg hazır.",
        "missing": "Eksik",
        "install_ytdlp": "yt-dlp için: pip install -U yt-dlp",
        "install_ffmpeg": "ffmpeg'i kurup PATH'e ekleyin.",
        "need_url": "Önce URL girin.",
        "fetching": "Analiz ediliyor...",
        "not_found": "bulunamadı",
        "error": "Hata",
        "invalid_start": "Geçersiz başlangıç",
        "invalid_end": "Geçersiz bitiş",
        "end_before_start": "Bitiş zamanı başlangıçtan büyük olmalı.",
        "need_format": "Format seçiniz.",
        "ffmpeg_required": "Bu işlem için ffmpeg gerekli.",
        "downloading": "İndiriliyor",
        "processing": "İşleniyor",
        "cutting": "Kesiliyor",
        "done": "Tamamlandı!",
        "canceling": "İptal ediliyor...",
        "canceled": "İptal edildi.",
        "formats_found": "format",
        "formats_not_found": "Format bulunamadı.",
        "auto": "Otomatik",
        "video": "Video",
        "audio": "Ses",
        "best_video": "En İyi Video + Ses",
        "best_audio_mp3": "En İyi Ses (MP3)",
        "best_audio_aac": "En İyi Ses (AAC)",
        "phase_download": "İndirme",
        "phase_cut": "Kesme",
        "saved_to": "Kaydedildi",
        "temp_deleted": "Geçici dosya silindi.",
        "copy_note": "Not: copy modu yeniden kodlamaz; bazı videolarda ilk saniyelerde donma veya küçük zaman kayması normaldir.",
    },
    "en": {
        "app_title": "yt-dlp GUI",
        "tagline": "YouTube and 1000+ sites",
        "language": "Language",
        "url": "Video URL",
        "paste": "Paste",
        "fetch_formats": "Fetch Formats",
        "quality": "Quality / Format",
        "start": "Start",
        "end": "End",
        "time_hint": "e.g. 27:50 or 01:02:03",
        "output_format": "Output Format",
        "cut_method": "Cut Method",
        "direct": "Direct cut (fast, may snap to keyframes)",
        "post": "Download full → cut (fast copy)",
        "reencode": "Download full → re-encode (most accurate)",
        "codec": "Video Codec (re-encode mode)",
        "h264": "h264 - compatible",
        "h265": "h265 - smaller file",
        "copy": "copy - no re-encode",
        "reencode_size": "Re-encode Resolution",
        "size_source": "Original",
        "size_1080": "1080p",
        "size_720": "720p - fast",
        "size_480": "480p - fastest",
        "twitter_tip": "For MP4 sharing, re-encode + h264 is the safest option.",
        "folder": "Save Folder",
        "choose": "Choose",
        "download": "Download",
        "cancel": "Cancel",
        "ready": "Ready",
        "missing_deps": "Missing dependency - see log",
        "deps_ready": "yt-dlp and ffmpeg are ready.",
        "missing": "Missing",
        "install_ytdlp": "For yt-dlp: pip install -U yt-dlp",
        "install_ffmpeg": "Install ffmpeg and add it to PATH.",
        "need_url": "Enter a URL first.",
        "fetching": "Analyzing...",
        "not_found": "not found",
        "error": "Error",
        "invalid_start": "Invalid start time",
        "invalid_end": "Invalid end time",
        "end_before_start": "End time must be greater than start time.",
        "need_format": "Choose a format.",
        "ffmpeg_required": "ffmpeg is required for this operation.",
        "downloading": "Downloading",
        "processing": "Processing",
        "cutting": "Cutting",
        "done": "Completed!",
        "canceling": "Canceling...",
        "canceled": "Canceled.",
        "formats_found": "formats",
        "formats_not_found": "No formats found.",
        "auto": "Automatic",
        "video": "Video",
        "audio": "Audio",
        "best_video": "Best Video + Audio",
        "best_audio_mp3": "Best Audio (MP3)",
        "best_audio_aac": "Best Audio (AAC)",
        "phase_download": "Download",
        "phase_cut": "Cut",
        "saved_to": "Saved to",
        "temp_deleted": "Temporary file deleted.",
        "copy_note": "Note: copy mode does not re-encode; brief first-second freeze or small timing drift can happen on some videos.",
    },
}


def find_exe(name):
    found = shutil.which(name)
    if found:
        return found

    app_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    for ext in ("", ".exe"):
        candidate = os.path.join(app_dir, name + ext)
        if os.path.isfile(candidate):
            return candidate

    if sys.platform == "win32":
        candidate = os.path.join(os.path.dirname(sys.executable), "Scripts", name + ".exe")
        if os.path.isfile(candidate):
            return candidate

    return None


def missing_deps():
    return [name for name in ("yt-dlp", "ffmpeg") if not find_exe(name)]


def time_to_seconds(value):
    value = value.strip()
    if not value:
        return None
    if re.fullmatch(r"\d+(\.\d+)?", value):
        return float(value)
    parts = value.split(":")
    if len(parts) not in (2, 3):
        raise ValueError(value)
    if any(not re.fullmatch(r"\d{1,2}", part) for part in parts):
        raise ValueError(value)
    nums = [int(part) for part in parts]
    if len(nums) == 2:
        minutes, seconds = nums
        hours = 0
    else:
        hours, minutes, seconds = nums
    if minutes > 59 or seconds > 59:
        raise ValueError(value)
    return hours * 3600 + minutes * 60 + seconds


def seconds_to_time(seconds):
    seconds = max(0.0, float(seconds))
    whole = int(seconds)
    ms = int(round((seconds - whole) * 1000))
    hours = whole // 3600
    minutes = (whole % 3600) // 60
    sec = whole % 60
    if ms:
        return f"{hours:02d}:{minutes:02d}:{sec:02d}.{ms:03d}"
    return f"{hours:02d}:{minutes:02d}:{sec:02d}"


def ffmpeg_time_to_seconds(value):
    match = re.match(r"(\d+):(\d+):(\d+(?:\.\d+)?)", value)
    if not match:
        return None
    return int(match.group(1)) * 3600 + int(match.group(2)) * 60 + float(match.group(3))


def short_duration(seconds):
    seconds = max(0, int(round(float(seconds))))
    minutes, sec = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    if hours:
        return f"{hours} sa {minutes:02d} dk"
    if minutes:
        return f"{minutes} dk {sec:02d} sn"
    return f"{sec} sn"


def normalize_eta(value):
    value = value.strip()
    if not value or value.lower() == "unknown":
        return ""
    parts = value.split(":")
    try:
        if len(parts) == 3:
            seconds = int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
        elif len(parts) == 2:
            seconds = int(parts[0]) * 60 + int(parts[1])
        else:
            return value
    except ValueError:
        return value
    return short_duration(seconds)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.lang = tk.StringVar(value="tr")
        self._proc = None
        self._fmap = {}
        self._labels = []
        self._buttons = []
        self._radios = []
        self._phase_weights = (1.0, 0.0)
        self._build()
        self._apply_language()
        self._fit_to_screen()
        self.after(150, self._check_startup)

    def t(self, key):
        return I18N[self.lang.get()].get(key, key)

    def _fit_to_screen(self):
        self.update_idletasks()
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        width = min(760, max(560, sw - 120))
        height = min(680, max(460, sh - 160))
        self.geometry(f"{width}x{height}+{(sw - width) // 2}+{max(20, (sh - height) // 2)}")
        self.minsize(560, 420)

    def _build(self):
        self.title("yt-dlp GUI")
        self.configure(bg=BG)
        self.resizable(True, True)

        hdr = tk.Frame(self, bg=BG)
        hdr.pack(fill="x", padx=14, pady=(10, 0))
        self.title_lbl = tk.Label(hdr, font=FNLG, bg=BG, fg=ACCENT)
        self.title_lbl.pack(side="left")
        self.tagline_lbl = tk.Label(hdr, font=FNSM, bg=BG, fg=DIM)
        self.tagline_lbl.pack(side="left", padx=8)

        lang_frame = tk.Frame(hdr, bg=BG)
        lang_frame.pack(side="right")
        self.lang_lbl = tk.Label(lang_frame, font=FNSM, bg=BG, fg=DIM)
        self.lang_lbl.pack(side="left", padx=(0, 6))
        self.lang_menu = ttk.OptionMenu(lang_frame, self.lang, "tr", "tr", "en", command=lambda _: self._apply_language())
        self.lang_menu.pack(side="left")

        tk.Frame(self, bg=BORDER, height=1).pack(fill="x", padx=14, pady=(6, 0))

        self._cv = tk.Canvas(self, bg=BG, bd=0, highlightthickness=0)
        sb = tk.Scrollbar(self, orient="vertical", command=self._cv.yview, bg=SURF, troughcolor=BG, bd=0, width=8)
        self._cv.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        self._cv.pack(side="left", fill="both", expand=True, padx=(14, 0))

        self._sf = tk.Frame(self._cv, bg=BG)
        self._cw = self._cv.create_window((0, 0), window=self._sf, anchor="nw")
        self._sf.bind("<Configure>", lambda _e: self._cv.configure(scrollregion=self._cv.bbox("all")))
        self._cv.bind("<Configure>", lambda e: self._cv.itemconfig(self._cw, width=e.width))
        self._cv.bind("<Enter>", lambda _e: self.bind("<MouseWheel>", self._mousewheel))
        self._cv.bind("<Leave>", lambda _e: self.unbind("<MouseWheel>"))

        frame = self._sf

        self._lbl(frame, "url")
        url_row = tk.Frame(frame, bg=BG)
        url_row.pack(fill="x", pady=(2, 8))
        self.url_var = tk.StringVar()
        self.url_entry = self._entry(url_row, self.url_var)
        self.url_entry.pack(side="left", fill="x", expand=True)
        self._btn(url_row, "paste", self._paste, small=True).pack(side="left", padx=(6, 0))

        fetch_row = tk.Frame(frame, bg=BG)
        fetch_row.pack(fill="x", pady=(0, 4))
        self.fetch_btn = self._btn(fetch_row, "fetch_formats", self._fetch, small=True)
        self.fetch_btn.pack(side="left")
        self.fetch_status = tk.Label(fetch_row, text="", font=FNSM, bg=BG, fg=DIM)
        self.fetch_status.pack(side="left", padx=8)

        self._lbl(frame, "quality")
        list_frame = tk.Frame(frame, bg=SURF, highlightbackground=BORDER, highlightthickness=1)
        list_frame.pack(fill="x", pady=(2, 8))
        list_scroll = tk.Scrollbar(list_frame, bg=SURF, troughcolor=SURF, bd=0, width=8)
        self.format_list = tk.Listbox(
            list_frame,
            bg=SURF,
            fg=TEXT,
            font=FNMONO,
            selectbackground=ACCENT,
            selectforeground="#ffffff",
            bd=0,
            highlightthickness=0,
            activestyle="none",
            height=6,
            yscrollcommand=list_scroll.set,
        )
        list_scroll.config(command=self.format_list.yview)
        list_scroll.pack(side="right", fill="y")
        self.format_list.pack(side="left", fill="both", expand=True, padx=4, pady=4)
        self.format_list.bind("<MouseWheel>", lambda e: self.format_list.yview_scroll(int(-1 * (e.delta / 120)), "units"))
        self.format_list.bind("<Enter>", lambda _e: self.unbind("<MouseWheel>"))
        self.format_list.bind("<Leave>", lambda _e: self.bind("<MouseWheel>", self._mousewheel) if self._cursor_in_canvas() else None)

        grid = tk.Frame(frame, bg=BG)
        grid.pack(fill="x", pady=(0, 6))
        grid.columnconfigure(0, weight=1)
        grid.columnconfigure(1, weight=1)
        grid.columnconfigure(2, weight=1)

        start_col = tk.Frame(grid, bg=BG)
        start_col.grid(row=0, column=0, sticky="ew", padx=(0, 6))
        self._lbl(start_col, "start")
        self.start_var = tk.StringVar()
        self._entry(start_col, self.start_var).pack(fill="x", pady=(2, 0))
        self.start_hint = tk.Label(start_col, font=("Segoe UI", 8), bg=BG, fg=DIM)
        self.start_hint.pack(anchor="w")

        end_col = tk.Frame(grid, bg=BG)
        end_col.grid(row=0, column=1, sticky="ew", padx=(0, 6))
        self._lbl(end_col, "end")
        self.end_var = tk.StringVar()
        self._entry(end_col, self.end_var).pack(fill="x", pady=(2, 0))
        self.end_hint = tk.Label(end_col, font=("Segoe UI", 8), bg=BG, fg=DIM)
        self.end_hint.pack(anchor="w")

        out_col = tk.Frame(grid, bg=BG)
        out_col.grid(row=0, column=2, sticky="ew")
        self._lbl(out_col, "output_format")
        self.output_format = tk.StringVar(value="mp4")
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("D.TMenubutton", background=SURF, foreground=TEXT, relief="flat", font=FONT)
        self.output_menu = ttk.OptionMenu(out_col, self.output_format, "mp4", *FMTS, command=lambda _: self._format_changed())
        self.output_menu.configure(style="D.TMenubutton")
        self.output_menu["menu"].configure(bg=SURF, fg=TEXT, activebackground=ACCENT, activeforeground="#ffffff", font=FONT, bd=0)
        self.output_menu.pack(fill="x", pady=(2, 0))

        self._lbl(frame, "cut_method")
        mode_row = tk.Frame(frame, bg=BG)
        mode_row.pack(fill="x", pady=(2, 6))
        self.mode = tk.StringVar(value="reencode")
        for value, key in (("direct", "direct"), ("post", "post"), ("reencode", "reencode")):
            self._radio(mode_row, self.mode, value, key).pack(anchor="w", pady=1)

        self._lbl(frame, "codec")
        codec_row = tk.Frame(frame, bg=BG)
        codec_row.pack(fill="x", pady=(2, 4))
        self.codec = tk.StringVar(value="h264")
        for value, key in (("h264", "h264"), ("h265", "h265"), ("copy", "copy")):
            self._radio(codec_row, self.codec, value, key).pack(side="left", padx=(0, 10))

        self._lbl(frame, "reencode_size")
        size_row = tk.Frame(frame, bg=BG)
        size_row.pack(fill="x", pady=(2, 4))
        self.reencode_size = tk.StringVar(value="source")
        for value, key in (("source", "size_source"), ("1080", "size_1080"), ("720", "size_720"), ("480", "size_480")):
            self._radio(size_row, self.reencode_size, value, key).pack(side="left", padx=(0, 10))

        self.tip_lbl = tk.Label(frame, text="", font=FNSM, bg=BG, fg=ORANGE, anchor="w")
        self.tip_lbl.pack(fill="x")

        self._lbl(frame, "folder")
        folder_row = tk.Frame(frame, bg=BG)
        folder_row.pack(fill="x", pady=(2, 10))
        self.folder = tk.StringVar(value=os.path.join(os.path.expanduser("~"), "Downloads"))
        self._entry(folder_row, self.folder).pack(side="left", fill="x", expand=True)
        self._btn(folder_row, "choose", self._browse, small=True).pack(side="left", padx=(6, 0))

        style.configure(
            "P.Horizontal.TProgressbar",
            troughcolor=SURF,
            background=ACCENT,
            bordercolor=SURF,
            lightcolor=ACCENT,
            darkcolor=ACCENT,
            thickness=8,
        )
        self.download_btn = self._btn(frame, "download", self._start, big=True)
        self.download_btn.pack(fill="x", pady=(0, 4))
        self.cancel_btn = self._btn(frame, "cancel", self._cancel, big=True, danger=True)
        self.cancel_btn.pack(fill="x")
        self.cancel_btn.config(state="disabled")

        tk.Frame(frame, bg=BORDER, height=1).pack(fill="x", pady=(10, 6))
        self.progress = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(frame, variable=self.progress, maximum=100, style="P.Horizontal.TProgressbar")
        self.progress_bar.pack(fill="x", pady=(0, 4))
        self.status = tk.StringVar()
        self.status_lbl = tk.Label(frame, textvariable=self.status, font=FNSM, bg=BG, fg=DIM, anchor="w")
        self.status_lbl.pack(fill="x")

        tk.Frame(frame, bg=BORDER, height=1).pack(fill="x", pady=(8, 6))
        log_frame = tk.Frame(frame, bg=SURF, highlightbackground=BORDER, highlightthickness=1)
        log_frame.pack(fill="both", expand=True, pady=(0, 14))
        log_scroll = tk.Scrollbar(log_frame, bg=SURF, troughcolor=SURF, bd=0, width=8)
        self.log = tk.Text(
            log_frame,
            bg=SURF,
            fg=TEXT,
            font=FNMONO,
            bd=0,
            padx=6,
            pady=4,
            state="disabled",
            wrap="word",
            height=7,
            insertbackground=TEXT,
            selectbackground=ACCENT,
            yscrollcommand=log_scroll.set,
        )
        self.log.bind("<MouseWheel>", lambda e: self.log.yview_scroll(int(-1 * (e.delta / 120)), "units"))
        self.log.bind("<Enter>", lambda _e: self.unbind("<MouseWheel>"))
        self.log.bind("<Leave>", lambda _e: self.bind("<MouseWheel>", self._mousewheel) if self._cursor_in_canvas() else None)
        log_scroll.config(command=self.log.yview)
        log_scroll.pack(side="right", fill="y")
        self.log.pack(side="left", fill="both", expand=True)

    def _mousewheel(self, event):
        self._cv.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _cursor_in_canvas(self):
        try:
            x, y = self.winfo_pointerxy()
            widget = self.winfo_containing(x, y)
            while widget:
                if widget == self._cv:
                    return True
                widget = getattr(widget, "master", None)
        except tk.TclError:
            return False
        return False

    def _lbl(self, parent, key):
        label = tk.Label(parent, font=FNSM, bg=BG, fg=DIM)
        label.pack(anchor="w")
        self._labels.append((label, key))
        return label

    def _entry(self, parent, var):
        return tk.Entry(
            parent,
            textvariable=var,
            font=FONT,
            bg=SURF,
            fg=TEXT,
            insertbackground=TEXT,
            relief="flat",
            bd=0,
            highlightbackground=BORDER,
            highlightthickness=1,
            highlightcolor=ACCENT,
        )

    def _btn(self, parent, key, command, small=False, big=False, danger=False):
        if danger:
            bg, fg, active = "#43262b", RED, "#553139"
        elif big:
            bg, fg, active = ACCENT, "#ffffff", ACCENT_H
        else:
            bg, fg, active = SURF_2, TEXT, BORDER
        font = FNSM if small else (FNLG if big else FONT)
        padx, pady = (6, 3) if small else ((8, 7) if big else (6, 4))
        button = tk.Button(
            parent,
            command=command,
            bg=bg,
            fg=fg,
            font=font,
            activebackground=active,
            activeforeground=fg,
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=padx,
            pady=pady,
        )
        button.bind("<Enter>", lambda _e: button.config(bg=active))
        button.bind("<Leave>", lambda _e: button.config(bg=bg))
        self._buttons.append((button, key))
        return button

    def _radio(self, parent, variable, value, key):
        radio = tk.Radiobutton(
            parent,
            variable=variable,
            value=value,
            font=FNSM,
            bg=BG,
            fg=TEXT,
            selectcolor=SURF,
            activebackground=BG,
            activeforeground=TEXT,
            cursor="hand2",
        )
        self._radios.append((radio, key))
        return radio

    def _apply_language(self):
        self.title(self.t("app_title"))
        self.title_lbl.config(text=self.t("app_title"))
        self.tagline_lbl.config(text=self.t("tagline"))
        self.lang_lbl.config(text=self.t("language"))
        for label, key in self._labels:
            label.config(text=self.t(key))
        for button, key in self._buttons:
            button.config(text=self.t(key))
        for radio, key in self._radios:
            radio.config(text=self.t(key))
        self.start_hint.config(text=self.t("time_hint"))
        self.end_hint.config(text=self.t("time_hint"))
        self.status.set(self.t("ready"))
        self._format_changed()
        self._default_formats()

    def _format_changed(self):
        text = self.t("twitter_tip") if self.output_format.get() == "mp4" else ""
        self.tip_lbl.config(text=text)

    def _default_formats(self):
        current_selection = None
        if self.format_list.curselection():
            current_selection = self.format_list.get(self.format_list.curselection()[0])
        self.format_list.delete(0, "end")
        self._fmap = {}
        rows = [
            (f"--- {self.t('video')} --------------------------", None),
            (f"  {self.t('best_video')}", "bestvideo+bestaudio/best"),
            ("  4K (2160p)", "bestvideo[height<=2160]+bestaudio/best[height<=2160]"),
            ("  2K (1440p)", "bestvideo[height<=1440]+bestaudio/best[height<=1440]"),
            ("  1080p", "bestvideo[height<=1080]+bestaudio/best[height<=1080]"),
            ("  720p", "bestvideo[height<=720]+bestaudio/best[height<=720]"),
            ("  480p", "bestvideo[height<=480]+bestaudio/best[height<=480]"),
            ("  360p", "bestvideo[height<=360]+bestaudio/best[height<=360]"),
            (f"--- {self.t('audio')} --------------------------", None),
            (f"  {self.t('best_audio_mp3')}", "bestaudio/best|audio|mp3"),
            (f"  {self.t('best_audio_aac')}", "bestaudio/best|audio|aac"),
        ]
        for label, fmt in rows:
            self.format_list.insert("end", label)
            self._fmap[label] = fmt
            if fmt is None:
                idx = self.format_list.size() - 1
                self.format_list.itemconfig(idx, fg=DIM, selectbackground=SURF, selectforeground=DIM)
        if current_selection and current_selection in self._fmap:
            idx = list(self._fmap).index(current_selection)
            self.format_list.selection_set(idx)
        else:
            self.format_list.selection_set(1)

    def _paste(self):
        try:
            self.url_var.set(self.clipboard_get().strip())
        except tk.TclError:
            pass

    def _browse(self):
        directory = filedialog.askdirectory(initialdir=self.folder.get())
        if directory:
            self.folder.set(directory)

    def _fetch(self):
        url = self.url_var.get().strip()
        if not url:
            messagebox.showwarning("URL", self.t("need_url"))
            return
        ytdlp = find_exe("yt-dlp")
        if not ytdlp:
            self.fetch_status.config(text=f"yt-dlp {self.t('not_found')}", fg=RED)
            return
        self.fetch_btn.config(state="disabled")
        self.fetch_status.config(text=self.t("fetching"), fg=ORANGE)
        threading.Thread(target=self._do_fetch, args=(ytdlp, url), daemon=True).start()

    def _do_fetch(self, ytdlp, url):
        try:
            result = subprocess.run(
                [ytdlp, "-F", "--no-playlist", url],
                capture_output=True,
                text=True,
                encoding=CONSOLE_ENCODING,
                errors="replace",
                creationflags=self._creation_flags(),
            )
            if result.returncode != 0:
                raise RuntimeError(result.stderr.strip() or result.stdout.strip())
            self.after(0, self._fill_formats, result.stdout)
        except Exception as exc:
            self.after(0, self.fetch_status.config, {"text": f"{self.t('error')}: {exc}", "fg": RED})
        finally:
            self.after(0, self.fetch_btn.config, {"state": "normal"})

    def _fill_formats(self, raw):
        videos, audios = [], []
        for line in raw.splitlines():
            parts = line.split()
            if len(parts) < 3 or not parts[0] or not parts[0][0].isalnum():
                continue
            fmt_id, ext, res = parts[0], parts[1], parts[2]
            if fmt_id.lower() in {"id", "format"} or line.startswith("["):
                continue
            note = ""
            bitrate = re.search(r"(\d+(?:\.\d+)?[kKmM])", line)
            if bitrate:
                note = bitrate.group(1)
            lower = line.lower()
            if res in ("audio", "only") or "audio only" in lower:
                audios.append((f"  {fmt_id:<8} {ext:<5} {self.t('audio'):<8} {note}", fmt_id))
            else:
                videos.append((f"  {fmt_id:<8} {ext:<5} {res:<12} {note}", fmt_id))

        if not videos and not audios:
            self.fetch_status.config(text=self.t("formats_not_found"), fg=ORANGE)
            return

        self.format_list.delete(0, "end")
        self._fmap = {}

        def header(text):
            self.format_list.insert("end", text)
            idx = self.format_list.size() - 1
            self.format_list.itemconfig(idx, fg=DIM, selectbackground=SURF, selectforeground=DIM)
            self._fmap[text] = None

        header(f"--- {self.t('auto')} --------------------------")
        for label, fmt in (
            (f"  {self.t('best_video')}", "bestvideo+bestaudio/best"),
            (f"  {self.t('best_audio_mp3')}", "bestaudio/best|audio|mp3"),
        ):
            self.format_list.insert("end", label)
            self._fmap[label] = fmt
        if videos:
            header(f"--- {self.t('video')} --------------------------")
            for label, fmt in reversed(videos):
                self.format_list.insert("end", label)
                self._fmap[label] = fmt
        if audios:
            header(f"--- {self.t('audio')} --------------------------")
            for label, fmt in reversed(audios):
                self.format_list.insert("end", label)
                self._fmap[label] = fmt

        self.format_list.selection_set(1)
        self.fetch_status.config(text=f"{len(videos) + len(audios)} {self.t('formats_found')}", fg=GREEN)

    def _get_format(self):
        selected = self.format_list.curselection()
        if not selected:
            return None, None
        label = self.format_list.get(selected[0])
        return label.strip(), self._fmap.get(label)

    def _start(self):
        url = self.url_var.get().strip()
        folder = self.folder.get().strip()
        start_text = self.start_var.get().strip()
        end_text = self.end_var.get().strip()

        if not url:
            messagebox.showerror(self.t("error"), self.t("need_url"))
            return
        try:
            start_sec = time_to_seconds(start_text)
        except ValueError:
            messagebox.showerror(self.t("error"), f"{self.t('invalid_start')}: {start_text}")
            return
        try:
            end_sec = time_to_seconds(end_text)
        except ValueError:
            messagebox.showerror(self.t("error"), f"{self.t('invalid_end')}: {end_text}")
            return
        if start_sec is not None and end_sec is not None and end_sec <= start_sec:
            messagebox.showerror(self.t("error"), self.t("end_before_start"))
            return

        _label, fmt = self._get_format()
        if fmt is None:
            messagebox.showerror(self.t("error"), self.t("need_format"))
            return

        ytdlp = find_exe("yt-dlp")
        ffmpeg = find_exe("ffmpeg")
        if not ytdlp:
            messagebox.showerror(self.t("error"), "yt-dlp not found.\npip install -U yt-dlp")
            return

        has_cut = start_sec is not None or end_sec is not None
        is_audio_request = "|audio|" in fmt or self.output_format.get() in AUDIO_FORMATS
        if ((has_cut and self.mode.get() in ("direct", "post", "reencode")) or is_audio_request) and not ffmpeg:
            messagebox.showerror(self.t("error"), self.t("ffmpeg_required"))
            return

        os.makedirs(folder, exist_ok=True)
        self.progress.set(0)
        self.progress_bar.config(mode="determinate")
        self.download_btn.config(state="disabled")
        self.cancel_btn.config(state="normal")
        self._log(
            f"\n> mode={self.mode.get()} fmt={self.output_format.get()} codec={self.codec.get()} size={self.reencode_size.get()} "
            f"start={start_text or '-'} end={end_text or '-'}",
            DIM,
        )
        if has_cut and self.mode.get() == "post":
            self._log(self.t("copy_note"), ORANGE)

        threading.Thread(
            target=self._run,
            args=(url, fmt, start_sec, end_sec, folder, ytdlp, ffmpeg),
            daemon=True,
        ).start()

    def _run(self, url, fmt, start_sec, end_sec, folder, ytdlp, ffmpeg):
        temp_dir = None
        try:
            has_cut = start_sec is not None or end_sec is not None
            mode = self.mode.get()
            output_format = self.output_format.get()
            is_audio = "|audio|" in fmt or output_format in AUDIO_FORMATS
            needs_post = has_cut and mode in ("post", "reencode")
            self._phase_weights = (0.75, 0.25) if needs_post else (1.0, 0.0)

            if needs_post:
                temp_dir = tempfile.mkdtemp(prefix="_ytdlp_gui_", dir=folder)
                output_template = os.path.join(temp_dir, "%(id)s.%(ext)s")
            else:
                output_template = os.path.join(folder, "%(title).180B.%(ext)s")

            cmd = [ytdlp, "--newline", "--no-playlist", "--no-part", "-o", output_template]
            if is_audio:
                audio_fmt = output_format if output_format in AUDIO_FORMATS else "mp3"
                base_fmt = fmt.split("|audio|")[0] if "|audio|" in fmt else "bestaudio/best"
                cmd += ["-f", base_fmt, "-x", "--audio-format", audio_fmt]
            else:
                merge_fmt = "mp4" if output_format in ("mp4", "mov", "avi") else output_format
                cmd += ["-f", fmt, "--merge-output-format", merge_fmt]

            if has_cut and mode == "direct":
                start = seconds_to_time(start_sec or 0)
                end = seconds_to_time(end_sec) if end_sec is not None else "inf"
                cmd += ["--download-sections", f"*{start}-{end}", "--force-keyframes-at-cuts"]

            cmd.append(url)
            self.after(0, self._set_status, f"{self.t('downloading')}...", ACCENT)
            downloaded = self._run_ytdlp(cmd, phase_start=0, phase_size=self._phase_weights[0])

            if needs_post:
                source = downloaded if downloaded and os.path.exists(downloaded) else self._newest_file(temp_dir)
                if not source:
                    raise RuntimeError("Downloaded file could not be found.")
                output = self._build_output_path(folder, source, output_format)
                self.after(0, self._set_status, f"{self.t('cutting')}...", ACCENT)
                self._run_ffmpeg_cut(source, output, start_sec, end_sec, mode, is_audio)
                self.after(0, self._log, f"{self.t('saved_to')}: {output}", GREEN)
            elif downloaded:
                self.after(0, self._log, f"{self.t('saved_to')}: {downloaded}", GREEN)

            self.after(0, self.progress.set, 100)
            self.after(0, self._set_status, self.t("done"), GREEN)
            self.after(0, self._log, self.t("done"), GREEN)
        except RuntimeError as exc:
            if str(exc) == "canceled":
                self.after(0, self._set_status, self.t("canceled"), ORANGE)
                self.after(0, self._log, self.t("canceled"), ORANGE)
            else:
                self.after(0, self._set_status, self.t("error"), RED)
                self.after(0, self._log, f"{self.t('error')}: {exc}", RED)
        except Exception as exc:
            self.after(0, self._set_status, self.t("error"), RED)
            self.after(0, self._log, f"{self.t('error')}: {exc}", RED)
        finally:
            if temp_dir:
                try:
                    shutil.rmtree(temp_dir)
                    self.after(0, self._log, self.t("temp_deleted"), DIM)
                except OSError:
                    pass
            self._proc = None
            self.after(0, self.download_btn.config, {"state": "normal"})
            self.after(0, self.cancel_btn.config, {"state": "disabled"})

    def _run_ytdlp(self, cmd, phase_start, phase_size):
        destination = None
        saw_percent = False
        self.after(0, self.progress_bar.config, {"mode": "indeterminate"})
        self.after(0, self.progress_bar.start, 12)
        self._proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            encoding=CONSOLE_ENCODING,
            errors="replace",
            creationflags=self._creation_flags(),
        )
        for raw_line in self._proc.stdout:
            line = raw_line.strip()
            if not line:
                continue
            match = re.search(r"\[download\]\s+([\d.]+)%", line)
            if match:
                if not saw_percent:
                    saw_percent = True
                    self.after(0, self.progress_bar.stop)
                    self.after(0, self.progress_bar.config, {"mode": "determinate"})
                percent = float(match.group(1))
                total = phase_start + percent * phase_size
                eta_match = re.search(r"\bETA\s+([0-9:]+|Unknown)", line, re.IGNORECASE)
                eta = normalize_eta(eta_match.group(1)) if eta_match else ""
                eta_text = f" · kalan ~{eta}" if eta else ""
                self.after(0, self.progress.set, min(99, total))
                self.after(0, self._set_status, f"{self.t('downloading')} %{percent:.1f}{eta_text}", ACCENT)
            destination = self._extract_destination(line, destination)
            self.after(0, self._log, line, self._line_color(line))

        self._proc.wait()
        self.after(0, self.progress_bar.stop)
        self.after(0, self.progress_bar.config, {"mode": "determinate"})
        if self._proc.returncode not in (0, None):
            if self._proc.returncode < 0:
                raise RuntimeError("canceled")
            raise RuntimeError(f"yt-dlp exit code: {self._proc.returncode}")
        return destination

    def _run_ffmpeg_cut(self, source, output, start_sec, end_sec, mode, is_audio):
        duration = None
        if start_sec is not None and end_sec is not None:
            duration = end_sec - start_sec

        if mode == "reencode" and start_sec and start_sec > 3:
            seek_margin = 3.0
            input_seek = max(0.0, start_sec - seek_margin)
            inner_seek = start_sec - input_seek
        elif start_sec:
            input_seek = start_sec
            inner_seek = 0.0
        else:
            input_seek = 0.0
            inner_seek = 0.0

        cmd = [
            ffmpeg := find_exe("ffmpeg"),
            "-y",
            "-hide_banner",
            "-nostdin",
            "-progress",
            "pipe:1",
            "-stats_period",
            "0.5",
        ]
        if input_seek:
            cmd += ["-ss", seconds_to_time(input_seek)]
        cmd += ["-i", source]
        if start_sec is not None:
            cmd += ["-ss", seconds_to_time(inner_seek)]
        if duration is not None:
            cmd += ["-t", seconds_to_time(duration)]
        elif end_sec is not None:
            cmd += ["-to", seconds_to_time(max(0.0, end_sec - input_seek))]

        if is_audio:
            if self.output_format.get() in {"mp3", "aac", "ogg", "m4a", "flac", "wav"}:
                cmd += ["-vn"]
            if mode == "reencode":
                codec = "libmp3lame" if self.output_format.get() == "mp3" else "aac"
                cmd += ["-c:a", codec]
            else:
                cmd += ["-c", "copy"]
        elif mode == "reencode":
            video_codec = {"h264": "libx264", "h265": "libx265", "copy": "copy"}.get(self.codec.get(), "libx264")
            if video_codec == "copy":
                cmd += ["-c", "copy"]
            else:
                max_height = {"1080": 1080, "720": 720, "480": 480}.get(self.reencode_size.get())
                if max_height:
                    cmd += ["-vf", f"scale=-2:min({max_height}\\,ih)"]
                cmd += ["-c:v", video_codec, "-preset", "superfast", "-crf", "21", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart"]
        else:
            cmd += ["-c", "copy", "-avoid_negative_ts", "make_zero"]

        cmd += [output]
        self.after(0, self._log, "> ffmpeg cut started", DIM)
        self.after(0, self.progress_bar.stop)
        self.after(0, self.progress_bar.config, {"mode": "determinate"})
        self.after(0, self.progress.set, self._phase_weights[0] * 100)
        self._proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            encoding=CONSOLE_ENCODING,
            errors="replace",
            creationflags=self._creation_flags(),
        )

        phase_start = self._phase_weights[0] * 100
        phase_size = self._phase_weights[1] * 100
        last_status = 0
        started_at = time.time()
        saw_progress = False
        if not duration:
            self.after(0, self.progress_bar.config, {"mode": "indeterminate"})
            self.after(0, self.progress_bar.start, 12)
        for raw_line in self._proc.stdout:
            line = raw_line.strip()
            if not line:
                continue
            out_time = None
            if line.startswith("out_time_ms="):
                try:
                    out_time = int(line.split("=", 1)[1]) / 1_000_000
                except ValueError:
                    out_time = None
            elif line.startswith("out_time="):
                out_time = ffmpeg_time_to_seconds(line.split("=", 1)[1])
            else:
                match = re.search(r"time=(\d+:\d+:\d+(?:\.\d+)?)", line)
                if match:
                    out_time = ffmpeg_time_to_seconds(match.group(1))

            if out_time is not None and duration:
                saw_progress = True
                percent = max(0, min(100, out_time / duration * 100))
                total = phase_start + percent / 100 * phase_size
                self.after(0, self.progress.set, min(99, total))
                if time.time() - last_status > 0.2:
                    last_status = time.time()
                    elapsed = max(0.1, time.time() - started_at)
                    remaining = (elapsed / percent * (100 - percent)) if percent > 0 else 0
                    eta = f" · kalan ~{short_duration(remaining)}" if remaining else ""
                    self.after(0, self._set_status, f"{self.t('processing')} %{percent:.1f}{eta}", ACCENT)
            elif line == "progress=end" and duration and not saw_progress:
                self.after(0, self.progress.set, min(99, phase_start + phase_size))
            elif not line.startswith(("frame=", "fps=", "stream_", "bitrate=", "total_size=", "out_time", "dup_frames=", "drop_frames=", "speed=", "progress=")):
                self.after(0, self._log, line, self._line_color(line))

        self._proc.wait()
        self.after(0, self.progress_bar.stop)
        self.after(0, self.progress_bar.config, {"mode": "determinate"})
        if self._proc.returncode not in (0, None):
            if self._proc.returncode < 0:
                raise RuntimeError("canceled")
            raise RuntimeError(f"ffmpeg exit code: {self._proc.returncode}")

    def _extract_destination(self, line, current):
        if "[download] Destination:" in line:
            return line.split("[download] Destination:", 1)[1].strip()
        if "[ExtractAudio] Destination:" in line:
            return line.split("[ExtractAudio] Destination:", 1)[1].strip()
        match = re.search(r'Merging formats into "(.+)"', line)
        if match:
            return match.group(1)
        match = re.search(r'\[download\]\s+(.+)\s+has already been downloaded', line)
        if match:
            return match.group(1)
        return current

    def _build_output_path(self, folder, source, output_format):
        base = os.path.splitext(os.path.basename(source))[0]
        base = re.sub(r"\s+", " ", base).strip()
        output = os.path.join(folder, f"{base}_cut.{output_format}")
        if not os.path.exists(output):
            return output
        stamp = time.strftime("%Y%m%d_%H%M%S")
        return os.path.join(folder, f"{base}_cut_{stamp}.{output_format}")

    def _newest_file(self, folder):
        files = []
        for root, _dirs, names in os.walk(folder):
            for name in names:
                path = os.path.join(root, name)
                if os.path.isfile(path):
                    files.append(path)
        return max(files, key=os.path.getmtime) if files else None

    def _cancel(self):
        if self._proc:
            try:
                self._proc.terminate()
            except OSError:
                pass
            self._set_status(self.t("canceling"), ORANGE)

    def _log(self, text, color=None):
        self.log.config(state="normal")
        tag = f"c{abs(hash(color or TEXT))}"
        self.log.tag_config(tag, foreground=color or TEXT)
        self.log.insert("end", text + "\n", tag)
        self.log.see("end")
        self.log.config(state="disabled")

    def _set_status(self, text, color=None):
        self.status.set(text)
        self.status_lbl.config(fg=color or DIM)

    def _line_color(self, line):
        upper = line.upper()
        if "ERROR" in upper:
            return RED
        if "WARNING" in upper:
            return ORANGE
        if any(token in line for token in ("Destination", "Merging", "has already been downloaded", "Deleting original file")):
            return GREEN
        return TEXT

    def _check_startup(self):
        missing = missing_deps()
        if missing:
            self._log(f"{self.t('missing')}: {', '.join(missing)}", ORANGE)
            if "yt-dlp" in missing:
                self._log(self.t("install_ytdlp"), ORANGE)
            if "ffmpeg" in missing:
                self._log(self.t("install_ffmpeg"), ORANGE)
            self._set_status(self.t("missing_deps"), ORANGE)
        else:
            self._log(self.t("deps_ready"), GREEN)
            self._set_status(self.t("ready"), DIM)

    def _creation_flags(self):
        return subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0


if __name__ == "__main__":
    App().mainloop()
