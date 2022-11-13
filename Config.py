param_values = []
coefficients = []
time = 1000
delta = 1
populations_count = 0


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
    delta = 1


def set_params(buf, buf1, t, d):
    global param_values, coefficients, time, delta
    param_values = buf
    coefficients = buf1
    time = t
    delta = d


# def planets_from_matrix(matrix):
#     """Заполнение массива планет по параметрам матрицы"""
#     global planets
#     planets = []
#     for i in range(planets_count):
#         planets.append(Planet(*matrix[i]))
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
