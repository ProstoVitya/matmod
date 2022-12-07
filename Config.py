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
        if self.N < 30 and not self.inRedBook:
            self.alpha *= 1.5
            self.inRedBook = True
        elif self.N > 30 and self.inRedBook:
            self.alpha /= 1.5
            self.inRedBook = False
        for obj in objs:
            # if self == obj:
            #     continue
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
