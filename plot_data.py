import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import os

style.use('fivethirtyeight')

def plot_data():
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
                    x, y = line.split(',')
                    xs.append(x)
                    ys.append(y)
            ax1.clear()
            ax1.plot(xs, ys)
            print("plot")

    ani = animation.FuncAnimation(fig, animate, interval=500)
    plt.show()
    print("Start Live Plot")



