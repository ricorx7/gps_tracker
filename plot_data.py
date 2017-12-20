import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import os
from datetime import datetime
from geopy.distance import vincenty

#style.use('fivethirtyeight')
style.use('seaborn')


def plot_lat_lon_data():
    fig = plt.figure()
    ax1 = fig.add_subplot(1,1,1)

    def animate(i):
        if os.path.exists("gps_pts.txt"):
            graph_data = open('gps_pts.txt', 'r').read()
            lines = graph_data.split('\n')
            xs = []
            ys = []
            for line in lines:
                if len(line) > 1:
                    x, y, ts = line.split(',')
                    xs.append(x)
                    ys.append(y)
            ax1.clear()
            ax1.plot(xs, ys)
            print("plot")

    ani = animation.FuncAnimation(fig, animate, interval=500)
    plt.show()
    print("Start Live Plot")


def plot_distance_data():
    fig = plt.figure()
    ax1 = fig.add_subplot(1,1,1)

    def animate(i):
        if os.path.exists("gps_pts.txt"):
            graph_data = open('gps_pts.txt', 'r').read()
            lines = graph_data.split('\n')
            xs = []
            ys = []
            prev_line = None
            for line in lines:
                if len(line) > 1:
                    if prev_line:
                        calculated_dist, curr_ts = calc_dist(prev_line, line)
                        print("{}, {}, {}".format(calculated_dist, prev_line, line))
                        prev_line = line
                        # Plot the distance traveled based off time
                        xs.append(datetime.now())
                        ys.append(calculated_dist)
                    else:
                        prev_line = line
            ax1.clear()
            ax1.plot(xs, ys)

    ani = animation.FuncAnimation(fig, animate, interval=500)
    plt.show()
    print("Start Live Plot")


def calc_dist(prev_pos, curr_pos):
    prev_lat, prev_lon, prev_ts = prev_pos.split(',')
    curr_lat, curr_lon, curr_ts = curr_pos.split(',')
    #print("{}, {}".format(prev_pos, curr_pos))
    prev_pos_flt = (float(prev_lat), float(prev_lon))
    curr_pos_flt = (float(curr_lat), float(curr_lon))

    return vincenty(prev_pos_flt, curr_pos_flt), curr_ts      # return in meters

