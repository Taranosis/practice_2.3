import tkinter as tk
from tkinter import simpledialog, messagebox
import requests

class GitHubApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("GitHub Viewer")
        self.geometry("700x500")

        self.text = tk.Text(self, wrap="word")
        self.text.pack(expand=True, fill="both")

        btn_frame = tk.Frame(self)
        btn_frame.pack(fill="x")

        tk.Button(btn_frame, text="Профиль пользователя", command=self.show_profile).pack(side="left")
        tk.Button(btn_frame, text="Список репозиториев", command=self.show_repos).pack(side="left")
        tk.Button(btn_frame, text="Поиск репозитория", command=self.search_repo).pack(side="left")

        self.github_user = ""

    def request_json(self, url, params=None):
        try:
            r = requests.get(url, params=params, timeout=5)
            if r.status_code == 404:
                messagebox.showerror("Ошибка", "Пользователь или репозиторий не найден")
                return None
            if r.status_code != 200:
                messagebox.showerror("Ошибка", f"Не удалось получить данные ({r.status_code})")
                return None
            return r.json()
        except requests.RequestException as e:
            messagebox.showerror("Ошибка", f"Ошибка запроса: {e}")
            return None

    def ask_user(self):
        if not self.github_user:
            user = simpledialog.askstring("GitHub User", "Введите имя пользователя GitHub").strip()
            if not user:
                messagebox.showerror("Ошибка", "Имя пользователя не может быть пустым")
                return False
            self.github_user = user
        return True

    def show_profile(self):
        if not self.ask_user():
            return
        profile_url = f"https://api.github.com/users/{self.github_user}"
        data = self.request_json(profile_url)
        if data:
            self.text.delete("1.0", "end")
            self.text.insert("end", "--- Профиль пользователя ---\n")
            self.text.insert("end", f"Имя: {data.get('name')}\n")
            self.text.insert("end", f"Ссылка: {data.get('html_url')}\n")
            self.text.insert("end", f"Количество репозиториев: {data.get('public_repos')}\n")
            self.text.insert("end", f"Количество подписок: {data.get('following')}\n")
            self.text.insert("end", f"Количество подписчиков: {data.get('followers')}\n")

    def show_repos(self):
        if not self.ask_user():
            return
        repos_url = f"https://api.github.com/users/{self.github_user}/repos"
        repos = self.request_json(repos_url)
        if repos is not None:
            self.text.delete("1.0", "end")
            self.text.insert("end", "--- Репозитории ---\n")
            if not repos:
                self.text.insert("end", "У пользователя нет репозиториев\n")
            for repo in repos:
                self.text.insert("end", f"Название: {repo.get('name')}\n")
                self.text.insert("end", f"Ссылка: {repo.get('html_url')}\n")
                self.text.insert("end", f"Язык: {repo.get('language')}\n")
                self.text.insert("end", f"Видимость: {repo.get('visibility') or 'public'}\n")
                self.text.insert("end", f"Ветка по умолчанию: {repo.get('default_branch')}\n")
                self.text.insert("end", "-"*40 + "\n")

    def search_repo(self):
        query = simpledialog.askstring("Поиск репозитория", "Введите название репозитория").strip()
        if not query:
            return
        params = {"q": query}
        data = self.request_json("https://api.github.com/search/repositories", params=params)
        if data is not None:
            items = data.get("items", [])
            self.text.delete("1.0", "end")
            self.text.insert("end", f"--- Результаты поиска для '{query}' ---\n")
            if not items:
                self.text.insert("end", "Репозитории не найдены\n")
            for repo in items:
                self.text.insert("end", f"Название: {repo.get('name')}\n")
                self.text.insert("end", f"Ссылка: {repo.get('html_url')}\n")
                self.text.insert("end", f"Описание: {repo.get('description')}\n")
                self.text.insert("end", "-"*40 + "\n")

if __name__ == "__main__":
    app = GitHubApp()
    app.mainloop()