import datetime
import sqlite3
import matplotlib.pyplot as plt


def quick_and_dirty(timestamps):
    for idx, row in enumerate(timestamps):
        hm = list(row)
        hm[0] = datetime.datetime.utcfromtimestamp(hm[0]) + datetime.timedelta(hours=1)
        timestamps[idx] = hm
    return timestamps


def query_database(table: str, column: str, time_window):
    time_window[0] = time_window[0]
    time_window[1] = time_window[1]
    con = sqlite3.connect(r"database/Gadgetbridge")
    cur = con.cursor()
    cur.execute("SELECT TIMESTAMP as T, %s "
                "FROM %s "
                "WHERE T BETWEEN ? AND ? "
                "ORDER BY T ASC" % (column, table),
                (time_window[0].timestamp(), time_window[1].timestamp()))
    rows = quick_and_dirty(cur.fetchall())
    con.close()
    return rows


def plot_steps(plot: plt, time_window):
    data = query_database("MI_BAND_ACTIVITY_SAMPLE", "STEPS", time_window)
    t = []
    steps = []
    steps_so_far = 0
    for point in data:
        steps_so_far += point[1]
        t.append(point[0])
        steps.append(steps_so_far)
    plot.plot(t, steps, label="Mi Band steps", color="brown")


def plot_raw_kind(plot: plt, time_window):
    data = query_database("MI_BAND_ACTIVITY_SAMPLE", "RAW_KIND", time_window)
    t = []
    raw_kind = []
    for point in data:
        t.append(point[0])
        raw_kind.append(point[1])
    plot.plot(t, raw_kind, label="rawKind")


def plot_pulse(plot: plt, time_window):
    data = query_database("MI_BAND_ACTIVITY_SAMPLE", "HEART_RATE", time_window)
    t = []
    pulse = []
    for point in data:
        t.append(point[0])
        pulse.append(point[1])
    plot.plot(t, pulse, '.-', label="Mi Band Pulse")


def plot_raw_intensity(plot: plt, time_window):
    data = query_database("MI_BAND_ACTIVITY_SAMPLE", "RAW_INTENSITY", time_window)
    t = []
    raw_intensity = []
    for point in data:
        t.append(point[0])
        raw_intensity.append(point[1])
    plot.plot(t, raw_intensity, '.-', label="Mi Band raw Intensity")


def plot_battery(plot: plt, time_window):
    data = query_database("BATTERY_LEVEL", "LEVEL", time_window)
    t = []
    battery = []
    for point in data:
        t.append(point[0])
        battery.append(point[1])
    plot.plot(t, battery, '.-', label="Mi Band Battery")
