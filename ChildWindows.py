import Config
from tkinter import *
import tkinter.messagebox


class Window1:
    def __init__(self, parent, title):
        self.root = Toplevel(parent)
        self.root.title(title)
        self.root.resizable(False, False)
        self.root.attributes('-toolwindow', True)
        self.root.attributes('-topmost', True)

        self.text = StringVar(value="2")
        Label(self.root, text="Число видов: ").grid(row=0, column=0)
        Entry(self.root, width=15, textvariable=self.text).grid(row=0, column=1, pady=10)
        Button(self.root, width=10, text="Ввод", command=self.save).grid(row=1, column=0, columnspan=2)
        self.grab_focus()

    def grab_focus(self):
        self.root.grab_set()
        self.root.focus_set()

    def save(self):
        text = self.text.get()
        if text.isdigit():
            n = int(text)
            if n >= 1:
                Config.default_values(n)
                self.root.destroy()
            else:
                tkinter.messagebox.showerror("Ошибка", "Значение должно быть больше 0")
        else:
            tkinter.messagebox.showerror("Ошибка", "Введенное значение не является числом")


class Window2:
    def __init__(self, parent, title):
        self.root = Toplevel(parent)
        self.root.title(title)
        self.root.attributes('-topmost', True)
        self.root.resizable(False, False)
        self.params = [[StringVar(value=str(Config.param_values[i][j])) for j in range(2)]
                       for i in range(Config.populations_count)]
        self.coefs = [[StringVar(value=str(Config.coefficients[i][j])) for j in range(Config.populations_count)]
                      for i in range(Config.populations_count)]
        self.delta = StringVar(value=str(Config.delta))
        self.t = StringVar(value=str(Config.time))

    def draw(self):
        big_frame = Frame(self.root)
        big_frame.pack(pady=5)
        Button(big_frame, width=10, text="Ввод", command=self.save).pack(side=LEFT, pady=5, padx=5)
        Label(big_frame, text="Шаг дифференцирования:").pack(side=LEFT)
        Entry(big_frame, width=10, textvariable=self.delta).pack(side=LEFT, padx=5)
        Label(big_frame, text="Время моделирования:").pack(side=LEFT)
        Entry(big_frame, width=20, textvariable=self.t).pack(side=LEFT, padx=5)

        big_frame = Frame(self.root)
        big_frame.pack(pady=5)

        frame_part = LabelFrame(big_frame, text="Численность популяции i-го вида и прирост", labelanchor=N)
        frame_part.pack(side=LEFT, padx=15, ipadx=5, ipady=5)

        frame = Frame(frame_part)
        frame.pack()
        Label(frame, width=5, text=str(Config.populations_count), relief=GROOVE).pack(side=LEFT)
        Label(frame, width=14, text="Количество", relief=GROOVE).pack(side=LEFT)
        Label(frame, width=14, text="Прирост", relief=GROOVE).pack(side=LEFT)
        for i in range(Config.populations_count):
            frame = Frame(frame_part)
            frame.pack()
            Label(frame, width=5, text=str(i), relief=GROOVE).pack(side=LEFT)
            for j in range(2):
                Entry(frame, width=16, textvariable=self.params[i][j]).pack(side=LEFT, padx=2)

        frame_part = LabelFrame(big_frame, text="Коэффициенты взаимодействия популяций", labelanchor=N)
        frame_part.pack(side=LEFT, padx=15, ipadx=5, ipady=5)

        frame = Frame(frame_part)
        frame.pack()
        if Config.populations_count == 0:
            Label(frame, width=5, text="", relief=GROOVE).pack(side=LEFT)
            for j in range(2):
                Label(frame, width=14, text="", relief=GROOVE).pack(side=LEFT)
        else:
            Label(frame, width=5, text="", relief=GROOVE).pack(side=LEFT)
            for j in range(Config.populations_count):
                Label(frame, width=14, text=str(j), relief=GROOVE).pack(side=LEFT)
            for i in range(Config.populations_count):
                frame = Frame(frame_part)
                frame.pack()
                Label(frame, width=5, text=str(i), relief=GROOVE).pack(side=LEFT)
                for j in range(Config.populations_count):
                    Entry(frame, width=16, textvariable=self.coefs[i][j]).pack(side=LEFT, padx=2)

        self.grab_focus()

    def grab_focus(self):
        self.root.grab_set()
        self.root.focus_set()

    def save(self):
        t = self.t.get()
        delta = self.delta.get()
        if t.isdigit() and Config.is_float(delta):
            t = int(t)
            delta = float(delta)
            if t > 0 and delta > 0:
                buff = [[0.0] * 2 for i in range(Config.populations_count)]
                for i in range(Config.populations_count):
                    if self.params[i][0].get().isdigit() and Config.is_float(self.params[i][1].get()):
                        buff[i][0] = int(self.params[i][0].get())
                        buff[i][1] = float(self.params[i][1].get())
                    else:
                        tkinter.messagebox.showerror("Ошибка",
                                                     "Введенное значение в Численности и приросте популяции не является корректным")
                        return
                buff1 = [[0.0] * Config.populations_count for i in range(Config.populations_count)]
                for i in range(Config.populations_count):
                    for j in range(Config.populations_count):
                        if Config.is_float(self.coefs[i][j].get()):
                            buff1[i][j] = float(self.coefs[i][j].get())
                        else:
                            tkinter.messagebox.showerror("Ошибка",
                                                         "Введенное значение в Коэффициентах взаимодействия популяций не является корректным")
                            return
            else:
                tkinter.messagebox.showerror("Ошибка", "Значение должно быть больше 0")
                return
        else:
            tkinter.messagebox.showerror("Ошибка", "Введенное значение не является числом")
            return
        Config.set_params(buff, buff1, t, delta)
        self.root.destroy()
