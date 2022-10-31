import sys
from PyQt5 import uic
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QColorDialog, QTableWidgetItem, QLCDNumber
from PyQt5.QtCore import QTimer
import sqlite3
import datetime

MONTHS_NAMES = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май',
                'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.InitUi()

    def InitUi(self):
        uic.loadUi('calendar_design.ui', self)  # Загружаем дизайн
        self.db_con =sqlite3.connect('calendar_db.db')

        self.notice_condition = 0
        self.bt_notices.clicked.connect(self.change_notice_condition)
        self.change_notice_condition()

        self.datetime_now = datetime.datetime.today()
        self.load_calendar()

        self.clock = QTimer()
        self.clock.setInterval(1000)
        self.clock.timeout.connect(self.display_clock)
        self.clock.start()

        self.bt_date_time_setting.clicked.connect(self.datetime_setting)

        self.bt_previous_month.clicked.connect(self.previous_month)
        self.bt_next_month.clicked.connect(self.next_month)

        self.bt_add_note.clicked.connect(self.add_note)

    def load_calendar(self):
        month_day = datetime.date(self.datetime_now.year, self.datetime_now.month, 1)
        # берём выбранную дату и меняем день на 1 число месяца

        previous_month = self.month_len(month_day - datetime.timedelta(days=1))  # длина предыдущего месяца
        calendar = [*[i for i in range(previous_month - 6, previous_month + 1)][-month_day.weekday():] +
                     [i for i in range(1, self.month_len(month_day) + 1)]]
        # календарь: часть предыдущего месяца + текущий месяц
        if len(calendar) % 7:
            calendar += [i for i in range(1, 7)][:7 - len(calendar) % 7]  # + последняя часть - начало след мес
        calendar = [calendar[x:x + 7] for x in range(0, len(calendar) - 1, 7)]  # распределение по неделям

        # отрисовка календаря
        self.table.setColumnCount(7)
        self.table.setRowCount(0)
        for i, row in enumerate(calendar):
            self.table.setRowCount(self.table.rowCount() + 1)
            for j, elem in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(elem)))
                if j > 4:
                    self.table.item(i, j).setBackground(QColor(255, 0, 0))

        self.calendar_month.setText(f'{MONTHS_NAMES[month_day.month - 1]} {month_day.year}')  # подпись мес год
        if self.table.rowCount() == 6:
            self.table.resize(720, 210)

    def month_len(self, month_day):  # длина месяца
        if ((month_day.month % 2 == 1 and month_day.month < 8)
                or (month_day.month % 2 == 0 and month_day.month > 7)):
            month_len = 31
        else:
            month_len = 30
            if month_day.month == 2:  # февраль
                month_len -= 1
                if month_day.year % 4:  # високосный год
                    month_len -= 1
        return month_len

    # прятки шторки уведомлений
    def change_notice_condition(self):
        if self.notice_condition:
            self.t_notices.show()
        else:
            self.t_notices.hide()
        self.notice_condition = not self.notice_condition

    # показ часы + дата
    def display_clock(self):
        time = datetime.datetime.now().time()
        hour = str(time.hour)
        if len(hour) == 1: hour = '0' + hour
        minute = str(time.minute)
        if len(minute) == 1: minute = '0' + minute

        date = datetime.datetime.now().date()
        if time.second % 2:  # моргающее :
            self.time.display(f'{hour}:{minute}')
        else:
            self.time.display(f'{hour} {minute}')
        day = str(date.day)
        if len(day) == 1: day = '0' + day

        month = str(date.month)
        if len(month) == 1: month = '0' + month
        self.date.setText(f'{day}/{month}/{date.year}')

    def datetime_setting(self):
        pass

    # месяц назад
    def previous_month(self):
        self.datetime_now = datetime.date(self.datetime_now.year, self.datetime_now.month, 1)
        self.datetime_now -= datetime.timedelta(days=31)
        self.datetime_now = datetime.date(self.datetime_now.year, self.datetime_now.month, 1)
        self.load_calendar()

    # месяц вперёд
    def next_month(self):
        self.datetime_now = datetime.date(self.datetime_now.year, self.datetime_now.month, 1)
        self.datetime_now += datetime.timedelta(days=31)
        self.datetime_now = datetime.date(self.datetime_now.year, self.datetime_now.month, 1)
        self.load_calendar()

    def add_note(self):
        cur = self.db_con.cursor()
        cur.execute("""UPDATE notes set title=1""")
        self.db_con.commit()
        cur.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
