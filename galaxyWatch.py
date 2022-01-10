import datetime
import sqlite3
import numpy as np
from typing import List
import matplotlib.pyplot as plt
import matplotlib.dates as md

# select your time windows to plot here
timeWindow = [datetime.datetime(2022, 1, 1, 7, 30), datetime.datetime(2022, 1, 1, 10)]
# timeWindow = [datetime.datetime(2022, 1, 11), datetime.datetime(2022, 1, 12)]


def query_database(table: str):
    con = sqlite3.connect(r"database/GalaxyWatch4.db")
    cur = con.cursor()
    cur.execute("SELECT *"
                "FROM %s "
                "WHERE time BETWEEN ? AND ? "
                "ORDER BY time ASC" % table,
                (timeWindow[0].timestamp(), timeWindow[1].timestamp()))
    rows = cur.fetchall()
    con.close()
    return rows


def plot_steps(plot: plt):
    rows = query_database("steps")
    if len(rows) == 0:
        return
    init_steps = rows[0][1]
    time: List[datetime] = []
    steps: List[int] = []
    for i in rows:
        time.append(datetime.datetime.fromtimestamp(i[0]))
        steps.append(i[1] - init_steps)
    plot.plot(time, steps, '.-', label='Schritte')
    plot.legend()


def plot_pulse(plot: plt):
    pulse_data = query_database("pulse")
    time: List[datetime] = []
    pulse: List[int] = []
    time_outliers: List[datetime] = []
    pulse_outliers: List[int] = []
    for idx, val in enumerate(pulse_data):
        if val[1] == 0 or (
                np.abs(pulse_data[idx - 1][1] - pulse_data[idx][1]) > 30):
            time_outliers.append(datetime.datetime.fromtimestamp(pulse_data[idx][0]))
            pulse_outliers.append(pulse_data[idx][1])
        else:
            time.append(datetime.datetime.fromtimestamp(val[0]))
            pulse.append(val[1])
    plot.plot(time, pulse, label='Puls')
    plot.plot(time_outliers, pulse_outliers, 'x', label='PulseOutliers')
    plot.legend()


def plot_acceleration(plot: plt):
    acc_data = query_database("acceleration")
    time: List[datetime] = []
    acc: List[(int, int, int, int)] = []
    for i in acc_data:
        time.append(datetime.datetime.fromtimestamp(i[0]))
        total = np.linalg.norm([i[1], i[2], i[3]], axis=0)
        acc.append([i[1], i[2], i[3], total])
    plot.plot(time, acc, '.-', label='Acceleration')
    plot.legend()


def plot_data(sensor: str, plot: plt):
    data = query_database(sensor)
    x: List[datetime] = []
    y: List[int] = []
    for i in data:
        x.append(datetime.datetime.fromtimestamp(i[0]))
        y.append(i[1])
    plot.plot(x, y, label=sensor)
    plot.legend()


if __name__ == '__main__':
    fig, axes = plt.subplots(3, 2, sharex=True, gridspec_kw={'hspace': 0, 'wspace': 0})
    # plt.setp(axa.xaxis.get_majorticklabels(), rotation=45)
    plt.xticks(rotation=45)
    fig.suptitle('Galaxy Watch Sensors - morning plus Ski lift')
    plt.xlabel("time")
    # plt.xlim([timeWindow[0], timeWindow[1]])

    plot_pulse(axes[0, 0])
    plot_data('airpressure', axes[1, 0])
    plot_acceleration(axes[2, 0])
    plot_data('battery', axes[0, 1])
    plot_steps(axes[1, 1])

    axes[0, 1].yaxis.tick_right()
    axes[1, 1].yaxis.tick_right()
    axes[2, 1].yaxis.tick_right()
    xfmt = md.DateFormatter('%d - %H:%M')
    plt.gca().xaxis.set_major_formatter(xfmt)
    plt.tight_layout()
    #plt.savefig("Galaxy Sensoren Skilift.pdf")
    plt.show()
