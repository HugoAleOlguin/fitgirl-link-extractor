# FitGirl FuckingFast Link Extractor (Pro)

A fast, lightweight, and user-friendly desktop application built in Python (Tkinter) to retrieve, categorize, filter, and extract direct download links from FuckingFast hosters on FitGirl Repack pages (fitgirl-repacks.site).

---

## Descripcion en Espanol

Una herramienta de escritorio rapida y liviana desarrollada en Python para extraer, categorizar, filtrar y obtener los enlaces directos de descarga desde hosters de FuckingFast en las paginas de FitGirl Repacks.

### Caracteristicas Principales
- Obtencion y Clasificacion Automatica: Extrae las partes y las agrupa automaticamente en secciones desplegables (Binarios Principales, Paquetes de Idioma por pais/idioma, Contenido Bonus, etc.).
- Soporte Multilingue (Espanol / Ingles): Selector de idioma integrado en la interfaz.
- Navegacion Fluida por Teclado:
  - Flechas (Arriba / Abajo): Navega de forma inteligente por la lista con resalte visual en azul.
  - Barra Espaciadora: Marca o desmarca la parte enfocada.
  - Clic de Raton: Sincroniza la navegacion para continuar desde el elemento clickeado.
- Buscador en Tiempo Real y Presets:
  - Filtrado instantaneo por texto.
  - Botones de seleccion rapida (Seleccionar Todo, Deseleccionar Todo, Solo Binarios Principales, Invertir Seleccion).
- Compatibilidad Instantanea con JDownloader 2 e IDM:
  - Al copiar los enlaces al portapapeles, incluye automaticamente el nombre del archivo (#fg-01.bin), lo que permite que JDownloader 2 e IDM los reconozcan inmediatamente sin realizar escaneos profundos.
- Bypass Automatico de Cloudflare Turnstile:
  - Utiliza undetected-chromedriver para superar los desafios de seguridad de Cloudflare sin intervencion manual.
  - Instalacion automatica en segundo plano si la dependencia no se encuentra en el sistema.
- Control de Detencion (Stop): Permite cancelar la extraccion en cualquier momento.

---

## English Description

A fast and lightweight desktop GUI application built in Python to retrieve, group, filter, and extract direct download URLs from FuckingFast hosters on FitGirl Repack pages.

### Key Features
- Automated Parsing & Categorization: Groups links into collapsible accordion sections (Core Binaries, Language Packs by country/language, Bonus Content, etc.).
- Multilingual UI (Spanish / English): Built-in language selector.
- Fluid Keyboard Navigation:
  - Arrow Keys (Up / Down): Smooth navigation with a distinct blue highlight.
  - Spacebar: Toggle checkbox on the focused item.
  - Mouse Click Sync: Seamlessly continues keyboard navigation from any clicked item.
- Real-time Search & Presets:
  - Live filter as you type.
  - Quick presets (Select All, Deselect All, Main Binaries Only, Invert Selection).
- Instant JDownloader 2 & IDM Clipboard Auto-Detection:
  - Copied URLs automatically append #filename (#fg-01.bin), allowing JDownloader 2 & IDM to grab them immediately without deep crawling.
- Automated Cloudflare Turnstile Bypass:
  - Powered by undetected-chromedriver to bypass Turnstile checks cleanly.
  - Automatic background dependency installer if missing.
- Stop Control: Interrupt long extraction tasks instantly.

---

## Installation & Running / Instalacion y Uso

### Prerequisites / Requisitos
- Python 3.8+ installed on Windows, Linux, or macOS.

### Steps / Pasos

1. Clone the repository / Clonar el repositorio:
   ```bash
   git clone https://github.com/zouhirdev/fitgirl-ff-link-extractor.git
   cd fitgirl-ff-link-extractor
   ```

2. Install dependencies / Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application / Ejecutar la aplicacion:
   ```bash
   python ff_grabber.py
   ```

---

## Configuration & Dependencies / Configuracion y Dependencias

- `requirements.txt`:
  - `requests`
  - `beautifulsoup4`
  - `undetected-chromedriver` (Optional, auto-installed if missing)
- `config.json`: Automatically saves your last used FitGirl URL, browser choice, and UI language selection.

---

## License / Licencia

MIT License. Free to use and modify.
