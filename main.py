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
        bookings = json.load(f)

    if bookings:
        time_slot = bookings[0]
        parts = time_slot.split("-")
        if len(parts) == 2 and all(p.strip().isdigit() for p in parts):
            start, end = map(int, parts)
            now_hour = datetime.datetime.now().hour
            if end <= now_hour:
                bookings = []
                save_bookings(bookings)
        else:
            bookings = []
            save_bookings(bookings)

    return bookings

def save_bookings(bookings):
    with open(FILENAME, "w", encoding="utf-8") as f:
        json.dump(bookings, f, ensure_ascii=False, indent=2)

def book_slot():
    bookings = load_bookings()
    now = datetime.datetime.now()
    current_hour = now.hour

    if bookings:
        code = d.yesno(f"Уже есть бронь на время '{bookings[0]}'.\nХотите изменить её? Это может помешать работе стенда", width=50)
        if code != d.OK:
            d.msgbox("Бронирование не изменено.", width=40)
            return
        code, end_input = d.inputbox(f"Текущая бронь: {bookings[0]}\nВведите новое время окончания (часы, 0 для отмены):")
        if code != d.OK:
            return
            
        end_input = end_input.strip()
        
        if end_input == "0":
            bookings = []
            save_bookings(bookings)
            d.msgbox("Бронь отменена.", width=40)
            return
            
        if not end_input.isdigit():
            d.msgbox("Неверный формат. Введите число часов.", width=50)
            return
            
        end_hour = int(end_input)
        if not (current_hour < end_hour <= 24):
            d.msgbox(f"Введите корректное время окончания (от {current_hour + 1} до 24).", width=50)
            return
            
        new_booking = f"{current_hour}-{end_hour}"
        bookings = [new_booking]
        save_bookings(bookings)
        d.msgbox(f"Бронь изменена на '{new_booking}'.", width=50)
        return

    # Новая бронь
    code, end_input = d.inputbox(f"Текущее время: {current_hour}:00\nВведите время окончания брони (часы):")
    if code != d.OK:
        d.msgbox("Бронирование отменено.", width=40)
        return
        
    end_input = end_input.strip()
    
    if not end_input.isdigit():
        d.msgbox("Неверный формат. Введите число часов.", width=50)
        return
        
    end_hour = int(end_input)
    if not (current_hour < end_hour <= 24):
        d.msgbox(f"Введите корректное время окончания (от {current_hour + 1} до 24).", width=50)
        return
        
    new_booking = f"{current_hour}-{end_hour}"
    bookings.append(new_booking)
    save_bookings(bookings)
    d.msgbox(f"Время '{new_booking}' забронировано.", width=50)

def main():
    while True:
        code, tag = d.menu("Меню:", choices=[
            ("1", "Забронировать/Изменить слот"),
            ("2", "Показать текущую бронь"),
            ("3", "Выход")
        ])
        if code != d.OK or tag == "3":
            break
        if tag == "1":
            book_slot()
        elif tag == "2":
            bookings = load_bookings()
            if bookings:
                d.msgbox("Текущая бронь:\n" + "\n".join(bookings), width=50)
            else:
                d.msgbox("Нет активных броней.", width=40)

if __name__ == "__main__":
    main()