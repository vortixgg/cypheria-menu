import sys
import os
import json
import string
import random
import shutil
import requests
import ipaddress
import subprocess
import platform
import threading
import time
import smtplib
import urllib.request
import zipfile
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl
                                     
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QListWidget,
    QPushButton,
    QLabel,
    QTabWidget,
    QInputDialog,
    QFileDialog,
    QMessageBox,
    QLineEdit,
    QSlider,
    QProgressDialog
)
from PyQt6.QtCore import (
    Qt,
    QSize,
    QTimer,
    QTime,
    QEvent
)
from PyQt6.QtGui import (
    QIcon,
    QPixmap
)

                                  
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

                  
STREAM_PROOF_ACTIVE = False
HIDE_KEYBIND = 0x2D                       
WINDOW_HIDDEN = False
def essay_bot(parent=None):
    """Auto-type essay from clipboard"""
    APP_ICON = QIcon("images/icon.ico")
    
                                     
    try:
        import pyautogui
    except ImportError:
        QMessageBox.critical(parent, "Missing Module", 
            "pyautogui is not installed!\n\nInstall it with:\npip install pyautogui")
        return
    
                   
    delay_str, ok = QInputDialog.getText(parent, "Essay Bot", 
        "Enter delay between words (seconds):\n\nRecommended: 0.1 - 0.5")
    if not ok:
        return
    
    try:
        delay = float(delay_str)
        if delay < 0:
            delay = 0.1
    except:
        QMessageBox.warning(parent, "Invalid Input", "Invalid delay value. Using default: 0.2")
        delay = 0.2
    
                              
    clipboard = QApplication.clipboard()
    essay = clipboard.text()
    
    if not essay.strip():
        QMessageBox.warning(parent, "Empty Clipboard", 
            "No text found in clipboard!\n\nCopy your essay first, then run this.")
        return
    
    word_count = len(essay.split())
    
                                      
    msg = QMessageBox(parent)
    msg.setWindowTitle("Essay Bot Ready")
    msg.setWindowIcon(APP_ICON)
    msg.setIcon(QMessageBox.Icon.Information)
    msg.setText(f"Essay loaded: {word_count} words\n\n"
                f"Delay: {delay}s per word\n\n"
                f"Open your Google Doc now!\n\n"
                f"Starting in 10 seconds...")
    msg.setStandardButtons(QMessageBox.StandardButton.Cancel)
    
                     
    countdown = 10
    
    def update_countdown():
        nonlocal countdown
        if countdown > 0:
            msg.setText(f"Essay loaded: {word_count} words\n\n"
                       f"Delay: {delay}s per word\n\n"
                       f"Open your Google Doc now!\n\n"
                       f"Starting in {countdown} seconds...")
            countdown -= 1
            QTimer.singleShot(1000, update_countdown)
        else:
            msg.close()
            start_typing()
    
    def start_typing():
                                
        progress = QProgressDialog("Typing essay...", "Stop", 0, word_count, parent)
        progress.setWindowTitle("Essay Bot Running")
        progress.setWindowModality(Qt.WindowModality.WindowModal)
        progress.setMinimumDuration(0)
        progress.setValue(0)
        
        words_typed = 0
        should_stop = False
        
        def typing_thread():
            nonlocal words_typed, should_stop
            
            try:
                import pyautogui
                import time
                
                words = essay.split()
                
                for i, word in enumerate(words):
                    if should_stop or progress.wasCanceled():
                        break
                    
                    pyautogui.write(word + " ", interval=0.01)
                    words_typed += 1
                    
                    QTimer.singleShot(0, lambda: progress.setValue(words_typed))
                    
                    time.sleep(delay)
                
            except Exception as e:
                QTimer.singleShot(0, lambda: QMessageBox.critical(
                    parent, "Error", f"Typing failed:\n{e}"))
            finally:
                QTimer.singleShot(0, progress.close)
                if not should_stop and words_typed == word_count:
                    QTimer.singleShot(100, lambda: QMessageBox.information(
                        parent, "Success!", 
                        f"Essay typed successfully!\n\n{words_typed} words written."))
        
        def on_cancel():
            nonlocal should_stop
            should_stop = True
        
        progress.canceled.connect(on_cancel)
        
                             
        thread = threading.Thread(target=typing_thread, daemon=True)
        thread.start()
    
    update_countdown()
    msg.exec()
def fake_bluescreen(parent=None):
    """Display fake bluescreen fullscreen - uncloseable except DEL key"""
    global STREAM_PROOF_ACTIVE
    
    try:
                                  
        fake_window = QDialog()
        fake_window.setWindowTitle("")
        fake_window.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | 
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        
                         
        screen = QApplication.primaryScreen().geometry()
        fake_window.setGeometry(0, 0, screen.width(), screen.height())
        
                             
        fake_window.setStyleSheet("background-color: #0078d7;")
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
                                
        label = QLabel()
        pixmap = QPixmap("images/bluescreen.png")
        
        if pixmap.isNull():
            QMessageBox.critical(parent, "Error", "bluescreen.png not found in images folder!")
            return
        
                              
        scaled_pixmap = pixmap.scaled(
            screen.width(), 
            screen.height(), 
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        
        label.setPixmap(scaled_pixmap)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)
        
        fake_window.setLayout(layout)
        
                                                 
        def closeEvent(event):
            event.ignore()                             
        
        fake_window.closeEvent = closeEvent
        
                                                     
        def keyPressEvent(event):
            if event.key() == Qt.Key.Key_Delete:
                                             
                fake_window.closeEvent = lambda e: e.accept()
                fake_window.close()
            else:
                                                  
                event.ignore()
        
        fake_window.keyPressEvent = keyPressEvent
        
                                      
        fake_window.show()
        if STREAM_PROOF_ACTIVE and platform.system() == "Windows":
            try:
                import ctypes
                hwnd = fake_window.winId().__int__()
                user32 = ctypes.windll.user32
                WDA_EXCLUDEFROMCAPTURE = 0x00000011
                user32.SetWindowDisplayAffinity(hwnd, WDA_EXCLUDEFROMCAPTURE)
            except:
                pass
        
        fake_window.exec()
        
    except Exception as e:
        QMessageBox.critical(parent, "Error", f"Failed to show fake bluescreen:\n{e}")
def play_games(parent=None):
    global STREAM_PROOF_ACTIVE
    
                    
    game, ok = QInputDialog.getItem(parent, "Play Games", 
        "Choose a game:", 
        ["Geometry Dash", "Flappy Bird", "Poki Games"], 
        0, False)
    if not ok:
        return
    
                             
    if game == "Geometry Dash":
        url = "https://geometrydashlite.io/geometry-dash-game"
    elif game == "Flappy Bird":
        url = "https://terrorist.center"
    elif game == "Poki Games":
        url = "https://poki.com"
    else:
        return
    
    try:
                            
        game_window = QDialog(parent)
        game_window.setWindowTitle(f"Playing: {game}")
        game_window.setWindowIcon(QIcon("images/icon.ico"))
        game_window.resize(1000, 700)
        
        layout = QVBoxLayout()
        
                        
        webview = QWebEngineView()
        webview.setUrl(QUrl(url))
        layout.addWidget(webview)
        
        game_window.setLayout(layout)
        game_window.show()
        
                                      
        if STREAM_PROOF_ACTIVE and platform.system() == "Windows":
            try:
                import ctypes
                hwnd = game_window.winId().__int__()
                user32 = ctypes.windll.user32
                WDA_EXCLUDEFROMCAPTURE = 0x00000011
                user32.SetWindowDisplayAffinity(hwnd, WDA_EXCLUDEFROMCAPTURE)
            except:
                pass
        
        game_window.exec()
    
    except Exception as e:
        QMessageBox.critical(parent, "Error", f"Failed to load game:\n{e}")
def data_poisoner(parent=None):
    APP_ICON = QIcon("images/icon.ico")
    
                                     
    try:
        import pyautogui
    except ImportError:
        QMessageBox.critical(parent, "Missing Module", 
            "pyautogui is not installed!\n\nInstall it with:\npip install pyautogui")
        return
    
                          
    browser, ok = QInputDialog.getItem(parent, "Data Poisoner", 
        "Select browser:",
        ["Chrome", "Brave", "Edge", "Firefox"], 
        0, False)
    if not ok:
        return
    
                       
    searches = [
        "how to make sourdough bread", "best vacuum cleaner 2024", "cute cat videos",
        "weather forecast", "recipe for chocolate cake", "home workout routine",
        "best restaurants near me", "how to fix leaky faucet", "yoga for beginners",
        "top movies 2024", "gardening tips", "budget travel destinations",
        "meditation techniques", "healthy breakfast ideas", "diy home decor",
        "best books to read", "piano lessons online", "photography tips",
        "learn spanish free", "minecraft building ideas", "guitar chords beginner",
        "woodworking projects", "crochet patterns", "painting tutorials",
        "stock market news", "crypto prices today", "real estate trends",
        "fashion trends 2024", "skincare routine", "hairstyles for long hair",
        "fitness tracker reviews", "gaming laptop comparison", "smartphone specs",
        "car maintenance tips", "electric vehicle range", "motorcycle safety gear",
        "camping gear essentials", "hiking trails near me", "fishing techniques",
        "coffee brewing methods", "tea types and benefits", "wine pairing guide",
        "running shoes review", "crossfit workouts", "swimming techniques",
        "bird watching guide", "stargazing app", "telescope recommendations",
        "plant care tips", "aquarium setup", "dog training methods",
        "historical facts", "space exploration news", "ocean documentaries"
    ]
    
                           
    control_dialog = QDialog(parent)
    control_dialog.setWindowTitle("Data Poisoner Running")
    control_dialog.setWindowIcon(APP_ICON)
    control_dialog.setFixedSize(400, 300)
    
    layout = QVBoxLayout()
    
    status_label = QLabel("Starting...")
    status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    layout.addWidget(status_label)
    
    log_list = QListWidget()
    log_list.setStyleSheet("""
        QListWidget::item:selected { background:#8b0000; color:white; }
        QListWidget::item:focus { outline:none; }
    """)
    layout.addWidget(log_list)
    
    stop_btn = QPushButton("STOP")
    stop_btn.setStyleSheet("background: #b30000; font-weight: bold;")
    layout.addWidget(stop_btn)
    
    control_dialog.setLayout(layout)
    
    should_stop = False
    poisoning_started = False
    
    def poison_thread():
        nonlocal should_stop, poisoning_started
        
        try:
            import pyautogui
            import time
            import random
            
            browser_map = {
                "Chrome": "chrome",
                "Brave": "brave",
                "Edge": "edge",
                "Firefox": "firefox"
            }
            
            browser_name = browser_map.get(browser, "chrome")
            
                          
            QTimer.singleShot(0, lambda: status_label.setText("Opening browser..."))
            QTimer.singleShot(0, lambda: log_list.addItem(f"[*] Opening {browser}..."))
            
            pyautogui.press("winleft")
            time.sleep(0.3)
            pyautogui.write(browser_name)
            time.sleep(0.2)
            pyautogui.press("enter")
            time.sleep(4)
            
            poisoning_started = True
            QTimer.singleShot(0, lambda: status_label.setText("Poisoning data..."))
            QTimer.singleShot(0, lambda: log_list.addItem("[✓] Browser opened!"))
            
            search_count = 0
            
            while not should_stop:
                query = random.choice(searches)
                
                                   
                pyautogui.hotkey("ctrl", "l")
                time.sleep(random.uniform(0.4, 1.2))
                
                             
                pyautogui.write(query, interval=random.uniform(0.03, 0.08))
                time.sleep(random.uniform(0.3, 0.8))
                pyautogui.press("enter")
                
                search_count += 1
                QTimer.singleShot(0, lambda q=query, c=search_count: log_list.addItem(f"[{c}] {q}"))
                QTimer.singleShot(0, lambda: log_list.scrollToBottom())
                
                                  
                read_time = random.uniform(5, 12)
                start = time.time()
                while time.time() - start < read_time and not should_stop:
                    pyautogui.scroll(random.randint(-600, -200))
                    time.sleep(random.uniform(0.6, 1.8))
                
                time.sleep(random.uniform(3, 8))
        
        except Exception as e:
            QTimer.singleShot(0, lambda: log_list.addItem(f"[!] Error: {e}"))
        finally:
            QTimer.singleShot(0, lambda: status_label.setText("Stopped"))
            QTimer.singleShot(0, lambda: stop_btn.setText("Close"))
    
    def stop_poisoning():
        nonlocal should_stop
        if poisoning_started and not should_stop:
            should_stop = True
            status_label.setText("Stopping...")
            log_list.addItem("[!] Stopping data poisoner...")
        else:
            control_dialog.close()
    
    stop_btn.clicked.connect(stop_poisoning)
    
                       
    thread = threading.Thread(target=poison_thread, daemon=True)
    thread.start()
    
    control_dialog.exec()
def download_and_extract_images():
    """Download images.zip from Dropbox and extract to current directory"""
    try:
        dropbox_url = 'https://www.dropbox.com/scl/fi/jiq8ongy0hyi3m8ocjg1k/images.zip?rlkey=h7lrlmwj8fh9uwjomckhdf53u&st=vhc7sxlk&dl=1'  
        zip_path = os.path.join(os.getcwd(), 'images.zip')
        images_folder = os.path.join(os.getcwd(), 'images')
        
        
        if os.path.exists(images_folder):
            return  
        
        
        urllib.request.urlretrieve(dropbox_url, zip_path)
        
        
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(os.getcwd())
        
        
        os.remove(zip_path)
        
    except Exception as e:
        print(f"Failed to download/extract images: {e}")

def start_keybind_listener():
    
    global WINDOW_HIDDEN
    
    if platform.system() != "Windows":
        return
    
    def keybind_thread():
        global HIDE_KEYBIND, WINDOW_HIDDEN
        import ctypes
        user32 = ctypes.windll.user32
        
        while True:
            time.sleep(0.05)
            
                                                 
            if user32.GetAsyncKeyState(HIDE_KEYBIND) & 0x8000:
                                          
                app = QApplication.instance()
                if app:
                    for widget in app.topLevelWidgets():
                        if isinstance(widget, QWidget) and widget.windowTitle() == "Cypheria menu v11.5":
                            WINDOW_HIDDEN = not WINDOW_HIDDEN
                            if WINDOW_HIDDEN:
                                QTimer.singleShot(0, widget.hide)
                            else:
                                QTimer.singleShot(0, widget.show)
                            break
                
                                      
                while user32.GetAsyncKeyState(HIDE_KEYBIND) & 0x8000:
                    time.sleep(0.05)
    
    thread = threading.Thread(target=keybind_thread, daemon=True)
    thread.start()

def keybind_selector(parent=None):
    """Let user select ANY key as hide keybind"""
    global HIDE_KEYBIND
    
    APP_ICON = QIcon("images/icon.ico")
    
    
    key_names = {
        
        0x70: "F1", 0x71: "F2", 0x72: "F3", 0x73: "F4",
        0x74: "F5", 0x75: "F6", 0x76: "F7", 0x77: "F8",
        0x78: "F9", 0x79: "F10", 0x7A: "F11", 0x7B: "F12",
        
                      
        0x2D: "INSERT", 0x2E: "DELETE", 0x24: "HOME", 0x23: "END",
        0x21: "PAGE UP", 0x22: "PAGE DOWN",
        
                    
        0x25: "LEFT ARROW", 0x26: "UP ARROW", 0x27: "RIGHT ARROW", 0x28: "DOWN ARROW",
        
                    
        0x60: "NUMPAD 0", 0x61: "NUMPAD 1", 0x62: "NUMPAD 2", 0x63: "NUMPAD 3",
        0x64: "NUMPAD 4", 0x65: "NUMPAD 5", 0x66: "NUMPAD 6", 0x67: "NUMPAD 7",
        0x68: "NUMPAD 8", 0x69: "NUMPAD 9",
        
                 
        0x41: "A", 0x42: "B", 0x43: "C", 0x44: "D", 0x45: "E", 0x46: "F",
        0x47: "G", 0x48: "H", 0x49: "I", 0x4A: "J", 0x4B: "K", 0x4C: "L",
        0x4D: "M", 0x4E: "N", 0x4F: "O", 0x50: "P", 0x51: "Q", 0x52: "R",
        0x53: "S", 0x54: "T", 0x55: "U", 0x56: "V", 0x57: "W", 0x58: "X",
        0x59: "Y", 0x5A: "Z",
        
                 
        0x30: "0", 0x31: "1", 0x32: "2", 0x33: "3", 0x34: "4",
        0x35: "5", 0x36: "6", 0x37: "7", 0x38: "8", 0x39: "9",
        
                 
        0xBA: ";", 0xBB: "=", 0xBC: ",", 0xBD: "-", 0xBE: ".", 0xBF: "/",
        0xC0: "`", 0xDB: "[", 0xDC: "\\", 0xDD: "]", 0xDE: "'",
    }
    
                              
    current_key = key_names.get(HIDE_KEYBIND, "INSERT")
    
                         
    key_choice, ok = QInputDialog.getItem(parent, "Hide Keybind", 
        f"Select keybind to hide/show window:\n\nCurrent: {current_key}",
        list(key_names.values()), 
        list(key_names.values()).index(current_key), 
        False)
    
    if not ok:
        return
    
                           
    for code, name in key_names.items():
        if name == key_choice:
            HIDE_KEYBIND = code
            break
    
    QMessageBox.information(parent, "Keybind Set", 
        f"Hide/Show keybind set to: {key_choice}\n\n"
        f"Press {key_choice} anywhere to toggle window visibility!")

def private_browser(parent=None):
    global STREAM_PROOF_ACTIVE
    
                 
    url, ok = QInputDialog.getText(parent, "Private Browser", 
        "Enter URL (include https://):")
    if not ok or not url.strip():
        return
    
    url = url.strip()
    if not url.startswith("http"):
        url = "https://" + url
    
    try:
                               
        browser_window = QDialog(parent)
        browser_window.setWindowTitle("Private Browser")
        browser_window.setWindowIcon(QIcon("images/icon.ico"))
        browser_window.resize(1200, 800)
        
        layout = QVBoxLayout()
        
                        
        webview = QWebEngineView()
        webview.setUrl(QUrl(url))
        layout.addWidget(webview)
        
        browser_window.setLayout(layout)
        browser_window.show()
        
                                      
        if STREAM_PROOF_ACTIVE and platform.system() == "Windows":
            try:
                import ctypes
                hwnd = browser_window.winId().__int__()
                user32 = ctypes.windll.user32
                WDA_EXCLUDEFROMCAPTURE = 0x00000011
                user32.SetWindowDisplayAffinity(hwnd, WDA_EXCLUDEFROMCAPTURE)
            except:
                pass
        
        browser_window.exec()
    
    except Exception as e:
        QMessageBox.critical(parent, "Error", f"Failed to open browser:\n{e}")

def discord_webhook_tool(parent=None):
    APP_ICON = QIcon("images/icon.ico")
    
                         
    webhook_url, ok = QInputDialog.getText(parent, "Discord Webhook Tool", 
        "Enter Discord webhook URL:")
    if not ok or not webhook_url.strip():
        return
    
    webhook_url = webhook_url.strip()
    
                                 
    if not webhook_url.startswith("https://discord.com/api/webhooks/"):
        QMessageBox.warning(parent, "Invalid URL", "Please enter a valid Discord webhook URL.")
        return
    
                    
    action, ok = QInputDialog.getItem(parent, "Webhook Action", 
        "Choose action:", 
        ["Send Message", "Get Webhook Info", "Delete Webhook", "Spam Messages"], 
        0, False)
    if not ok:
        return
    
    if action == "Send Message":
        send_webhook_message(webhook_url, parent)
    elif action == "Get Webhook Info":
        get_webhook_info(webhook_url, parent)
    elif action == "Delete Webhook":
        delete_webhook(webhook_url, parent)
    elif action == "Spam Messages":
        spam_webhook(webhook_url, parent)

def send_webhook_message(webhook_url, parent):
                     
    message, ok = QInputDialog.getMultiLineText(parent, "Send Message", "Enter message:")
    if not ok or not message.strip():
        return
    
                                 
    username, ok = QInputDialog.getText(parent, "Username (Optional)", 
        "Custom username (leave blank for default):")
    if not ok:
        return
    
    try:
        import requests
        
        payload = {"content": message}
        if username.strip():
            payload["username"] = username.strip()
        
        response = requests.post(webhook_url, json=payload)
        
        if response.status_code == 204:
            QMessageBox.information(parent, "Success", "Message sent successfully!")
        else:
            QMessageBox.warning(parent, "Failed", f"Failed to send message.\nStatus: {response.status_code}")
    
    except Exception as e:
        QMessageBox.critical(parent, "Error", f"Error sending message:\n{e}")

def get_webhook_info(webhook_url, parent):
    try:
        import requests
        
        response = requests.get(webhook_url)
        
        if response.status_code == 200:
            data = response.json()
            
            info_text = (
                f"Webhook Name: {data.get('name', 'Unknown')}\n"
                f"Webhook ID: {data.get('id', 'Unknown')}\n"
                f"Channel ID: {data.get('channel_id', 'Unknown')}\n"
                f"Guild ID: {data.get('guild_id', 'Unknown')}\n"
                f"Token: {data.get('token', 'Unknown')}\n"
                f"Avatar: {data.get('avatar', 'None')}\n"
                f"Type: {data.get('type', 'Unknown')}"
            )
            
            dialog = QDialog(parent)
            dialog.setWindowTitle("Webhook Info")
            dialog.setWindowIcon(QIcon("images/icon.ico"))
            dialog.setFixedSize(400, 250)
            
            layout = QVBoxLayout()
            label = QLabel(info_text)
            label.setWordWrap(True)
            layout.addWidget(label)
            
            copy_btn = QPushButton("Copy Info")
            copy_btn.clicked.connect(lambda: QApplication.clipboard().setText(info_text))
            layout.addWidget(copy_btn)
            
            dialog.setLayout(layout)
            dialog.exec()
        else:
            QMessageBox.warning(parent, "Failed", f"Failed to get webhook info.\nStatus: {response.status_code}")
    
    except Exception as e:
        QMessageBox.critical(parent, "Error", f"Error getting webhook info:\n{e}")

def delete_webhook(webhook_url, parent):
    reply = QMessageBox.question(parent, "Confirm Delete", 
        "Are you sure you want to DELETE this webhook?\nThis cannot be undone!",
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        QMessageBox.StandardButton.No)
    
    if reply != QMessageBox.StandardButton.Yes:
        return
    
    try:
        import requests
        
        response = requests.delete(webhook_url)
        
        if response.status_code == 204:
            QMessageBox.information(parent, "Success", "Webhook deleted successfully!")
        else:
            QMessageBox.warning(parent, "Failed", f"Failed to delete webhook.\nStatus: {response.status_code}")
    
    except Exception as e:
        QMessageBox.critical(parent, "Error", f"Error deleting webhook:\n{e}")

def spam_webhook(webhook_url, parent):
                     
    message, ok = QInputDialog.getText(parent, "Spam Message", "Enter message to spam:")
    if not ok or not message.strip():
        return
    
                   
    count_str, ok = QInputDialog.getText(parent, "Spam Count", "How many messages? (max 100)")
    if not ok:
        return
    
    try:
        count = int(count_str)
        if count < 1:
            count = 1
        if count > 100:
            reply = QMessageBox.question(parent, "Warning", 
                f"You chose {count} messages. This may get the webhook rate limited.\nContinue?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No)
            if reply != QMessageBox.StandardButton.Yes:
                return
    except:
        QMessageBox.warning(parent, "Error", "Invalid number.")
        return
    
                     
    progress = QProgressDialog("Sending messages...", "Cancel", 0, count, parent)
    progress.setWindowTitle("Spamming...")
    progress.setWindowModality(Qt.WindowModality.WindowModal)
    progress.setMinimumDuration(0)
    progress.setValue(0)
    
    sent_count = 0
    errors = []
    should_stop = False
    lock = threading.Lock()
    
    def update_ui():
        with lock:
            progress.setValue(sent_count)
            progress.setLabelText(f"Sent {sent_count}/{count} | Errors: {len(errors)}")
    
    timer = QTimer(parent)
    timer.timeout.connect(update_ui)
    timer.start(300)
    
    def spam_thread():
        nonlocal sent_count, should_stop
        try:
            import requests
            
            for i in range(count):
                with lock:
                    if should_stop:
                        break
                
                if progress.wasCanceled():
                    with lock:
                        should_stop = True
                    break
                
                try:
                    payload = {"content": message}
                    response = requests.post(webhook_url, json=payload)
                    
                    if response.status_code == 204:
                        with lock:
                            sent_count += 1
                    else:
                        with lock:
                            errors.append(f"Message #{i+1}: Status {response.status_code}")
                    
                    time.sleep(0.5)                             
                
                except Exception as e:
                    with lock:
                        errors.append(f"Message #{i+1}: {str(e)}")
        
        finally:
            QTimer.singleShot(0, timer.stop)
            QTimer.singleShot(0, lambda: progress.close())
            QTimer.singleShot(100, lambda: QMessageBox.information(
                parent, "Done", 
                f"Spam finished.\nSent: {sent_count}/{count}\nErrors: {len(errors)}"))
    
    def on_cancel():
        nonlocal should_stop
        with lock:
            should_stop = True
        QTimer.singleShot(0, timer.stop)
        QTimer.singleShot(0, lambda: progress.close())
    
    progress.canceled.connect(on_cancel)
    
    thread = threading.Thread(target=spam_thread, daemon=True)
    thread.start()


def website_info(parent=None):
    APP_ICON = QIcon("images/icon.ico")

                         
    url, ok = QInputDialog.getText(parent, "Website Info", "Enter website URL (include https://):")
    if not ok or not url.strip():
        return

    url = url.strip()

    try:
        import requests
        import time

        start = time.time()
        response = requests.get(url, timeout=5)
        elapsed = round((time.time() - start) * 1000, 2)         

        info_text = (
            f"URL: {url}\n"
            f"Status Code: {response.status_code}\n"
            f"Server: {response.headers.get('Server', 'Unknown')}\n"
            f"Content Type: {response.headers.get('Content-Type', 'Unknown')}\n"
            f"Redirected: {response.history != []}\n"
            f"Response Time: {elapsed} ms"
        )

                                
        dialog = QDialog(parent)
        dialog.setWindowTitle("Website Info")
        dialog.setWindowIcon(APP_ICON)
        dialog.setFixedSize(400, 250)

        layout = QVBoxLayout()
        label = QLabel(info_text)
        label.setWordWrap(True)
        layout.addWidget(label)

        copy_btn = QPushButton("Copy Info")
        layout.addWidget(copy_btn)
        copy_btn.clicked.connect(lambda: QApplication.clipboard().setText(info_text))

        dialog.setLayout(layout)
        dialog.exec()

    except Exception as e:
        msg = QMessageBox(QMessageBox.Icon.Critical, "Error", f"Could not retrieve website info:\n{e}")
        msg.setWindowIcon(APP_ICON)
        msg.exec()

def email_spammer(parent=None):
    CONFIG_FILE = "config.json"

    config = {"email": "", "app_password": ""}
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                config.update(json.load(f))
        except:
            pass

    email = config.get("email", "").strip()
    app_password = config.get("app_password", "").strip()

    if not email:
        email, ok = QInputDialog.getText(parent, "Gmail Setup", "Your Gmail address:")
        if not ok or not email.strip():
            return
        config["email"] = email = email.strip().lower()

    if not app_password:
        app_password, ok = QInputDialog.getText(
            parent, "App Password Setup", "Gmail App Password (16 chars, no spaces):",
            echo=QLineEdit.EchoMode.Password
        )
        if not ok or not app_password.strip():
            return
        cleaned = app_password.replace(" ", "").strip()
        if len(cleaned) != 16:
            QMessageBox.warning(parent, "Invalid", "App password must be exactly 16 chars.")
            return
        config["app_password"] = cleaned

    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

    target, ok = QInputDialog.getText(parent, "Target", "Target email address:")
    if not ok or not target.strip():
        return
    target = target.strip()

    subject, ok = QInputDialog.getText(parent, "Message", "Email subject:")
    if not ok:
        return

    body, ok = QInputDialog.getMultiLineText(parent, "Message", "Email body:")
    if not ok:
        return

    attachment = None
    add_attach, ok = QInputDialog.getItem(parent, "Attachment", "Add attachment?", ["No", "Yes"], 0, False)
    if ok and add_attach == "Yes":
        path, _ = QFileDialog.getOpenFileName(parent, "Select file")
        if path:
            attachment = path

    amount_str, ok = QInputDialog.getText(parent, "Amount", "How many emails? (max 100 recommended)")
    if not ok:
        return
    try:
        amount = int(amount_str)
        if amount < 1:
            amount = 1
        if amount > 100:
            reply = QMessageBox.question(
                parent, "Warning",
                f"You chose {amount} emails.\nContinue?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            if reply != QMessageBox.StandardButton.Yes:
                return
    except:
        QMessageBox.warning(parent, "Error", "Invalid number.")
        return

    warning_text = (
        f"Target: {target}\n"
        f"Subject: {subject}\n"
        f"Body length: {len(body)} chars\n"
        f"Attachment: {os.path.basename(attachment) if attachment else 'None'}\n"
        f"Count: {amount}\n\n"
        "WARNING: Bulk sending risks suspension!"
    )
    reply = QMessageBox.question(
        parent, "Confirm", warning_text,
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        QMessageBox.StandardButton.No
    )
    if reply != QMessageBox.StandardButton.Yes:
        return

                                                      
    progress = QProgressDialog("Sending emails...", "Cancel", 0, amount, parent)
    progress.setWindowTitle("Sending...")
    progress.setWindowModality(Qt.WindowModality.WindowModal)
    progress.setMinimumDuration(0)
    progress.setValue(0)

    sent_count = 0
    errors = []
    should_stop = False
    lock = threading.Lock()

    def update_ui():
        with lock:
            progress.setValue(sent_count)
            progress.setLabelText(f"Sent {sent_count}/{amount} | Errors: {len(errors)}")

    timer = QTimer(parent)
    timer.timeout.connect(update_ui)
    timer.start(300)

    def sending_thread_func():
        nonlocal sent_count, should_stop
        try:
            for i in range(amount):
                with lock:
                    if should_stop:
                        break

                try:
                    msg = MIMEMultipart()
                    msg['From'] = email
                    msg['To'] = target
                    msg['Subject'] = subject
                    msg.attach(MIMEText(body, 'plain'))

                    if attachment:
                        part = MIMEBase('application', 'octet-stream')
                        with open(attachment, 'rb') as f:
                            part.set_payload(f.read())
                        encoders.encode_base64(part)
                        part.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(attachment)}"')
                        msg.attach(part)

                    with smtplib.SMTP("smtp.gmail.com", 587) as server:
                        server.ehlo()
                        server.starttls()
                        server.ehlo()
                        server.login(email, config["app_password"])
                        server.send_message(msg)

                    with lock:
                        sent_count += 1

                    time.sleep(random.uniform(0.3, 0.45))

                except Exception as e:
                    err_msg = f"Email #{i+1}: {type(e).__name__} - {str(e)}"
                    print(err_msg)
                    with lock:
                        errors.append(err_msg)

                    if "535" in str(e) or "auth" in str(e).lower() or "quota" in str(e).lower():
                        QTimer.singleShot(0, lambda: QMessageBox.warning(parent, "Error", "Login or limit issue. Check console."))
                        with lock:
                            should_stop = True
                        break

        finally:
            QTimer.singleShot(0, timer.stop)
            QTimer.singleShot(0, lambda: progress.close())
            QTimer.singleShot(100, lambda: QMessageBox.information(parent, "Done", f"Operation finished.\nSent: {sent_count}/{amount}\nErrors: {len(errors)}"))

    thread = threading.Thread(target=sending_thread_func, daemon=True)
    thread.start()

    def on_cancel():
        nonlocal should_stop
        with lock:
            should_stop = True
        QTimer.singleShot(0, timer.stop)
        QTimer.singleShot(0, lambda: progress.close())

    progress.canceled.connect(on_cancel)

    progress.canceled.connect(on_cancel)
def ping_tool(parent=None):
    APP_ICON = QIcon("images/icon.ico")

                         
    host, ok = QInputDialog.getText(parent, "Ping ip adress", "Enter IP or Hostname:")
    if not ok or not host.strip():
        return

    host = host.strip()

    try:
                                       
        param = "-n" if platform.system().lower()=="windows" else "-c"
        command = ["ping", param, "4", host]             

        result = subprocess.run(command, capture_output=True, text=True, timeout=10)
        output = result.stdout.strip() if result.returncode == 0 else result.stderr.strip()

                                
        dialog = QDialog(parent)
        dialog.setWindowTitle(f"Ping Results: {host}")
        dialog.setWindowIcon(APP_ICON)
        dialog.setFixedSize(500, 300)

        layout = QVBoxLayout()
        label = QLabel(output)
        label.setWordWrap(True)
        layout.addWidget(label)

        copy_btn = QPushButton("Copy Results")
        layout.addWidget(copy_btn)
        copy_btn.clicked.connect(lambda: QApplication.clipboard().setText(output))

        dialog.setLayout(layout)
        dialog.exec()

    except Exception as e:
        msg = QMessageBox(QMessageBox.Icon.Critical, "Ping Error", f"Ping failed:\n{e}")
        msg.setWindowIcon(APP_ICON)
        msg.exec()
        
def file_shredder(log_list):
    from PyQt6.QtWidgets import QFileDialog, QMessageBox
    import os
    import random

                        
    file_path, _ = QFileDialog.getOpenFileName(None, "Select file to shred")
    if not file_path:
        return

    try:
        file_size = os.path.getsize(file_path)

                                                     
        with open(file_path, "r+b") as f:
            for i in range(3):
                f.seek(0)
                f.write(os.urandom(file_size))
                f.flush()
                os.fsync(f.fileno())
        
                                  
        os.remove(file_path)

        log_list.addItem(f"[✓] Shredded: {file_path}")
        log_list.scrollToBottom()
        QMessageBox.information(None, "File Shredder", f"File shredded successfully:\n{file_path}")

    except Exception as e:
        log_list.addItem(f"[!] Error shredding file: {e}")
        log_list.scrollToBottom()
        QMessageBox.critical(None, "File Shredder Error", f"Could not shred file:\n{e}")

MAGIC = b"AESGCM1"
def ip_lookup(parent=None):
    APP_ICON = QIcon("images/icon.ico")


    ip, ok = QInputDialog.getText(parent, "IP Lookup", "Enter IP address:")
    if not ok or not ip.strip():
        return

    ip = ip.strip()


    try:
        ipaddress.ip_address(ip)
    except ValueError:
        msg = QMessageBox(QMessageBox.Icon.Warning, "Invalid IP", "Please enter a valid IP address.")
        msg.setWindowIcon(APP_ICON)
        msg.exec()
        return

    try:
        response = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
        data = response.json()

        if data.get("status") != "success":
            raise Exception("Lookup failed")

        info_text = (
            f"IP: {data.get('query')}\n\n"
            f"Country: {data.get('country')}\n"
            f"Region: {data.get('regionName')}\n"
            f"City: {data.get('city')}\n"
            f"ZIP: {data.get('zip')}\n"
            f"ISP: {data.get('isp')}\n"
            f"Organization: {data.get('org')}\n"
            f"Timezone: {data.get('timezone')}\n"
            f"Latitude: {data.get('lat')}\n"
            f"Longitude: {data.get('lon')}"
        )


        dialog = QDialog(parent)
        dialog.setWindowTitle("IP Information")
        dialog.setWindowIcon(APP_ICON)
        dialog.setFixedSize(400, 320)

        layout = QVBoxLayout()

        label = QLabel(info_text)
        label.setWordWrap(True)
        layout.addWidget(label)

        copy_btn = QPushButton("Copy Info")
        layout.addWidget(copy_btn)

        def copy_info():
            QApplication.clipboard().setText(info_text)

        copy_btn.clicked.connect(copy_info)

        dialog.setLayout(layout)
        dialog.exec()

    except Exception as e:
        msg = QMessageBox(QMessageBox.Icon.Critical, "Error", f"Lookup failed:\n{e}")
        msg.setWindowIcon(APP_ICON)
        msg.exec()
           
def derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=200_000,
    )
    return kdf.derive(password.encode())

        
def encrypt_in_place(path: str, password: str):
    with open(path, "rb") as f:
        data = f.read()
    salt = os.urandom(16)
    nonce = os.urandom(12)
    key = derive_key(password, salt)
    aesgcm = AESGCM(key)
    ciphertext = aesgcm.encrypt(nonce, data, None)
    with open(path, "wb") as f:
        f.write(MAGIC + salt + nonce + ciphertext)

def decrypt_in_place(path: str, password: str):
    with open(path, "rb") as f:
        data = f.read()
    if not data.startswith(MAGIC):
        raise ValueError("File is not encrypted or is corrupted")
    salt = data[7:23]
    nonce = data[23:35]
    ciphertext = data[35:]
    key = derive_key(password, salt)
    aesgcm = AESGCM(key)
    plaintext = aesgcm.decrypt(nonce, ciphertext, None)
    with open(path, "wb") as f:
        f.write(plaintext)

def encryptor(log_list: QListWidget):
    choice, ok = QInputDialog.getItem(None, "Encryptor", "Choose action:", ["Encrypt", "Decrypt"], 0, False)
    if not ok or choice not in ("Encrypt", "Decrypt"):
        return
    password, ok = QInputDialog.getText(None, choice, f"Enter password for {choice.lower()}:")
    if not ok or not password:
        return
    file_path, _ = QFileDialog.getOpenFileName(None, f"Select file to {choice.lower()}")
    if not file_path:
        return
    try:
        if choice == "Encrypt":
            encrypt_in_place(file_path, password)
            log_list.addItem(f"[✓] Encrypted: {file_path}")
            QMessageBox.information(None, "Encryptor", f"File encrypted successfully:\n{file_path}")
        else:
            decrypt_in_place(file_path, password)
            log_list.addItem(f"[✓] Decrypted: {file_path}")
            QMessageBox.information(None, "Encryptor", f"File decrypted successfully:\n{file_path}")
    except Exception as e:
        log_list.addItem(f"[!] Error: {e}")
        QMessageBox.critical(None, "Encryptor Error", f"An error occurred:\n{e}")

def clear_logs(log_list):
    log_list.clear()

               
def apply_dark_red_theme(app):
    app.setStyleSheet("""
        QWidget { background-color:#0f0f0f; color:#e6e6e6; font-family:Segoe UI; }
        QTabWidget::pane { border:1px solid #222; background:#121212; }
        QTabBar::tab { background:#1b1b1b; padding:8px; margin:2px; border-radius:6px; }
        QTabBar::tab:selected { background:#8b0000; color:white; }
        QPushButton { background:#8b0000; border:none; padding:8px; border-radius:8px; color:white; }
        QPushButton:hover { background:#b30000; }
        QPushButton:pressed { background:#5a0000; }
        QListWidget { background:#111; border:1px solid #222; border-radius:6px; }
        QListWidget::item:selected { background:#8b0000; color:white; }
        QListWidget::item:focus { outline: none; }
        QComboBox,QLineEdit { background:#1a1a1a; border:1px solid #333; padding:5px; border-radius:6px; }
        QLabel { color:white; }
    """)

                            
def password_generator(log_list):
    from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QSlider, QPushButton, QLineEdit, QApplication
    from PyQt6.QtCore import Qt

    dialog = QDialog()
    dialog.setWindowTitle("Password Generator")
    dialog.setFixedSize(300, 180)

    layout = QVBoxLayout()

    label = QLabel("Password length: 16")
    layout.addWidget(label)

    slider = QSlider(Qt.Orientation.Horizontal)
    slider.setMinimum(8)
    slider.setMaximum(64)
    slider.setValue(16)
    slider.setStyleSheet("""
        QSlider::groove:horizontal {
            border: 1px solid #222;
            height: 8px;
            background: #1a1a1a;
            border-radius: 4px;
        }
        QSlider::handle:horizontal {
            background: #8b0000;
            border: 1px solid #b30000;
            width: 18px; height: 18px; margin: -5px 0; border-radius: 9px;
        }
        QSlider::sub-page:horizontal { background: #8b0000; border-radius:4px; }
        QSlider::add-page:horizontal { background: #333; border-radius:4px; }
    """)
    layout.addWidget(slider)
    slider.valueChanged.connect(lambda val: label.setText(f"Password length: {val}"))

    password_field = QLineEdit()
    password_field.setReadOnly(True)
    layout.addWidget(password_field)

    generate_btn = QPushButton("Generate")
    layout.addWidget(generate_btn)

    copy_btn = QPushButton("Copy")
    layout.addWidget(copy_btn)

    def generate_password():
        length = slider.value()
        chars = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(chars) for _ in range(length))
        password_field.setText(password)
        log_list.addItem("[✓] Password generated")
        log_list.scrollToBottom()

    def copy_password():
        QApplication.clipboard().setText(password_field.text())
        log_list.addItem("[✓] Password copied")
        log_list.scrollToBottom()

    generate_btn.clicked.connect(generate_password)
    copy_btn.clicked.connect(copy_password)

    dialog.setLayout(layout)
    dialog.exec()

         
def create_privacy():
    import json
    from PyQt6.QtGui import QPixmap

    tab = QWidget()
    main_layout = QHBoxLayout()

    sidebar_layout = QVBoxLayout()
    content_layout = QVBoxLayout()


    log_list = QListWidget()
    content_layout.addWidget(QLabel("Logs:"))
    content_layout.addWidget(log_list)


    encrypt_btn = QPushButton("Encrypt / Decrypt")
    encrypt_btn.setIcon(QIcon("images/encrypt.png"))
    encrypt_btn.setIconSize(QSize(24, 24))
    encrypt_btn.clicked.connect(lambda: encryptor(log_list))
    sidebar_layout.addWidget(encrypt_btn)

    password_btn = QPushButton("Password Generator")
    password_btn.setIcon(QIcon("images/password.png"))
    password_btn.setIconSize(QSize(24, 24))
    password_btn.clicked.connect(lambda: password_generator(log_list))
    sidebar_layout.addWidget(password_btn)
    
    shred_btn = QPushButton("Secure File Shredder")
    shred_btn.setIcon(QIcon("images/shred.png"))
    shred_btn.setIconSize(QSize(24, 24))
    shred_btn.clicked.connect(lambda: file_shredder(log_list))
    sidebar_layout.addWidget(shred_btn)
    
                         

    
    clear_btn = QPushButton("Clear Session Logs")
    clear_btn.setIcon(QIcon("images/clear.png"))
    clear_btn.setIconSize(QSize(24, 24))
    clear_btn.clicked.connect(lambda: log_list.clear())
    sidebar_layout.addWidget(clear_btn)

    reset_btn = QPushButton("Remove user/pass")
    reset_btn.setIcon(QIcon("images/username.png"))
    reset_btn.setIconSize(QSize(24, 24))

    def reset_user_pass():
        config_path = os.path.join(os.getcwd(), "config.json")                  
        config = {"user": "lol", "password": "lol"}
        with open(config_path, "w") as f:
            json.dump(config, f)
        log_list.addItem("[✓] User and password removed")
        log_list.scrollToBottom()

    reset_btn.clicked.connect(reset_user_pass)
    sidebar_layout.addWidget(reset_btn)
    
                         
                         
    stream_layout = QHBoxLayout()
    stream_label = QLabel("Stream-Proof:")
    stream_layout.addWidget(stream_label)
    
    stream_switch = QPushButton()
    stream_switch.setCheckable(True)
    stream_switch.setFixedSize(40, 20)                
    stream_switch.setStyleSheet("""
        QPushButton {
            background: #3a3a3a;
            border: 2px solid #1a1a1a;
            border-radius: 10px;
        }
        QPushButton:checked {
            background: #8b0000;
        }
    """)
    stream_switch.toggled.connect(lambda checked: toggle_stream_proof(checked, log_list))
    stream_layout.addWidget(stream_switch)
    
                                   
    ghost_label = QLabel()
    ghost_pixmap = QPixmap("images/ghost.png")
    ghost_pixmap = ghost_pixmap.scaled(20, 20, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
    ghost_label.setPixmap(ghost_pixmap)
    stream_layout.addWidget(ghost_label)
    
    stream_layout.addStretch()
    
    sidebar_layout.addLayout(stream_layout)

    time_label = QLabel()
    time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    sidebar_layout.addWidget(time_label)


    logo_label = QLabel()
    pixmap = QPixmap("images/icon.ico")
    pixmap = pixmap.scaled(80, 80, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
    logo_label.setPixmap(pixmap)
    logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    sidebar_layout.addWidget(logo_label)

    sidebar_layout.addStretch()


    timer = QTimer(time_label)
    timer.timeout.connect(lambda: time_label.setText(QTime.currentTime().toString("hh:mm:ss AP")))
    timer.start(1000)
    time_label.setText(QTime.currentTime().toString("hh:mm:ss AP"))


    main_layout.addLayout(sidebar_layout, 1)
    main_layout.addLayout(content_layout, 3)
    tab.setLayout(main_layout)

    return tab



BROWSER_PATHS = {
    "Chrome": r"%LOCALAPPDATA%\Google\Chrome\User Data\Default\Cookies",
    "Edge": r"%LOCALAPPDATA%\Microsoft\Edge\User Data\Default\Cookies",
    "Firefox": r"%APPDATA%\Mozilla\Firefox\Profiles",
    "Brave": r"%LOCALAPPDATA%\BraveSoftware\Brave-Browser\User Data\Default\Cookies",
    "Opera": r"%APPDATA%\Opera Software\Opera Stable\Cookies"
}

def clear_browser_cookies(log_list):
    for browser, path in BROWSER_PATHS.items():
        real_path = os.path.expandvars(path)
        if browser == "Firefox":
            if os.path.exists(real_path):
                profiles = [f for f in os.listdir(real_path) if os.path.isdir(os.path.join(real_path,f))]
                removed=False
                for prof in profiles:
                    cookie_file = os.path.join(real_path, prof, "cookies.sqlite")
                    if os.path.exists(cookie_file):
                        try: os.remove(cookie_file); removed=True
                        except PermissionError: log_list.addItem(f"[!] Close Firefox before clearing cookies")
                if removed: log_list.addItem("[✓] Firefox cookies cleared")
            else: log_list.addItem("[!] Firefox not found")
        else:
            if os.path.exists(real_path):
                try: os.remove(real_path)
                except PermissionError: log_list.addItem(f"[!] Close {browser} before clearing cookies")
                else: log_list.addItem(f"[✓] {browser} cookies cleared")
            else: log_list.addItem(f"[!] {browser} not found")

def clear_temp_files(log_list):
    temp_dir = os.path.expandvars(r"%TEMP%")
    deleted_count=0
    for item in os.listdir(temp_dir):
        path_item=os.path.join(temp_dir,item)
        try:
            if os.path.isfile(path_item): os.remove(path_item)
            else: shutil.rmtree(path_item,ignore_errors=True)
            deleted_count+=1
        except Exception: continue
    log_list.addItem(f"[✓] Temp files cleared: {deleted_count} items deleted")

def create_trace_cleaner_tab():
    tab = QWidget()
    layout = QVBoxLayout()

    button_layout=QHBoxLayout()
    cookies_btn = QPushButton("Clear Cookies")
    cookies_btn.setIcon(QIcon("images/cookies.png"))
    cookies_btn.setIconSize(QSize(24,24))
    cookies_btn.clicked.connect(lambda: clear_browser_cookies(log_list))
    button_layout.addWidget(cookies_btn)

    temp_btn = QPushButton("Clear Temp Files")
    temp_btn.setIcon(QIcon("images/temp.png"))
    temp_btn.setIconSize(QSize(24,24))
    temp_btn.clicked.connect(lambda: clear_temp_files(log_list))
    button_layout.addWidget(temp_btn)

    layout.addLayout(button_layout)

    log_list = QListWidget()
    log_list.setStyleSheet("""
        QListWidget::item:selected { background:#8b0000; color:white; }
        QListWidget::item:focus { outline:none; }
    """)
    layout.addWidget(QLabel("Logs:"))
    layout.addWidget(log_list)

    clear_btn = QPushButton("Clear Session Logs")
    clear_btn.setIcon(QIcon("images/clear.png"))
    clear_btn.setIconSize(QSize(24,24))
    clear_btn.clicked.connect(lambda: log_list.clear())
    layout.addWidget(clear_btn)

    tab.setLayout(layout)
    return tab

def toggle_stream_proof(enabled, log_list):
    """Enable or disable stream-proofing - makes window invisible on streams"""
    global STREAM_PROOF_ACTIVE
    
    if platform.system() != "Windows":
        log_list.addItem("[!] Stream-proof only works on Windows")
        return
    
    try:
        import ctypes
        
                                    
        app = QApplication.instance()
        main_window = None
        for widget in app.topLevelWidgets():
            if isinstance(widget, QWidget) and widget.isVisible() and widget.windowTitle() == "Cypheria menu v11.5":
                main_window = widget
                break
        
        if not main_window:
            log_list.addItem("[!] Could not find main window")
            return
        
        hwnd = main_window.winId().__int__()
        
        user32 = ctypes.windll.user32
        WDA_EXCLUDEFROMCAPTURE = 0x00000011
        
        if enabled:
            user32.SetWindowDisplayAffinity(hwnd, WDA_EXCLUDEFROMCAPTURE)
            STREAM_PROOF_ACTIVE = True
            log_list.addItem("[✓] Stream-proof ENABLED - Window invisible on streams")
        else:
            user32.SetWindowDisplayAffinity(hwnd, 0)
            STREAM_PROOF_ACTIVE = False
            log_list.addItem("[✓] Stream-proof DISABLED - Window visible again")
            
    except Exception as e:
        log_list.addItem(f"[!] Stream-proof error: {e}")
def create_emergency_tab():
    tab = QWidget()
    layout = QVBoxLayout()
    layout.addWidget(QLabel("Emergency Placeholder"))
    tab.setLayout(layout)
    return tab

def create_troll():
    tab = QWidget()
    main_layout = QHBoxLayout(tab)
    
             
    sidebar_layout = QVBoxLayout()
    
    spammer_btn = QPushButton("Email Spammer")
    spammer_btn.setIcon(QIcon("images/email.png"))
    spammer_btn.setIconSize(QSize(24, 24))
    spammer_btn.clicked.connect(lambda: email_spammer(tab))
    sidebar_layout.addWidget(spammer_btn)
    
    poison_btn = QPushButton("Data Poisoner")
    poison_btn.setIcon(QIcon("images/poison.png"))
    poison_btn.setIconSize(QSize(24, 24))
    poison_btn.clicked.connect(lambda: data_poisoner(tab))
    sidebar_layout.insertWidget(1, poison_btn)
    
    fake_bsod_btn = QPushButton("Fake Bluescreen")
    fake_bsod_btn.setIcon(QIcon("images/error.png"))
    fake_bsod_btn.setIconSize(QSize(24, 24))
    fake_bsod_btn.clicked.connect(lambda: fake_bluescreen(tab))
    sidebar_layout.insertWidget(3, fake_bsod_btn)
    
    sidebar_layout.addStretch() 
    
    
    credit_label = QLabel("made by hugo <3")
    credit_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    credit_label.setStyleSheet("""
        color: #8b0000; 
        font-size: 14px; 
        font-weight: bold;
        padding: 10px;
    """)
    sidebar_layout.addWidget(credit_label)
    
    content_layout = QVBoxLayout()
    logo_label = QLabel()
    pixmap = QPixmap("images/icon.ico")
    pixmap = pixmap.scaled(80, 80, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
    logo_label.setPixmap(pixmap)
    logo_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)
    content_layout.addWidget(logo_label)
    content_layout.addStretch()
    
    main_layout.addLayout(sidebar_layout, 1)
    main_layout.addLayout(content_layout, 3)
    
    return tab


def create_surveillance():
    tab = QWidget()
    main_layout = QHBoxLayout()                                  
    
                                        
    sidebar_layout = QVBoxLayout()
    
                             
    row1_layout = QHBoxLayout()
    
    ip_btn = QPushButton("IP Lookup")
    ip_btn.setIcon(QIcon("images/ip.png"))  
    ip_btn.setIconSize(QSize(24, 24))
    ip_btn.clicked.connect(lambda: ip_lookup(tab)) 
    row1_layout.addWidget(ip_btn)
    
    ping_btn = QPushButton("Ping Ip Adress")
    ping_btn.setIcon(QIcon("images/ping.png"))
    ping_btn.setIconSize(QSize(24, 24))
    ping_btn.clicked.connect(lambda: ping_tool(tab))
    row1_layout.addWidget(ping_btn)
    
    website_btn = QPushButton("Website Info")
    website_btn.setIcon(QIcon("images/website.png")) 
    website_btn.setIconSize(QSize(24, 24))
    website_btn.clicked.connect(lambda: website_info(tab))
    row1_layout.addWidget(website_btn)
    
    sidebar_layout.addLayout(row1_layout)
    
                            
    row2_layout = QHBoxLayout()
    
    discord_btn = QPushButton("Webhook Tool")
    discord_btn.setIcon(QIcon("images/discord.png"))  
    discord_btn.setIconSize(QSize(24, 24))
    discord_btn.clicked.connect(lambda: discord_webhook_tool(tab))
    row2_layout.addWidget(discord_btn)
    
    games_btn = QPushButton("Play Games")
    games_btn.setIcon(QIcon("images/game.png"))
    games_btn.setIconSize(QSize(24, 24))
    games_btn.clicked.connect(lambda: play_games(tab))
    row2_layout.addWidget(games_btn)
    
    private_btn = QPushButton("Private Browser")
    private_btn.setIcon(QIcon("images/private.png"))
    private_btn.setIconSize(QSize(24, 24))
    private_btn.clicked.connect(lambda: private_browser(tab))
    row2_layout.addWidget(private_btn)
    
    sidebar_layout.addLayout(row2_layout)
    
                       
    row3_layout = QHBoxLayout()
    
    keybind_btn = QPushButton("Hide Keybind")
    keybind_btn.setIcon(QIcon("images/keyboard.png"))
    keybind_btn.setIconSize(QSize(24, 24))
    keybind_btn.clicked.connect(lambda: keybind_selector(tab))
    row3_layout.addWidget(keybind_btn)
    
    essay_btn = QPushButton("Essay Bot")
    essay_btn.setIcon(QIcon("images/essay.png"))
    essay_btn.setIconSize(QSize(24, 24))
    essay_btn.clicked.connect(lambda: essay_bot(tab))
    row3_layout.addWidget(essay_btn)
    
    exit_btn = QPushButton("Exit")
    exit_btn.setIcon(QIcon("images/exit.png"))
    exit_btn.setIconSize(QSize(24, 24))
    exit_btn.setStyleSheet("background: #b30000;")
    exit_btn.clicked.connect(lambda: sys.exit())
    row3_layout.addWidget(exit_btn)
    
    sidebar_layout.addLayout(row3_layout)
    
    sidebar_layout.addStretch()                       
    
    content_layout = QVBoxLayout()
    logo_label = QLabel()
    pixmap = QPixmap("images/icon.ico")                 
    pixmap = pixmap.scaled(80, 80, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
    logo_label.setPixmap(pixmap)
    logo_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)
    content_layout.addWidget(logo_label)
    content_layout.addStretch()  
    
                                 
    main_layout.addLayout(sidebar_layout, 1)   
    main_layout.addLayout(content_layout, 3)   
    tab.setLayout(main_layout)
    
    return tab




              
def main():
    CONFIG_FILE = os.path.join(os.getcwd(), "config.json")
    default_config = {"user": None, "password": None}

    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "w") as f:
            json.dump(default_config, f, indent=4)
        config = default_config
    else:
        try:
            with open(CONFIG_FILE, "r") as f:
                file_content = f.read().strip()
                config = json.loads(file_content) if file_content else default_config
        except:
            config = default_config

    username = config.get("user")
    password = config.get("password")

    app = QApplication(sys.argv)
    
                                 
    download_and_extract_images()
    
    apply_dark_red_theme(app)

    APP_ICON = QIcon("images/icon.ico")

   
    if username is None or password is None:
        dialog = QDialog()
        dialog.setWindowTitle("Create Account")
        dialog.setWindowIcon(APP_ICON)
        dialog.setFixedSize(300, 180)
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Username:"))
        user_input = QLineEdit()
        layout.addWidget(user_input)
        layout.addWidget(QLabel("Password:"))
        pass_input = QLineEdit()
        pass_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(pass_input)
        save_btn = QPushButton("Save")
        layout.addWidget(save_btn)
        dialog.setLayout(layout)

        def save_credentials():
            new_user = user_input.text().strip()
            new_pass = pass_input.text().strip()
            if not new_user or not new_pass:
                msg = QMessageBox(QMessageBox.Icon.Warning, "Error", "Fields cannot be empty!", parent=dialog)
                msg.setWindowIcon(APP_ICON)
                msg.exec()
                return
            with open(CONFIG_FILE, "w") as f:
                json.dump({"user": new_user, "password": new_pass}, f, indent=4)
            dialog.accept()

        save_btn.clicked.connect(save_credentials)
        dialog.exec()

        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
        username = config.get("user")
        password = config.get("password")

   
    if username != "lol" or password != "lol":
        user_input_name, ok1 = QInputDialog.getText(None, "Login Required", "Enter username:")
        if not ok1: sys.exit()
        user_input_pass, ok2 = QInputDialog.getText(None, "Login Required", "Enter password:", QLineEdit.EchoMode.Password)
        if not ok2: sys.exit()
        if user_input_name != username or user_input_pass != password:
            msg = QMessageBox(QMessageBox.Icon.Warning, "Access Denied", "Incorrect username or password!")
            msg.setWindowIcon(APP_ICON)
            msg.exec()
            sys.exit()

 
    window = QWidget()
    window.setWindowTitle("Cypheria menu v11.5")
    window.setGeometry(500, 500, 500, 500)
    window.setWindowIcon(APP_ICON)

    tabs = QTabWidget()
    tabs.addTab(create_privacy(), QIcon("images/privacy.png"), "Privacy")
    tabs.addTab(create_trace_cleaner_tab(), QIcon("images/trace.png"), "Trace Cleaner")
    tabs.addTab(create_surveillance(), QIcon("images/surveillance.png"), "Surveillance")
    tabs.addTab(create_troll(), QIcon("images/troll.png"), "Troll")


    layout = QVBoxLayout()
    layout.addWidget(tabs)
    window.setLayout(layout)
    window.show()
    
                                          
    start_keybind_listener()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()