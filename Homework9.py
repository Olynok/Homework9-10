import tkinter as tk
from tkinter import ttk
import requests
from bs4 import BeautifulSoup


def get_currency_exchange_rate():
    url = 'https://nbp.pl/en/'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        usd_rate_element = soup.find('td', {'data-table': 'USD'})

        if usd_rate_element:
            span_element = usd_rate_element.find('span', {'class': 'bidi_text'})
            usd_rate = span_element.text.strip() if span_element else None
            return usd_rate

    print(f"Не удалось получить данные о курсе доллара.")
    return None


class CurrencyConverter:
    def __init__(self, exchange_rate):
        self.exchange_rate = exchange_rate

    def convert_to_usd(self, amount):
        return amount / float(self.exchange_rate.replace(',', ''))


class CurrencyConverterGUI:
    def __init__(self, exchange_rate):
        self.converter = CurrencyConverter(exchange_rate)

        self.window = tk.Tk()
        self.window.title("Конвертер валюты")

        self.label = ttk.Label(self.window, text="Введите количество валюты:")
        self.label.grid(row=0, column=0, padx=10, pady=10)

        self.entry = ttk.Entry(self.window)
        self.entry.grid(row=0, column=1, padx=10, pady=10)

        self.convert_button = ttk.Button(self.window, text="Конвертировать", command=self.convert)
        self.convert_button.grid(row=1, column=0, columnspan=2, pady=10)

    def convert(self):
        amount = float(self.entry.get())
        result = self.converter.convert_to_usd(amount)

        result_text = f"{amount} ваша валюты равны {result:.2f} долларам США."
        result_label = ttk.Label(self.window, text=result_text)
        result_label.grid(row=2, column=0, columnspan=2, pady=10)


if __name__ == "__main__":
    exchange_rate = get_currency_exchange_rate()
    if exchange_rate:
        app = CurrencyConverterGUI(exchange_rate)
        app.window.mainloop()
