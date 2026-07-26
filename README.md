# FitGirl Repack Link Extractor Pro

FitGirl Repack Link Extractor Pro is the ultimate lightweight, high-performance desktop GUI tool designed to retrieve, categorize, filter, and extract direct download links from FuckingFast hosters on FitGirl Repack pages (`fitgirl-repacks.site`).

Built for speed and ease of use, it automatically bypasses Cloudflare Turnstile security checks, categorizes repack files by language and main setup binaries, and formats extracted URLs for instant auto-detection in JDownloader 2, IDM (Internet Download Manager), and Free Download Manager.

---

## Key Features

- **Automated Categorization**: Automatically separates Core Repack Binaries (`setup.exe`, `fg-01.bin`, `fg-part1.rar`) from optional language packs (Spanish, English, German, French, Italian, Japanese, Polish, Russian, Chinese, Portuguese) and bonus content.
- **Instant JDownloader 2 & IDM Auto-Detection**: Extracted links append file anchor hashes (`#fg-01.bin`), allowing download managers to immediately recognize file extensions and queue downloads without deep crawling.
- **Cloudflare Turnstile Bypass**: Powered by `undetected-chromedriver` to pass Turnstile checks seamlessly.
- **Bilingual Interface**: Full support for **English** and **Spanish (Español)** UI text and category headers.
- **Keyboard Navigation**: Navigate the checklist with Arrow Keys (Up/Down) with a distinct blue highlight, toggle items with Spacebar, and sync focus from mouse clicks.
- **Real-Time Live Search**: Instantly filter files by typing in the search bar.
- **Quick Selection Presets**: Select All, Deselect All, Main Binaries Only, and Invert Selection.
- **Stop Control**: Cancel extraction operations at any time without freezing the app.
- **Single Standalone Executable**: No Python installation required when using the pre-compiled `.exe`.

---

## Downloads (Pre-Compiled Executable)

Download the latest standalone Windows executable from the Releases section:
- **`FitGirl_Link_Extractor_Pro.exe`** (Single-file portable executable)

---

## Running from Source

### Requirements
- Python 3.8 or higher
- `requests`
- `beautifulsoup4`
- `undetected-chromedriver` (Auto-installed if missing)

### Quick Start
1. Clone this repository:
   ```bash
   git clone https://github.com/zouhirdev/fitgirl-ff-link-extractor.git
   cd fitgirl-ff-link-extractor
   ```

2. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```

3. Launch the application:
   ```bash
   python ff_grabber.py
   ```

---

## Keyboard Shortcuts

| Shortcut | Action |
| --- | --- |
| **Down Arrow** | Move focus to next link item |
| **Up Arrow** | Move focus to previous link item |
| **Spacebar** | Check / Uncheck focused link item |
| **Mouse Click** | Focus clicked link and sync arrow navigation |

---

## SEO & Frequently Asked Questions (FAQ)

### What is FitGirl Repack Link Extractor Pro?
FitGirl Repack Link Extractor Pro is a open-source desktop link grabber utility designed specifically to parse and extract direct download links from FuckingFast mirrors on `fitgirl-repacks.site`.

### How does it bypass Cloudflare Turnstile?
The application uses stealth browser automation (`undetected-chromedriver`) to solve Cloudflare Turnstile challenges automatically without user intervention.

### How do I import links into JDownloader 2?
Simply click **Copy All Links** or **Copiar Todos los Enlaces** in the app. JDownloader 2 automatically detects the formatted direct download links from your clipboard.

---

## License

Distributed under the MIT License. Free for personal and community use.
