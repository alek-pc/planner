import sys
from PyQt5.QtGui import QColor, QBrush, QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QAbstractItemView, QColorDialog
from PyQt5.QtCore import QTimer, QTime
import sqlite3
import datetime
from constants import *
from planner_design import *
from settings_design import *


class MainWindow(Ui_Window, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.db_con = sqlite3.connect('planner_db.sqlite')
        self.db_cur = self.db_con.cursor()

        self.datetime_now = datetime.datetime.today()

        self.widgets = [self.bt_add_note, self.bt_del_note, self.bt_next_month, self.bt_previous_month,
                        self.bt_settings, self.calendar_month, self.date, self.event_list, self.event_text,
                        self.event_time, self.bt_add_event, self.bt_del_event, self.event_mode, self.label,
                        self.note_text, self.notes_list, self.table, self.time]

        self.settings = self.db_cur.execute("""select * from settings_db""").fetchone()

        self.background_color = self.settings[0]
        self.text_color = self.settings[1]
        self.simple_day_color = self.settings[2]
        self.weekend_color = self.settings[3]
        self.common_holiday_color = self.settings[4]
        self.personal_holiday_color = self.settings[5]
        self.additional_weekend_color = self.settings[6]
        self.notice_color = self.settings[7]

        for widget in self.widgets:
            widget.setStyleSheet(f"""color: {self.text_color};
border: 1px solid {self.text_color}""")

        self.l_item = None
        self.event_list_ind = 0

        self.clock = QTimer()

        self.calendar = None
        self.note_res = None

        self.res = None
        self.res_notices = []
        self.res_per_holidays = []
        self.res_com_holidays = []
        self.res_additional_weekends = []

        self.ex = None

        self.InitUi()

    def InitUi(self):
        # uic.loadUi('planner_design.ui', self)  # Загружаем дизайн

        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)  # запрет на редактирование таблицы

        self.bt_settings.clicked.connect(self.show_settings)

        self.setStyleSheet("QPlainTextEdit { background-color: yellow }")
        self.setStyleSheet(f'background-color: {self.background_color};')

        self.load_calendar()

        self.table.cellPressed[int, int].connect(self.cell_pressed)

        self.clock.setInterval(1000)
        self.clock.timeout.connect(self.display_clock)
        self.clock.start()

        self.bt_previous_month.clicked.connect(self.previous_month)
        self.bt_next_month.clicked.connect(self.next_month)

        self.bt_add_note.clicked.connect(self.add_note)
        self.bt_del_note.clicked.connect(self.del_note)
        self.display_notes()

        self.event_mode.currentIndexChanged.connect(self.event_mode_changed)
        self.bt_add_event.clicked.connect(self.add_event)
        self.bt_del_event.clicked.connect(self.del_event)

        # поздравление с праздниками
        personal_holidays = self.db_cur.execute(f"""select title from personal_holidays_db 
    where interval='{datetime.date.today().day}.{datetime.date.today().month}'""").fetchall()
        if personal_holidays:
            self.event_text.setPlainText(f'Поздравляем Вас с {personal_holidays[0][0]}!!!')

        common_holidays = self.db_cur.execute(f"""select title from common_holidays_db 
            where interval='{datetime.date.today().day}.{datetime.date.today().month}'""").fetchall()
        if common_holidays:
            self.event_text.setPlainText(f'Поздравляем Вас с {common_holidays[0][0]}!!!')

    def load_calendar(self):
        month_day = datetime.date(self.datetime_now.year, self.datetime_now.month, 1)
        # берём выбранную дату и меняем день на 1 число месяца

        previous_month = self.month_len(month_day - datetime.timedelta(days=1))  # длина предыдущего месяца
        self.calendar = [*[i for i in range(previous_month - 6, previous_month + 1)][-month_day.weekday():] +
                          [i for i in range(1, self.month_len(month_day) + 1)]]
        # календарь: часть предыдущего месяца + текущий месяц
        if len(self.calendar) % 7:
            self.calendar += [i for i in range(1, 7)][
                             :7 - len(self.calendar) % 7]  # + последняя часть - начало след мес
        self.calendar = [self.calendar[x:x + 7] for x in
                         range(0, len(self.calendar) - 1, 7)]  # распределение по неделям

        # отрисовка календаря
        self.table.setColumnCount(7)
        self.table.setRowCount(0)

        for i, row in enumerate(self.calendar):
            self.table.setRowCount(self.table.rowCount() + 1)
            for j, elem in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(elem)))
                self.table.item(i, j).setFont(QFont('Segoe UI', 15, QFont.Bold))
                self.table.item(i, j).setForeground(QBrush(QColor(self.simple_day_color)))
                if j > 4:
                    self.table.item(i, j).setForeground(QBrush(QColor(self.weekend_color)))

                if i > 1 and elem < 7:
                    date = [str(elem),
                            str((datetime.datetime(self.datetime_now.year, self.datetime_now.month, 1) +
                                 datetime.timedelta(days=31)).month),
                            str((datetime.datetime(self.datetime_now.year, self.datetime_now.month, 1) +
                                 datetime.timedelta(days=31)).year)]
                elif i == 0 and elem > 20:
                    date = [str(elem),
                            str((datetime.datetime(self.datetime_now.year, self.datetime_now.month, 1) -
                                 datetime.timedelta(days=1)).month),
                            str((datetime.datetime(self.datetime_now.year, self.datetime_now.month, 1) -
                                 datetime.timedelta(days=20)).year)]
                else:
                    date = [str(elem), str(self.datetime_now.month),
                            str(self.datetime_now.year)]

                interval = []
                for x in self.db_cur.execute("""select interval from common_holidays_db""").fetchall():
                    interval += [str(y) for y in str(x[0]).split()]
                if '.'.join(date[:2]) in interval:
                    self.table.item(i, j).setForeground(QBrush(QColor(self.common_holiday_color)))

                interval = []
                for x in self.db_cur.execute("""select interval from personal_holidays_db""").fetchall():
                    interval += [str(y) for y in str(x[0]).split()]
                if '.'.join(date[:2]) in interval:
                    self.table.item(i, j).setForeground(QBrush(QColor(self.personal_holiday_color)))

                interval = []
                for x in self.db_cur.execute("""select interval from additional_weekends_db""").fetchall():
                    interval += [str(y) for y in str(x[0]).split()]
                if '.'.join(date) in interval:
                    self.table.item(i, j).setForeground(QBrush(QColor(self.personal_holiday_color)))

                interval = []
                for x in self.db_cur.execute("""select date from notices_db""").fetchall():
                    interval += [str(y) for y in str(x[0]).split()]
                if '.'.join(date) in interval:
                    self.table.item(i, j).setForeground(QBrush(QColor(self.notice_color)))

        self.calendar_month.setText(f'{MONTHS_NAMES[month_day.month - 1]} {month_day.year}')  # подпись мес год

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
        text = self.note_text.toPlainText().split('\n')  # текст заметки
        title = ' '.join(text[0].split()[1:])  # название заметки
        note = ' '.join(' '.join(text[1:]).split()[1:])  # заметка
        self.db_cur.execute(f"""insert into notes_db(title, text) values('{title}', '{note}')""")
        # добавляем заметку в бд
        self.db_con.commit()  # сохрание изменений
        self.display_notes()

        self.note_text.setPlainText('Название: \nЗаписка: ')

    def display_notes(self):
        self.notes_list.clear()
        self.note_res = sorted(self.db_cur.execute(f"""select title, text from notes_db""").fetchall())
        for el in self.note_res:
            self.notes_list.addItem(el[0])
        self.notes_list.itemSelectionChanged.connect(self.note_item_changed)

    def note_item_changed(self):
        self.note_text.setPlainText(f"""Название: {self.note_res[self.notes_list.currentRow()][0]}
Запись: {self.note_res[self.notes_list.currentRow()][1]}""")

    def del_note(self):
        self.db_cur.execute(f"""delete from notes_db where title='{self.note_res[self.notes_list.currentRow()][0]}'
and text='{self.note_res[self.notes_list.currentRow()][1]}'""")
        self.db_con.commit()

        self.display_notes()
        self.note_text.setPlainText('Название: \nЗаписка: ')

    def add_event(self):
        text = self.event_text.toPlainText().split('\n')  # текст события

        if len(self.table.selectedItems()) == 1:  # выбран 1 день на календаре
            if self.table.currentRow() > 1 and int(self.table.currentItem().text()) < 7:
                date = [str(self.table.currentItem().text()),
                        str((self.datetime_now + datetime.timedelta(days=31)).month),
                        str((self.datetime_now + datetime.timedelta(days=31)).year)]
            elif self.table.currentRow() == 0 and int(self.table.currentItem().text()) > 20:
                date = [str(self.table.currentItem().text()),
                        str((self.datetime_now - datetime.timedelta(days=20)).month),
                        str((self.datetime_now - datetime.timedelta(days=20)).year)]
            else:
                date = [str(self.table.currentItem().text()), str(self.datetime_now.month), str(self.datetime_now.year)]
        else:  # выбрано несколько дней
            date = []
            for item in self.table.selectedItems():
                if self.table.indexFromItem(item).row() > 1 and int(item.text()) < 7:
                    date.append([str(item.text()),
                                 str((self.datetime_now + datetime.timedelta(days=31)).month),
                                 str((self.datetime_now + datetime.timedelta(days=31)).year)])
                elif self.table.indexFromItem(item).row() == 0 and int(item.text()) > 20:
                    date.append([str(item.text()),
                                 str((self.datetime_now - datetime.timedelta(days=20)).month),
                                 str((self.datetime_now - datetime.timedelta(days=20)).year)])
                else:
                    date.append([str(item.text()), str(self.datetime_now.month),
                                 str(self.datetime_now.year)])

        if self.event_mode.currentIndex() == 0:  # напоминание
            title = ' '.join(text[0].split()[1:])  # название события
            event = ' '.join(' '.join(text[1:]).split()[1:])  # событие
            time = self.event_time.time()

            if len(date[0]) == 3:
                date = ' '.join(['.'.join(i) for i in date])
            else:
                date = '.'.join(date)

            self.db_cur.execute(f"""insert into notices_db(title, text, date, time) 
values('{title}', '{event}', '{date}', '{time.hour()}:{time.minute()}')""")

        elif self.event_mode.currentIndex() == 1:  # свой выходной

            if len(date[0]) == 3:
                date = ' '.join(['.'.join(i) for i in date])
            else:
                date = '.'.join(date)

            self.db_cur.execute(f"""insert into additional_weekends_db(title, interval) 
            values('{' '.join(text[0].split()[1:])}', '{date}')""")
        else:  # свой праздник

            if len(date[0]) == 3:
                date = ' '.join(['.'.join(i[:2]) for i in date])
            else:
                date = '.'.join(date[:2])

            self.db_cur.execute(f"""insert into personal_holidays_db(title, interval) 
                        values('{' '.join(text[0].split()[1:])}', '{date}')""")

        self.db_con.commit()
        self.cell_pressed(list_cond=1)
        self.load_calendar()

    def del_event(self):
        if self.table.currentItem():
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
                self.cell_pressed(list_cond=1)
                self.load_calendar()
        else:
            self.event_text.setPlainText('Не выбрана дата')

    def cell_pressed(self, list_cond=0):  # индекс события
        if self.l_item == self.table.currentItem() and list_cond == 0:
            self.table.currentItem().setSelected(0)
            self.table.setCurrentItem(None)
            self.l_item = None
            self.event_list.clear()

        else:
            self.l_item = self.table.currentItem()
            self.event_text.setPlainText("Название: \nОписание: ")
            self.event_list_ind = 0

            # дата события
            if self.table.currentRow() > 1 and int(self.table.currentItem().text()) < 7:
                date = [str(self.table.currentItem().text()),
                        str((self.datetime_now + datetime.timedelta(days=31)).month),
                        str(self.datetime_now.year)]
            elif self.table.currentRow() == 0 and int(self.table.currentItem().text()) > 20:
                date = [str(self.table.currentItem().text()),
                        str((self.datetime_now - datetime.timedelta(days=20)).month),
                        str(self.datetime_now.year)]
            else:
                date = [str(self.table.currentItem().text()), str(self.datetime_now.month), str(self.datetime_now.year)]

            # данные из бд
            self.res_notices = []
            for notice in self.db_cur.execute(f"""select title, text, time, date from notices_db""").fetchall():
                if '.'.join(date) in str(notice[3]).split():
                    self.res_notices.append(tuple(notice))

            self.res_per_holidays = []
            for holiday in self.db_cur.execute(f"""select title, interval from personal_holidays_db""").fetchall():
                if '.'.join(date[:2]) in str(holiday[1]).split():
                    self.res_per_holidays.append(tuple(holiday))

            self.res_additional_weekends = []
            for holiday in self.db_cur.execute(f"""select title, interval from additional_weekends_db""").fetchall():
                if '.'.join(date) in str(holiday[1]).split():
                    self.res_additional_weekends.append(tuple(holiday))

            self.res_com_holidays = []
            for holiday in self.db_cur.execute(f"""select title, interval from common_holidays_db""").fetchall():
                if '.'.join(date[:2]) in str(holiday[1]).split():
                    self.res_com_holidays.append(tuple(holiday))

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
                self.res = self.res_com_holidays + self.res_per_holidays + self.res_additional_weekends + \
                           self.res_notices

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

    def event_mode_changed(self):
        if self.event_mode.currentIndex() == 0:
            self.event_time.show()
            self.event_text.setGeometry(400, 440, 329, 180)
        else:
            self.event_time.hide()
            self.event_text.setGeometry(400, 410, 329, 210)

    def show_settings(self):
        self.ex = Settings()
        self.ex.show()
        self.close()

    def closeEvent(self, event):
        self.db_cur.close()


class Settings(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.db_con = sqlite3.connect('planner_db.sqlite')
        self.db_cur = self.db_con.cursor()
        self.colors = list(self.db_cur.execute("""select * from settings_db""").fetchone())
        self.btns = None
        self.column_names = ['background_color', 'text_color', 'workday_color', 'weekend_color', 'common_holiday_color',
                             'personal_holiday_color', 'additional_weekend_color', 'notice_color', 'font_type',
                             'font_size']
        self.rbt_checked = 0
        self.ex2 = None
        self.InitUi()

    def InitUi(self):
        self.bt_back.clicked.connect(self.show_main)
        self.btns = [self.bt1, self.bt2, self.bt3, self.bt4, self.bt5, self.bt6, self.bt7, self.bt8]
        for i, bt in enumerate(self.btns):
            bt.setStyleSheet(f'background-color: {self.colors[i]}')
            bt.clicked.connect(self.change_color)
        self.standard.clicked.connect(self.color_standard)

        self.rbt_dark_theme.toggled.connect(self.turn_dark_theme)
        self.rbt_light_theme.toggled.connect(self.turn_light_theme)
        self.check_theme()

    def turn_dark_theme(self):
        if not self.rbt_checked:
            self.db_cur.execute(f"""update settings_db set {', '.join([f"{i} = '{k}'" for i, k
                                                                       in DARK_THEME_COLORS.items()])}""")
            self.db_con.commit()
            self.update_bt_color()

    def turn_light_theme(self):
        if not self.rbt_checked:
            self.db_cur.execute(f"""update settings_db set {', '.join([f"{i} = '{k}'" for i, k
                                                                       in LIGHT_THEME_COLORS.items()])}""")
            self.db_con.commit()
            self.update_bt_color()

    def check_theme(self):
        self.rbt_checked = 1
        colors = list(self.db_cur.execute("""select background_color, text_color from settings_db""").fetchone())
        if (colors[0] == LIGHT_THEME_COLORS['background_color']
                and colors[1] == LIGHT_THEME_COLORS['text_color']):
            self.rbt_light_theme.setChecked(1)
        elif (colors[0] == DARK_THEME_COLORS['background_color']
              and colors[1] == DARK_THEME_COLORS['text_color']):
            self.rbt_dark_theme.setChecked(1)
        else:
            self.rbt_own_theme.setChecked(1)
        self.rbt_checked = 0

    def update_bt_color(self):
        colors = list(self.db_cur.execute("""select * from settings_db""").fetchone())
        for i, bt in enumerate(self.btns):
            bt.setStyleSheet(f'background-color: {colors[i]}')

    def show_main(self):
        self.ex2 = MainWindow()
        self.db_con.close()
        self.ex2.show()
        self.close()

    def color_standard(self):
        self.db_cur.execute(
            f"""update settings_db set {', '.join([f"{i} = '{k}'" for i, k in STANDARD_CALENDAR_COLORS.items()])}""")
        self.db_con.commit()

        self.update_bt_color()

    def change_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.sender().setStyleSheet(f"background-color: '{color.name()}'")

            self.db_cur.execute(f"""update settings_db 
set {self.column_names[self.btns.index(self.sender())]} = '{color.name()}'""")
            self.db_con.commit()

            self.check_theme()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
