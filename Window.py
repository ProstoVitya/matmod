import tkinter.filedialog
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from ChildWindows import *


class Window:
    def __init__(self, width, height, title):
        self.root = Tk()
        self.root.title(title)
        self.root.geometry(f"+100+75")
        # self.root.resizable(False, False)
        self.displayed_time = StringVar(value="0")
        self.displayed_count = StringVar(value="0.0")
        self.button = self.fig = self.ax = self.canvas = None

    def run(self):
        self.draw()
        self.root.mainloop()

    def draw(self):
        self.draw_menu()
        frame = Frame(self.root)
        frame.pack(side=LEFT, padx=10)
        self.fig = plt.Figure(figsize=(7, 4))
        self.ax = self.fig.add_subplot(111)
        self.fig.subplots_adjust(left=0.06, right=0.975, bottom=0.08, top=0.95)
        self.canvas = FigureCanvasTkAgg(self.fig, frame)
        self.canvas.get_tk_widget().pack()
        self.toolbar = NavigationToolbar2Tk(self.canvas, frame)
        self.canvas._tkcanvas.pack()

        frame = Frame(self.root)
        frame.pack(side=LEFT, anchor=N, padx=10)
        Label(frame, text="Текущее время (с)").pack(pady=(10, 0))
        Entry(frame, width=25, textvariable=self.displayed_time, state=DISABLED).pack()
        Label(frame, text="Число особей (шт)").pack(pady=(10, 0))
        Entry(frame, width=25, textvariable=self.displayed_count, state=DISABLED).pack()
        self.button = Button(frame, width=20, text="Запуск модели", command=self.start_exec)
        self.button.pack(pady=(20, 0))

        # frame = Frame(self.root)
        # frame.pack(side=LEFT, padx=12)
        # self.button = Button(frame, width=20, height=10, text="Запуск модели", command=self.start_exec)
        # self.button.pack()

    def draw_menu(self):
        main_menu = Menu(self.root)

        file_menu = Menu(main_menu, tearoff=0)
        file_menu.add_command(label="Новая система", command=self.create_system)
        file_menu.add_command(label="Сохранить", command=self.save_file)
        file_menu.add_command(label="Открыть", command=self.open_file)
        main_menu.add_cascade(label="Файл", menu=file_menu)

        main_menu.add_command(label="Параметры", command=self.change_params)
        self.root.configure(menu=main_menu)

    def create_system(self):
        Window1(self.root, "Новая система")

    def change_params(self):
        a = Window2(self.root, "Параметры")
        a.draw()

    def open_file(self):
        filename = tkinter.filedialog.askopenfilename(filetypes=(("Text file", ".txt"),))
        if filename:
            Config.read_from_file(filename)

    def save_file(self):
        filename = tkinter.filedialog.asksaveasfilename(defaultextension=".txt", filetypes=(("Text file", "*.txt"),))
        if filename:
            Config.write_to_file(filename)

    def start_exec(self):
        print('\nStarted execution...')
        print(Config.populations_count)
        for i, population in zip(range(Config.populations_count), Config.populations):
            print(i, population)
        if Config.populations_count == 0:
            tkinter.messagebox.showerror("Ошибка!", "Сначала необходимо создать систему")
            return
        self.ax.cla()
        self.ax.set_xlim([0, Config.time])
        self.ax.set_ylim([0, 3 * Config.get_max_N()])
        lines = [self.ax.plot([], [])[0] for _ in range(Config.populations_count)]

        def anim(frame):
            xdata.append(frame)
            n=0
            for i, population in enumerate(Config.populations):
                population.interaction(Config.populations, Config.delta)
                ydata[i].append(population.N)
                lines[i].set_data(xdata, ydata[i])
                n += population.N

            self.displayed_time.set(str(frame))
            self.displayed_count.set(str(n))
            return lines

        xdata = []
        ydata = [[] for _ in range(Config.populations_count)]
        x = np.arange(0, Config.time, Config.delta)
        anim = animation.FuncAnimation(self.fig, func=anim, frames=x, interval=1,
                                       blit=True, repeat=False)
        self.canvas.draw()
