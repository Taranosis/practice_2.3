import tkinter as tk
from tkinter import simpledialog, messagebox
import requests
import json
import os

API_URL = "https://www.cbr-xml-daily.ru/daily_json.js"
SAVE_FILE = "resource/save.json"

if not os.path.exists("resource"):
    os.makedirs("resource")

def read():
    if not os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f)
    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}

def save(data):
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def get_rates():
    try:
        r = requests.get(API_URL, timeout=5)
        r.raise_for_status()
        return r.json().get("Valute", {})
    except requests.RequestException as e:
        messagebox.showerror("Ошибка", f"Не удалось получить курсы: {e}")
        return {}

class CurrencyMonitor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Монитор валют")
        self.geometry("500x400")
        self.rates = {}
        self.groups = read()

        self.text = tk.Text(self, wrap="word")
        self.text.pack(expand=True, fill="both")

        btn_frame = tk.Frame(self)
        btn_frame.pack(fill="x")

        tk.Button(btn_frame, text="Все курсы", command=self.show_all).pack(side="left")
        tk.Button(btn_frame, text="Курс по коду", command=self.show_one).pack(side="left")
        tk.Button(btn_frame, text="Создать группу", command=self.create_group).pack(side="left")
        tk.Button(btn_frame, text="Список групп", command=self.list_groups).pack(side="left")
        tk.Button(btn_frame, text="Добавить валюту в группу", command=self.add_to_group).pack(side="left")
        tk.Button(btn_frame, text="Удалить валюту из группы", command=self.remove_from_group).pack(side="left")
        tk.Button(btn_frame, text="Обновить курсы", command=self.update_rates).pack(side="left")

        self.update_rates()

    def update_rates(self):
        self.rates = get_rates()
        self.text.insert("end", "Курсы обновлены\n")
        self.text.see("end")

    def show_all(self):
        self.text.delete("1.0", "end")
        for code, val in self.rates.items():
            self.text.insert("end", f"{code}: {val['Value']}\n")

    def show_one(self):
        code = simpledialog.askstring("Курс валюты", "Введите код валюты").upper()
        value = self.rates.get(code, {}).get('Value')
        self.text.delete("1.0", "end")
        if value is not None:
            self.text.insert("end", f"{code}: {value}\n")
        else:
            self.text.insert("end", "Валюта не найдена\n")

    def create_group(self):
        name = simpledialog.askstring("Создать группу", "Имя группы").strip()
        if not name:
            return
        if name in self.groups:
            messagebox.showinfo("Инфо", "Группа уже существует")
            return
        self.groups[name] = []
        while True:
            code = simpledialog.askstring("Добавить валюту", "Код валюты (Enter — выход)").upper()
            if not code:
                break
            if code in self.rates:
                if code not in self.groups[name]:
                    self.groups[name].append(code)
            else:
                messagebox.showwarning("Ошибка", "Валюта не найдена")
        save(self.groups)
        messagebox.showinfo("Сохранено", "Группа сохранена")

    def list_groups(self):
        self.text.delete("1.0", "end")
        if not self.groups:
            self.text.insert("end", "Нет групп\n")
        else:
            for n, vals in self.groups.items():
                self.text.insert("end", f"{n}: {vals}\n")

    def add_to_group(self):
        name = simpledialog.askstring("Группа", "Введите имя группы").strip()
        code = simpledialog.askstring("Валюта", "Введите код валюты").upper()
        if name in self.groups and code in self.rates:
            if code not in self.groups[name]:
                self.groups[name].append(code)
                save(self.groups)
                messagebox.showinfo("Добавлено", "Валюта добавлена в группу")
            else:
                messagebox.showinfo("Инфо", "Валюта уже в группе")
        else:
            messagebox.showerror("Ошибка", "Группа или валюта не найдены")

    def remove_from_group(self):
        name = simpledialog.askstring("Группа", "Введите имя группы").strip()
        code = simpledialog.askstring("Валюта", "Введите код валюты").upper()
        if name in self.groups and code in self.groups[name]:
            self.groups[name].remove(code)
            save(self.groups)
            messagebox.showinfo("Удалено", "Валюта удалена из группы")
        else:
            messagebox.showerror("Ошибка", "Группа или валюта не найдены")

if __name__ == "__main__":
    app = CurrencyMonitor()
    app.mainloop()