import tkinter as tk
import requests
from threading import Thread

URLS = [
    "https://github.com/",
    "https://www.binance.com/en",
    "https://tomtit.tomsk.ru/",
    "https://jsonplaceholder.typicode.com/",
    "https://moodle.tomtit-tomsk.ru/",
]

def get_status(code):
    if code == 200:
        return "доступен"
    if code == 403:
        return "вход запрещен"
    if code == 404:
        return "не найден"
    if code >= 500:
        return "не доступен"
    return "неизвестно"

def check_urls():
    text_output.delete("1.0", tk.END)
    def worker():
        for url in URLS:
            try:
                response = requests.get(url, timeout=5)
                status = get_status(response.status_code)
                result = f"{url} – {status} – {response.status_code}\n"
            except requests.RequestException:
                result = f"{url} – не доступен – ошибка\n"
            text_output.insert(tk.END, result)
    Thread(target=worker).start()

root = tk.Tk()
root.title("Проверка доступности URL")
root.geometry("700x400")

label = tk.Label(root, text="Нажмите кнопку, чтобы проверить доступность URL:")
label.pack(pady=10)

check_button = tk.Button(root, text="Проверить URL", command=check_urls)
check_button.pack(pady=5)

text_frame = tk.Frame(root)
text_frame.pack(pady=10, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(text_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

text_output = tk.Text(text_frame, wrap=tk.NONE, yscrollcommand=scrollbar.set)
text_output.pack(fill=tk.BOTH, expand=True)
scrollbar.config(command=text_output.yview)

root.mainloop()