import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json
from datetime import datetime

API_KEY = 'ВАШ_API_КЛЮЧ'  # Замените на свой ключ

class CurrencyConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Currency Converter")

        # Валюты (пример)
        self.currencies = ['USD', 'EUR', 'RUB', 'GBP', 'JPY']

        # Интерфейс
        ttk.Label(root, text="Из:").grid(row=0, column=0, padx=5, pady=5)
        self.from_currency = ttk.Combobox(root, values=self.currencies)
        self.from_currency.current(0)
        self.from_currency.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(root, text="В:").grid(row=1, column=0, padx=5, pady=5)
        self.to_currency = ttk.Combobox(root, values=self.currencies)
        self.to_currency.current(1)
        self.to_currency.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(root, text="Сумма:").grid(row=2, column=0, padx=5, pady=5)
        self.amount_entry = ttk.Entry(root)
        self.amount_entry.grid(row=2, column=1, padx=5, pady=5)

        self.convert_btn = ttk.Button(root, text="Конвертировать", command=self.convert)
        self.convert_btn.grid(row=3, column=0, columnspan=2, pady=10)

        # Таблица истории
        self.history_tree = ttk.Treeview(root, columns=('date', 'from', 'to', 'amount', 'result'), show='headings')
        self.history_tree.heading('date', text='Дата')
        self.history_tree.heading('from', text='Из')
        self.history_tree.heading('to', text='В')
        self.history_tree.heading('amount', text='Сумма')
        self.history_tree.heading('result', text='Результат')
        self.history_tree.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        # Загрузка истории
        self.load_history()

    def convert(self):
        amount_str = self.amount_entry.get()
        from_cur = self.from_currency.get()
        to_cur = self.to_currency.get()

        # Проверка ввода
        if not amount_str.replace('.', '', 1).isdigit():
            messagebox.showerror("Ошибка", "Сумма должна быть положительным числом")
            return
        
        amount = float(amount_str)

        # Запрос к API
        url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/pair/{from_cur}/{to_cur}/{amount}"
        
        try:
            response = requests.get(url)
            data = response.json()
            if data.get('result') == 'success':
                result = data['conversion_result']
                self.show_result(amount, from_cur, to_cur, result)
                self.save_to_history(amount, from_cur, to_cur, result)
            else:
                messagebox.showerror("Ошибка API", data.get('error-type', 'Неизвестная ошибка'))
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось получить данные: {e}")

    def show_result(self, amount, from_cur, to_cur, result):
        messagebox.showinfo("Результат", f"{amount} {from_cur} = {result:.2f} {to_cur}")

    def save_to_history(self, amount, from_cur, to_cur, result):
        entry = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "from": from_cur,
            "to": to_cur,
            "amount": amount,
            "result": result
        }

        try:
            with open("history.json", "r+") as f:
                try:
                    history = json.load(f)
                except json.JSONDecodeError:
                    history = []
                history.append(entry)
                f.seek(0)
                json.dump(history, f, indent=2)
                f.truncate()
            self.load_history()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить историю: {e}")

    def load_history(self):
        for i in self.history_tree.get_children():
            self.history_tree.delete(i)
        
        try:
            with open("history.json", "r") as f:
                history = json.load(f)
                for item in history:
                    self.history_tree.insert('', tk.END, values=(item['date'], item['from'], item['to'], item['amount'], f"{item['result']:.2f}"))
        except (FileNotFoundError, json.JSONDecodeError):
            pass

if __name__ == "__main__":
    root = tk.Tk()
    app = CurrencyConverterApp(root)
    root.mainloop()
