import datetime
import sqlite3
import numpy as np
from typing import List
import matplotlib.pyplot as plt


def query_database(table: str, time_window):
    con = sqlite3.connect(r"database/GalaxyWatch4.db")
    cur = con.cursor()
    cur.execute("SELECT *"
                "FROM %s "
                "WHERE time BETWEEN ? AND ? "
                "ORDER BY time ASC" % table,
                (time_window[0].timestamp(), time_window[1].timestamp()))
    rows = cur.fetchall()
    con.close()
    return rows


def plot_steps(plot: plt, time_window):
    rows = query_database("steps", time_window)
    if len(rows) == 0:
        return
    init_steps = rows[0][1]
    time: List[datetime] = []
    steps: List[int] = []
    prev_steps = 0
    prev_add = 0
    for i in rows:
        current_steps = i[1] - init_steps + prev_add
        if prev_steps > current_steps:
            prev_add += prev_steps
            init_steps = i[1]
            current_steps += prev_steps
        prev_steps = current_steps
        time.append(datetime.datetime.fromtimestamp(i[0]))
        steps.append(current_steps)
    plot.plot(time, steps, '.-', label='Schritte')


def plot_pulse(plot: plt, time_window):
    pulse_data = query_database("pulse", time_window)
    time: List[datetime] = []
    pulse: List[int] = []
    time_outliers: List[datetime] = []
    pulse_outliers: List[int] = []
    for idx, val in enumerate(pulse_data):
        if val[1] == 0 or np.abs(pulse_data[idx - 1][1] - pulse_data[idx][1]) > 30:
            time_outliers.append(datetime.datetime.fromtimestamp(val[0]))
            pulse_outliers.append(val[1])
        else:
            time.append(datetime.datetime.fromtimestamp(val[0]))
            pulse.append(val[1])
    plot.plot(time_outliers, pulse_outliers, '.', label='Galaxy PulseOutliers')
    plot.plot(time, pulse, label='Galaxy Puls')


def plot_acceleration(plot: plt, time_window):
    acc_data = query_database("acceleration", time_window)
    time: List[datetime] = []
    acc: List[(int, int, int, int)] = []
    for i in acc_data:
        time.append(datetime.datetime.fromtimestamp(i[0]))
        total = np.linalg.norm([i[1], i[2], i[3]], axis=0)
        acc.append([i[1], i[2], i[3], total])
    plot.plot(time, acc, '.-', label='Acceleration', alpha=1)


def plot_data(sensor: str, plot: plt, time_window):
    data = query_database(sensor, time_window)
    x: List[datetime] = []
    y: List[int] = []
    for i in data:
        x.append(datetime.datetime.fromtimestamp(i[0]))
        y.append(i[1])
    plot.plot(x, y, label=sensor)
