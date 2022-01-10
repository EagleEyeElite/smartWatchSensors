import sqlite3
import os
from enum import Enum


class SensorId(Enum):
    PULSE = 21
    ACCELERATION = 1
    AIRPRESSURE = 6
    STEPS = 19
    OK = 231


def write_to_database(cur):
    directory = os.fsencode('sensorData')
    for file in os.listdir(directory):
        with open('sensorData/' + os.fsdecode(file), 'r') as f:
            first_line = f.readline().replace(',', '.').split()
            cur.execute("SELECT EXISTS(SELECT 1 FROM battery WHERE time=? LIMIT 1)", (int(int(first_line[1]) / 1000),))
            if cur.fetchone()[0] == 1:
                print("File %s is already in database. Skipping" % os.fsencode(file))
                continue
        for line in open('sensorData/' + os.fsdecode(file), 'r').readlines():
            data = line.replace(',', '.').split()
            sensor_id = SensorId(int(data[0]))
            time = int(int(data[1]) / 1000)
            sensor = int(float(data[2]))
            cur.execute("INSERT INTO battery VALUES (?, ?)", (time, float(data[5])))
            if sensor_id == SensorId.OK:
                continue
            if sensor_id == SensorId.ACCELERATION:
                cur.execute("INSERT INTO acceleration VALUES (?, ?, ?, ?)",
                            (time, float(data[2]), float(data[3]), float(data[4])))
                continue
            if sensor_id == SensorId.PULSE:
                cur.execute("INSERT INTO pulse VALUES (:b, :c)", (time, sensor))
                continue
            if sensor_id == SensorId.STEPS:
                cur.execute("INSERT INTO steps VALUES (?, ?)", (time, sensor))
                continue
            if sensor_id == SensorId.AIRPRESSURE:
                cur.execute("INSERT INTO airpressure VALUES (?, ?)", (time, sensor))
                continue


if __name__ == '__main__':
    con = sqlite3.connect('database/GalaxyWatch4.db')
    cur = con.cursor()
    write_to_database(cur)
    con.commit()
    con.close()
