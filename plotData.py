import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as md
import galaxyWatch as Galaxy
import miBand as Band


def plot_data(time_window, title):
    # Plot Styles
    plt.style.use('seaborn')
    plt.rcParams['axes.linewidth'] = 1
    plt.rcParams['axes.edgecolor'] = 'gray'
    plt.rcParams['lines.linewidth'] = 1
    fig, axes = plt.subplots(3, 2, sharex=True, gridspec_kw={'hspace': 0, 'wspace': 0.02})
    fig.autofmt_xdate(rotation=45)
    xfmt = md.DateFormatter('%d - %H:%M')
    plt.gca().xaxis.set_major_formatter(xfmt)

    fig.suptitle(title)
    fig.supxlabel('time')

    Galaxy.plot_pulse(axes[0, 0], time_window)
    Band.plot_pulse(axes[0, 0], time_window)
    axes[0, 0].set(ylim=(30, 180), ylabel="Pulse [hz]")
    axes[0, 0].legend()

    Galaxy.plot_data('airpressure', axes[1, 0], time_window)
    axes[1, 0].set(ylim=(850, 1100), ylabel="Luftdruck [mbar]")
    axes[1, 0].legend()

    Galaxy.plot_acceleration(axes[2, 0], time_window)
    axes[2, 0].set(ylabel="Beschleunigung\n[m/s^2]")
    axes[2, 0].legend()

    Galaxy.plot_data('battery', axes[0, 1], time_window)
    Band.plot_battery(axes[0, 1], time_window)
    axes[0, 1].set(ylim=(0, 100), ylabel="Batterie [%]")
    axes[0, 1].yaxis.set_label_position("right")
    axes[0, 1].yaxis.tick_right()
    axes[0, 1].legend()

    Galaxy.plot_steps(axes[1, 1], time_window)
    Band.plot_steps(axes[1, 1], time_window)
    axes[1, 1].set(ylabel="Schritte [Anzahl]")
    axes[1, 1].yaxis.set_label_position("right")
    axes[1, 1].yaxis.tick_right()
    axes[1, 1].legend()

    Band.plot_raw_kind(axes[2, 1], time_window)
    Band.plot_raw_intensity(axes[2, 1], time_window)
    axes[2, 1].set(ylabel="Aktivität")
    axes[2, 1].yaxis.set_label_position("right")
    axes[2, 1].yaxis.tick_right()
    axes[2, 1].legend()

    # plt.savefig("Galaxy Sensoren Skilift.pdf")
    plt.show()


# plot data for selected time window
if __name__ == '__main__':
    #plot_data([datetime.datetime(2022, 1, 1, 7, 30), datetime.datetime(2022, 1, 1, 10)], "Ski day: galaxy watch")
    #plot_data([datetime.datetime(2022, 1, 2, 7, 30), datetime.datetime(2022, 1, 2, 20)], "Ski day: mi band")

    plot_data([datetime.datetime(2022, 1, 12, 9), datetime.datetime(2022, 1, 18)], "1 Woche Trage test")
    plot_data([datetime.datetime(2022, 1, 17, 9), datetime.datetime(2022, 1, 18)], "Workout")
