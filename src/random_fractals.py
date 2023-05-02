import numpy as np
import matplotlib.pyplot as plt
from . import mandelbrot_f as mb
from matplotlib.colors import Normalize

# from .draw_2d import COLORMAP
from PIL import Image


IMG_PATH = "/home/pedro/.config/i3/mandelbrot/tmp_wallpaper.png"

# COLORMAP = plt.get_cmap("gray")
# COLORMAP.set_bad([1.0, 1.0, 1.0, 1.0])
# COLORMAP.set_over('w')


def get_cmap(name="plasma"):
    COLORMAP = plt.get_cmap(name)
    COLORMAP.set_bad([1.0, 1.0, 1.0, 1.0])
    return COLORMAP


def out_to_image_bw(out, fac=50, impath=IMG_PATH):
    out = np.flip(out, axis=1)
    out = np.log10(1 + out.T)
    out = (255 / fac) * (fac * (out - out.min()) / (out.max() - out.min()))
    img = Image.fromarray(out.astype(np.uint8), "L")
    img.save(impath)


def plot_fractal(x, y, img, cmap="plasma", show=False):
    fig, ax = plt.subplots(1, 1, figsize=[15, 7])
    ax.pcolorfast(x, y, np.log10(img.T), cmap=get_cmap(cmap))
    ax.set(aspect="equal")
    if show:
        plt.show()


def out_to_image_cmap(out, cmap="plasma", impath=IMG_PATH):
    COLORMAP = get_cmap(cmap)
    out = np.flip(out, axis=1)
    out = np.ma.masked_where(out == 0, out)
    out = np.log10(out.T)
    out = (out - np.min(out)) / (np.max(out) - np.min(out))
    out = np.uint8(255 * COLORMAP(out))
    img = Image.fromarray((out[:, :, :3]))
    img.save(impath)


def random_julia_far(resx=3440, resy=1440, max_iter=1000, cmap="gray", impath=IMG_PATH):
    c = 2 * ((0.5 - np.random.rand()) + 1j * (0.5 - np.random.rand()))
    print(c)
    ylim = -2, 2
    y = np.linspace(*ylim, resy)
    dy = y[1] - y[0]
    x = np.linspace(-dy * (resx - 1) / 2, dy * (resx - 1) / 2, resx)
    fractal = mb.fractals.julia(x, y, c, max_iter)
    out_to_image_cmap(fractal, cmap=cmap, impath=impath)


def make_fractal_r0(
    c, max_iter, x0, y0, pixelwidth, method=mb.fractals.julia, resx=500, resy=500
):
    x = np.linspace(
        x0 - pixelwidth * (resx - 1) / 2, x0 + pixelwidth * (resx - 1) / 2, resx
    )
    y = np.linspace(
        y0 - pixelwidth * (resy - 1) / 2, y0 + pixelwidth * (resy - 1) / 2, resy
    )
    fractal = method(x, y, c, max_iter)
    return fractal, x, y


def random_fractal(
    method=mb.fractals.julia,
    resx=3440,
    resy=1440,
    max_iter=1000,
    cmap="plasma",
    minvar=10,
    plot=False,
    impath=IMG_PATH,
):
    for i in range(500):
        x0, y0 = np.random.rand(2)
        pixelwidth = 10 ** (-4 - 6 * np.random.rand())
        c = 2 * ((0.5 - np.random.rand()) + 1j * (0.5 - np.random.rand()))
        fractal, *_ = make_fractal_r0(
            c,
            max_iter=100,
            x0=x0,
            y0=y0,
            pixelwidth=pixelwidth * 2,
            resx=500,
            resy=400,
            method=method,
        )
        fractal = np.ma.masked_where(fractal == 0, fractal)
        if fractal.std() > minvar:
            print(i, fractal.std())
            fractal, x, y = make_fractal_r0(
                c,
                max_iter=max_iter,
                x0=x0,
                y0=y0,
                pixelwidth=pixelwidth,
                resx=resx,
                resy=resy,
                method=method,
            )
    # print(np.diff(x), np.diff(y))
            out_to_image_cmap(fractal, cmap=cmap, impath=impath)
            if plot:
                plot_fractal(x, y, fractal, cmap)
