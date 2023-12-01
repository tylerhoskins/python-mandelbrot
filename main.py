import math
import numpy as np
import matplotlib.pyplot as plt


def mandelbrot(c, max_iter):
    z = c
    for n in range(max_iter):
        if abs(z) > 2:
            return n
        z = z * z + c
    return max_iter


def draw_mandelbrot(xmin, xmax, ymin, ymax, width, height, max_iter):
    r1 = np.linspace(xmin, xmax, width)
    r2 = np.linspace(ymin, ymax, height)
    return (
        r1,
        r2,
        np.array([[mandelbrot(complex(r, i), max_iter) for r in r1] for i in r2]),
    )


fig, ax = plt.subplots()

has_ever_interacted = False


def onclick(event):
    global has_ever_interacted
    has_ever_interacted = True
    print(
        "%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f"
        % (
            "double" if event.dblclick else "single",
            event.button,
            event.x,
            event.y,
            event.xdata,
            event.ydata,
        )
    )


def on_xlims_change(axes):
    print("xlims changed to %s" % str(axes.get_xlim()))


def on_ylims_change(axes):
    global has_ever_interacted
    print("ylims changed to %s" % str(axes.get_ylim()))

    if has_ever_interacted:
        print("has interacted")
        has_ever_interacted = False
        x_start, x_end = axes.get_xlim()
        y_start, y_end = axes.get_ylim()

        # Calculate new iterations for mandelbrot based on new zoom:
        original_area = (1 - -2) * (1.5 - -1.5)
        print("original area: ", original_area)

        new_area = (x_end - x_start) * (y_end - y_start)
        print("new area: ", new_area)

        # Rate of change of two areas:
        rate_of_change = new_area / original_area

        new_iterations = math.floor(256 / rate_of_change)
        print("new iterations: ", new_iterations)
        redraw(x_start, x_end, y_start, y_end, 1000, 1000, 256)


def redraw(xmin, xmax, ymin, ymax, width, height, max_iter):
    print("redraw")

    plt.cla()
    d = draw_mandelbrot(xmin, xmax, ymin, ymax, width, height, max_iter)
    plt.imshow(d[2], extent=(xmin, xmax, ymin, ymax))

    # Connect zoom event handlers
    plt.gca().callbacks.connect("xlim_changed", on_xlims_change)
    plt.gca().callbacks.connect("ylim_changed", on_ylims_change)

    # Register button event handlers
    fig = plt.subplots()
    fig.canvas.mpl_connect("button_press_event", onclick)


def draw(xmin, xmax, ymin, ymax, width, height, max_iter):
    d = draw_mandelbrot(xmin, xmax, ymin, ymax, width, height, max_iter)
    plt.imshow(d[2], extent=(xmin, xmax, ymin, ymax))

    # Connect zoom event handlers
    plt.gca().callbacks.connect("xlim_changed", on_xlims_change)
    plt.gca().callbacks.connect("ylim_changed", on_ylims_change)

    plt.show()


# Register button event handlers
cid = fig.canvas.mpl_connect("button_press_event", onclick)

draw(-2.0, 1.0, -1.5, 1.5, 1000, 1000, 256)
