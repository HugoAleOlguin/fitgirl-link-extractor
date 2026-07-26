import setuptools  # Register distutils fallback
import os
import sys
import time
import re
import json
import threading
import subprocess
import requests
from bs4 import BeautifulSoup

import tkinter as tk
from tkinter import ttk, messagebox, filedialog

# Lazy import for undetected-chromedriver
uc = None

def get_uc():
    global uc
    if uc is None or uc is False:
        try:
            import undetected_chromedriver as uc_module
            uc = uc_module
        except ImportError:
            uc = False
    return uc if uc is not False else None


CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")

# I18N Translations Dictionary
TRANSLATIONS = {
    "English": {
        "url_label": "FitGirl Game URL:",
        "fetch_btn": "1. Fetch Links",
        "extract_btn": "2. Extract Selected",
        "stop_btn": "Stop",
        "select_all": "Select All",
        "deselect_all": "Deselect All",
        "main_only": "Main Binaries Only",
        "invert_sel": "Invert Selection",
        "search_label": "Search:",
        "checklist_title": "Found Parts (Categorized & Expandable)",
        "output_title": "Extracted Direct Download Links",
        "clear_btn": "Clear Output",
        "save_txt_btn": "Save to .txt",
        "copy_btn": "Copy All Links",
        "status_waiting": "Waiting for input...",
        "status_fetching": "Fetching page...",
        "status_installing": "Installing browser dependency (undetected-chromedriver)... please wait.",
        "status_installed": "Browser dependency installed successfully! Ready to extract.",
        "status_dep_missing": "Warning: undetected-chromedriver missing. Click 'Extract' when ready.",
        "cat_core": "Core Repack & Main Binaries",
        "cat_spanish": "Optional Spanish Pack",
        "cat_mexican": "Optional Mexican Pack",
        "cat_english": "Optional English Pack",
        "cat_german": "Optional German Pack",
        "cat_italian": "Optional Italian Pack",
        "cat_french": "Optional French Pack",
        "cat_polish": "Optional Polish Pack",
        "cat_russian": "Optional Russian Pack",
        "cat_japanese": "Optional Japanese Pack",
        "cat_korean": "Optional Korean Pack",
        "cat_trad_chinese": "Optional Traditional Chinese",
        "cat_simp_chinese": "Optional Simplified Chinese",
        "cat_brazilian": "Optional Brazilian Pack",
        "cat_bonus": "Optional Bonus Content",
        "cat_general": "General Repack Parts",
        "selected_fmt": "Selected: {selected} / {total}",
        "msg_copied": "Copied {count} direct download links to clipboard!\nJDownloader / IDM will auto-detect them.",
        "msg_no_links": "No links found to process."
    },
    "Español": {
        "url_label": "URL del juego en FitGirl:",
        "fetch_btn": "1. Obtener Enlaces",
        "extract_btn": "2. Extraer Seleccionados",
        "stop_btn": "Detener",
        "select_all": "Seleccionar Todo",
        "deselect_all": "Deseleccionar Todo",
        "main_only": "Solo Binarios Principales",
        "invert_sel": "Invertir Selección",
        "search_label": "Buscar:",
        "checklist_title": "Partes Encontradas (Categorizadas y Desplegables)",
        "output_title": "Enlaces de Descarga Directa Extraídos",
        "clear_btn": "Limpiar Resultado",
        "save_txt_btn": "Guardar en .txt",
        "copy_btn": "Copiar Todos los Enlaces",
        "status_waiting": "Esperando enlace de FitGirl...",
        "status_fetching": "Obteniendo página...",
        "status_installing": "Instalando dependencia (undetected-chromedriver)... por favor espera.",
        "status_installed": "¡Dependencia instalada correctamente! Listo para extraer.",
        "status_dep_missing": "Aviso: undetected-chromedriver no instalado. Haz clic en 'Extraer' cuando gustes.",
        "cat_core": "Binarios Principales y Core Repack",
        "cat_spanish": "Paquete Opcional Español",
        "cat_mexican": "Paquete Opcional Mexicano",
        "cat_english": "Paquete Opcional Inglés",
        "cat_german": "Paquete Opcional Alemán",
        "cat_italian": "Paquete Opcional Italiano",
        "cat_french": "Paquete Opcional Francés",
        "cat_polish": "Paquete Opcional Polaco",
        "cat_russian": "Paquete Opcional Ruso",
        "cat_japanese": "Paquete Opcional Japonés",
        "cat_korean": "Paquete Opcional Coreano",
        "cat_trad_chinese": "Paquete Opcional Chino Tradicional",
        "cat_simp_chinese": "Paquete Opcional Chino Simplificado",
        "cat_brazilian": "Paquete Opcional Brasileño",
        "cat_bonus": "Contenido Opcional Bonus",
        "cat_general": "Partes Generales del Repack",
        "selected_fmt": "Seleccionados: {selected} / {total}",
        "msg_copied": "¡Se copiaron {count} enlaces directos al portapapeles!\nJDownloader y IDM los detectarán automáticamente.",
        "msg_no_links": "No se encontraron enlaces para procesar."
    }
}


def categorize_link(link, lang="English"):
    """Dynamically categorizes FitGirl files into human-readable groups."""
    t = TRANSLATIONS.get(lang, TRANSLATIONS["English"])
    filename = link.split('#')[-1] if '#' in link else link.split('/')[-1]
    filename_lower = filename.lower()

    opt_match = re.search(r'fg-(?:optional|selective)-([a-z0-9\-]+)', filename_lower)

    if opt_match:
        tag = opt_match.group(1)

        if "spanish" in tag or "espanol" in tag:
            return t["cat_spanish"]
        elif "mexican" in tag:
            return t["cat_mexican"]
        elif "english" in tag:
            return t["cat_english"]
        elif "german" in tag:
            return t["cat_german"]
        elif "italian" in tag:
            return t["cat_italian"]
        elif "french" in tag or "francais" in tag:
            return t["cat_french"]
        elif "polish" in tag:
            return t["cat_polish"]
        elif "russian" in tag:
            return t["cat_russian"]
        elif "japanese" in tag:
            return t["cat_japanese"]
        elif "korean" in tag:
            return t["cat_korean"]
        elif "traditional-chinese" in tag:
            return t["cat_trad_chinese"]
        elif "chinese" in tag or "simplified" in tag:
            return t["cat_simp_chinese"]
        elif "brazilian" in tag or "portuguese" in tag:
            return t["cat_brazilian"]
        elif any(kw in tag for kw in ["bonus", "content", "soundtrack", "credits", "4k", "hd"]):
            return t["cat_bonus"]
        else:
            clean_tag = tag.replace('-', ' ').title()
            return f"Optional {clean_tag} Pack" if lang == "English" else f"Paquete Opcional {clean_tag}"

    if "setup" in filename_lower or re.search(r'fg-\d+\.bin', filename_lower) or "part" in filename_lower or "repack" in filename_lower:
        return t["cat_core"]

    return t["cat_general"]


class FitgirlExtractorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FitGirl FF Link Extractor (Pro)")
        self.root.geometry("820x860")
        self.root.minsize(680, 700)

        self.config = self.load_config()
        self.lang = self.config.get("language", "English")

        self.checkbox_vars = {}        # {url: BooleanVar}
        self.item_widgets = []          # List of tuples: (chk_widget, link_url, filename, category_name, flat_index)
        self.category_sections = {}     # {category_name: dict_info}
        self.focused_index = -1
        self.cancel_event = threading.Event()
        self.is_processing = False

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(2, weight=1)
        self.root.rowconfigure(5, weight=1)

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure(
            "Custom.Horizontal.TProgressbar",
            background="#24890d",
            troughcolor="#e0e0e0",
            bordercolor="#24890d",
            lightcolor="#24890d",
            darkcolor="#24890d"
        )
        self.style.configure("Compact.TLabelframe", padding=1)

        self.default_bg = self.root.cget("bg") or "#f0f0f0"

        self.setup_ui()

        # Keyboard Navigation & Mousewheel Bindings
        self.root.bind_all("<MouseWheel>", self._on_mousewheel)
        self.root.bind_all("<Button-4>", self._on_mousewheel)
        self.root.bind_all("<Button-5>", self._on_mousewheel)

        self.root.bind("<Down>", self._nav_down)
        self.root.bind("<Up>", self._nav_up)
        self.root.bind("<space>", self._nav_toggle_space)

        self.root.after(100, self.check_and_autoinstall_deps)

    def t(self, key):
        return TRANSLATIONS.get(self.lang, TRANSLATIONS["English"]).get(key, key)

    def load_config(self):
        defaults = {
            "last_url": "https://fitgirl-repacks.site/grand-theft-auto-v/",
            "browser": "Auto-Detect Browser",
            "language": "English"
        }
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    defaults.update(json.load(f))
            except Exception:
                pass
        return defaults

    def save_config(self):
        self.config["last_url"] = self.url_var.get().strip()
        self.config["browser"] = self.browser_var.get()
        self.config["language"] = self.lang_var.get()
        try:
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=4)
        except Exception:
            pass

    def check_and_autoinstall_deps(self):
        if get_uc() is None:
            self.status_var.set(self.t("status_installing"))
            self.extract_btn.config(state="disabled")

            def run_pip():
                try:
                    subprocess.check_call([sys.executable, "-m", "pip", "install", "undetected-chromedriver"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    global uc
                    uc = None
                    get_uc()
                    self.root.after(0, lambda: self.status_var.set(self.t("status_installed")))
                except Exception:
                    self.root.after(0, lambda: self.status_var.set(self.t("status_dep_missing")))
                finally:
                    if self.checkbox_vars:
                        self.root.after(0, lambda: self.extract_btn.config(state="normal"))

            threading.Thread(target=run_pip, daemon=True).start()

    def change_language(self, event=None):
        self.lang = self.lang_var.get()
        self.save_config()
        self.retranslate_ui()

    def retranslate_ui(self):
        self.url_label.config(text=self.t("url_label"))
        self.fetch_btn.config(text=self.t("fetch_btn"))
        self.extract_btn.config(text=self.t("extract_btn"))
        self.stop_btn.config(text=self.t("stop_btn"))
        self.select_all_btn.config(text=self.t("select_all"))
        self.deselect_all_btn.config(text=self.t("deselect_all"))
        self.main_only_btn.config(text=self.t("main_only"))
        self.invert_sel_btn.config(text=self.t("invert_sel"))
        self.search_lbl.config(text=self.t("search_label"))
        self.checklist_frame.config(text=self.t("checklist_title"))
        self.output_frame.config(text=self.t("output_title"))
        self.clear_btn.config(text=self.t("clear_btn"))
        self.export_txt_btn.config(text=self.t("save_txt_btn"))
        self.copy_btn.config(text=self.t("copy_btn"))
        self.status_var.set(self.t("status_waiting"))
        self.update_counter()

    def setup_ui(self):
        # 1. Input Frame
        input_frame = ttk.Frame(self.root, padding="8 6 8 2")
        input_frame.grid(row=0, column=0, sticky="ew")
        input_frame.columnconfigure(1, weight=1)

        self.url_label = ttk.Label(input_frame, text=self.t("url_label"), font=("Arial", 10, "bold"))
        self.url_label.grid(row=0, column=0, sticky="w", pady=1)

        self.url_var = tk.StringVar(value=self.config.get("last_url", ""))
        self.url_entry = ttk.Entry(input_frame, textvariable=self.url_var, font=("Arial", 10))
        self.url_entry.grid(row=1, column=0, columnspan=3, sticky="ew", pady=2)

        self.fetch_btn = ttk.Button(input_frame, text=self.t("fetch_btn"), command=self.start_fetch_thread)
        self.fetch_btn.grid(row=2, column=0, sticky="w", pady=2)

        options_frame = ttk.Frame(input_frame)
        options_frame.grid(row=2, column=2, sticky="e")

        # Language Selector Combobox
        self.lang_var = tk.StringVar(value=self.lang)
        self.lang_combo = ttk.Combobox(options_frame, textvariable=self.lang_var, state="readonly", width=10)
        self.lang_combo['values'] = ("English", "Español")
        self.lang_combo.bind("<<ComboboxSelected>>", self.change_language)
        self.lang_combo.pack(side="right", padx=(5, 0))

        self.browser_var = tk.StringVar(value=self.config.get("browser", "Auto-Detect Browser"))
        self.browser_combo = ttk.Combobox(options_frame, textvariable=self.browser_var, state="readonly", width=18)
        self.browser_combo['values'] = (
            "Auto-Detect Browser",
            "Google Chrome",
            "Microsoft Edge",
            "Brave",
            "Mozilla Firefox"
        )
        self.browser_combo.pack(side="right")

        # 2. Status & Search Frame
        middle_frame = ttk.Frame(self.root, padding="8 2 8 2")
        middle_frame.grid(row=1, column=0, sticky="ew")
        middle_frame.columnconfigure(0, weight=1)

        self.status_var = tk.StringVar(value=self.t("status_waiting"))
        status_label = ttk.Label(middle_frame, textvariable=self.status_var, font=("Arial", 9, "italic"), foreground="#333")
        status_label.grid(row=0, column=0, sticky="w")

        search_subframe = ttk.Frame(middle_frame)
        search_subframe.grid(row=0, column=1, sticky="e")
        self.search_lbl = ttk.Label(search_subframe, text=self.t("search_label"), font=("Arial", 9))
        self.search_lbl.pack(side="left", padx=2)
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *args: self.filter_checklist())
        self.search_entry = ttk.Entry(search_subframe, textvariable=self.search_var, width=22)
        self.search_entry.pack(side="left", padx=2)

        # 3. Checklist Area
        self.checklist_frame = ttk.LabelFrame(self.root, text=self.t("checklist_title"), padding="2 2 2 2")
        self.checklist_frame.grid(row=2, column=0, sticky="nsew", padx=8, pady=2)
        self.checklist_frame.rowconfigure(0, weight=1)
        self.checklist_frame.columnconfigure(0, weight=1)

        self.canvas = tk.Canvas(self.checklist_frame, highlightthickness=0)
        self.scrollbar_list = ttk.Scrollbar(self.checklist_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar_list.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.itemconfig(self.canvas_window, width=e.width))

        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.scrollbar_list.grid(row=0, column=1, sticky="ns")

        controls_frame = ttk.Frame(self.checklist_frame)
        controls_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(2, 0))

        self.select_all_btn = ttk.Button(controls_frame, text=self.t("select_all"), command=self.select_all)
        self.select_all_btn.pack(side="left", padx=2)

        self.deselect_all_btn = ttk.Button(controls_frame, text=self.t("deselect_all"), command=self.deselect_all)
        self.deselect_all_btn.pack(side="left", padx=2)

        self.main_only_btn = ttk.Button(controls_frame, text=self.t("main_only"), command=self.select_main_only)
        self.main_only_btn.pack(side="left", padx=2)

        self.invert_sel_btn = ttk.Button(controls_frame, text=self.t("invert_sel"), command=self.invert_selection)
        self.invert_sel_btn.pack(side="left", padx=2)

        self.counter_var = tk.StringVar(value="Selected: 0 / 0")
        ttk.Label(controls_frame, textvariable=self.counter_var, font=("Arial", 9, "bold"), foreground="#24890d").pack(side="left", padx=8)

        self.stop_btn = ttk.Button(controls_frame, text=self.t("stop_btn"), command=self.stop_extraction, state="disabled")
        self.stop_btn.pack(side="right", padx=2)

        self.extract_btn = ttk.Button(controls_frame, text=self.t("extract_btn"), command=self.start_extraction_thread, state="disabled")
        self.extract_btn.pack(side="right", padx=2)

        # 4. Progress Bar
        self.progress = ttk.Progressbar(
            self.root,
            orient="horizontal",
            mode="determinate",
            style="Custom.Horizontal.TProgressbar"
        )
        self.progress.grid(row=4, column=0, sticky="ew", padx=8, pady=2)

        # 5. Output Direct Links Frame
        self.output_frame = ttk.LabelFrame(self.root, text=self.t("output_title"), padding="2 2 2 2")
        self.output_frame.grid(row=5, column=0, sticky="nsew", padx=8, pady=2)
        self.output_frame.columnconfigure(0, weight=1)
        self.output_frame.rowconfigure(0, weight=1)

        self.text_area = tk.Text(self.output_frame, wrap="none", font=("Consolas", 9), height=9)
        self.text_area.grid(row=0, column=0, sticky="nsew")

        scrollbar_y = ttk.Scrollbar(self.output_frame, orient="vertical", command=self.text_area.yview)
        scrollbar_y.grid(row=0, column=1, sticky="ns")
        self.text_area.configure(yscrollcommand=scrollbar_y.set)

        scrollbar_x = ttk.Scrollbar(self.output_frame, orient="horizontal", command=self.text_area.xview)
        scrollbar_x.grid(row=1, column=0, sticky="ew")
        self.text_area.configure(xscrollcommand=scrollbar_x.set)

        # 6. Bottom Export Frame
        btn_frame = ttk.Frame(self.root, padding="8 2 8 6")
        btn_frame.grid(row=6, column=0, sticky="ew")

        self.clear_btn = ttk.Button(btn_frame, text=self.t("clear_btn"), command=self.clear_output)
        self.clear_btn.pack(side="left")

        self.export_txt_btn = ttk.Button(btn_frame, text=self.t("save_txt_btn"), command=self.export_txt)
        self.export_txt_btn.pack(side="right", padx=2)

        self.copy_btn = ttk.Button(btn_frame, text=self.t("copy_btn"), command=self.copy_to_clipboard)
        self.copy_btn.pack(side="right", padx=2)

    # --- Mousewheel Logic ---
    def _on_mousewheel(self, event):
        try:
            widget = self.root.winfo_containing(event.x_root, event.y_root)
            if widget and (widget == self.canvas or str(widget).startswith(str(self.scrollable_frame))):
                if hasattr(event, 'delta') and event.delta != 0:
                    direction = -1 if event.delta > 0 else 1
                    self.canvas.yview_scroll(direction, "units")
                elif hasattr(event, 'num'):
                    if event.num == 4:
                        self.canvas.yview_scroll(-1, "units")
                    elif event.num == 5:
                        self.canvas.yview_scroll(1, "units")
        except Exception:
            pass

    # --- Keyboard Navigation & Blue Active Selection ---
    def _get_visible_items(self):
        visible = []
        for item in self.item_widgets:
            chk, link, fn, cat, idx = item
            if chk.winfo_viewable() or (chk.master and chk.master.winfo_viewable()):
                visible.append((chk, link, fn, cat, idx))
        return visible

    def _highlight_focused_item(self):
        visible = self._get_visible_items()
        if not visible:
            return

        if self.focused_index < 0:
            self.focused_index = 0
        elif self.focused_index >= len(visible):
            self.focused_index = len(visible) - 1

        focused_tuple = visible[self.focused_index]
        focused_widget = focused_tuple[0]

        for item in self.item_widgets:
            chk = item[0]
            if chk == focused_widget:
                chk.config(bg="#0078d7", fg="#ffffff", selectcolor="#005a9e", activebackground="#005a9e", activeforeground="#ffffff")
            else:
                chk.config(bg=self.default_bg, fg="#000000", selectcolor="#ffffff", activebackground=self.default_bg, activeforeground="#000000")

        focused_widget.focus_set()

        try:
            self.root.update_idletasks()
            canvas_h = self.canvas.winfo_height()
            if canvas_h <= 0:
                return

            w_y1 = focused_widget.winfo_rooty() - self.canvas.winfo_rooty()
            w_y2 = w_y1 + focused_widget.winfo_height()

            if w_y1 < 0:
                self.canvas.yview_scroll(int(w_y1 // 18) - 1, "units")
            elif w_y2 > canvas_h:
                self.canvas.yview_scroll(int((w_y2 - canvas_h) // 18) + 1, "units")
        except Exception:
            pass

    def _nav_down(self, event):
        visible = self._get_visible_items()
        if visible:
            if self.focused_index < len(visible) - 1:
                self.focused_index += 1
                self._highlight_focused_item()
        return "break"

    def _nav_up(self, event):
        visible = self._get_visible_items()
        if visible:
            if self.focused_index > 0:
                self.focused_index -= 1
                self._highlight_focused_item()
        return "break"

    def _nav_toggle_space(self, event):
        focus = self.root.focus_get()
        if focus and isinstance(focus, ttk.Entry):
            return

        visible = self._get_visible_items()
        if visible and 0 <= self.focused_index < len(visible):
            chk_widget, link_url, _, _, _ = visible[self.focused_index]
            var = self.checkbox_vars.get(link_url)
            if var:
                var.set(not var.get())
                self.update_counter()
            return "break"

    # --- Selection Controls ---
    def select_all(self):
        for var in self.checkbox_vars.values():
            var.set(True)
        self.update_counter()

    def deselect_all(self):
        for var in self.checkbox_vars.values():
            var.set(False)
        self.update_counter()

    def select_main_only(self):
        core_cat = self.t("cat_core")
        for item in self.item_widgets:
            chk, link, filename, cat, idx = item
            if cat == core_cat or cat == TRANSLATIONS["English"]["cat_core"]:
                self.checkbox_vars[link].set(True)
            else:
                self.checkbox_vars[link].set(False)
        self.update_counter()

    def invert_selection(self):
        for var in self.checkbox_vars.values():
            var.set(not var.get())
        self.update_counter()

    def update_counter(self):
        total = len(self.checkbox_vars)
        selected = sum(1 for v in self.checkbox_vars.values() if v.get())
        self.counter_var.set(self.t("selected_fmt").format(selected=selected, total=total))

    def filter_checklist(self):
        query = self.search_var.get().strip().lower()

        for category_name, sec in self.category_sections.items():
            sec_visible_count = 0
            for chk_widget, link, filename, idx in sec["items"]:
                if not query or query in filename.lower() or query in category_name.lower():
                    chk_widget.pack(anchor="w", padx=10, pady=0)
                    sec_visible_count += 1
                else:
                    chk_widget.pack_forget()

            if sec_visible_count > 0:
                sec["frame"].pack(fill="x", expand=True, padx=2, pady=1)
            else:
                sec["frame"].pack_forget()

        self.focused_index = 0

    # --- Export Utilities ---
    def copy_to_clipboard(self):
        raw_text = self.text_area.get(1.0, tk.END).strip()
        if not raw_text:
            messagebox.showwarning("Warning", self.t("msg_no_links"))
            return

        formatted_links = []
        for line in raw_text.splitlines():
            line_str = line.strip()
            if line_str and not line_str.startswith("#"):
                formatted_links.append(line_str)

        if formatted_links:
            clipboard_content = "\n".join(formatted_links)
            self.root.clipboard_clear()
            self.root.clipboard_append(clipboard_content)
            messagebox.showinfo("Success", self.t("msg_copied").format(count=len(formatted_links)))
        else:
            messagebox.showwarning("Warning", self.t("msg_no_links"))

    def export_txt(self):
        raw_text = self.text_area.get(1.0, tk.END).strip()
        if not raw_text:
            messagebox.showwarning("Warning", self.t("msg_no_links"))
            return

        links = [line.strip() for line in raw_text.splitlines() if line.strip() and not line.startswith("#")]
        if not links:
            messagebox.showwarning("Warning", self.t("msg_no_links"))
            return

        filepath = filedialog.asksaveasfilename(
            title="Save Direct Links",
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if filepath:
            try:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write("\n".join(links) + "\n")
                messagebox.showinfo("Exported", f"Successfully saved to:\n{filepath}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {str(e)}")

    def clear_output(self):
        self.text_area.delete(1.0, tk.END)
        self.progress.config(value=0)

    def update_ui(self, status=None, progress_val=None, max_val=None, text_append=None):
        if status is not None:
            self.status_var.set(status)
        if max_val is not None:
            self.progress.config(maximum=max_val)
        if progress_val is not None:
            self.progress.config(value=progress_val)
        if text_append is not None:
            self.text_area.insert(tk.END, text_append + "\n")
            self.text_area.see(tk.END)

    # --- Step 1: Fetching Links ---
    def start_fetch_thread(self):
        url = self.url_var.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a valid FitGirl URL.")
            return

        self.save_config()

        self.fetch_btn.config(state="disabled")
        self.extract_btn.config(state="disabled")
        self.status_var.set(self.t("status_fetching"))

        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.checkbox_vars.clear()
        self.item_widgets.clear()
        self.category_sections.clear()

        thread = threading.Thread(target=self.run_fetch, args=(url,), daemon=True)
        thread.start()

    def run_fetch(self, url):
        try:
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
            res = requests.get(url, headers=headers, timeout=10)
            res.raise_for_status()
            soup = BeautifulSoup(res.text, 'html.parser')

            ff_links = []
            for a in soup.find_all('a', href=True):
                if 'fuckingfast.co' in a['href'] and a['href'] not in ff_links:
                    ff_links.append(a['href'])

            self.root.after(0, self.populate_checkboxes, ff_links)

        except requests.exceptions.ConnectionError:
            self.root.after(0, self.update_ui, "Network Error: Cannot reach FitGirl. Is your ISP blocking it? Try a VPN/Custom DNS.")
            self.root.after(0, lambda: self.fetch_btn.config(state="normal"))
        except Exception as e:
            self.root.after(0, self.update_ui, f"Error fetching links: {str(e)}")
            self.root.after(0, lambda: self.fetch_btn.config(state="normal"))

    def populate_checkboxes(self, links):
        if not links:
            self.status_var.set("No FuckingFast links found on this page!")
            self.fetch_btn.config(state="normal")
            return

        grouped = {}
        for link in links:
            cat = categorize_link(link, self.lang)
            grouped.setdefault(cat, []).append(link)

        global_idx = 0

        for cat_name, cat_links in grouped.items():
            sec_frame = ttk.LabelFrame(self.scrollable_frame, text="", padding=1, style="Compact.TLabelframe")
            sec_frame.pack(fill="x", expand=True, padx=2, pady=1)

            hdr_frame = ttk.Frame(sec_frame)
            hdr_frame.pack(fill="x", expand=True)

            is_expanded = tk.BooleanVar(value=True)

            toggle_btn = ttk.Button(hdr_frame, text="-", width=2)
            toggle_btn.pack(side="left", padx=1)

            title_lbl = ttk.Label(hdr_frame, text=f"{cat_name} ({len(cat_links)})", font=("Arial", 9, "bold"))
            title_lbl.pack(side="left", padx=2)

            # Flexible padding buttons without truncating fixed widths
            sec_select_btn = ttk.Button(hdr_frame, text=self.t("select_all"), padding=(4, 1))
            sec_select_btn.pack(side="right", padx=2)

            sec_deselect_btn = ttk.Button(hdr_frame, text=self.t("deselect_all"), padding=(4, 1))
            sec_deselect_btn.pack(side="right", padx=2)

            items_container = ttk.Frame(sec_frame)
            items_container.pack(fill="x", expand=True, pady=0)

            sec_items = []
            for link in cat_links:
                var = tk.BooleanVar(value=True)
                var.trace_add("write", lambda *args: self.update_counter())
                self.checkbox_vars[link] = var

                filename = link.split('#')[-1] if '#' in link else link.split('/')[-1]

                chk = tk.Checkbutton(
                    items_container,
                    text=filename,
                    variable=var,
                    anchor="w",
                    bg=self.default_bg,
                    fg="#000000",
                    selectcolor="#ffffff",
                    activebackground=self.default_bg,
                    activeforeground="#000000",
                    relief="flat",
                    bd=0,
                    padx=4,
                    pady=0,
                    font=("Arial", 9)
                )
                chk.pack(anchor="w", fill="x", padx=10, pady=0)

                def make_click_handler(flat_index=global_idx):
                    def on_click(event):
                        visible = self._get_visible_items()
                        for v_i, item in enumerate(visible):
                            if item[4] == flat_index:
                                self.focused_index = v_i
                                self._highlight_focused_item()
                                break
                    return on_click

                chk.bind("<Button-1>", make_click_handler(global_idx))

                item_tuple = (chk, link, filename, cat_name, global_idx)
                sec_items.append(item_tuple)
                self.item_widgets.append(item_tuple)
                global_idx += 1

            def make_toggle(container=items_container, btn=toggle_btn, exp_var=is_expanded):
                def toggle():
                    if exp_var.get():
                        container.pack_forget()
                        btn.config(text="+")
                        exp_var.set(False)
                    else:
                        container.pack(fill="x", expand=True, pady=0)
                        btn.config(text="-")
                        exp_var.set(True)
                return toggle

            toggle_btn.config(command=make_toggle())

            def make_sec_select(c_links=cat_links, val=True):
                def sec_action():
                    for l in c_links:
                        if l in self.checkbox_vars:
                            self.checkbox_vars[l].set(val)
                    self.update_counter()
                return sec_action

            sec_select_btn.config(command=make_sec_select(cat_links, True))
            sec_deselect_btn.config(command=make_sec_select(cat_links, False))

            self.category_sections[cat_name] = {
                "frame": sec_frame,
                "container": items_container,
                "items": sec_items
            }

        self.update_counter()
        self.focused_index = 0
        self.status_var.set(f"Found {len(links)} parts across {len(grouped)} categories. Ready to extract.")
        self.fetch_btn.config(state="normal")
        self.extract_btn.config(state="normal")

    # --- Step 2: Extraction Engine (Browser Automation with Cloudflare Bypass) ---
    def get_browser_path(self, selected_browser="Auto-Detect Browser"):
        browser_paths = {
            "Google Chrome": [
                r"%ProgramFiles%\Google\Chrome\Application\chrome.exe",
                r"%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe",
                r"%LocalAppData%\Google\Chrome\Application\chrome.exe",
                "/usr/bin/google-chrome",
                "/usr/bin/google-chrome-stable",
                "/var/lib/flatpak/exports/bin/com.google.Chrome"
            ],
            "Microsoft Edge": [
                r"%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe",
                r"%ProgramFiles%\Microsoft\Edge\Application\msedge.exe",
                r"%LocalAppData%\Microsoft\Edge\Application\msedge.exe",
                "/usr/bin/microsoft-edge-stable",
                "/usr/bin/microsoft-edge"
            ],
            "Brave": [
                r"%ProgramFiles%\BraveSoftware\Brave-Browser\Application\brave.exe",
                r"%ProgramFiles(x86)%\BraveSoftware\Brave-Browser\Application\brave.exe",
                r"%LocalAppData%\BraveSoftware\Brave-Browser\Application\brave.exe",
                "/usr/bin/brave-browser",
                "/usr/bin/brave",
                "/var/lib/flatpak/exports/bin/com.brave.Browser"
            ],
            "Mozilla Firefox": [
                r"%ProgramFiles%\Mozilla Firefox\firefox.exe",
                r"%ProgramFiles(x86)%\Mozilla Firefox\firefox.exe",
                r"%LocalAppData%\Mozilla Firefox\firefox.exe",
                "/usr/bin/firefox",
                "/var/lib/flatpak/exports/bin/org.mozilla.firefox"
            ]
        }

        if selected_browser != "Auto-Detect Browser":
            paths_to_check = browser_paths.get(selected_browser, [])
        else:
            paths_to_check = []
            for paths in browser_paths.values():
                paths_to_check.extend(paths)

        for path in paths_to_check:
            expanded_path = os.path.expandvars(path)
            if os.path.exists(expanded_path):
                return expanded_path
        return None

    def stop_extraction(self):
        if self.is_processing:
            self.cancel_event.set()
            self.status_var.set("Stopping extraction...")
            self.stop_btn.config(state="disabled")

    def start_extraction_thread(self):
        selected_links = [url for url, var in self.checkbox_vars.items() if var.get()]

        if not selected_links:
            messagebox.showwarning("Warning", self.t("msg_no_links"))
            return

        self.save_config()
        self.cancel_event.clear()
        self.is_processing = True

        self.fetch_btn.config(state="disabled")
        self.extract_btn.config(state="disabled")
        self.stop_btn.config(state="normal")
        self.clear_output()

        thread = threading.Thread(target=self.run_extraction, args=(selected_links,), daemon=True)
        thread.start()

    def run_extraction(self, links):
        total = len(links)

        uc_lib = get_uc()
        selected_browser = self.browser_var.get()
        browser_executable = self.get_browser_path(selected_browser)

        if not browser_executable:
            self.root.after(0, self.update_ui, f"Error: Could not find {selected_browser} on your system.")
            self._reset_extraction_state()
            return

        if not uc_lib and os.path.basename(browser_executable).lower() not in ['firefox', 'msedge']:
            self.root.after(0, self.update_ui, "Error: undetected-chromedriver is missing. Installing in background...")
            self.check_and_autoinstall_deps()
            self._reset_extraction_state()
            return

        browser_name = os.path.basename(browser_executable).replace('.exe', '')
        self.root.after(0, self.update_ui, f"Initializing {browser_name} to bypass Cloudflare...", 0, total)

        driver = None

        def create_driver(version=None):
            if browser_name.lower() == 'firefox':
                from selenium import webdriver
                from selenium.webdriver.firefox.options import Options
                opts = Options()
                opts.binary_location = browser_executable
                opts.set_preference("dom.webdriver.enabled", False)
                opts.set_preference("useAutomationExtension", False)
                return webdriver.Firefox(options=opts)

            elif browser_name.lower() == 'msedge':
                from selenium import webdriver
                from selenium.webdriver.edge.options import Options
                opts = Options()
                opts.binary_location = browser_executable
                opts.add_experimental_option("excludeSwitches", ["enable-automation"])
                opts.add_experimental_option('useAutomationExtension', False)
                opts.add_argument("--disable-blink-features=AutomationControlled")
                return webdriver.Edge(options=opts)

            else:
                opts = uc_lib.ChromeOptions()
                return uc_lib.Chrome(
                    options=opts,
                    use_subprocess=True,
                    browser_executable_path=browser_executable,
                    version_main=version
                )

        try:
            try:
                driver = create_driver()
            except Exception as e:
                error_msg = str(e)
                if browser_name.lower() not in ['firefox', 'msedge'] and "Current browser version is" in error_msg:
                    match = re.search(r"Current browser version is (\d+)", error_msg)
                    if match:
                        correct_version = int(match.group(1))
                        self.root.after(0, self.update_ui, f"Auto-fixing ChromeDriver version to v{correct_version}...")
                        driver = create_driver(version=correct_version)
                    else:
                        raise e
                else:
                    raise e

            for i, link in enumerate(links, 1):
                if self.cancel_event.is_set():
                    self.root.after(0, self.update_ui, f"Extraction cancelled by user. ({i-1}/{total} completed)")
                    break

                filename = link.split('#')[-1] if '#' in link else link.split('/')[-1]
                self.root.after(0, self.update_ui, f"Processing [{i}/{total}]: {filename}")
                direct_url = None

                try:
                    driver.get(link)
                    for _ in range(25):
                        if self.cancel_event.is_set():
                            break
                        time.sleep(0.8)
                        page_html = driver.page_source

                        match_old = re.search(r'window\.open\("([^"]+)"\)', page_html)
                        if match_old:
                            direct_url = match_old.group(1)
                            break

                        match_new = re.search(r'hx-post="([^"]+)"', page_html)
                        if match_new:
                            post_endpoint = match_new.group(1)
                            post_url = f"https://fuckingfast.co{post_endpoint}"

                            cookies = {c['name']: c['value'] for c in driver.get_cookies()}
                            user_agent = driver.execute_script("return navigator.userAgent;")
                            headers = {"User-Agent": user_agent, "HX-Request": "true"}

                            try:
                                res = requests.post(post_url, cookies=cookies, headers=headers, allow_redirects=False, timeout=5)
                                if 'HX-Redirect' in res.headers:
                                    direct_url = res.headers['HX-Redirect']
                                    break
                                elif 'Location' in res.headers:
                                    direct_url = res.headers['Location']
                                    break
                                elif res.status_code == 200:
                                    match_url = re.search(r'(https://dl\.fuckingfast\.co/dl/[^\'"]+)', res.text)
                                    if match_url:
                                        direct_url = match_url.group(1)
                                        break
                            except Exception:
                                pass
                except Exception as e:
                    self.root.after(0, self.update_ui, None, i, None, f"# ERROR: {str(e)} -> {filename}")

                if direct_url:
                    if filename and '#' not in direct_url:
                        direct_url = f"{direct_url}#{filename}"
                    self.root.after(0, self.update_ui, None, i, None, direct_url)
                elif not self.cancel_event.is_set():
                    self.root.after(0, self.update_ui, None, i, None, f"# FAILED: {filename} ({link})")

            if not self.cancel_event.is_set():
                self.root.after(0, self.update_ui, f"Extraction complete! Processed {total} links.")

        except Exception as e:
            self.root.after(0, self.update_ui, f"Extraction Error: {str(e)}")

        finally:
            self._reset_extraction_state()
            if driver:
                try:
                    driver.quit()
                except Exception:
                    pass

    def _reset_extraction_state(self):
        self.is_processing = False
        self.root.after(0, lambda: self.fetch_btn.config(state="normal"))
        self.root.after(0, lambda: self.extract_btn.config(state="normal"))
        self.root.after(0, lambda: self.stop_btn.config(state="disabled"))


if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style(root)
    if "clam" in style.theme_names():
        style.theme_use("clam")

    app = FitgirlExtractorApp(root)
    root.mainloop()
