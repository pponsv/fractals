import numpy as np
import matplotlib.pyplot as plt
from . import mandelbrot_f as mb
from PIL import Image

COLORMAP = plt.get_cmap("magma")


def get_ax_size(ax):
    bbox = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    width, height = bbox.width, bbox.height
    width *= fig.dpi
    height *= fig.dpi
    return width, height


def update(fig, ax, cbar):
    # global cbar
    xlim = ax.get_xlim()
    x0 = xlim[0]
    xlim = xlim - x0
    ylim = ax.get_ylim()
    y0 = ylim[0]
    ylim = ylim - y0
    xr, yr = get_ax_size(ax)
    x = np.linspace(*xlim, int(xr), dtype=np.float64)
    y = np.linspace(*ylim, int(yr), dtype=np.float64)
    out = method(x + x0, y + y0, c, iters)
    out = out / np.max(out)
    print(x.shape, y.shape, out.shape)
    ax.clear()
    maps = ax.pcolorfast(x + x0, y + y0, np.log10(out.T), cmap=COLORMAP)
    cbar.update_normal(maps)
    fig.canvas.draw()


def on_press(event):
    update(fig, ax, cbar)


def plot_interactive():
    global fig, ax, cbar, c, COLORMAP, iters
    x = np.linspace(-1.5, 1.5, 2560)
    y = np.linspace(-1.5, 1.5, 1620)
    out = method(x, y, c, iters)
    fig, ax = plt.subplots(1, 1)
    # cmap = plt.get_cmap('gray')
    # COLORMAP = plt.get_cmap("plasma")
    maps = ax.pcolorfast(x, y, np.log10(out.T), cmap=COLORMAP)
    cbar = fig.colorbar(maps)
    ax.axis("equal")
    fig.canvas.mpl_connect("button_release_event", on_press)
    fig.canvas.mpl_connect("key_press_event", enter_press)
    plt.show()


def enter_press(event):
    if event.key == "enter":
        save_toimage()


def save_toimage():
    global iters, fig, ax, cbar, c, COLORMAP, out, img, res_save_x, res_save_y
    print(COLORMAP)
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    resx, resy = res_fact * res_save_x, res_fact * res_save_y
    # x = np.linspace(*xlim, resx)
    y = np.linspace(*ylim, resy)
    dy = y[1] - y[0]
    xmean = (xlim[1] + xlim[0]) / 2
    print(f"XMEAN: {xmean}")
    x = np.linspace(xmean - dy * (resx - 1) / 2, xmean + dy * (resx - 1) / 2, resx)
    print(x)
    print(y)
    out = method(x, y, c, iters)
    out = np.flip(out, axis=1)
    out = out / np.max(out)
    out = np.log10(out.T)
    out[out == -np.inf] = 0
    print(out.min(), out.max())
    out = (out - out.min()) / (np.max(out) - np.min(out))
    out = COLORMAP(out)
    print(out.min(), out.max())
    out = np.uint8(255 * out)
    print(f"SHAPE: {out.shape}")
    print(out.min(), out.max())
    # fact = 255
    # out = (255 / fact) * (fact * (out - out.min()) / (out.max() - out.min()))
    img = Image.fromarray((out[:, :, :3]))
    # img = Image.fromarray(out, 'L')
    img.save("../tmp.png")
    # plt.figure()
    # plt.imshow(img, cmap='gray')
    # plt.show()
    # print('done')
    # fig, ax = plt.subplots(1,1)
    # cmap = plt.get_cmap('gray')
    # maps = ax.pcolorfast(x, y, np.log10(out.T), cmap=cmap)
    # ax.axis('equal')
    # plt.show()


# method = mb.julia

if __name__ == "__main__":
    mb.fractals.pow = 2.0
    mb.fractals.fac = 0.5
    method = mb.fractals.mandelbrot_new
    # method = mb.fractals.julia

    mult = 4
    res = 500
    res_save_x, res_save_y = 3440, 1440
    res_fact = 2
    black_and_white = False
    iters = 1000
    c = 0.3 - 0.443j  # Extremadamente denso
    c = 0.3 - 0.44j  #
    c = 0.234 - 0.63j
    c = (0.34849278179090426+0.02295392259871587j) # Muy bonito en Julia
    # c = 0+0j

    plot_interactive()
    print(img)
    # plot_toimage()
    # cmap = plt.get_cmap('gray')

    # resx, resy = 2560, 1620

    # iters = 1000

    # x = np.linspace(-1.5, 1.5, resx)
    # y = np.linspace(-1.5, 1.5, resy)

    # c = 0.22j - 1

    # t0 = thread_time_ns()
    # out = method(x, y, c, iters)
    # print(1e-9*(thread_time_ns()-t0))

    # fig, ax = plt.subplots(1,1)
    # maps = ax.pcolorfast(x, y, np.log10(out.T), cmap=cmap)
    # cbar = fig.colorbar(maps)
    # ax.axis('equal')

    plt.show()
