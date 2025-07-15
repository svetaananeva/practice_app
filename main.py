import json
import os
from dialog import Dialog
import datetime

d = Dialog()
d.set_background_title("Бронирование компьютера")

FILENAME = "booking.json"

def load_bookings():
    if not os.path.exists(FILENAME):
        return []
    with open(FILENAME, "r", encoding="utf-8") as f:
        return json.load(f)

def save_bookings(bookings):
    with open(FILENAME, "w", encoding="utf-8") as f:
        json.dump(bookings, f, ensure_ascii=False, indent=2)

def book_slot():
    bookings = load_bookings()

    code, time_input = d.inputbox("Введите время бронирования (например, 10-12):")
    if code != d.OK:
        d.msgbox("Бронирование отменено.", width=40)
        return

    time_input = time_input.strip()

    if not time_input:
        d.msgbox("Пустой ввод недопустим.", width=40)
        return

    parts = time_input.split("-")
    if len(parts) != 2 or not all(p.strip().isnumeric() for p in parts):
        d.msgbox("Неверный формат. Введите часы через тире, например: 10-12", width=50)
        return
    
    now_hour = datetime.datetime.now().hour
    start, end = map(int, parts)
    if not (0 <= start < 24 and 0 < end <= 24 and start < end and end > now_hour):
        d.msgbox("Введите корректный диапазон часов.", width=50)
        return
    

    if time_input in bookings:
        d.msgbox(f"Время '{time_input}' уже занято. Выберите другое.", width=50)
        return

    bookings.append(time_input)
    save_bookings(bookings)
    d.msgbox(f"Время '{time_input}' забронировано.", width=50)

'''def validate_booking():
    bookings = load_bookings()
    valid_bookings = []
    now_hour = datetime.datetime.now().hour
    for i in bookings:
        parts = i.strip().split("-")
        start, end = map(int, parts)
        if 0 <= start < 24 and 0 < end <= 24 and start < end and end > now_hour:
            valid_bookings.append(f"{start}-{end}")'''


def main():
    while True:
        code, tag = d.menu("Меню:", choices=[
            ("1", "Забронировать слот"),
            ("2", "Показать все брони"),
            ("3", "Выход")
        ])
        if code != d.OK or tag == "3":
            break
        if tag == "1":
            book_slot()
        elif tag == "2":
            bookings = load_bookings()
            if bookings:
                d.msgbox("Забронированные слоты:\n" + "\n".join(bookings), width=50)
            else:
                d.msgbox("Нет забронированных слотов.", width=40)

if __name__ == "__main__":
    main()