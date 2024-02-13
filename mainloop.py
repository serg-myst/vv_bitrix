import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
from tkinter import filedialog as fd
from gui import Gui
from datetime import datetime, timedelta
from get_users import get_users_list
from excel import save_to_excel
import os
from tkcalendar import *


class Task:
    root = tk.Tk()

    def __init__(self, catalog):
        ex = Gui(self.root)
        ex.center_window()
        self.root.config(background='#FFFAFA')
        self.catalog = catalog

    def create_widgets(self):
        self.root.grid_columnconfigure(1, weight=1)

        empty_label = tk.Label(self.root,
                               text=f'Выгрузка текущих задач IT-отдела. На дату: {datetime.now().strftime("%d.%m.%Y")}')
        empty_label.config(pady=10, padx=5, bg='#FFFAFA', font=('Arial', 10, 'bold'), fg='#808080', anchor='w')
        empty_label.grid(row=0, column=0, columnspan=3, stick='we')

        myLabel_1 = tk.Label(self.root, text='Каталог выгрузки:', anchor='e')
        myLabel_1.config(bd=2, bg='#FFFAFA', height=1, font=('Arial', 12, 'bold'), width=15, anchor='w', padx=5)
        myLabel_1.grid(row=1, column=0, stick='e')

        myLabel_2 = tk.Label(self.root, text=self.catalog, anchor='e')
        myLabel_2.config(bd=2, bg='#FFFAFA', height=1, anchor=CENTER, fg='#C0C0C0', relief=RIDGE, width=55)
        myLabel_2.grid(row=1, column=1, stick='w')

        empty_label_1 = tk.Label(self.root, text='')
        empty_label_1.config(bg='#FFFAFA')
        empty_label_1.grid(row=1, column=2, ipadx=8)

        btn_file = tk.Button(empty_label_1, text='...')
        btn_file.config(command=lambda button=btn_file: self.get_catalog(myLabel_2), height=1, pady=2, bg='#FFFAFA',
                        bd=3, relief=RAISED)
        btn_file.grid(row=1, column=3)

        style = ttk.Style()
        style.configure('TSeparator', background='grey')

        sep = ttk.Separator(
            master=self.root,
            orient=HORIZONTAL,
            style='TSeparator',
            class_=ttk.Separator
        )

        sep.grid(row=2, column=0, columnspan=3, pady=5, stick="ew", padx=5)

        frame = tk.LabelFrame(self.root, text='Установите период вывода завершенных задач')
        frame.config(bg='#FFFAFA', height=100, padx=25)
        frame.grid(row=3, column=0, columnspan=3, stick="ew", padx=5)

        label_per_start = tk.Label(frame, text='Период с ', anchor='e', bg='#FFFAFA')
        label_per_start.grid(row=3, column=1, pady=25, ipadx=50, stick='e')

        entry_per_start = tk.Label(frame, width=15, justify=CENTER, font=('Arial', 9, 'bold'),
                                   fg='#000000')
        entry_per_start.grid(row=3, column=2, pady=25, padx=5)
        entry_per_start.config(text=(datetime.now() - timedelta(days=7)).strftime("%d.%m.%Y"))

        btn_start = tk.Button(frame, text='...')
        btn_start.config(command=lambda button=btn_start: self.calendar(self.root, entry_per_start))
        btn_start.grid(row=3, column=3, pady=25, padx=5)

        label_per_stop = tk.Label(frame, text='по', anchor='e', bg='#FFFAFA')
        label_per_stop.grid(row=3, column=4, pady=25, stick='e')

        entry_per_stop = tk.Label(frame, width=15, justify=CENTER, font=('Arial', 9, 'bold'),
                                  fg='#000000')
        entry_per_stop.grid(row=3, column=5, pady=25, padx=5)
        entry_per_stop.config(text=datetime.now().strftime("%d.%m.%Y"))

        btn_stop = tk.Button(frame, text='...')
        btn_stop.config(command=lambda button=btn_stop: self.calendar(self.root, entry_per_stop))
        btn_stop.grid(row=3, column=6, pady=25, padx=5)

        empty_label_2 = tk.Label(self.root, text='')
        empty_label_2.config(bg='#FFFAFA')
        empty_label_2.grid(row=4, column=0, columnspan=3, pady=10)

        bt = tk.Button(self.root)
        bt.config(text='Сформировать отчет',
                  command=lambda button=btn_file: self.get_result(self.catalog, empty_label_2, entry_per_start,
                                                                  entry_per_stop), padx=5,
                  pady=7, bd=5, relief=GROOVE)
        bt.grid(row=5, column=0, columnspan=3, stick='e', padx=15)

    def get_result(self, catalog, label, label_date1, label_date2):

        d1 = datetime.strptime(label_date1['text'], '%d.%m.%Y').date()
        d2 = datetime.strptime(label_date2['text'], '%d.%m.%Y').date()

        if d1 > d2:
            label.config(text='Неверно указан период!', fg='#FF0000', anchor='w')
        else:
            if os.path.exists(catalog):
                result_list = get_users_list(d1.strftime('%Y-%m-%d'),
                                             (d2 + timedelta(days=1)).strftime('%Y-%m-%d'))
                save_to_excel(result_list, catalog, label)
            else:
                label.config(text='Ошибка формирования отчета. Выбранный каталог не существует!', fg='#FF0000',
                             anchor='w')

    def get_catalog(self, label):
        name = fd.askdirectory()
        if name:
            self.catalog = name
            label.config(text=name, fg='#000000', anchor='w')

    def grab_date(self, cal, label, window):
        label.config(text=cal.get_date())
        window.destroy()

    def calendar(self, main_window, label):
        window = Tk()
        window.title('calendar')
        window.geometry(f'300x250+{main_window.winfo_x() + 100}+{main_window.winfo_y() + 200}')
        cal = Calendar(window, selectmode='day', year=2024, month=2, day=11, date_pattern="dd.mm.yyyy")
        cal.pack(pady=10)
        btn = Button(window, text='Выбрать')
        btn.config(command=lambda button=btn: self.grab_date(cal, label, window), anchor='n')
        btn.pack()
        window.grab_set()
        window.focus_set()
        window.wait_window()
        window.mainloop()

    def start(self):
        self.create_widgets()
        self.root.mainloop()


if __name__ == '__main__':
    ts = Task(catalog='<<выберите папку>>')
    ts.start()
