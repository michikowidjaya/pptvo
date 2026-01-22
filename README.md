# ppt-auto-vo

Automated pipeline untuk mengonversi PPTX atau PDF menjadi video slideshow (MP4) dengan voiceover.

---

## Ringkasan

- **Python**: Gratis, menggunakan `gTTS` (Google TTS). Mudah digunakan dan tidak memerlukan API berbayar.
- **TypeScript**: Menggunakan ElevenLabs (kualitas suara lebih baik), memerlukan API key berbayar.

---

## Persyaratan sistem

- `ffmpeg`
- `pdftoppm` (Poppler)
- LibreOffice (untuk konversi PPTX)

Untuk Python juga diperlukan paket Python yang tercantum di `requirements.txt`.

---

## Instalasi (Python)

1. Pasang dependency Python:

2. Pasang dependency sistem (contoh Ubuntu/Debian):

```bash
sudo apt install ffmpeg poppler-utils libreoffice
```

---

## Menjalankan (Python)

- Jalankan pipeline langsung:

```bash
python pptx_to_video.py --file slides.pptx
python pptx_to_video.py --file document.pdf
```

- Atau jalankan antarmuka Streamlit untuk UI sederhana:

```bash
streamlit run streamlit_app.py
# buka http://localhost:8501
```

---

## Menjalankan (TypeScript)

Persyaratan: Node.js 18+, ElevenLabs API key (jika ingin TTS berkualitas tinggi).

```bash
npm install
cp .env.example .env
# edit .env -> set ELEVENLABS_API_KEY dan ELEVENLABS_VOICE_ID
npm run build
npm run watch
```

---

## Output & Struktur folder

- Final video: `output/output.mp4`
- Cache/intermediate:
	- Python: `temp/` (pdf/, slides/, audio/, slide_videos/)
	- TypeScript: `cache/`

Contoh struktur:

```
project-root/
├── input/          # tempat meletakkan slides.pptx / document.pdf / script.txt
├── output/         # output/output.mp4
├── temp/           # cache Python
├── cache/          # cache TypeScript
├── pptx_to_video.py
├── streamlit_app.py
└── src/            # TypeScript sumber
```

---

## Pilih implementasi

- Pilih **Python** untuk solusi cepat dan gratis.
- Pilih **TypeScript** jika memerlukan TTS berkualitas tinggi (ElevenLabs).

---

Jika ingin, saya bisa menambahkan:
- contoh `script.txt` template
- tombol auto-fill script dari PDF (ekstraksi teks)
- panduan setup ElevenLabs

Silakan beri tahu fitur mana yang Anda inginkan.

**Requirements:**
- Python 3.8+
- FFmpeg (required)
- pdftoppm / poppler-utils (required)
- LibreOffice (required for PPTX files)

**Quick Start:**
```bash
# Install Python dependencies
pip install -r requirements.txt

# Install system dependencies (Ubuntu/Debian)
sudo apt install ffmpeg poppler-utils libreoffice

# Install system dependencies (macOS)
brew install ffmpeg poppler libreoffice

# Run pipeline with PPTX
python3 pptx_to_video.py --file slides.pptx

# Run pipeline with PDF
python3 pptx_to_video.py --file document.pdf

# Or use the helper script
./run_pipeline.sh
```

**Documentation:** See [README_PYTHON.md](README_PYTHON.md) for detailed documentation.

---

### 2. TypeScript Implementation (Original)

**Pipeline:** PPTX + INSTRUKSI.txt → (LibreOffice) PDF → (pdftoppm) PNG → (ElevenLabs API) TTS → (FFmpeg) render → output.mp4

**Features:**
- ✅ High-quality TTS using ElevenLabs API
- ✅ Multi-voice support
- ✅ Watch mode for development
- ✅ **Background PNG overlay** - Add custom background to every slide

**Requirements:**
- Node.js 18+
- FFmpeg (ffmpeg + ffprobe)
- LibreOffice (soffice)
- Poppler (pdftoppm)
- ElevenLabs API key (paid)

**Setup:**
```bash
npm i
cp .env.example .env
# Edit .env and add your ELEVENLABS_API_KEY and ELEVENLABS_VOICE_ID
# Optionally add BACKGROUND_PATH for custom background image
```

**Run:**
```bash
npm run build    # One-time build
npm run watch    # Watch mode for development
```

---

## Output

Both implementations produce:
- **Final video:** `output/output.mp4`
- **Intermediate files:** `cache/` (TypeScript) or `temp/` (Python)

## Folder Structure

```
project-root/
├── input/
│   ├── slides.pptx          # Your PowerPoint file
│   ├── document.pdf          # Or your PDF file
│   └── INSTRUKSI.txt         # (Optional) Instructions
├── output/
│   └── output.mp4            # Final video output
├── temp/                     # Python implementation cache
│   ├── pdf/
│   │   └── input.pdf        # PDF source (converted from PPTX or copied from input)
│   ├── slides/              # RAW PNG slides (slide-1.png, slide-2.png, ...)
│   ├── audio/               # MP3 audio files (slide-1.mp3, slide-2.mp3, ...)
│   ├── slide_videos/        # Per-slide videos (slide-1.mp4, slide-2.mp4, ...)
│   └── slides_list.txt      # Concatenation list for FFmpeg
├── cache/                    # TypeScript implementation cache
├── pptx_to_video.py         # Python implementation
├── run_pipeline.sh          # Python helper script
└── src/                     # TypeScript implementation
```

## Which Implementation to Use?

**Choose Python if:**
- You want a free solution (no API costs)
- You prefer Python
- You don't need high-quality voice synthesis
- You want simpler setup

**Choose TypeScript if:**
- You need professional-quality voiceover
- You have an ElevenLabs API key
- You're already familiar with Node.js
- You need watch mode for iterative development

## Streamlit Frontend

You can run a lightweight Streamlit UI to upload/select input files and run the Python pipeline from a browser.

1. Install dependencies (already included in `requirements.txt`):

```bash
pip install -r requirements.txt
```

2. Start the app:

```bash
streamlit run streamlit_app.py
```

The app exposes an uploader (or lets you pick files from `input/`), a language setting, and a run button. After the pipeline completes it will show logs and let you preview/download `output/output.mp4`.
