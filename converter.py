import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json
import os

# --- 1. Настройки и API ---
API_KEY = "YOUR_API_KEY"  # Замените на ваш ключ
API_URL = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/"

DATA_FILE = "history.json"

# --- Функции работы с данными ---
def load_history():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []

def save_history(history):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=4)

# --- Функции логики приложения ---
def convert_currency():
    from_code = from_currency.get()
    to_code = to_currency.get()
    
    try:
        amount_val = float(amount.get())
        # 4. Проверка корректности ввода
        if amount_val <= 0:
            raise ValueError("Сумма должна быть положительной")
    except ValueError as e:
        messagebox.showerror("Ошибка ввода", str(e))
        return

    status_label.config(text="Загрузка курсов...", fg="blue")
    root.update_idletasks() # Обновляем окно, чтобы показать статус

    try:
        response = requests.get(f"{API_URL}{from_code}")
        response.raise_for_status() # Проверка на ошибки HTTP
        data = response.json()
        
        if data.get('result') != 'success':
            raise Exception(f"Ошибка API: {data.get('error-type', 'Неизвестная ошибка')}")

        rate = data['conversion_rates'].get(to_code)
        if rate is None:
            raise Exception(f"Конвертация из {from_code} в {to_code} недоступна.")

        result = round(amount_val * rate, 2)
        
        # Отображение результата
        result_label.config(text=f"Результат: {result} {to_code}")
        status_label.config(text="Готово", fg="green")
        
        # Сохранение в историю (Шаг 3)
        entry = {
            "from": from_code,
            "to": to_code,
            "amount": amount_val,
            "result": result,
            "rate": rate,
            "date": data['time_last_update_utc']
        }
        history.append(entry)
        save_history(history)
        update_history_list()

    except requests.exceptions.RequestException as e:
        status_label.config(text="Ошибка сети", fg="red")
        messagebox.showerror("Ошибка сети", "Проверьте подключение к интернету.")
    except Exception as e:
        status_label.config(text="Ошибка API", fg="red")
        messagebox.showerror("Ошибка", str(e))

def update_history_list():
    history_listbox.delete(0, tk.END)
    for entry in history:
        text = f"{entry['amount']} {entry['from']} -> {entry['result']} {entry['to']} (Курс: {entry['rate']})"
        history_listbox.insert(tk.END, text)


# --- Инициализация ---
history = load_history()

# --- Создание GUI ---
root = tk.Tk()
root.title("Currency Converter")
root.geometry("600x500")
root.resizable(False, False)
root.configure(bg='#f4f7f6')

# --- Блок конвертации ---
main_frame = tk.Frame(root, bg='#f4f7f6')
main_frame.pack(pady=10, padx=20, fill='x')

tk.Label(main_frame, text="Из:", bg='#f4f7f6').grid(row=0, column=0, padx=5, pady=5, sticky='e')
tk.Label(main_frame, text="В:", bg='#f4f7f6').grid(row=1, column=0, padx=5, pady=5, sticky='e')
tk.Label(main_frame, text="Сумма:", bg='#f4f7f6').grid(row=2, column=0, padx=5, pady=5, sticky='e')

# Списки валют (можно расширить)
CURRENCIES = ["USD", "EUR", "GBP", "JPY", "RUB", "CHF", "AUD", "CAD"]

from_currency = ttk.Combobox(main_frame, values=CURRENCIES, state="readonly")
to_currency = ttk.Combobox(main_frame, values=CURRENCIES, state="readonly")
amount = tk.Entry(main_frame)

from_currency.current(0) # USD по умолчанию
to_currency.current(1)   # EUR по умолчанию

from_currency.grid(row=0, column=1, padx=5, pady=5)
to_currency.grid(row=1, column=1, padx=5, pady=5)
amount.grid(row=2, column=1, padx=5, pady=5)
amount.insert(0, "100")

tk.Button(main_frame, text="⇄ Поменять местами", command=lambda: swap_currencies()).grid(row=1, column=2, padx=10)
tk.Button(root, text="🔄 Конвертировать", command=convert_currency).pack(pady=10)

result_label = tk.Label(root, text="Результат появится здесь", font=('Arial', 12), bg='#f4f7f6')
result_label.pack(pady=5)
status_label = tk.Label(root, text="", bg='#f4f7f6')
status_label.pack(pady=5)

# --- Блок истории ---
history_frame = tk.LabelFrame(root, text="История конвертаций", bg='#f4f7f6', padx=10, pady=10)
history_frame.pack(padx=20, pady=(20, 10), fill='both', expand=True)

history_scrollbar = ttk.Scrollbar(history_frame)
history_scrollbar.pack(side='right', fill='y')

history_listbox = tk.Вот пошаговая инструкция и готовый код для создания приложения **Currency Converter** (Конвертер валют) на Python.

Проект использует внешний API для получения актуальных курсов, сохраняет историю в JSON и управляется через Git.

### 1. Структура проекта

Создайте папку `CurrencyConverter`. Внутри неё будут:
*   `converter.py` — основной файл программы.
*   `history.json` — файл для хранения истории (создается автоматически).
*   `README.md` — описание проекта.

### 2. Код приложения (converter.py)

> **Важное замечание:** Для работы этого кода вам понадобится API-ключ. Инструкция по его получению находится в разделе README ниже.
