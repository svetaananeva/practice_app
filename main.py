import json
import os
import datetime
from dialog import Dialog

d = Dialog()
d.set_background_title("Бронирование компьютера")

FILENAME = "booking.json"

def load_bookings():
    if not os.path.exists(FILENAME):
        return []

    try:
        with open(FILENAME, "r", encoding="utf-8") as f:
            bookings = json.load(f)

        if (
            isinstance(bookings, list)
            and len(bookings) == 2
            and all(isinstance(b, str) for b in bookings)
        ):
            datetime.datetime.fromisoformat(bookings[0])
            datetime.datetime.fromisoformat(bookings[1])
            return bookings
    except Exception:
        pass

    save_bookings([])
    return []

def save_bookings(bookings):
    with open(FILENAME, "w", encoding="utf-8") as f:
        json.dump(bookings, f, ensure_ascii=False, indent=2)

def book_slot():
    bookings = load_bookings()
    now = datetime.datetime.now()

    if bookings:
        start = datetime.datetime.fromisoformat(bookings[0])
        end = datetime.datetime.fromisoformat(bookings[1])

        code = d.yesno(
            f"Уже есть бронь:\nс {start.strftime('%d.%m %H:00')} по {end.strftime('%d.%m %H:00')}.\n"
            "Хотите изменить её? Это может помешать работе стенда!" ,
            width=60
        )
        if code != d.OK:
            d.msgbox("Бронирование не изменено.", width=40)
            return

    # Выбор даты окончания
    code, date_str = d.inputbox("Введите дату окончания (дд.мм):", init=now.strftime("%d.%m"))
    if code != d.OK:
        return

    try:
        end_day, end_month = map(int, date_str.strip().split("."))
        end_date = datetime.datetime(year=now.year, month=end_month, day=end_day)
    except ValueError:
        d.msgbox("Неверный формат даты. Введите в формате дд.мм", width=50)
        return

    # Выбор часа окончания
    code, hour_str = d.inputbox("Введите час окончания (0-23):")
    if code != d.OK:
        return

    if not hour_str.isdigit():
        d.msgbox("Введите целое число часов от 0 до 23.", width=50)
        return

    end_hour = int(hour_str)
    if not (0 <= end_hour <= 23):
        d.msgbox("Час должен быть от 0 до 23.", width=50)
        return

    end_datetime = datetime.datetime(year=now.year, month=end_month, day=end_day, hour=end_hour)

    if end_datetime <= now:
        d.msgbox("Окончание брони должно быть позже текущего времени.", width=50)
        return

    bookings = [now.isoformat(), end_datetime.isoformat()]
    save_bookings(bookings)

    d.msgbox(
        f"Новая бронь создана:\nс {now.strftime('%d.%m %H:00')} по {end_datetime.strftime('%d.%m %H:00')}",
        width=60
    )

def extend_booking():
    bookings = load_bookings()
    if not bookings:
        d.msgbox("Нет текущей брони для продления.", width=50)
        return

    start = datetime.datetime.fromisoformat(bookings[0])
    old_end = datetime.datetime.fromisoformat(bookings[1])

    # Ввод новой даты
    code, date_str = d.inputbox("Введите новую дату окончания (дд.мм):", init=old_end.strftime("%d.%m"))
    if code != d.OK:
        return

    try:
        day, month = map(int, date_str.strip().split("."))
        new_end_date = datetime.datetime(year=start.year, month=month, day=day)
    except Exception:
        d.msgbox("Неверный формат даты.", width=50)
        return

    # Ввод нового часа
    code, hour_str = d.inputbox("Введите час окончания (0–23):", init=str(old_end.hour))
    if code != d.OK:
        return

    if not hour_str.isdigit():
        d.msgbox("Час должен быть числом от 0 до 23.", width=50)
        return

    new_hour = int(hour_str)
    if not (0 <= new_hour <= 23):
        d.msgbox("Час должен быть от 0 до 23.", width=50)
        return

    new_end_datetime = datetime.datetime(year=start.year, month=month, day=day, hour=new_hour)

    if new_end_datetime <= old_end:
        d.msgbox("Новое окончание должно быть позже текущего.", width=60)
        return

    bookings[1] = new_end_datetime.isoformat()
    save_bookings(bookings)

    d.msgbox(
        f"Бронь продлена:\nс {start.strftime('%d.%m %H:00')} по {new_end_datetime.strftime('%d.%m %H:00')}",
        width=60
    )

def main():
    while True:
        code, tag = d.menu("Меню:", choices=[
            ("1", "Забронировать стенд"),
            ("2", "Показать текущую бронь"),
            ("3", "Продлить текущую бронь"),
            ("4", "Выход")
        ], width=50, height=15, menu_height=6)

        if code != d.OK or tag == "4":
            break

        if tag == "1":
            book_slot()
        elif tag == "2":
            bookings = load_bookings()
            if bookings:
                start = datetime.datetime.fromisoformat(bookings[0])
                end = datetime.datetime.fromisoformat(bookings[1])
                d.msgbox(f"Текущая бронь:\nс {start.strftime('%d.%m %H:00')} по {end.strftime('%d.%m %H:00')}", width=60)
            else:
                d.msgbox("Нет активных броней.", width=40)
        elif tag == "3":
            extend_booking()

if __name__ == "__main__":
    main()

