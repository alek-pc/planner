import sys
from PyQt5 import uic
from PyQt5.QtGui import QPainter, QColor, QBrush, QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QAbstractItemView, \
    QTableWidget
from PyQt5.QtCore import QTimer, Qt, QTime
import sqlite3
import datetime


MONTHS_NAMES = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май',
                'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.InitUi()

    def InitUi(self):
        uic.loadUi('planner_design.ui', self)  # Загружаем дизайн
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)  # запрет на редактирование таблицы
        self.db_con = sqlite3.connect('planner_db.sqlite')
        self.db_cur = self.db_con.cursor()

        self.notice_condition = 0
        self.bt_notices.clicked.connect(self.change_notice_condition)
        self.change_notice_condition()

        self.datetime_now = datetime.datetime.today()

        self.table.cellPressed[int, int].connect(self.cell_pressed)
        self.event_list_ind = 0
        self.load_calendar()

        self.clock = QTimer()
        self.clock.setInterval(1000)
        self.clock.timeout.connect(self.display_clock)
        self.clock.start()

        self.bt_previous_month.clicked.connect(self.previous_month)
        self.bt_next_month.clicked.connect(self.next_month)

        self.bt_add_note.clicked.connect(self.add_note)
        self.bt_del_note.clicked.connect(self.del_note)

        self.bt_add_event.clicked.connect(self.add_event)
        self.bt_del_event.clicked.connect(self.del_event)

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
                self.table.item(i, j).setFont(QFont('Segoe UI', 15, QFont.Bold))
                self.table.item(i, j).setForeground(QBrush(QColor(0, 0, 255)))
                if j > 4:
                    # self.table.item(i, j).setBackground(QColor(200, 0, 0))
                    self.table.item(i, j).setForeground(QBrush(QColor(255, 0, 0)))

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
        if len(hour) == 1:
            hour = '0' + hour
        minute = str(time.minute)
        if len(minute) == 1:
            minute = '0' + minute

        date = datetime.datetime.now().date()
        if time.second % 2:  # моргающее :
            self.time.display(f'{hour}:{minute}')
        else:
            self.time.display(f'{hour} {minute}')

        self.date.setText(f'{date.day} {MONTHS_NAMES[date.month - 1].lower()} {date.year} года')

    # месяц назад
    def previous_month(self):
        self.datetime_now = datetime.date(self.datetime_now.year, self.datetime_now.month, 1)
        self.datetime_now -= datetime.timedelta(days=1)
        self.datetime_now = datetime.date(self.datetime_now.year, self.datetime_now.month, 1)
        self.load_calendar()

    # месяц вперёд
    def next_month(self):
        self.datetime_now = datetime.date(self.datetime_now.year, self.datetime_now.month, 1)
        self.datetime_now += datetime.timedelta(days=31)
        self.datetime_now = datetime.date(self.datetime_now.year, self.datetime_now.month, 1)
        self.load_calendar()

    # добавить заметку
    def add_note(self):
        text = self.t_note.toPlainText().split('\n')  # текст заметки
        title = ' '.join(text[0].split()[1:])  # название заметки
        note = ' '.join(' '.join(text[1:]).split()[1:])  # заметка
        self.db_cur.execute(f"""insert into notes_db(title, text) values('{title}', '{note}')""")
        # добавляем заметку в бд
        self.db_con.commit()  # сохрание изменений

    def del_note(self):
        pass

    def add_event(self):
        text = self.event_text.toPlainText().split('\n')  # текст события

        if len(self.table.selectedItems()) == 1:  # выбран 1 день на календаре
            date = f'{self.table.selectedItems()[0].text()}.{self.datetime_now.month}.{self.datetime_now.year}'
        else:  # выбрано несколько дней
            date = f'{self.table.selectedItems()[0].text()}-{self.table.selectedItems()[-1].text()}.' \
                   f'{self.datetime_now.month}.{self.datetime_now.year}'

        if self.event_mode.currentIndex() == 0:  # напоминание
            title = ' '.join(text[0].split()[1:])  # название события
            event = ' '.join(' '.join(text[1:]).split()[1:])  # событие
            time = self.event_time.time()

            self.db_cur.execute(f"""insert into notices_db(title, text, date, time) 
values('{title}', '{event}', '{date}', '{time.hour()}:{time.minute()}')""")

        elif self.event_mode.currentIndex() == 1:  # свой выходной
            self.db_cur.execute(f"""insert into additional_weekends_db(title, interval) 
            values('{' '.join(text[0].split()[1:])}', '{date}')""")
        else:  # свой праздник
            self.db_cur.execute(f"""insert into personal_holidays_db(title, interval) 
                        values('{' '.join(text[0].split()[1:])}', '{date}')""")
        self.db_con.commit()
        self.cell_pressed()

    def del_event(self):
        event = self.res[self.event_list_ind]  # выбранное событие

        if event in self.res_com_holidays:  # общий праздник удалить нельзя
            self.event_text.setPlainText('Нельзя удалить общий праздник')
        else:
            if event in self.res_per_holidays:
                self.db_cur.execute(f"""delete from personal_holidays_db where title='{event[0]}'
and interval='{event[1]}'""")
            elif event in self.res_additional_weekends:
                self.db_cur.execute(f"""delete from additional_weekends_db where title='{event[0]}'
and interval='{event[1]}'""")
            elif event in self.res_notices:
                self.db_cur.execute(f"""delete from notices_db where title='{event[0]}' 
    and text='{event[1]}' and date='{event[3]}' and time='{event[2]}'""")
            self.db_con.commit()
            self.cell_pressed()

    def cell_pressed(self):  # индекс события
        self.event_text.setPlainText("Название: \nОписание: ")
        self.event_list_ind = 0

        # дата события
        if self.table.currentRow() > 1 and int(self.table.currentItem().text()) < 7:
            date = [str(self.table.currentItem().text()), str((self.datetime_now + datetime.timedelta(days=31)).month),
                    str(self.datetime_now.year)]
        elif self.table.currentRow() == 0 and int(self.table.currentItem().text()) > 20:
            date = [str(self.table.currentItem().text()), str((self.datetime_now - datetime.timedelta(days=20)).month),
                    str(self.datetime_now.year)]
        else:
            date = [str(self.table.currentItem().text()), str(self.datetime_now.month), str(self.datetime_now.year)]

        # данные из бд
        self.res_notices = self.db_cur.execute(f"""select title, text, time, date from notices_db 
where date='{'.'.join(date)}'""").fetchall()

        self.res_per_holidays = self.db_cur.execute(f"""select title, interval from personal_holidays_db 
where interval='{'.'.join(date[:2])}'""").fetchall()

        self.res_additional_weekends = self.db_cur.execute(f"""select title, interval from additional_weekends_db
where interval='{'.'.join(date)}'""").fetchall()

        self.res_com_holidays = self.db_cur.execute(f"""select title, interval from common_holidays_db
where interval='{'.'.join(date[:2])}'""").fetchall()

        if not self.res_notices + self.res_per_holidays + self.res_com_holidays + self.res_additional_weekends:
            self.event_list.clear()
            self.event_list.addItem('Никаких событий не запланировано')
        else:
            self.event_list.clear()

            self.res_com_holidays = sorted(self.res_com_holidays)
            for el in self.res_com_holidays:
                self.event_list.addItem(el[0])

            self.res_per_holidays = sorted(self.res_per_holidays)
            for el in self.res_per_holidays:
                self.event_list.addItem(el[0])

            self.res_additional_weekends = sorted(self.res_additional_weekends)
            for el in self.res_additional_weekends:
                self.event_list.addItem(el[0])

            self.res_notices = sorted(self.res_notices, key=lambda x: int(x[2].split(':')[0]))
            for el in self.res_notices:
                hour = el[2].split(':')[0]
                if len(hour) == 1:
                    hour = '0' + hour

                minute = el[2].split(':')[1]
                if len(minute) == 1:
                    minute = '0' + minute

                self.event_list.addItem(f"{el[0]} - {hour}:{minute}")
            self.event_list.itemSelectionChanged.connect(self.select_event)
            self.res = self.res_com_holidays + self.res_per_holidays + self.res_additional_weekends + self.res_notices

    def display_events(self):
        res = self.res_com_holidays + self.res_per_holidays + self.res_additional_weekends + self.res_notices
        ind = self.event_list_ind
        if ind < len(res):
            if res:
                if res[ind] in self.res_notices:
                    self.event_mode.setCurrentIndex(0)
                    # установка времени как в напоминании
                    self.event_time.show()
                    self.event_time.setTime(QTime(int(res[ind][2].split(':')[0]), int(res[ind][2].split(':')[1])))

                    self.event_text.setPlainText(f"""Название: {res[ind][0]}
Описание: {res[ind][1]}""")  # текст события
                else:
                    self.event_time.hide()
                    if res[ind] in self.res_com_holidays or res[ind] in self.res_per_holidays:
                        self.event_mode.setCurrentIndex(2)
                    elif res[ind] in self.res_additional_weekends:
                        self.event_mode.setCurrentIndex(1)
                    interval = str(res[ind][1])
                    if len(interval.split('.')[0]) == 1:
                        interval = '0' + interval
                    if len(interval.split('.')[1]) == 1:
                        interval = interval[:interval.index('.') + 1] + '0' + interval[interval.index('.') + 1:]

                    self.event_text.setPlainText(f"""Название: {res[ind][0]}
Длится {interval}""")

    def select_event(self):
        if (len(self.event_list.selectedItems()) > 0
                and self.event_list.selectedItems()[0].text() != 'Никаких событий не запланировано'):
            self.event_list_ind = self.event_list.currentRow()
            self.display_events()

    def closeEvent(self, event):
        self.db_cur.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
