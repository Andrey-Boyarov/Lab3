from tkinter import *

import warnings
import matplotlib.cbook
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

warnings.filterwarnings("ignore", category=matplotlib.cbook.mplDeprecation)

import numpy as np

import matplotlib.pyplot as plt
import math
import random

T = 100
N = 3
a = 0.1
b = 0.1
c = 1
t = 0.0
error = 0
matrix = []
points_matrix = []
plot_array = []


def is_float(value):
    try:
        float(value)
        return True
    except:
        return False


def split_time(Time: float, a: float, N: int):
    t = 0.0
    time_array = []
    while True:
        t += random.expovariate(a) / N
        if t > Time:
            return time_array
        time_array.append(t)


def calls_duration(I: int, b: float):
    dur_array = []
    for i in range(I):
        dur_array.append(random.expovariate(b))
    return dur_array


def get_busy_line(matrix: np.ndarray):
    free_lines = 0
    for i in range(matrix.shape[0]):
        if np.all(matrix[i][:] == 0):
            free_lines += 1
    return matrix.shape[0] - free_lines


def start_exec(t, n, a, beta, c):
    plt.close()
    T = int(t.get())
    N = int(n.get())
    a = float(a.get())
    b = float(beta.get())
    c = int(c.get())
    declined = 0
    t_array = split_time(T, a, N)
    d_array = calls_duration(len(t_array), b)
    if int(erlang.get()) != 0:
        t_array = [x for index, x in enumerate(t_array) if index % int(erlang.get()) == 0]
        d_array = [x for index, x in enumerate(d_array) if index % int(erlang.get()) == 0]
    print(f"Calls number:{len(t_array)}\nDurations number:{len(d_array)}")
    print("Calls starts:", t_array, '\nDurations:', d_array)
    matrix = np.zeros((N, math.ceil(T / 0.1)), dtype=float)
    points_matrix = np.zeros((N, math.ceil(T / 0.1)), dtype=float)
    number = 0
    k = 0
    for i in range(len(t_array)):
        start_index = int(t_array[i] / 0.1)
        end_of_call = t_array[i] + d_array[i]
        end_index = int(end_of_call / 0.1)
        if end_of_call > T:
            end_index = math.ceil(T / 0.1) - 1
        if i == 0:
            for j in range(start_index, end_index + 1):
                matrix[0][j] += 1
                number = 0
        else:
            id = []
            for j in range(start_index, end_index + 1):
                id.append(j)
            flag = False
            for line in range(0, N):
                if np.any(matrix[line][id] != 0):
                    continue
                else:
                    matrix[line][id] += 1
                    number = line
                    flag = True
                    break
            if not flag:
                for line in range(0, N):
                    if np.all(matrix[line][id] < c):
                        matrix[line][id] += 1
                        number = line
                        flag = True
                        break

            if not flag:
                declined += 1
                number = float('nan')
        if number >= 0:
            k += 1
            for j in range(start_index, end_index + 1):
                t = 0
                for i in range(matrix.shape[0]):
                    if matrix[i][j] != 0:
                        t += 1
            print(
                f" Call:{k}\n\tChannel{number + 1}|Start:{start_index}|End:{end_index}|Duration:{end_of_call}|Efficiency:{k / (k + declined)}")
            points_matrix[number][start_index] = number + 1
            ef = k / (k + declined)
            efficiency.set(str(ef))
            disp_count.set(str(k))
            rejected.set((str(declined)))
            points_matrix[number][end_index] = number + 1
    print(f"Declined: {declined}")
    busy_lines = get_busy_line(matrix)
    busy.set(str(busy_lines))
    print(f"Busy: {busy_lines}")
    plot_array = np.linspace(0, T, math.ceil(T / 0.1))
    for i in range(np.shape(matrix)[0]):
        for j in range(np.shape(matrix)[1]):
            if matrix[i][j] == 0:
                matrix[i][j] = float('nan')
            else:
                matrix[i][j] = (i + 1)
            if points_matrix[i][j] == 0:
                points_matrix[i][j] = float('nan')

    for i in range(np.shape(matrix)[0]):
        plt.plot(plot_array, matrix[i][:], c='red')
        plt.scatter(plot_array, points_matrix[i][:], 10,
                    c='red')

    plt.xlabel("Время")
    plt.grid()
    plt.ylabel("Каналы")
    plt.locator_params(axis='x', nbins=20)
    plt.locator_params(axis='y', nbins=N)

    plt.show()


def start_this_exec():
    start_exec(t, n, a, beta, c)


root = Tk()
root.title("LR 3")
root.geometry(f"+100+75")
root.resizable(False, False)
efficiency = StringVar(value="0")

t = StringVar(value=str(T))
a = StringVar(value=str(a))
beta = StringVar(value=str(b))
n = StringVar(value=str(N))
c = StringVar(value=str(c))
erlang = StringVar(value=str(error))

disp_count = StringVar(value='0')
rejected = StringVar(value='0')
busy = StringVar(value='0')
workload = StringVar(value='0')

fig = ax = canvas = None

master_frame = LabelFrame(root, borderwidth=0, highlightthickness=0)
master_frame.pack(padx=5, pady=5, ipadx=5, ipady=5)

frame = Frame(master_frame)
frame.pack(side=TOP, pady=(0, 0))
Label(frame, text="Время моделирования:").pack(side=LEFT, padx=(10, 0))
Entry(frame, width=8, textvariable=t).pack(side=LEFT)
Label(frame, text="Показатель для времени:").pack(side=LEFT, padx=(10, 0))
Entry(frame, width=8, textvariable=a).pack(side=LEFT)
Label(frame, text="Показатель для длительности:").pack(side=LEFT, padx=(10, 0))
Entry(frame, width=8, textvariable=beta).pack(side=LEFT)

frame = Frame(master_frame)
frame.pack(side=TOP, pady=(10, 0))
Label(frame, text="Число линий:").pack(side=LEFT, padx=(10, 0))
Entry(frame, width=8, textvariable=n).pack(side=LEFT)
Label(frame, text="Емкость накопителя:").pack(side=LEFT, padx=(10, 0))
Entry(frame, width=8, textvariable=c).pack(side=LEFT)
Label(frame, text="Параметр Эрланга:").pack(side=LEFT, padx=(10, 0))
Entry(frame, width=8, textvariable=erlang).pack(side=LEFT)

frame = Frame(master_frame)
frame.pack(side=TOP, pady=(10, 0))
Label(frame, text="Число вызовов:").pack(side=LEFT)
Entry(frame, width=8, textvariable=disp_count, state=DISABLED, disabledbackground='green', disabledforeground='white').pack(side=LEFT)
Label(frame, text="Загруженные линии:").pack(side=LEFT, padx=(10, 0))
Entry(frame, width=8, textvariable=busy, state=DISABLED, disabledbackground="green", disabledforeground='white').pack(side=LEFT)
Label(frame, text="Отклоненные вызовы:").pack(side=LEFT, padx=(10, 0))
Entry(frame, width=8, textvariable=rejected, state=DISABLED, disabledbackground="green", disabledforeground='white').pack(side=LEFT)
Label(frame, text="Эффективность:").pack(side=LEFT)
Entry(frame, width=16, textvariable=efficiency, state=DISABLED, disabledbackground="blue", disabledforeground='white').pack(side=LEFT, padx=(10, 0))

master_frame = Frame(root)
master_frame.pack(pady=10)
Button(master_frame, width=10, text="Запуск", command=start_this_exec).pack(side=LEFT, padx=15)

root.mainloop()
