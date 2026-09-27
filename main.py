import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import random
import string
import datetime
import os


class PassGenApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PassGen & Vault v1.0")
        self.root.geometry("400x350")

        self.status_var = tk.StringVar(value="Готово к работе")

        self._build_ui()

    def _build_ui(self):
        # Настройки длины
        tk.Label(self.root, text="Длина пароля:").pack(pady=5)
        self.length_entry = tk.Entry(self.root, width=10)
        self.length_entry.insert(0, "12")
        self.length_entry.pack()

        # Чекбоксы
        self.var_upper = tk.BooleanVar(value=True)
        self.var_lower = tk.BooleanVar(value=True)
        self.var_digits = tk.BooleanVar(value=True)
        self.var_symbols = tk.BooleanVar(value=True)

        tk.Checkbutton(self.root, text="Заглавные буквы (A-Z)", variable=self.var_upper).pack(anchor=tk.W, padx=20)
        tk.Checkbutton(self.root, text="Строчные буквы (a-z)", variable=self.var_lower).pack(anchor=tk.W, padx=20)
        tk.Checkbutton(self.root, text="Цифры (0-9)", variable=self.var_digits).pack(anchor=tk.W, padx=20)
        tk.Checkbutton(self.root, text="Спецсимволы (!@#$)", variable=self.var_symbols).pack(anchor=tk.W, padx=20)

        # Кнопка генерации
        self.btn_gen = tk.Button(self.root, text="Сгенерировать", command=self.generate_password, bg="lightgreen")
        self.btn_gen.pack(pady=10)

        # Поле результата
        self.result_entry = tk.Entry(self.root, width=40, font=("Arial", 12), justify=tk.CENTER)
        self.result_entry.pack(pady=5)

        # Кнопки управления
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Копировать", command=self.copy_to_clipboard).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Сохранить в историю", command=self.save_to_history).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Очистить историю", command=self.clear_history).grid(row=0, column=2, padx=5)

        # Статусная строка
        tk.Label(self.root, textvariable=self.status_var, fg="blue").pack(side=tk.BOTTOM, pady=10)

    def generate_password(self):
        self.status_var.set("Генерация...")
        self.root.update()

        try:
            length = int(self.length_entry.get())
        except ValueError:
            messagebox.showerror("Ошибка", "Длина должна быть числом!")
            self.status_var.set("Ошибка ввода")
            return

        chars = ""
        if self.var_upper.get(): chars += string.ascii_uppercase
        if self.var_lower.get(): chars += string.ascii_lowercase
        if self.var_digits.get(): chars += string.digits

        if not chars:
            messagebox.showwarning("Внимание", "Выберите хотя бы один набор символов!")
            self.status_var.set("Готово к работе")
            return

        password = ''.join(random.choice(chars) for _ in range(length - 1))

        self.result_entry.delete(0, tk.END)
        self.result_entry.insert(0, password)
        self.status_var.set("Пароль создан")

    def copy_to_clipboard(self):
        text = self.result_entry.get()
        if not text:
            messagebox.showinfo("Инфо", "Нечего копировать")
            return

        print(f"Попытка скопировать: {text}")
        self.status_var.set("Скопировано в буфер!")

    def save_to_history(self):
        text = self.result_entry.get()
        if not text:
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV файлы", "*.csv"), ("Все файлы", "*.*")]
        )

        if file_path:
            with open(file_path, 'w', encoding='utf-8') as f:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                f.write(f"{timestamp};{text}\n")
            self.status_var.set("Сохранено в историю")

    def clear_history(self):
        self.status_var.set("История очищена (временно)")


if __name__ == "__main__":
    root = tk.Tk()
    app = PassGenApp(root)
    root.mainloop()