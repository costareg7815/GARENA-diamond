import pyautogui
import webbrowser
import time
import random
import subprocess
import os
from colorama import init, Fore as f, Back, Style
import sys
import threading

# تهيئة colorama للالوان في console
init()

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

# دعم متعدد اللغات
LANGUAGES = {
    "en": {
        "welcome": "Shop2Game Automation Tool",
        "made_by": "MADE BY:KIRA99",
        "powered_by": "POWERED BY PYTHON",
        "attempts": "How many attempts do you want to perform? ",
        "proxy_question": "Do you want to use proxy list? (y/n): ",
        "proxy_file": "Enter proxy file name (proxies.txt): ",
        "starting": "🚀 Starting attempt",
        "opening_browser": "🧭 Opening new incognito browser window...",
        "closing_browser": "🛑 Closing browser...",
        "searching": "🔍 Searching for:",
        "found": "✅ Found and clicked:",
        "not_found": "❌ Not found:",
        "success": "✅ Steps completed successfully.",
        "completed": "🎉 All attempts completed.",
        "loading": "⏳ Loading...",
        "proxy_loaded": "🔌 Loaded {} proxies.",
        "error": "❌ Error:"
    },
    "ar": {
        "welcome": "أداة أتمتة Shop2Game",
        "made_by": "صنع بواسطة: اسمك",
        "powered_by": "مدعوم بلغة بايثون",
        "attempts": "كم عدد المحاولات التي تريد تنفيذها؟ ",
        "proxy_question": "هل تريد استخدام قائمة بروكسي؟ (y/n): ",
        "proxy_file": "أدخل اسم ملف البروكسي (proxies.txt): ",
        "starting": "🚀 بدء المحاولة رقم",
        "opening_browser": "🧭 فتح نافذة متصفح خفي جديدة...",
        "closing_browser": "🛑 إغلاق المتصفح...",
        "searching": "🔍 البحث عن:",
        "found": "✅ تم الضغط على:",
        "not_found": "❌ لم يتم العثور على:",
        "success": "✅ تم تنفيذ الخطوات بنجاح.",
        "completed": "🎉 انتهت كل المحاولات.",
        "loading": "⏳ جاري التحميل...",
        "proxy_loaded": "🔌 تم تحميل {} بروكسي.",
        "error": "❌ خطأ:"
    }
}

current_lang = "en"  # اللغة الافتراضية

def set_language():
    """اختيار اللغة"""
    global current_lang
    print(f"{f.CYAN}1. English (en)\n2. العربية (ar){Style.RESET_ALL}")
    choice = input("Choose language / اختر اللغة (1/2): ")
    current_lang = "en" if choice == "1" else "ar"

def t_(key):
    """ترجمة النص حسب اللغة الحالية"""
    return LANGUAGES[current_lang].get(key, key)

def show_banner():
    """عرض شعار البرنامج"""
    print(f.CYAN + Style.BRIGHT + """
╦╔═ ╦ ╦═╗ ╔═╗
╠╩╗ ║ ╠╦╝ ╠═╣   """ + t_("made_by") + """
╩ ╩ ╩ ╩╚═ ╩ ╩   """ + t_("powered_by") + "\n" + Style.RESET_ALL)
    print(f.YELLOW + "="*50 + Style.RESET_ALL)

class Spinner:
    """علامة تحميل متحركة"""
    def __init__(self):
        self.spinner_chars = ["⣾", "⣽", "⣻", "⢿", "⡿", "⣟", "⣯", "⣷"]
        self.stop_running = False
        self.spinner_thread = None

    def spin(self):
        i = 0
        while not self.stop_running:
            sys.stdout.write(f"\r{self.spinner_chars[i]} {t_('loading')}")
            sys.stdout.flush()
            time.sleep(0.1)
            i = (i + 1) % len(self.spinner_chars)

    def start(self):
        self.stop_running = False
        self.spinner_thread = threading.Thread(target=self.spin)
        self.spinner_thread.start()

    def stop(self):
        self.stop_running = True
        if self.spinner_thread:
            self.spinner_thread.join()
        sys.stdout.write("\r" + " " * 20 + "\r")
        sys.stdout.flush()

def generate_card_number():
    """إنشاء رقم بطاقة عشوائي"""
    return ''.join(str(random.randint(0, 9)) for _ in range(16))

def load_proxies(filename="proxies.txt"):
    """تحميل قائمة البروكسي من ملف"""
    try:
        with open(filename, "r") as f:
            proxies = [line.strip() for line in f if line.strip()]
        print(f.GREEN + t_("proxy_loaded").format(len(proxies)) + Style.RESET_ALL)
        return proxies
    except FileNotFoundError:
        print(f.RED + t_("error") + f" {filename} not found!" + Style.RESET_ALL)
        return []

def scroll_and_find_click(image, timeout=10, scroll_attempts=10):
    """البحث عن صورة على الشاشة والنقر عليها مع إمكانية التمرير"""
    print(f.YELLOW + t_("searching") + f" {image}" + Style.RESET_ALL)
    start = time.time()
    attempts = 0
    
    spinner = Spinner()
    spinner.start()
    
    try:
        while time.time() - start < timeout:
            pos = pyautogui.locateCenterOnScreen(image, confidence=0.8)
            if pos:
                spinner.stop()
                pyautogui.click(pos)
                print(f.GREEN + t_("found") + f" {image}" + Style.RESET_ALL)
                time.sleep(0.5)
                return True
            else:
                pyautogui.scroll(-300)
                attempts += 1
                if attempts >= scroll_attempts:
                    break
                time.sleep(0.3)
        
        spinner.stop()
        print(f.RED + t_("not_found") + f" {image}" + Style.RESET_ALL)
        return False
    except:
        spinner.stop()
        return False

def open_incognito(url, proxy=None):
    """فتح نافذة متصفح خفي جديدة مع إمكانية استخدام بروكسي"""
    print(f.BLUE + t_("opening_browser") + Style.RESET_ALL)
    
    chrome_cmd = [chrome_path, "--incognito"]
    if proxy:
        chrome_cmd.extend([f"--proxy-server={proxy}"])
    chrome_cmd.append(url)
    
    subprocess.Popen(chrome_cmd)
    time.sleep(7)

def close_browser():
    """إغلاق المتصفح"""
    print(f.MAGENTA + t_("closing_browser") + Style.RESET_ALL)
    os.system("taskkill /im chrome.exe /f")
    time.sleep(2)

def main():
    """الدالة الرئيسية"""
    show_banner()
    set_language()
    
    # اختيار استخدام البروكسي
    use_proxy = input(f.CYAN + t_("proxy_question") + Style.RESET_ALL).lower() == "y"
    proxies = []
    proxy_index = 0
    
    if use_proxy:
        proxy_file = input(f.CYAN + t_("proxy_file") + Style.RESET_ALL) or "proxies.txt"
        proxies = load_proxies(proxy_file)
        if not proxies:
            print(f.RED + t_("error") + " No proxies loaded. Continuing without proxy." + Style.RESET_ALL)
            use_proxy = False
    
    count = int(input(f.CYAN + t_("attempts") + Style.RESET_ALL))
    
    for i in range(count):
        print(f"\n" + f.GREEN + t_("starting") + f" {i+1}" + Style.RESET_ALL)
        
        # اختيار البروكسي إذا كان متاحًا
        current_proxy = proxies[proxy_index % len(proxies)] if use_proxy and proxies else None
        proxy_index += 1
        
        open_incognito("https://shop2game.com/", current_proxy)
        time.sleep(2)

        # 1. step1 → كتابة الرقم الثابت
        if scroll_and_find_click("step1.png", timeout=10):
            time.sleep(1)
            pyautogui.hotkey("ctrl", "a")
            pyautogui.press("backspace")
            pyautogui.write("12835225112")
            time.sleep(1)
        else:
            close_browser()
            continue

        # 2. step2
        if not scroll_and_find_click("step2.png", timeout=10):
            close_browser()
            continue
        time.sleep(1)

        # 3. step3 → مجرد ضغط فقط
        if not scroll_and_find_click("step3.png", timeout=10):
            close_browser()
            continue
        time.sleep(1)

        # 4. step4 → ضغط + إدخال رقم 16 خانة
        if scroll_and_find_click("step4.png", timeout=10):
            time.sleep(1)
            pyautogui.hotkey("ctrl", "a")
            pyautogui.press("backspace")
            pyautogui.write(generate_card_number())
            time.sleep(1)
        else:
            close_browser()
            continue

        # 5. step5
        if not scroll_and_find_click("step5.png", timeout=10):
            close_browser()
            continue
        time.sleep(1)

        print(f.GREEN + t_("success") + Style.RESET_ALL)
        time.sleep(3)
        close_browser()

    print(f"\n" + f.GREEN + Style.BRIGHT + t_("completed") + Style.RESET_ALL)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f.RED + "\n❌ Process interrupted by user" + Style.RESET_ALL)
    except Exception as e:
        print(f.RED + t_("error") + f" {str(e)}" + Style.RESET_ALL)
