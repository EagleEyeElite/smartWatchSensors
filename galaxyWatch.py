import datetime
import numpy as np
from typing import List
import matplotlib.pyplot as plt
import matplotlib.dates as md
import os
from enum import Enum


class SensorId(Enum):
    PULSE = 21
    ACCELERATION = 1
    AIRPRESSURE = 6
    STEPS = 19
    OK = 231


class PlotType(Enum):
    PULSE = SensorId.PULSE
    ACCELERATION = SensorId.ACCELERATION
    AIRPRESSURE = SensorId.AIRPRESSURE
    STEPS = SensorId.STEPS
    BATTERY = 2


class DataEntry:
    def __init__(self, time: datetime, battery: int, entry_type: SensorId, sensor_data: int or [int, int, int]):
        self.time: datetime = time
        self.battery: int = battery
        self.type: SensorId = entry_type
        self.sensor: int or [int, int, int] = sensor_data

    def __lt__(self, other):
        return self.time < other.time


def get_sensor_data():
    watch_data = []
    directory = os.fsencode('sensorData')
    for file in os.listdir(directory):
        if file.title() == b'Gadgetbridge':
            continue
        for line in open('sensorData/' + os.fsdecode(file), 'r').readlines():
            data = line.replace(',', '.').split()
            sensor_id = SensorId(int(data[0]))
            if sensor_id == SensorId.OK:
                continue
            timestamp = datetime.datetime.utcfromtimestamp(int(data[1]) / 1000)
            battery = int(float(data[5]))
            sensor_data = int(float(data[2]))
            if sensor_id == SensorId.ACCELERATION:
                sensor_data = [int(float(data[2])), int(float(data[3])), int(float(data[4]))]
            watch_data.append(DataEntry(timestamp, battery, sensor_id, sensor_data))
    watch_data.sort()
    return watch_data


def plot_steps(data: List[DataEntry], plot: plt):
    step_data = []
    for i in data:
        if i.type == SensorId.STEPS:
            step_data.append(i)
    init_steps = step_data[0].sensor
    time: List[datetime] = []
    steps: List[int] = []
    for i in step_data:
        time.append(i.time)
        steps.append(i.sensor - init_steps)
    plot.plot(time, steps, '.-', label='Schritte')
    plot.legend()


def plot_pulse(data: List[DataEntry], plot: plt):
    pulse_data = []
    for i in data:
        if i.type == SensorId.PULSE:
            pulse_data.append(i)
    time: List[datetime] = []
    pulse: List[int] = []
    time_outliers: List[datetime] = []
    pulse_outliers: List[int] = []
    for idx, val in enumerate(pulse_data):
        if val.sensor == 0 or (
                np.abs(pulse_data[idx - 1].sensor - pulse_data[idx].sensor) > 30):
            time_outliers.append(pulse_data[idx].time)
            pulse_outliers.append(pulse_data[idx].sensor)
        else:
            time.append(val.time)
            pulse.append(val.sensor)
    plot.plot(time, pulse, label='Puls')
    plot.plot(time_outliers, pulse_outliers, 'x', label='PulseOutliers')
    plot.legend()


def plot_acceleration(data: List[DataEntry], plot: plt):
    acc_data = []
    for i in data:
        if i.type == SensorId.ACCELERATION:
            acc_data.append(i)
    time: List[datetime] = []
    acc: List[int, int, int, int] = []
    for i in acc_data:
        time.append(i.time)
        total = np.linalg.norm(i.sensor)
        acc.append([*i.sensor, total])
    plot.plot(time, acc, '.-', label='Acceleration')
    plot.legend()


def plot_data(data: List[DataEntry], sensor: PlotType, plot: plt):
    x: List[datetime] = []
    y: List[int] = []
    if sensor == PlotType.ACCELERATION:
        y: List[int, int, int] = []
    for i in data:
        if sensor == PlotType.BATTERY:
            x.append(i.time)
            y.append(i.battery)
            continue
        if i.type == sensor.value:
            x.append(i.time)
            y.append(i.sensor)
    plot.plot(x, y, label=sensor.name)
    plot.legend()


if __name__ == '__main__':
    # timeWindow = [datetime.datetime(2020, 1, 1), datetime.datetime(2024, 1, 1)]
    timeWindow = [datetime.datetime(2022, 1, 1, 6, 30), datetime.datetime(2022, 1, 1, 9)]
    watch_data = get_sensor_data()
    watch_data = [i for i in watch_data if timeWindow[0] < i.time < timeWindow[1]]
    fig, axes = plt.subplots(3, 2, sharex=True, gridspec_kw={'hspace': 0, 'wspace': 0})
    # plt.setp(axa.xaxis.get_majorticklabels(), rotation=45)
    plt.xticks(rotation=45)
    fig.suptitle('Galaxy Watch Sensors - morning plus Ski lift')
    plt.xlabel("time")
    # plt.xlim([timeWindow[0], timeWindow[1]])
    plot_pulse(watch_data, axes[0, 0])
    # plot_data(watch_data, PlotType.PULSE, axes[0, 0])
    plot_data(watch_data, PlotType.AIRPRESSURE, axes[1, 0])
    plot_acceleration(watch_data, axes[2, 0])
    # plot_data(watch_data, PlotType.ACCELERATION, axes[2, 0])
    plot_data(watch_data, PlotType.BATTERY, axes[0, 1])
    plot_steps(watch_data, axes[1, 1])
    # plot_data(watch_data, PlotType.STEPS, axes[1, 1])
    axes[0, 1].yaxis.tick_right()
    axes[1, 1].yaxis.tick_right()
    axes[2, 1].yaxis.tick_right()
    xfmt = md.DateFormatter('%d - %H:%M')
    plt.gca().xaxis.set_major_formatter(xfmt)
    plt.tight_layout()
    plt.savefig("Galaxy Sensoren Skilift.pdf")
    plt.show()
