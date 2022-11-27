param_values = []
coefficients = []
time = 1000
delta = 1
populations_count = 0
populations = []


def is_float(value):
    try:
        float(value)
        return True
    except:
        return False


def default_values(n):
    global populations_count, param_values, coefficients, time, delta
    populations_count = n
    param_values = [[0.0] * 2 for i in range(populations_count)]
    for i in range(populations_count):
        param_values[i][0] = 100 * (i + 1)
        param_values[i][1] = -0.01
    param_values[0][1] = 0.01

    coefficients = [[0.0] * populations_count for i in range(populations_count)]
    for i in range(populations_count):
        for j in range(i + 1, populations_count):
            coefficients[i][j] = -0.0001
            coefficients[j][i] = 0.0001
    time = 1000
    delta = 1.0
    populations_from_matrix(param_values)


def set_params(buf, buf1, t, d):
    global param_values, coefficients, time, delta
    param_values = buf
    coefficients = buf1
    time = t
    delta = d
    populations_from_matrix(param_values)


def populations_from_matrix(matrix):
    global populations
    populations = []
    for i in range(populations_count):
        populations.append(Population(i, *matrix[i]))


#
#
# def read_from_file(filename):
#     """Чтение данных из файла"""
#     with open(filename, 'r') as file:
#         first_line = True
#         for line in file:
#             if first_line:
#                 n, t, dt = [int(x) for x in line.split()]
#                 buff = [[0.0] * COLUMNS for i in range(n)]
#                 first_line = False
#                 i = 0
#             else:
#                 line = line.split()
#                 for j in range(COLUMNS - 1):
#                     buff[i][j] = float(line[j])
#                 buff[i][COLUMNS - 1] = line[COLUMNS - 1]
#                 i += 1
#     global planets_count
#     planets_count = n
#     set_params(buff, t, dt, 2)
#
#
# def write_to_file(filename):
#     """Запись данных в файл"""
#     with open(filename, 'w') as file:
#         print(planets_count, time, time_step, file=file)
#         for planet in planets:
#             print(planet, file=file)

class Population:
    def __init__(self, id: int, n: int, alpha: float):
        self.id = id
        self.alpha = alpha
        self.N = n
        self.data = []
        self.inRedBook = False

    def __str__(self):
        return f"{self.alpha} {self.N}"

    def interaction(self, objs, delta):
        f = 0
        if self.N < 50 and not self.inRedBook:
            self.alpha *= 2
            self.inRedBook = True
            print(self.id, 'in a red book')
        elif self.N > 50 and self.inRedBook:
            self.alpha /= 2
            self.inRedBook = False
            print(self.id, 'quit a red book')
        for obj in objs:
            if self == obj:
                continue
            f += coefficients[self.id][obj.id] * self.N * obj.N
        self.N += delta * (self.N * self.alpha + f)
        if self.N < 2:
            self.N = 0


def get_max_N():
    max = 0
    for obj in populations:
        buf = obj.N
        if max < buf:
            max = buf
    return max
