import tkinter.filedialog
from ChildWindows import *


class Window:
    def __init__(self, width, height, title):
        self.root = Tk()
        self.root.title(title)
        self.root.geometry(f"{width}x{height}+100+75")
        self.root.resizable(False, False)
        self.displayed_time = StringVar(value="0")
        self.displayed_count = StringVar(value="0.0")
        self.button = None

    def run(self):
        self.draw()
        self.root.mainloop()

    def draw(self):
        self.draw_menu()
        frame = Frame(self.root)
        frame.pack(side=LEFT, anchor=N, padx=10)
        Label(frame, text="Текущее время (с)").pack(pady=(10, 0))
        Entry(frame, width=25, textvariable=self.displayed_time, state=DISABLED).pack()
        Label(frame, text="Общая энергия (Дж)").pack(pady=(10, 0))
        Entry(frame, width=25, textvariable=self.displayed_count, state=DISABLED).pack()
        frame = Frame(self.root)
        frame.pack(side=LEFT, padx=12)
        self.button = Button(frame, width=20, height=10, text="Запуск модели", command=self.start_exec)
        self.button.pack()

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
        print(Config.planets_count)
        for planet in Config.planets:
            print(planet)
        if len(Config.planets) == 0:
            tkinter.messagebox.showerror("Ошибка!", "Сначала необходимо создать систему")
            return
