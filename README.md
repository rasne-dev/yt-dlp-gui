# yt-dlp GUI

A simple desktop app for downloading videos and audio with [yt-dlp](https://github.com/yt-dlp/yt-dlp).

> This is an independent graphical interface for yt-dlp. It is not the official yt-dlp project.

## Features

- Download videos or audio from YouTube and many other yt-dlp supported sites
- Fetch available formats and choose quality
- Download or export a selected time range, including fractional seconds (e.g. `21.5`)
- Preview the exact start/end frame of a cut before downloading, without downloading the full video
- Three cut modes: direct cut, full download + cut, full download + re-encode
- Re-encode to h264/h265 for better compatibility
- Optional re-encode resolution: original, 1080p, 720p, 480p
- MP4, MKV, WEBM, MOV, AVI, MP3, AAC, OGG, M4A, FLAC and WAV output options
- Progress bar, status text, estimated remaining time and log view
- Turkish and English interface

## Requirements

- Python 3.8 or newer
- yt-dlp (**keep this updated** — see note below)
- ffmpeg
- A JavaScript runtime for YouTube (**[Deno](https://deno.com/) recommended**) — required by yt-dlp to solve YouTube's playback challenges; without it, YouTube downloads commonly fail with `HTTP Error 403: Forbidden`

### Windows Setup

Open **PowerShell** or **Command Prompt** and run:

```bash
python --version
pip --version
pip install -U yt-dlp
```

If `python` is not recognized, install Python from <https://www.python.org/downloads/>. During installation, enable **Add python.exe to PATH**.

Install ffmpeg with winget:

```bash
winget install Gyan.FFmpeg
```

Close and reopen PowerShell, then check:

```bash
ffmpeg -version
yt-dlp --version
```

Install Deno (needed by yt-dlp to solve YouTube's playback challenges; without it, YouTube downloads commonly fail with `HTTP Error 403: Forbidden`):

```bash
winget install DenoLand.Deno
```

Close and reopen PowerShell after installing Deno so it is picked up on `PATH`.

If `winget` is not available, install ffmpeg manually:

1. Download a Windows build from <https://www.gyan.dev/ffmpeg/builds/>.
2. Extract the ZIP file, for example to `C:\ffmpeg`.
3. Make sure this file exists: `C:\ffmpeg\bin\ffmpeg.exe`.
4. Open **Start Menu → Edit the system environment variables**.
5. Click **Environment Variables**.
6. Under **User variables**, select **Path**, then click **Edit**.
7. Click **New** and add:

```text
C:\ffmpeg\bin
```

8. Click **OK** on all windows.
9. Close and reopen PowerShell.
10. Check:

```bash
ffmpeg -version
```

### macOS Setup

```bash
brew install python ffmpeg deno
python3 -m pip install -U yt-dlp
```

### Linux Setup

Debian/Ubuntu:

```bash
sudo apt update
sudo apt install python3 python3-pip ffmpeg
curl -fsSL https://deno.land/install.sh | sh
python3 -m pip install -U yt-dlp
```

## Run From Source

```bash
python ytdlp_gui.py
```

## Run the Ready EXE

If you downloaded a ready-to-use package, open the `dist` folder and run:

```text
dist/ytdlp_gui.exe
```

You do not need to run Python commands for the EXE version. However, `yt-dlp` and `ffmpeg` still need to be installed and available on your system.

Some packages may include `yt-dlp.exe` and `ffmpeg.exe` next to `ytdlp_gui.exe`. In that case, the app can use those bundled files directly. If downloads, cutting, merging or re-encoding start failing, these bundled tools may be outdated. Download the latest versions of yt-dlp and ffmpeg and replace the old `.exe` files.

## Build an EXE

```bash
pyinstaller --noconfirm --clean --onefile --windowed ytdlp_gui.py
```

The EXE file will be created in:

```text
dist/ytdlp_gui.exe
```

## How To Use

1. Paste a video URL.
2. Click **Fetch Formats**.
3. Choose the video or audio format.
4. Optional: enter start and end times, for example `31:23` and `33:00` (fractional seconds like `31:23.5` also work), or drag the handles on the timeline.
5. Optional: click **🔍 Preview** to see the exact first/last frame of the selected range before committing to a download — useful for spotting keyframe drift early (see [Preview](#preview) below).
6. Choose the output format.
7. If you use re-encode mode, choose codec and resolution.
8. Click **Download**.

## Preview

The **🔍 Preview** button lets you check a cut before spending time on a full download. It downloads only a couple of seconds around your selected start and end points (using the same `--download-sections` + `--force-keyframes-at-cuts` approach as Direct cut) and shows you the actual first and last frame.

- If the frames look right, go ahead and download.
- If the start/end frame looks off, it usually means the video needs "Full download → cut" or "Full download → re-encode" instead of "Direct cut" for that particular clip.
- Each point has a timeout (~25 seconds). If a point times out or fails (for example due to network issues or an outdated yt-dlp / missing JS runtime), preview simply skips that frame and shows whatever it could get.
- Preview is not available for audio-only formats.

## Cut Modes

**Direct cut** is the fastest option. It asks yt-dlp to download only the selected section. On some videos, the start point may shift slightly because video files are cut around keyframes.

**Full download → cut** downloads the whole file first and cuts without re-encoding. It is usually fast, but the first second can freeze on some videos if the cut does not start on a keyframe.

**Full download → re-encode** downloads the whole file first and creates a new encoded clip. This is slower, but usually gives the most accurate and compatible result. For Twitter/X and general sharing, MP4 + h264 is recommended.

## Re-Encode Resolution

Use **Original** for maximum quality.

Use **720p** or **480p** when you want faster processing and smaller files. 720p usually takes much less time than 1080p because it processes fewer pixels.

## Notes

- **Keep yt-dlp updated.** YouTube changes its playback protection frequently; yt-dlp versions older than ~90 days commonly fail. Run `pip install -U yt-dlp` (or `yt-dlp -U` for the standalone exe) regularly.
- If you see `WARNING: No supported JavaScript runtime could be found` or `HTTP Error 403: Forbidden` on YouTube links, install [Deno](https://deno.com/) (see Requirements above) and update yt-dlp — this is now required for most YouTube downloads, not just an optional warning.
- Re-encoding is CPU-heavy and can take several minutes on long or high-resolution videos.
- If the app is open, Windows may block overwriting `dist/ytdlp_gui.exe`. Close the app before rebuilding.
- The `build` folder is only a temporary PyInstaller folder. It is not required for users.
- Bundled `yt-dlp.exe` and `ffmpeg.exe` files can become outdated. Updating them often fixes download, cutting, or conversion errors.
- If you edit `ytdlp_gui.py`, those changes only apply when you run it with `python ytdlp_gui.py` or rebuild the EXE — editing the source does not change an already-built `dist/ytdlp_gui.exe`.

## License

This project is released under the Unlicense.

yt-dlp is a separate project and follows its own license:
<https://github.com/yt-dlp/yt-dlp/blob/master/LICENSE>

---

# yt-dlp GUI Türkçe

[yt-dlp](https://github.com/yt-dlp/yt-dlp) ile video ve ses indirmek için basit bir masaüstü uygulaması.

> Bu proje yt-dlp için hazırlanmış bağımsız bir grafik arayüzdür. Resmi yt-dlp projesi değildir.

## Özellikler

- YouTube ve yt-dlp'nin desteklediği birçok siteden video veya ses indirme
- Mevcut formatları getirip kalite seçme
- Belirli bir zaman aralığını indirme veya dışa aktarma, buçuklu saniye desteğiyle (örn. `21.5`)
- İndirmeden önce kesmenin gerçek başlangıç/bitiş karesini, tüm videoyu indirmeden önizleme
- Üç kesme modu: direkt kes, tam indir + kes, tam indir + yeniden kodla
- Daha iyi uyumluluk için h264/h265 yeniden kodlama
- Yeniden kodlama çözünürlüğü seçimi: orijinal, 1080p, 720p, 480p
- MP4, MKV, WEBM, MOV, AVI, MP3, AAC, OGG, M4A, FLAC ve WAV çıktı seçenekleri
- İlerleme çubuğu, durum yazısı, tahmini kalan süre ve log ekranı
- Türkçe ve İngilizce arayüz

## Gereksinimler

- Python 3.8 veya üzeri
- yt-dlp (**güncel tutun** — aşağıdaki nota bakın)
- ffmpeg
- YouTube için bir JavaScript motoru (**[Deno](https://deno.com/) önerilir**) — yt-dlp'nin YouTube'un oynatma doğrulamasını çözmesi için gerekli; kurulu değilse YouTube indirmeleri genellikle `HTTP Error 403: Forbidden` hatası verir

### Windows Kurulumu

**PowerShell** veya **Komut İstemi** açıp şunları çalıştırın:

```bash
python --version
pip --version
pip install -U yt-dlp
```

`python` tanınmıyorsa Python'u <https://www.python.org/downloads/> adresinden kurun. Kurulum ekranında **Add python.exe to PATH** seçeneğini işaretleyin.

ffmpeg'i winget ile kurun:

```bash
winget install Gyan.FFmpeg
```

PowerShell'i kapatıp tekrar açın, sonra kontrol edin:

```bash
ffmpeg -version
yt-dlp --version
```

Deno'yu kurun (yt-dlp'nin YouTube'un oynatma doğrulamasını çözmesi için gerekli; kurulu değilse YouTube indirmeleri genellikle `HTTP Error 403: Forbidden` hatası verir):

```bash
winget install DenoLand.Deno
```

Deno kurulumundan sonra PATH'e eklenmesi için PowerShell'i kapatıp tekrar açın.

`winget` yoksa ffmpeg'i elle kurun:

1. Windows sürümünü <https://www.gyan.dev/ffmpeg/builds/> adresinden indirin.
2. ZIP dosyasını çıkarın, örneğin `C:\ffmpeg` klasörüne.
3. Şu dosyanın var olduğundan emin olun: `C:\ffmpeg\bin\ffmpeg.exe`.
4. **Başlat Menüsü → Sistem ortam değişkenlerini düzenle** ekranını açın.
5. **Ortam Değişkenleri** butonuna tıklayın.
6. **Kullanıcı değişkenleri** altında **Path** seçip **Düzenle** butonuna tıklayın.
7. **Yeni** butonuna tıklayıp şunu ekleyin:

```text
C:\ffmpeg\bin
```

8. Tüm pencerelerde **Tamam** butonuna basın.
9. PowerShell'i kapatıp tekrar açın.
10. Kontrol edin:

```bash
ffmpeg -version
```

### macOS Kurulumu

```bash
brew install python ffmpeg deno
python3 -m pip install -U yt-dlp
```

### Linux Kurulumu

Debian/Ubuntu:

```bash
sudo apt update
sudo apt install python3 python3-pip ffmpeg
curl -fsSL https://deno.land/install.sh | sh
python3 -m pip install -U yt-dlp
```

## Kaynak Koddan Çalıştırma

```bash
python ytdlp_gui.py
```

## Hazır EXE ile Çalıştırma

Hazır paket indirdiyseniz `dist` klasörünü açıp şu dosyayı çalıştırın:

```text
dist/ytdlp_gui.exe
```

EXE sürümünü kullanmak için Python komutları çalıştırmanız gerekmez. Ancak `yt-dlp` ve `ffmpeg` yine sistemde kurulu ve erişilebilir olmalıdır.

Bazı paketlerde `ytdlp_gui.exe` yanında `yt-dlp.exe` ve `ffmpeg.exe` dosyaları bulunabilir. Bu durumda uygulama bu dosyaları doğrudan kullanabilir. İndirme, kesme, birleştirme veya yeniden kodlama hata vermeye başlarsa bu paketli araçlar eski kalmış olabilir. yt-dlp ve ffmpeg'in güncel sürümlerini indirip eski `.exe` dosyalarının yerine koyun.

## EXE Oluşturma

```bash
pyinstaller --noconfirm --clean --onefile --windowed ytdlp_gui.py
```

EXE dosyası şu klasörde oluşur:

```text
dist/ytdlp_gui.exe
```

## Kullanım

1. Video URL'sini yapıştırın.
2. **Formatları Getir** butonuna tıklayın.
3. Video veya ses formatını seçin.
4. İsteğe bağlı: başlangıç ve bitiş zamanı girin, örneğin `31:23` ve `33:00` (buçuklu saniye de olur: `31:23.5`), ya da timeline üzerindeki tutamaçları sürükleyin.
5. İsteğe bağlı: seçilen aralığın gerçek ilk/son karesini indirmeden önce görmek için **🔍 Önizle** butonuna tıklayın — özellikle keyframe kaymasını erkenden fark etmek için kullanışlıdır (aşağıdaki [Önizleme](#önizleme) bölümüne bakın).
6. Çıktı formatını seçin.
7. Yeniden kodlama modunu kullanıyorsanız codec ve çözünürlük seçin.
8. **İndir** butonuna tıklayın.

## Önizleme

**🔍 Önizle** butonu, tam indirmeye vakit harcamadan kesmenin nasıl görüneceğini kontrol etmenizi sağlar. Seçtiğiniz başlangıç ve bitiş noktalarının etrafından sadece birkaç saniyelik bir bölüm indirir (Direkt kes'te kullanılan aynı `--download-sections` + `--force-keyframes-at-cuts` yöntemiyle) ve gerçek ilk/son kareyi gösterir.

- Kareler doğru görünüyorsa rahatlıkla indirebilirsiniz.
- Başlangıç/bitiş karesi kaymış görünüyorsa, genellikle o klip için "Direkt kes" yerine "Tam indir → kes" ya da "Tam indir → yeniden kodla" modunun gerektiği anlamına gelir.
- Her nokta için bir zaman aşımı vardır (~25 saniye). Bir nokta zaman aşımına uğrarsa veya başarısız olursa (örneğin ağ sorunu ya da eski yt-dlp / eksik JS motoru yüzünden), önizleme o kareyi atlar ve elde edebildiğini gösterir.
- Sadece ses formatları için önizleme yapılamaz.

## Kesme Modları

**Direkt kes** en hızlı seçenektir. yt-dlp'den sadece seçilen aralığı indirmesini ister. Bazı videolarda başlangıç noktası keyframe yüzünden biraz kayabilir.

**Tam indir → kes** önce tüm dosyayı indirir, sonra yeniden kodlama yapmadan keser. Genelde hızlıdır; ancak kesme noktası keyframe'e denk gelmezse bazı videolarda ilk saniyede görüntü donabilir.

**Tam indir → yeniden kodla** önce tüm dosyayı indirir ve seçilen aralığı yeni bir dosya olarak kodlar. Daha yavaştır, ama genelde en doğru ve en uyumlu sonucu verir. Twitter/X ve genel paylaşım için MP4 + h264 önerilir.

## Yeniden Kodlama Çözünürlüğü

En yüksek kalite için **Orijinal** seçeneğini kullanın.

Daha hızlı işlem ve daha küçük dosya için **720p** veya **480p** seçin. 720p, 1080p'ye göre daha az piksel işlediği için genelde belirgin şekilde daha hızlıdır.

## Notlar

- **yt-dlp'yi güncel tutun.** YouTube oynatma korumasını sık sık değiştiriyor; ~90 günden eski yt-dlp sürümleri genellikle çalışmıyor. Düzenli olarak `pip install -U yt-dlp` (veya standalone exe için `yt-dlp -U`) çalıştırın.
- YouTube linklerinde `WARNING: No supported JavaScript runtime could be found` ya da `HTTP Error 403: Forbidden` görüyorsanız, [Deno](https://deno.com/)'yu kurun (yukarıdaki Gereksinimler'e bakın) ve yt-dlp'yi güncelleyin — bu artık çoğu YouTube indirmesi için gerekli, sadece isteğe bağlı bir uyarı değil.
- Yeniden kodlama işlemciyi yoğun kullanır ve uzun veya yüksek çözünürlüklü videolarda birkaç dakika sürebilir.
- Uygulama açıksa Windows `dist/ytdlp_gui.exe` dosyasının üzerine yazmayı engelleyebilir. Yeniden paketlemeden önce uygulamayı kapatın.
- `build` klasörü sadece PyInstaller'ın geçici çalışma klasörüdür. Kullanıcılar için gerekli değildir.
- Paket içindeki `yt-dlp.exe` ve `ffmpeg.exe` zamanla eski kalabilir. Bu dosyaları güncellemek indirme, kesme veya dönüştürme hatalarını çoğu zaman çözer.
- `ytdlp_gui.py` dosyasını düzenlerseniz, değişiklikler yalnızca `python ytdlp_gui.py` ile çalıştırdığınızda ya da EXE'yi yeniden derlediğinizde geçerli olur — kaynağı düzenlemek zaten derlenmiş `dist/ytdlp_gui.exe` dosyasını değiştirmez.

## Lisans

Bu proje Unlicense ile yayınlanmıştır.

yt-dlp ayrı bir projedir ve kendi lisansına tabidir:
<https://github.com/yt-dlp/yt-dlp/blob/master/LICENSE>
