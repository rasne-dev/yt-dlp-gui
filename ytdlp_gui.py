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


BG      = "#1e2029"
SURF    = "#2a2d3a"
SURF_2  = "#353848"
ACCENT  = "#5b8dee"
ACCENT_H= "#7aa3f5"
TEXT    = "#eef0f8"
DIM     = "#8892a4"
GREEN   = "#4ec994"
RED     = "#f06b6b"
ORANGE  = "#f0aa4a"
BORDER  = "#3d4259"
FONT    = ("Segoe UI", 10)
FNSM    = ("Segoe UI", 9)
FNLG    = ("Segoe UI", 11, "bold")
FNMONO  = ("Consolas", 9)
FMTS    = ["mp4", "mkv", "webm", "mov", "avi", "mp3", "aac", "ogg", "m4a", "flac", "wav"]
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
        "direct": "Direkt kes  (hızlı, bazen keyframe'e kayar)",
        "post": "Tam indir → kes  (hızlı kopya)",
        "reencode": "Tam indir → yeniden kodla  (en doğru, yavaş)",
        "codec": "Codec  (yeniden kodlama modunda)",
        "h264": "h264 – uyumlu",
        "h265": "h265 – küçük dosya",
        "copy": "copy – kodlama yok",
        "reencode_size": "Çözünürlük  (yeniden kodlamada)",
        "size_source": "Orijinal",
        "size_1080": "1080p",
        "size_720": "720p",
        "size_480": "480p",
        "twitter_tip": "MP4 paylaşımı için  yeniden kodla + h264  en güvenli seçenek.",
        "folder": "Kayıt Klasörü",
        "choose": "Seç",
        "download": "İndir",
        "cancel": "İptal",
        "ready": "Hazır",
        "missing_deps": "Eksik bağımlılık — log'a bakın",
        "deps_ready": "yt-dlp ve ffmpeg hazır.",
        "missing": "Eksik",
        "install_ytdlp": "yt-dlp kurmak için: pip install -U yt-dlp",
        "install_ffmpeg": "ffmpeg'i kurup PATH'e ekleyin.",
        "need_url": "Önce URL girin.",
        "fetching": "Analiz ediliyor…",
        "not_found": "bulunamadı",
        "error": "Hata",
        "invalid_start": "Geçersiz başlangıç zamanı",
        "invalid_end": "Geçersiz bitiş zamanı",
        "end_before_start": "Bitiş başlangıçtan büyük olmalı.",
        "need_format": "Format seçin.",
        "ffmpeg_required": "Bu işlem için ffmpeg gerekli.",
        "downloading": "İndiriliyor",
        "processing": "İşleniyor",
        "cutting": "Kesiliyor",
        "ffmpeg_start": "ffmpeg kesme başladı…",
        "done": "Tamamlandı!",
        "canceling": "İptal ediliyor…",
        "canceled": "İptal edildi.",
        "formats_found": "format bulundu",
        "formats_not_found": "Format bulunamadı.",
        "auto": "Otomatik",
        "video": "Video",
        "audio": "Ses",
        "best_video": "En İyi Video + Ses",
        "best_audio_mp3": "En İyi Ses (MP3)",
        "best_audio_aac": "En İyi Ses (AAC)",
        "saved_to": "Kaydedildi",
        "eta_remaining": "  ·  kalan ~{}",
        "copy_note": "copy modu yeniden kodlamaz; bazı videolarda ilk saniyelerde küçük kayma normaldir.",
        "timeline_hint": "Süre için önce Formatları Getir'e bas",
        "timeline_drag": "Yeşil = başlangıç · Kırmızı = bitiş  (sürükle veya track'e tıkla)",
        "range_label": "Seçili",
        "full_video": "Tüm video",
        "open_folder": "📂 Klasörü Aç",
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
        "direct": "Direct cut  (fast, may snap to keyframes)",
        "post": "Download full → cut  (fast copy)",
        "reencode": "Download full → re-encode  (most accurate, slow)",
        "codec": "Codec  (re-encode mode)",
        "h264": "h264 – compatible",
        "h265": "h265 – smaller file",
        "copy": "copy – no re-encode",
        "reencode_size": "Resolution  (re-encode)",
        "size_source": "Original",
        "size_1080": "1080p",
        "size_720": "720p",
        "size_480": "480p",
        "twitter_tip": "For MP4 sharing, re-encode + h264 is the safest option.",
        "folder": "Save Folder",
        "choose": "Choose",
        "download": "Download",
        "cancel": "Cancel",
        "ready": "Ready",
        "missing_deps": "Missing dependency — see log",
        "deps_ready": "yt-dlp and ffmpeg are ready.",
        "missing": "Missing",
        "install_ytdlp": "To install yt-dlp: pip install -U yt-dlp",
        "install_ffmpeg": "Install ffmpeg and add it to PATH.",
        "need_url": "Enter a URL first.",
        "fetching": "Analyzing…",
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
        "ffmpeg_start": "ffmpeg cutting started…",
        "done": "Completed!",
        "canceling": "Canceling…",
        "canceled": "Canceled.",
        "formats_found": "formats found",
        "formats_not_found": "No formats found.",
        "auto": "Automatic",
        "video": "Video",
        "audio": "Audio",
        "best_video": "Best Video + Audio",
        "best_audio_mp3": "Best Audio (MP3)",
        "best_audio_aac": "Best Audio (AAC)",
        "saved_to": "Saved to",
        "eta_remaining": "  ·  ~{} left",
        "copy_note": "copy mode doesn't re-encode; brief drift on first seconds is normal.",
        "timeline_hint": "Fetch formats first to enable the timeline",
        "timeline_drag": "Green = start · Red = end  (drag or click track)",
        "range_label": "Selected",
        "full_video": "Full video",
        "open_folder": "📂 Open Folder",
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
    nums = [int(p) for p in parts]
    if len(nums) == 2:
        hours, minutes, seconds = 0, nums[0], nums[1]
    else:
        hours, minutes, seconds = nums
    if minutes > 59 or seconds > 59:
        raise ValueError(value)
    return hours * 3600 + minutes * 60 + seconds


def seconds_to_time(seconds):
    seconds = max(0.0, float(seconds))
    whole = int(seconds)
    ms = int(round((seconds - whole) * 1000))
    h = whole // 3600
    m = (whole % 3600) // 60
    s = whole % 60
    if ms:
        return f"{h:02d}:{m:02d}:{s:02d}.{ms:03d}"
    return f"{h:02d}:{m:02d}:{s:02d}"


def ffmpeg_time_to_seconds(value):
    match = re.match(r"(\d+):(\d+):(\d+(?:\.\d+)?)", value)
    if not match:
        return None
    return int(match.group(1)) * 3600 + int(match.group(2)) * 60 + float(match.group(3))


def short_duration(seconds, lang="tr"):
    seconds = max(0, int(round(float(seconds))))
    minutes, sec = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    if lang == "en":
        if hours:   return f"{hours}h {minutes:02d}m"
        if minutes: return f"{minutes}m {sec:02d}s"
        return f"{sec}s"
    else:
        if hours:   return f"{hours} sa {minutes:02d} dk"
        if minutes: return f"{minutes} dk {sec:02d} sn"
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


def _fmt_compact(t):
    """'00:27:50' → '27:50'"""
    if t and t.startswith("00:"):
        return t[3:]
    return t or ""


# ─────────────────────────────────────────────────────────────
class TimelineWidget(tk.Canvas):
    H        = 52
    TRACK_H  = 7
    HANDLE_R = 10
    PAD      = 16

    C_TRACK  = "#3a3f55"
    C_RANGE  = "#5b8dee"
    C_START  = "#4ec994"
    C_END    = "#f06b6b"
    C_HINT   = "#555c72"
    C_BG     = "#1e2029"

    def __init__(self, parent, on_change=None, **kwargs):
        kwargs.setdefault("bg", self.C_BG)
        kwargs.setdefault("highlightthickness", 0)
        kwargs.setdefault("height", self.H)
        super().__init__(parent, **kwargs)
        self._duration  = 0.0
        self._start_sec = 0.0
        self._end_sec   = 0.0
        self._dragging  = None
        self._on_change = on_change
        self.bind("<Configure>",       self._redraw)
        self.bind("<ButtonPress-1>",   self._on_press)
        self.bind("<B1-Motion>",       self._on_drag)
        self.bind("<ButtonRelease-1>", self._on_release)

    # ── Public API ────────────────────────────────────────────
    def set_duration(self, seconds):
        self._duration  = max(0.0, float(seconds))
        self._start_sec = 0.0
        self._end_sec   = self._duration
        self._redraw()

    def set_range(self, start, end):
        if self._duration <= 0:
            return
        self._start_sec = max(0.0, min(float(start or 0), self._duration))
        self._end_sec   = max(0.0, min(float(end or self._duration), self._duration))
        self._redraw()

    def get_range(self):
        return self._start_sec, self._end_sec

    # ── Koordinat yardımcıları ────────────────────────────────
    def _track_x(self):
        return self.PAD, max(self.PAD + 1, self.winfo_width() - self.PAD)

    def _track_y(self):
        return self.HANDLE_R + 6          # daha yukarıda → altta etiket için yer

    def _sec_to_x(self, sec):
        x0, x1 = self._track_x()
        if self._duration <= 0:
            return x0
        return x0 + (sec / self._duration) * (x1 - x0)

    def _x_to_sec(self, x):
        x0, x1 = self._track_x()
        if x1 <= x0:
            return 0.0
        return max(0.0, min(1.0, (x - x0) / (x1 - x0))) * self._duration

    # ── Çizim ─────────────────────────────────────────────────
    def _redraw(self, _event=None):
        self.delete("all")
        w = self.winfo_width()
        if w < 10:
            return
        ty = self._track_y()
        x0, x1 = self._track_x()
        th = self.TRACK_H

        # Arka plan track
        self.create_rectangle(x0, ty - th//2, x1, ty + th//2,
                               fill=self.C_TRACK, outline="")

        if self._duration <= 0:
            self.create_text(w // 2, ty, text="–", fill=self.C_HINT,
                             font=("Segoe UI", 9))
            return

        sx = self._sec_to_x(self._start_sec)
        ex = self._sec_to_x(self._end_sec)

        # Seçili aralık
        self.create_rectangle(sx, ty - th//2, ex, ty + th//2,
                               fill=self.C_RANGE, outline="")

        # Tutamaçlar — end önce (start üste çıksın)
        self._draw_handle(ex, ty, self.C_END,   "end")
        self._draw_handle(sx, ty, self.C_START, "start")

        # Etiketler (tutamaç altında, kesilmeden)
        ly = ty + self.HANDLE_R + 8
        self.create_text(sx, ly, text=_fmt_compact(seconds_to_time(self._start_sec)),
                         fill=self.C_START, font=("Segoe UI", 8), anchor="n")
        self.create_text(ex, ly, text=_fmt_compact(seconds_to_time(self._end_sec)),
                         fill=self.C_END,   font=("Segoe UI", 8), anchor="n")
        self.create_text(x1, ly, text=_fmt_compact(seconds_to_time(self._duration)),
                         fill=self.C_HINT,  font=("Segoe UI", 8), anchor="ne")

    def _draw_handle(self, x, y, color, tag):
        r = self.HANDLE_R
        self.create_oval(x-r, y-r, x+r, y+r, fill=color, outline=self.C_BG, width=2, tags=tag)

    # ── Tıklama / sürükleme ───────────────────────────────────
    def _pick_handle(self, x, y):
        """Hangi tutamaca (veya track noktasına) tıklandı?"""
        if self._duration <= 0:
            return None
        ty = self._track_y()
        sx = self._sec_to_x(self._start_sec)
        ex = self._sec_to_x(self._end_sec)
        r  = self.HANDLE_R + 5           # biraz geniş hit area

        in_s = (x - sx)**2 + (y - ty)**2 <= r**2
        in_e = (x - ex)**2 + (y - ty)**2 <= r**2

        if in_s and in_e:
            return "start" if abs(x - sx) <= abs(x - ex) else "end"
        if in_s:
            return "start"
        if in_e:
            return "end"

        # Track şeridine tıklandıysa en yakın tutamacı seç
        x0, x1 = self._track_x()
        if x0 <= x <= x1 and abs(y - ty) <= self.TRACK_H // 2 + 8:
            return "start" if abs(x - sx) <= abs(x - ex) else "end"

        return None

    def _move(self, handle, x):
        sec     = self._x_to_sec(x)
        min_gap = max(0.5, self._duration * 0.001)
        if handle == "start":
            self._start_sec = max(0.0, min(sec, self._end_sec - min_gap))
        else:
            self._end_sec = min(self._duration, max(sec, self._start_sec + min_gap))
        self._redraw()
        if self._on_change:
            self._on_change(self._start_sec, self._end_sec)

    def _on_press(self, e):
        self._dragging = self._pick_handle(e.x, e.y)
        if self._dragging:
            self.config(cursor="sb_h_double_arrow")
            self._move(self._dragging, e.x)   # anında snap

    def _on_drag(self, e):
        if self._dragging and self._duration > 0:
            self._move(self._dragging, e.x)

    def _on_release(self, _e):
        self._dragging = None
        self.config(cursor="")


# ─────────────────────────────────────────────────────────────
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.lang           = tk.StringVar(value="tr")
        self._proc          = None
        self._canceling     = False
        self._fmap          = {}
        self._labels        = []
        self._buttons       = []
        self._radios        = []
        self._phase_weights = (1.0, 0.0)
        self._duration      = 0.0
        self._tl_updating   = False
        self._formats_fetched = False   # dil değişince formatları sıfırlama
        self._build()
        self._apply_language()
        self._fit_to_screen()
        self.after(200, self._check_startup)

    def t(self, key):
        return I18N[self.lang.get()].get(key, key)

    # ── Pencere boyutu ────────────────────────────────────────
    def _fit_to_screen(self):
        self.update_idletasks()
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        w = min(720, max(540, sw - 140))
        h = min(int(sh * 0.88), max(500, sh - 120))
        self.geometry(f"{w}x{h}+{(sw-w)//2}+{max(10,(sh-h)//2)}")
        self.minsize(500, 440)

    # ── UI inşası ─────────────────────────────────────────────
    def _build(self):
        self.title("yt-dlp GUI")
        self.configure(bg=BG)
        self.resizable(True, True)

        # Başlık çubuğu
        hdr = tk.Frame(self, bg=BG)
        hdr.pack(fill="x", padx=16, pady=(12, 0))
        self.title_lbl   = tk.Label(hdr, font=FNLG, bg=BG, fg=ACCENT)
        self.title_lbl.pack(side="left")
        self.tagline_lbl = tk.Label(hdr, font=FNSM, bg=BG, fg=DIM)
        self.tagline_lbl.pack(side="left", padx=8)

        lang_f = tk.Frame(hdr, bg=BG)
        lang_f.pack(side="right")
        self.lang_lbl = tk.Label(lang_f, font=FNSM, bg=BG, fg=DIM)
        self.lang_lbl.pack(side="left", padx=(0, 4))
        self.lang_menu = ttk.OptionMenu(lang_f, self.lang, "tr", "tr", "en",
                                        command=lambda _: self._apply_language())
        self.lang_menu.pack(side="left")

        tk.Frame(self, bg=BORDER, height=1).pack(fill="x", padx=16, pady=(8, 0))

        # Scrollable alan
        self._cv = tk.Canvas(self, bg=BG, bd=0, highlightthickness=0)
        sb = tk.Scrollbar(self, orient="vertical", command=self._cv.yview,
                          bg=SURF, troughcolor=BG, bd=0, width=6)
        self._cv.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        self._cv.pack(side="left", fill="both", expand=True, padx=(16, 0))

        self._sf = tk.Frame(self._cv, bg=BG)
        self._cw = self._cv.create_window((0, 0), window=self._sf, anchor="nw")
        self._sf.bind("<Configure>", lambda _e: self._cv.configure(scrollregion=self._cv.bbox("all")))
        self._cv.bind("<Configure>", lambda e: self._cv.itemconfig(self._cw, width=e.width))
        self._cv.bind("<Enter>", lambda _e: self.bind("<MouseWheel>", self._mousewheel))
        self._cv.bind("<Leave>", lambda _e: self.unbind("<MouseWheel>"))

        f = self._sf   # kısaltma

        # URL
        self._lbl(f, "url")
        url_row = tk.Frame(f, bg=BG)
        url_row.pack(fill="x", pady=(3, 8))
        self.url_var   = tk.StringVar()
        self.url_entry = self._entry(url_row, self.url_var)
        self.url_entry.pack(side="left", fill="x", expand=True)
        self._btn(url_row, "paste", self._paste, small=True).pack(side="left", padx=(6, 0))

        # Format getir
        fetch_row = tk.Frame(f, bg=BG)
        fetch_row.pack(fill="x", pady=(0, 4))
        self.fetch_btn = self._btn(fetch_row, "fetch_formats", self._fetch, small=True)
        self.fetch_btn.pack(side="left")
        self.fetch_status = tk.Label(fetch_row, text="", font=FNSM, bg=BG, fg=DIM,
                                     wraplength=420, justify="left", anchor="w")
        self.fetch_status.pack(side="left", padx=8, fill="x", expand=True)

        # Format listesi
        self._lbl(f, "quality")
        list_frame = tk.Frame(f, bg=SURF, highlightbackground=BORDER, highlightthickness=1)
        list_frame.pack(fill="x", pady=(3, 8))
        list_scroll = tk.Scrollbar(list_frame, bg=SURF, troughcolor=SURF, bd=0, width=6)
        self.format_list = tk.Listbox(
            list_frame, bg=SURF, fg=TEXT, font=FNMONO,
            selectbackground=ACCENT, selectforeground="#ffffff",
            bd=0, highlightthickness=0, activestyle="none", height=6,
            yscrollcommand=list_scroll.set,
        )
        list_scroll.config(command=self.format_list.yview)
        list_scroll.pack(side="right", fill="y")
        self.format_list.pack(side="left", fill="both", expand=True, padx=4, pady=4)
        self.format_list.bind("<MouseWheel>", lambda e: self.format_list.yview_scroll(int(-1*(e.delta/120)), "units"))
        self.format_list.bind("<Enter>", lambda _e: self.unbind("<MouseWheel>"))
        self.format_list.bind("<Leave>", lambda _e: self.bind("<MouseWheel>", self._mousewheel) if self._cursor_in_canvas() else None)
        self.format_list.bind("<<ListboxSelect>>", self._on_format_select)

        # Başlangıç / Bitiş / Format grid
        grid = tk.Frame(f, bg=BG)
        grid.pack(fill="x", pady=(0, 4))
        grid.columnconfigure(0, weight=1)
        grid.columnconfigure(1, weight=1)
        grid.columnconfigure(2, weight=1)

        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("D.TMenubutton", background=SURF, foreground=TEXT, relief="flat", font=FONT)
        style.configure("P.Horizontal.TProgressbar",
                        troughcolor=SURF, background=ACCENT,
                        bordercolor=SURF, lightcolor=ACCENT, darkcolor=ACCENT, thickness=9)

        for col, key, var_attr, hint_attr in (
            (0, "start", "start_var", "start_hint"),
            (1, "end",   "end_var",   "end_hint"),
        ):
            col_f = tk.Frame(grid, bg=BG)
            col_f.grid(row=0, column=col, sticky="ew", padx=(0, 6))
            self._lbl(col_f, key)
            var = tk.StringVar()
            setattr(self, var_attr, var)
            self._entry(col_f, var).pack(fill="x", pady=(3, 0))
            hint = tk.Label(col_f, font=("Segoe UI", 8), bg=BG, fg=DIM)
            hint.pack(anchor="w")
            setattr(self, hint_attr, hint)

        out_col = tk.Frame(grid, bg=BG)
        out_col.grid(row=0, column=2, sticky="ew")
        self._lbl(out_col, "output_format")
        self.output_format = tk.StringVar(value="mp4")
        self.output_menu = ttk.OptionMenu(out_col, self.output_format, "mp4", *FMTS,
                                          command=lambda _: self._format_changed())
        self.output_menu.configure(style="D.TMenubutton")
        self.output_menu["menu"].configure(bg=SURF, fg=TEXT, activebackground=ACCENT,
                                           activeforeground="#fff", font=FONT, bd=0)
        self.output_menu.pack(fill="x", pady=(3, 0))

        # Timeline
        tl_frame = tk.Frame(f, bg=SURF, highlightbackground=BORDER, highlightthickness=1)
        tl_frame.pack(fill="x", pady=(6, 2))
        self.timeline = TimelineWidget(tl_frame, on_change=self._on_timeline_change)
        self.timeline.pack(fill="x", padx=8, pady=(6, 4))

        tl_info = tk.Frame(f, bg=BG)
        tl_info.pack(fill="x", pady=(2, 8))
        self.tl_hint_lbl = tk.Label(tl_info, font=("Segoe UI", 8), bg=BG, fg=DIM, anchor="w")
        self.tl_hint_lbl.pack(side="left")
        self.tl_range_lbl = tk.Label(tl_info, font=("Segoe UI", 8), bg=BG, fg=ACCENT, anchor="e")
        self.tl_range_lbl.pack(side="right")

        self.start_var.trace_add("write", lambda *_: self._on_entry_change())
        self.end_var.trace_add("write",   lambda *_: self._on_entry_change())

        # Kesme yöntemi
        tk.Frame(f, bg=BORDER, height=1).pack(fill="x", pady=(0, 8))
        self._lbl(f, "cut_method")
        mode_row = tk.Frame(f, bg=BG)
        mode_row.pack(fill="x", pady=(3, 6))
        self.mode = tk.StringVar(value="post")
        for val, key in (("direct", "direct"), ("post", "post"), ("reencode", "reencode")):
            self._radio(mode_row, self.mode, val, key).pack(anchor="w", pady=2)

        # Codec / çözünürlük
        codec_size_row = tk.Frame(f, bg=BG)
        codec_size_row.pack(fill="x", pady=(0, 4))
        codec_size_row.columnconfigure(0, weight=1)
        codec_size_row.columnconfigure(1, weight=1)

        codec_col = tk.Frame(codec_size_row, bg=BG)
        codec_col.grid(row=0, column=0, sticky="ew", padx=(0, 12))
        self._lbl(codec_col, "codec")
        codec_row = tk.Frame(codec_col, bg=BG)
        codec_row.pack(fill="x", pady=(2, 0))
        self.codec = tk.StringVar(value="h264")
        self._codec_radios = []
        for val, key in (("h264","h264"), ("h265","h265"), ("copy","copy")):
            rb = self._radio(codec_row, self.codec, val, key)
            rb.pack(anchor="w", pady=1)
            self._codec_radios.append(rb)

        size_col = tk.Frame(codec_size_row, bg=BG)
        size_col.grid(row=0, column=1, sticky="ew")
        self._lbl(size_col, "reencode_size")
        size_row = tk.Frame(size_col, bg=BG)
        size_row.pack(fill="x", pady=(2, 0))
        self.reencode_size = tk.StringVar(value="source")
        self._size_radios = []
        for val, key in (("source","size_source"),("1080","size_1080"),("720","size_720"),("480","size_480")):
            rb = self._radio(size_row, self.reencode_size, val, key)
            rb.pack(anchor="w", pady=1)
            self._size_radios.append(rb)

        self.mode.trace_add("write", lambda *_: self._update_reencode_widgets())

        self.tip_lbl = tk.Label(f, text="", font=FNSM, bg=BG, fg=ORANGE, anchor="w")
        self.tip_lbl.pack(fill="x", pady=(4, 0))

        # Klasör
        tk.Frame(f, bg=BORDER, height=1).pack(fill="x", pady=(8, 8))
        self._lbl(f, "folder")
        folder_row = tk.Frame(f, bg=BG)
        folder_row.pack(fill="x", pady=(3, 10))
        self.folder = tk.StringVar(value=os.path.join(os.path.expanduser("~"), "Downloads"))
        self._entry(folder_row, self.folder).pack(side="left", fill="x", expand=True)
        self._btn(folder_row, "choose", self._browse, small=True).pack(side="left", padx=(6, 0))

        # İndir / İptal
        self.download_btn = self._btn(f, "download", self._start, big=True)
        self.download_btn.pack(fill="x", pady=(0, 4))
        self.cancel_btn = self._btn(f, "cancel", self._cancel, big=True, danger=True)
        self.cancel_btn.pack(fill="x")
        self.cancel_btn.config(state="disabled")

        # Progress
        tk.Frame(f, bg=BORDER, height=1).pack(fill="x", pady=(10, 6))
        self.progress = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(f, variable=self.progress, maximum=100,
                                             style="P.Horizontal.TProgressbar")
        self.progress_bar.pack(fill="x", pady=(0, 4))
        self.status = tk.StringVar()
        self.status_lbl = tk.Label(f, textvariable=self.status, font=FNSM, bg=BG, fg=DIM, anchor="w")
        self.status_lbl.pack(fill="x")

        # Log
        tk.Frame(f, bg=BORDER, height=1).pack(fill="x", pady=(8, 6))
        log_frame = tk.Frame(f, bg=SURF, highlightbackground=BORDER, highlightthickness=1)
        log_frame.pack(fill="both", expand=True, pady=(0, 14))
        log_scroll = tk.Scrollbar(log_frame, bg=SURF, troughcolor=SURF, bd=0, width=6)
        self.log = tk.Text(
            log_frame, bg=SURF, fg=TEXT, font=FNMONO,
            bd=0, padx=6, pady=4, state="disabled", wrap="word", height=7,
            insertbackground=TEXT, selectbackground=ACCENT,
            yscrollcommand=log_scroll.set,
        )
        self.log.bind("<MouseWheel>", lambda e: self.log.yview_scroll(int(-1*(e.delta/120)), "units"))
        self.log.bind("<Enter>", lambda _e: self.unbind("<MouseWheel>"))
        self.log.bind("<Leave>", lambda _e: self.bind("<MouseWheel>", self._mousewheel) if self._cursor_in_canvas() else None)
        log_scroll.config(command=self.log.yview)
        log_scroll.pack(side="right", fill="y")
        self.log.pack(side="left", fill="both", expand=True)

    # ── Yardımcı widget oluşturucular ─────────────────────────
    def _mousewheel(self, event):
        self._cv.yview_scroll(int(-1*(event.delta/120)), "units")

    def _cursor_in_canvas(self):
        try:
            x, y = self.winfo_pointerxy()
            w = self.winfo_containing(x, y)
            while w:
                if w == self._cv: return True
                w = getattr(w, "master", None)
        except tk.TclError:
            pass
        return False

    def _lbl(self, parent, key):
        lbl = tk.Label(parent, font=FNSM, bg=BG, fg=DIM)
        lbl.pack(anchor="w")
        self._labels.append((lbl, key))
        return lbl

    def _entry(self, parent, var):
        return tk.Entry(parent, textvariable=var, font=FONT,
                        bg=SURF, fg=TEXT, insertbackground=TEXT,
                        relief="flat", bd=0,
                        highlightbackground=BORDER, highlightthickness=1, highlightcolor=ACCENT)

    def _btn(self, parent, key, command, small=False, big=False, danger=False):
        if danger:    bg, fg, act = "#3e2227", RED,     "#4e2c33"
        elif big:     bg, fg, act = ACCENT,   "#fff",   ACCENT_H
        else:         bg, fg, act = SURF_2,   TEXT,     BORDER
        font = FNSM if small else (FNLG if big else FONT)
        px, py = (8, 3) if small else ((10, 8) if big else (8, 5))
        btn = tk.Button(parent, command=command, bg=bg, fg=fg, font=font,
                        activebackground=act, activeforeground=fg,
                        relief="flat", bd=0, cursor="hand2", padx=px, pady=py)
        btn.bind("<Enter>", lambda _e: btn.config(bg=act))
        btn.bind("<Leave>", lambda _e: btn.config(bg=bg))
        self._buttons.append((btn, key))
        return btn

    def _radio(self, parent, var, value, key):
        rb = tk.Radiobutton(parent, variable=var, value=value, font=FNSM,
                            bg=BG, fg=TEXT, selectcolor=SURF_2,
                            activebackground=BG, activeforeground=TEXT, cursor="hand2")
        self._radios.append((rb, key))
        return rb

    # ── Dil / UI güncelleme ───────────────────────────────────
    def _update_reencode_widgets(self):
        state = "normal" if self.mode.get() == "reencode" else "disabled"
        for rb in self._codec_radios + self._size_radios:
            rb.config(state=state)

    def _apply_language(self):
        self.title(self.t("app_title"))
        self.title_lbl.config(text=self.t("app_title"))
        self.tagline_lbl.config(text=self.t("tagline"))
        self.lang_lbl.config(text=self.t("language"))
        for lbl, key in self._labels:   lbl.config(text=self.t(key))
        for btn, key in self._buttons:  btn.config(text=self.t(key))
        for rb,  key in self._radios:   rb.config(text=self.t(key))
        self.start_hint.config(text=self.t("time_hint"))
        self.end_hint.config(text=self.t("time_hint"))
        self.status.set(self.t("ready"))
        if self._duration <= 0:
            self.tl_hint_lbl.config(text=self.t("timeline_hint"))
            self.tl_range_lbl.config(text="")
        else:
            self.tl_hint_lbl.config(text=self.t("timeline_drag"))
        self._format_changed()
        # Fetch edilmiş formatlar varsa koru, yoksa varsayılanları yükle
        if not self._formats_fetched:
            self._default_formats()
        self._update_reencode_widgets()

    def _format_changed(self):
        self.tip_lbl.config(text=self.t("twitter_tip") if self.output_format.get() == "mp4" else "")

    def _default_formats(self):
        cur = self.format_list.get(self.format_list.curselection()[0]) if self.format_list.curselection() else None
        self.format_list.delete(0, "end")
        self._fmap = {}
        rows = [
            (f"--- {self.t('video')} ---", None),
            (f"  {self.t('best_video')}",  "bestvideo+bestaudio/best"),
            ("  4K (2160p)",               "bestvideo[height<=2160]+bestaudio/best[height<=2160]"),
            ("  2K (1440p)",               "bestvideo[height<=1440]+bestaudio/best[height<=1440]"),
            ("  1080p",                    "bestvideo[height<=1080]+bestaudio/best[height<=1080]"),
            ("  720p",                     "bestvideo[height<=720]+bestaudio/best[height<=720]"),
            ("  480p",                     "bestvideo[height<=480]+bestaudio/best[height<=480]"),
            ("  360p",                     "bestvideo[height<=360]+bestaudio/best[height<=360]"),
            (f"--- {self.t('audio')} ---", None),
            (f"  {self.t('best_audio_mp3')}", "bestaudio/best|audio|mp3"),
            (f"  {self.t('best_audio_aac')}", "bestaudio/best|audio|aac"),
        ]
        for label, fmt in rows:
            self.format_list.insert("end", label)
            self._fmap[label] = fmt
            if fmt is None:
                idx = self.format_list.size() - 1
                self.format_list.itemconfig(idx, fg=DIM, selectbackground=SURF, selectforeground=DIM)
        if cur and cur in self._fmap:
            try:
                self.format_list.selection_set(list(self._fmap).index(cur))
            except ValueError:
                self.format_list.selection_set(1)
        else:
            self.format_list.selection_set(1)

    # ── Buton aksiyonları ─────────────────────────────────────
    def _on_format_select(self, _event=None):
        """Başlık satırı seçilince bir sonraki geçerli satıra atla."""
        sel = self.format_list.curselection()
        if not sel:
            return
        idx = sel[0]
        lbl = self.format_list.get(idx)
        if self._fmap.get(lbl) is None:   # başlık
            # aşağı doğru ilk geçerli satırı bul
            for i in range(idx + 1, self.format_list.size()):
                if self._fmap.get(self.format_list.get(i)) is not None:
                    self.format_list.selection_clear(0, "end")
                    self.format_list.selection_set(i)
                    self.format_list.see(i)
                    return
            # bulunamazsa yukarı bak
            for i in range(idx - 1, -1, -1):
                if self._fmap.get(self.format_list.get(i)) is not None:
                    self.format_list.selection_clear(0, "end")
                    self.format_list.selection_set(i)
                    self.format_list.see(i)
                    return

    def _paste(self):
        try:
            self.url_var.set(self.clipboard_get().strip())
        except tk.TclError:
            pass

    def _browse(self):
        d = filedialog.askdirectory(initialdir=self.folder.get())
        if d:
            self.folder.set(d)

    # ── Timeline ↔ Entry senkronu ─────────────────────────────
    def _on_timeline_change(self, start_sec, end_sec):
        if self._tl_updating:
            return
        self._tl_updating = True
        try:
            dur = self._duration
            if start_sec <= 0.1 and end_sec >= dur - 0.1:
                self.start_var.set("")
                self.end_var.set("")
            else:
                self.start_var.set(_fmt_compact(seconds_to_time(start_sec)))
                self.end_var.set(_fmt_compact(seconds_to_time(end_sec)))
            self._update_range_label(start_sec, end_sec)
        finally:
            self._tl_updating = False

    def _on_entry_change(self):
        if self._tl_updating or self._duration <= 0:
            return
        self._tl_updating = True
        try:
            try:    s = time_to_seconds(self.start_var.get()) or 0.0
            except: s = 0.0
            try:    e = time_to_seconds(self.end_var.get()) or self._duration
            except: e = self._duration
            self.timeline.set_range(s, e)
            self._update_range_label(s, e)
        finally:
            self._tl_updating = False

    def _update_range_label(self, s, e):
        dur = self._duration
        if dur <= 0:
            return
        if s <= 0.1 and e >= dur - 0.1:
            self.tl_range_lbl.config(text=self.t("full_video"))
        else:
            self.tl_range_lbl.config(
                text=f"{self.t('range_label')}: {_fmt_compact(seconds_to_time(max(0.0, e-s)))}")

    def _set_duration(self, duration):
        self._duration = duration
        self.timeline.set_duration(duration)
        self.start_var.set("")
        self.end_var.set("")
        self.tl_hint_lbl.config(text=self.t("timeline_drag"))
        self.tl_range_lbl.config(text=self.t("full_video"))

    # ── Fetch ─────────────────────────────────────────────────
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
        self.url_entry.config(state="disabled")
        self.fetch_status.config(text=self.t("fetching"), fg=ORANGE)
        threading.Thread(target=self._do_fetch, args=(ytdlp, url), daemon=True).start()

    def _do_fetch(self, ytdlp, url):
        try:
            result = subprocess.run(
                [ytdlp, "-F", "--no-playlist", url],
                capture_output=True, text=True,
                encoding=CONSOLE_ENCODING, errors="replace",
                creationflags=self._creation_flags(),
            )
            if result.returncode != 0:
                err = (result.stderr or result.stdout or "").strip()
                # Sadece ilk 2 satırı göster
                short = "\n".join(err.splitlines()[:2])
                raise RuntimeError(short)
            self.after(0, self._fill_formats, result.stdout)

            # Süre
            dur = subprocess.run(
                [ytdlp, "--no-playlist", "--print", "duration", url],
                capture_output=True, text=True,
                encoding=CONSOLE_ENCODING, errors="replace",
                creationflags=self._creation_flags(),
            )
            if dur.returncode == 0:
                try:
                    self.after(0, self._set_duration, float(dur.stdout.strip()))
                except ValueError:
                    pass
        except Exception as exc:
            self.after(0, self.fetch_status.config,
                       {"text": f"{self.t('error')}: {exc}", "fg": RED})
        finally:
            self.after(0, self.fetch_btn.config, {"state": "normal"})
            self.after(0, self.url_entry.config, {"state": "normal"})

    def _fill_formats(self, raw):
        videos, audios = [], []
        for line in raw.splitlines():
            parts = line.split()
            if len(parts) < 3 or not parts[0][0:1].isalnum():
                continue
            fmt_id, ext, res = parts[0], parts[1], parts[2]
            if fmt_id.lower() in {"id", "format"} or line.startswith("["):
                continue
            note = ""
            m = re.search(r"(\d+(?:\.\d+)?[kKmM])", line)
            if m:
                note = m.group(1)
            if res in ("audio", "only") or "audio only" in line.lower():
                audios.append((f"  {fmt_id:<8} {ext:<5} {self.t('audio'):<8} {note}", fmt_id))
            else:
                videos.append((f"  {fmt_id:<8} {ext:<5} {res:<12} {note}", fmt_id))

        if not videos and not audios:
            self.fetch_status.config(text=self.t("formats_not_found"), fg=ORANGE)
            return

        self.format_list.delete(0, "end")
        self._fmap = {}

        def hdr(text):
            self.format_list.insert("end", text)
            idx = self.format_list.size() - 1
            self.format_list.itemconfig(idx, fg=DIM, selectbackground=SURF, selectforeground=DIM)
            self._fmap[text] = None

        hdr(f"--- {self.t('auto')} ---")
        for lbl, fmt in ((f"  {self.t('best_video')}", "bestvideo+bestaudio/best"),
                         (f"  {self.t('best_audio_mp3')}", "bestaudio/best|audio|mp3")):
            self.format_list.insert("end", lbl)
            self._fmap[lbl] = fmt
        if videos:
            hdr(f"--- {self.t('video')} ---")
            for lbl, fmt in reversed(videos):
                self.format_list.insert("end", lbl)
                self._fmap[lbl] = fmt
        if audios:
            hdr(f"--- {self.t('audio')} ---")
            for lbl, fmt in reversed(audios):
                self.format_list.insert("end", lbl)
                self._fmap[lbl] = fmt

        self.format_list.selection_set(1)
        self.fetch_status.config(text=f"{len(videos)+len(audios)} {self.t('formats_found')}", fg=GREEN)
        self._formats_fetched = True

    def _get_format(self):
        sel = self.format_list.curselection()
        if not sel:
            return None, None
        lbl = self.format_list.get(sel[0])
        return lbl.strip(), self._fmap.get(lbl)

    # ── İndirme başlatma ──────────────────────────────────────
    def _start(self):
        url        = self.url_var.get().strip()
        folder     = self.folder.get().strip()
        start_text = self.start_var.get().strip()
        end_text   = self.end_var.get().strip()

        if not url:
            messagebox.showerror(self.t("error"), self.t("need_url"))
            return
        try:    start_sec = time_to_seconds(start_text)
        except: messagebox.showerror(self.t("error"), f"{self.t('invalid_start')}: {start_text}"); return
        try:    end_sec   = time_to_seconds(end_text)
        except: messagebox.showerror(self.t("error"), f"{self.t('invalid_end')}: {end_text}"); return
        if start_sec is not None and end_sec is not None and end_sec <= start_sec:
            messagebox.showerror(self.t("error"), self.t("end_before_start"))
            return

        _, fmt = self._get_format()
        if fmt is None:
            messagebox.showerror(self.t("error"), self.t("need_format"))
            return

        ytdlp  = find_exe("yt-dlp")
        ffmpeg = find_exe("ffmpeg")
        if not ytdlp:
            messagebox.showerror(self.t("error"), f"yt-dlp {self.t('not_found')}.\npip install -U yt-dlp")
            return

        has_cut       = start_sec is not None or end_sec is not None
        is_audio      = "|audio|" in fmt or self.output_format.get() in AUDIO_FORMATS
        needs_merge   = "+" in fmt
        needs_ffmpeg  = has_cut or is_audio or needs_merge
        if needs_ffmpeg and not ffmpeg:
            messagebox.showerror(self.t("error"), self.t("ffmpeg_required"))
            return

        os.makedirs(folder, exist_ok=True)
        self.progress.set(0)
        self.progress_bar.config(mode="determinate")
        self.download_btn.config(state="disabled")
        self.cancel_btn.config(state="normal")
        self._log(f"\n▶  {url[:80]}\n   mode={self.mode.get()}  fmt={self.output_format.get()}"
                  f"  start={start_text or '–'}  end={end_text or '–'}", DIM)
        if has_cut and self.mode.get() == "post":
            self._log(f"⚠  {self.t('copy_note')}", ORANGE)

        threading.Thread(target=self._run,
                         args=(url, fmt, start_sec, end_sec, folder, ytdlp, ffmpeg),
                         daemon=True).start()

    # ── _run ─────────────────────────────────────────────────
    def _run(self, url, fmt, start_sec, end_sec, folder, ytdlp, ffmpeg):
        temp_dir = None
        try:
            has_cut      = start_sec is not None or end_sec is not None
            mode         = self.mode.get()
            output_format= self.output_format.get()
            is_audio     = "|audio|" in fmt or output_format in AUDIO_FORMATS
            needs_post   = has_cut and mode in ("post", "reencode")
            self._phase_weights = (0.75, 0.25) if needs_post else (1.0, 0.0)

            if needs_post:
                temp_dir          = tempfile.mkdtemp(prefix="_ytdlp_gui_", dir=folder)
                output_template   = os.path.join(temp_dir, "%(id)s.%(ext)s")
            else:
                output_template   = os.path.join(folder, "%(title).180B.%(ext)s")

            cmd = [ytdlp, "--newline", "--no-playlist", "--no-part", "-o", output_template]
            if ffmpeg:
                # find_exe() sadece Python tarafında ffmpeg'i bulur; yt-dlp'nin kendi iç
                # işlemleri (format birleştirme, ses çıkarma, --download-sections /
                # --force-keyframes-at-cuts) ffmpeg'i PATH'te aramaz. Konumu açıkça
                # bildirmezsek yt-dlp bulunamıyor sanır ve merge/kesme sessizce
                # bozuk çalışır ya da hata verir (bundled exe / Scripts klasörü durumu).
                cmd += ["--ffmpeg-location", ffmpeg]
            if is_audio:
                af = output_format if output_format in AUDIO_FORMATS else "mp3"
                bf = fmt.split("|audio|")[0] if "|audio|" in fmt else "bestaudio/best"
                cmd += ["-f", bf, "-x", "--audio-format", af]
            else:
                mf = "mp4" if output_format in ("mp4", "mov", "avi") else output_format
                cmd += ["-f", fmt, "--merge-output-format", mf]

            if has_cut and mode == "direct":
                s = seconds_to_time(start_sec or 0)
                e = seconds_to_time(end_sec) if end_sec is not None else "inf"
                cmd += ["--download-sections", f"*{s}-{e}", "--force-keyframes-at-cuts"]

            cmd.append(url)
            self.after(0, self._set_status, f"{self.t('downloading')}…", ACCENT)
            downloaded = self._run_ytdlp(cmd, 0, self._phase_weights[0])

            if needs_post:
                source = downloaded if downloaded and os.path.exists(downloaded) else self._newest_file(temp_dir)
                if not source:
                    raise RuntimeError("İndirilen dosya bulunamadı.")
                output = self._build_output_path(folder, source, output_format)
                self.after(0, self._set_status, f"{self.t('cutting')}…", ACCENT)
                self._run_ffmpeg_cut(source, output, start_sec, end_sec, mode, is_audio)
                self.after(0, self._log, f"✔  {self.t('saved_to')}: {output}", GREEN)
                self.after(0, self._log_open_folder, folder)
            elif downloaded:
                self.after(0, self._log, f"✔  {self.t('saved_to')}: {downloaded}", GREEN)
                self.after(0, self._log_open_folder, folder)

            self.after(0, self.progress.set, 100)
            self.after(0, self._set_status, self.t("done"), GREEN)
            self.after(0, self._log, f"✔  {self.t('done')}", GREEN)
            # 2 saniye sonra progress'i sıfırla
            self.after(2000, self.progress.set, 0)

        except RuntimeError as exc:
            if str(exc) == "canceled":
                self.after(0, self._set_status, self.t("canceled"), ORANGE)
                self.after(0, self._log, f"✖  {self.t('canceled')}", ORANGE)
            else:
                self.after(0, self._set_status, self.t("error"), RED)
                self.after(0, self._log, f"✖  {self.t('error')}: {exc}", RED)
        except Exception as exc:
            self.after(0, self._set_status, self.t("error"), RED)
            self.after(0, self._log, f"✖  {self.t('error')}: {exc}", RED)
        finally:
            self._proc      = None
            self._canceling = False
            self.after(0, self.download_btn.config, {"state": "normal"})
            self.after(0, self.cancel_btn.config,   {"state": "disabled"})

    # ── yt-dlp process ────────────────────────────────────────
    def _run_ytdlp(self, cmd, phase_start, phase_size):
        destination = None
        saw_percent = False
        self.after(0, self.progress_bar.config, {"mode": "indeterminate"})
        self.after(0, self.progress_bar.start, 12)
        self._proc = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True, bufsize=1, encoding=CONSOLE_ENCODING, errors="replace",
            creationflags=self._creation_flags(),
        )
        for raw in self._proc.stdout:
            line = raw.strip()
            if not line:
                continue
            m = re.search(r"\[download\]\s+([\d.]+)%", line)
            if m:
                if not saw_percent:
                    saw_percent = True
                    self.after(0, self.progress_bar.stop)
                    self.after(0, self.progress_bar.config, {"mode": "determinate"})
                pct = float(m.group(1))
                total = phase_start + (pct / 100.0) * phase_size * 100
                em = re.search(r"\bETA\s+([0-9:]+|Unknown)", line, re.IGNORECASE)
                eta = normalize_eta(em.group(1)) if em else ""
                eta_txt = self.t("eta_remaining").format(eta) if eta else ""
                self.after(0, self.progress.set, min(99, total))
                self.after(0, self._set_status, f"{self.t('downloading')} %{pct:.1f}{eta_txt}", ACCENT)
            destination = self._extract_destination(line, destination)
            self.after(0, self._log, line, self._line_color(line))

        self._proc.wait()
        self.after(0, self.progress_bar.stop)
        self.after(0, self.progress_bar.config, {"mode": "determinate"})
        if self._proc.returncode not in (0, None):
            if self._canceling or self._proc.returncode < 0:
                raise RuntimeError("canceled")
            raise RuntimeError(f"yt-dlp exit {self._proc.returncode}")
        return destination

    # ── ffmpeg kesme ─────────────────────────────────────────
    def _run_ffmpeg_cut(self, source, output, start_sec, end_sec, mode, is_audio):
        duration = (end_sec - start_sec) if start_sec is not None and end_sec is not None else None

        if mode == "reencode" and start_sec and start_sec > 3:
            margin     = 3.0
            in_seek    = max(0.0, start_sec - margin)
            inner_seek = start_sec - in_seek
        elif start_sec:
            in_seek, inner_seek = start_sec, 0.0
        else:
            in_seek, inner_seek = 0.0, 0.0

        ffmpeg_exe = find_exe("ffmpeg")
        if not ffmpeg_exe:
            raise RuntimeError("ffmpeg bulunamadı")

        cmd = [ffmpeg_exe, "-y", "-hide_banner", "-nostdin",
               "-progress", "pipe:1", "-stats_period", "0.5"]
        if in_seek:
            cmd += ["-ss", seconds_to_time(in_seek)]
        cmd += ["-i", source]
        if inner_seek > 0:
            cmd += ["-ss", seconds_to_time(inner_seek)]
        if duration is not None:
            cmd += ["-t", seconds_to_time(duration)]
        elif end_sec is not None:
            cmd += ["-to", seconds_to_time(max(0.0, end_sec - in_seek))]

        if is_audio:
            cmd += ["-vn"]
            if mode == "reencode":
                codec = "libmp3lame" if self.output_format.get() == "mp3" else "aac"
                cmd += ["-c:a", codec]
            else:
                cmd += ["-c", "copy"]
        elif mode == "reencode":
            vc = {"h264": "libx264", "h265": "libx265", "copy": "copy"}.get(self.codec.get(), "libx264")
            if vc == "copy":
                cmd += ["-c", "copy"]
            else:
                mh = {"1080": 1080, "720": 720, "480": 480}.get(self.reencode_size.get())
                if mh:
                    cmd += ["-vf", f"scale=-2:min({mh}\\,ih)"]
                cmd += ["-c:v", vc, "-preset", "superfast", "-crf", "21",
                        "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart"]
        else:
            cmd += ["-c", "copy", "-avoid_negative_ts", "make_zero"]

        cmd += [output]
        self.after(0, self._log, f"⚙  {self.t('ffmpeg_start')}", DIM)
        self.after(0, self.progress_bar.stop)
        self.after(0, self.progress_bar.config, {"mode": "determinate"})
        self.after(0, self.progress.set, self._phase_weights[0] * 100)

        self._proc = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True, bufsize=1, encoding=CONSOLE_ENCODING, errors="replace",
            creationflags=self._creation_flags(),
        )
        phase_start = self._phase_weights[0] * 100
        phase_size  = self._phase_weights[1] * 100
        last_st     = 0
        started_at  = time.time()
        saw_prog    = False
        if not duration:
            self.after(0, self.progress_bar.config, {"mode": "indeterminate"})
            self.after(0, self.progress_bar.start, 12)

        for raw in self._proc.stdout:
            line = raw.strip()
            if not line:
                continue
            out_time = None
            if line.startswith("out_time_ms="):
                try:    out_time = int(line.split("=",1)[1]) / 1_000_000
                except: pass
            elif line.startswith("out_time="):
                out_time = ffmpeg_time_to_seconds(line.split("=",1)[1])
            else:
                m = re.search(r"time=(\d+:\d+:\d+(?:\.\d+)?)", line)
                if m:
                    out_time = ffmpeg_time_to_seconds(m.group(1))

            if out_time is not None and duration:
                saw_prog = True
                pct   = max(0, min(100, out_time / duration * 100))
                total = phase_start + pct / 100 * phase_size
                self.after(0, self.progress.set, min(99, total))
                if time.time() - last_st > 0.2:
                    last_st = time.time()
                    elapsed = max(0.1, time.time() - started_at)
                    rem = (elapsed / pct * (100 - pct)) if pct > 0 else 0
                    eta = self.t("eta_remaining").format(short_duration(rem, self.lang.get())) if rem else ""
                    self.after(0, self._set_status, f"{self.t('processing')} %{pct:.1f}{eta}", ACCENT)
            elif line == "progress=end" and duration and not saw_prog:
                self.after(0, self.progress.set, min(99, phase_start + phase_size))
            elif not line.startswith(("frame=","fps=","stream_","bitrate=","total_size=",
                                       "out_time","dup_frames=","drop_frames=","speed=","progress=")):
                self.after(0, self._log, line, self._line_color(line))

        self._proc.wait()
        self.after(0, self.progress_bar.stop)
        self.after(0, self.progress_bar.config, {"mode": "determinate"})
        if self._proc.returncode not in (0, None):
            if self._canceling or self._proc.returncode < 0:
                raise RuntimeError("canceled")
            raise RuntimeError(f"ffmpeg exit {self._proc.returncode}")

    # ── Yardımcılar ───────────────────────────────────────────
    def _extract_destination(self, line, current):
        if "[download] Destination:" in line:
            return line.split("[download] Destination:", 1)[1].strip()
        if "[ExtractAudio] Destination:" in line:
            return line.split("[ExtractAudio] Destination:", 1)[1].strip()
        m = re.search(r'Merging formats into "(.+)"', line)
        if m: return m.group(1)
        m = re.search(r'\[download\]\s+(.+)\s+has already been downloaded', line)
        if m: return m.group(1)
        return current

    def _build_output_path(self, folder, source, fmt):
        base   = re.sub(r"\s+", " ", os.path.splitext(os.path.basename(source))[0]).strip()
        output = os.path.join(folder, f"{base}_cut.{fmt}")
        if not os.path.exists(output):
            return output
        return os.path.join(folder, f"{base}_cut_{time.strftime('%Y%m%d_%H%M%S')}.{fmt}")

    def _newest_file(self, folder):
        try:
            files = [os.path.join(folder, f) for f in os.listdir(folder)
                     if os.path.isfile(os.path.join(folder, f))]
            return max(files, key=os.path.getmtime) if files else None
        except OSError:
            return None

    def _cancel(self):
        if self._proc:
            self._canceling = True
            try:
                if sys.platform == "win32":
                    subprocess.run(["taskkill", "/F", "/T", "/PID", str(self._proc.pid)],
                                   creationflags=subprocess.CREATE_NO_WINDOW, check=False)
                else:
                    self._proc.terminate()
            except Exception:
                pass
            self._set_status(self.t("canceling"), ORANGE)

    def _log(self, text, color=None):
        self.log.config(state="normal")
        # 500 satır limiti
        lines = int(self.log.index("end-1c").split(".")[0])
        if lines > 500:
            self.log.delete("1.0", "50.0")
        tag = f"c{abs(hash(color or TEXT))}"
        self.log.tag_config(tag, foreground=color or TEXT)
        self.log.insert("end", text + "\n", tag)
        self.log.see("end")
        self.log.config(state="disabled")

    def _log_open_folder(self, folder):
        """Log'a tıklanabilir 'Klasörü Aç' butonu ekle."""
        self.log.config(state="normal")
        tag = f"openfolder_{abs(hash(folder))}"
        self.log.tag_config(tag, foreground=ACCENT, underline=True)
        self.log.tag_bind(tag, "<Button-1>", lambda _e, f=folder: self._open_folder(f))
        self.log.tag_bind(tag, "<Enter>", lambda _e: self.log.config(cursor="hand2"))
        self.log.tag_bind(tag, "<Leave>", lambda _e: self.log.config(cursor=""))
        self.log.insert("end", f"   {self.t('open_folder')}\n", tag)
        self.log.see("end")
        self.log.config(state="disabled")

    def _open_folder(self, folder):
        try:
            if sys.platform == "win32":
                os.startfile(folder)
            elif sys.platform == "darwin":
                subprocess.Popen(["open", folder])
            else:
                subprocess.Popen(["xdg-open", folder])
        except Exception:
            pass

    def _set_status(self, text, color=None):
        self.status.set(text)
        self.status_lbl.config(fg=color or DIM)

    def _line_color(self, line):
        u = line.upper()
        if "ERROR"   in u: return RED
        if "WARNING" in u: return ORANGE
        if any(t in line for t in ("Destination", "Merging", "already been downloaded")): return GREEN
        return TEXT

    def _check_startup(self):
        miss = missing_deps()
        if miss:
            self._log(f"⚠  {self.t('missing')}: {', '.join(miss)}", ORANGE)
            if "yt-dlp"  in miss: self._log(self.t("install_ytdlp"),  ORANGE)
            if "ffmpeg"  in miss: self._log(self.t("install_ffmpeg"), ORANGE)
            self._set_status(self.t("missing_deps"), ORANGE)
        else:
            self._log(f"✔  {self.t('deps_ready')}", GREEN)
            self._set_status(self.t("ready"), DIM)

    def _creation_flags(self):
        return subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0


if __name__ == "__main__":
    App().mainloop()
