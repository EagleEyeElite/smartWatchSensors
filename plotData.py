import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as md
import galaxyWatch as Galaxy
import miBand as Band


if __name__ == '__main__':
    # Ski day: Galaxy Watch
    # timeWindow = [datetime.datetime(2022, 1, 1, 7, 30), datetime.datetime(2022, 1, 1, 10)]
    # Ski day Mi Band:
    # timeWindow = [datetime.datetime(2022, 1, 2, 7, 30), datetime.datetime(2022, 1, 2, 20)]

    # test day with both
    timeWindow = [datetime.datetime(2022, 1, 12, 9), datetime.datetime(2022, 1, 12, 12)]

    # Plot Styles
    plt.style.use('seaborn')
    plt.rcParams['axes.linewidth'] = 1
    plt.rcParams['axes.edgecolor'] = 'gray'
    plt.rcParams['lines.linewidth'] = 1
    fig, axes = plt.subplots(3, 2, sharex=True, gridspec_kw={'hspace': 0, 'wspace': 0.02})
    fig.autofmt_xdate(rotation=45)
    xfmt = md.DateFormatter('%d - %H:%M')
    plt.gca().xaxis.set_major_formatter(xfmt)

    fig.suptitle('Galaxy and Mi Band Sensors')
    fig.supxlabel('time')

    Galaxy.plot_pulse(axes[0, 0], timeWindow)
    Band.plot_pulse(axes[0, 0], timeWindow)
    axes[0, 0].set_ylim(50, 180)
    axes[0, 0].legend()
    Galaxy.plot_data('airpressure', axes[1, 0], timeWindow)
    axes[1, 0].legend()
    Galaxy.plot_acceleration(axes[2, 0], timeWindow)
    axes[2, 0].legend()
    Galaxy.plot_data('battery', axes[0, 1], timeWindow)
    Band.plot_battery(axes[0, 1], timeWindow)
    axes[0, 1].set_ylim(0, 100)
    axes[0, 1].legend()
    Galaxy.plot_steps(axes[1, 1], timeWindow)
    Band.plot_steps(axes[1, 1], timeWindow)
    axes[1, 1].legend()
    Band.plot_raw_kind(axes[2, 1], timeWindow)
    Band.plot_raw_intensity(axes[2, 1], timeWindow)
    axes[2, 1].legend()

    axes[0, 1].yaxis.tick_right()
    axes[1, 1].yaxis.tick_right()
    axes[2, 1].yaxis.tick_right()

    #plt.savefig("Galaxy Sensoren Skilift.pdf")
    plt.show()
