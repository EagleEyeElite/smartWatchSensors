import datetime
import sqlite3
import matplotlib.pyplot as plt
import matplotlib.dates as md

# timeWindow = [datetime.datetime(2022, 1, 2, 6), datetime.datetime(2022, 1, 2, 18)]
timeWindow = [datetime.datetime(2022, 1, 11, 14), datetime.datetime(2022, 1, 12, 18)]


class MiBandDataPoint:
    def __init__(self, time, raw_intensity, steps, raw_kind, heart_rate):
        if heart_rate == 0 or heart_rate == 255:
            heart_rate = None
        self.time = datetime.datetime.utcfromtimestamp(time)
        self.rawIntensity = raw_intensity
        self.steps = steps
        self.rawKind = raw_kind
        self.heartRate = heart_rate

    def __str__(self):
        return \
            "Timestamp: {time}, " \
            "raw intensity: {rInt}, " \
            "steps: {steps}, " \
            "raw kind: {rawKind}, " \
            "heart rate: {hr}". \
            format(time=self.time, rInt=self.rawIntensity, steps=self.steps, rawKind=self.rawKind, hr=self.heartRate)


def query_database():
    conn = sqlite3.connect(r"database/Gadgetbridge")
    cur = conn.cursor()
    cur.execute("SELECT * FROM MI_BAND_ACTIVITY_SAMPLE")
    rows = cur.fetchall()
    conn.close()
    datapoints = []
    steps = 0
    for row in rows:
        if not (timeWindow[0] < datetime.datetime.utcfromtimestamp(row[0]) < timeWindow[1]):
            continue
        steps += row[4]
        data = MiBandDataPoint(row[0], row[3], steps, row[5], row[6])
        datapoints.append(data)
    return datapoints


if __name__ == '__main__':
    datapoints = query_database()
    x = []
    rawKind = []
    steps = []
    heartRate = []
    rawIntensity = []
    for point in datapoints:
        x.append(point.time)
        rawKind.append(point.rawKind)
        steps.append(point.steps)
        heartRate.append(point.heartRate)
        rawIntensity.append(point.rawIntensity)
    fig, ax1 = plt.subplots()
    plt.title("Mi Band")
    plt.xlabel("Zeit")
    plt.ylabel("Stand [%]")
    #plt.xlim([timeWindow[0], timeWindow[1]])
    fig.suptitle('Mi Band - anderer Ski Tag')
    ax2 = ax1.twinx()
    ax1.plot(x, rawKind, label="rawKind")
    ax2.plot(x, steps, label="steps", color="brown")
    ax1.plot(x, heartRate, '.-', label="heartRate")
    ax1.plot(x, rawIntensity, label="rawIntensity")
    plt.xticks(rotation=45)
    xfmt = md.DateFormatter('%d - %H:%M')
    plt.gca().xaxis.set_major_formatter(xfmt)
    fig.legend()
    #plt.savefig("Mi Band anderer Tag Skilift.pdf")
    plt.show()
