import numpy as np
import matplotlib.pyplot as plt

# import mandelbrot_f as mb_f
from ..src import fractals
from PIL import Image


def get_cmap(name="plasma"):
    cmap = plt.get_cmap(name)
    cmap.set_bad([1.0, 1.0, 1.0, 1.0])
    return cmap


def get_ax_size(fig, ax):
    bbox = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    width, height = bbox.width, bbox.height
    width *= fig.dpi
    height *= fig.dpi
    return width, height


def get_x0_y0(ax):
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    return (xlim[0] + xlim[1]) / 2, (ylim[0] + ylim[1]) / 2


def get_pixelsize(fig, ax):
    width, height = get_ax_size(fig, ax)
    xlim = ax.get_xlim()
    return np.diff(xlim) / width


def rand_complex(shape=1):
    return np.sqrt(np.random.uniform(0, 1, shape)) * np.exp(
        1.0j * np.random.uniform(0, 2 * np.pi, shape)
    )


class FractalPlot:
    def __init__(
        self,
        method,
        c=rand_complex(),
        max_iter=1000,
        colormap="plasma",
        resx=2000,
        resy=2000,
        impath="./mandelbrot.png",
    ) -> None:
        self.method = method
        self.x = np.linspace(-1.5, 1.5, 2000)
        self.y = np.linspace(-1.5, 1.5, 2000)
        self.c = c
        self.max_iter = max_iter
        self.resx, self.resy = resx, resy
        self.impath = impath
        self.cmap = get_cmap(colormap)

    def recalculate(self):
        self.out = self.method(self.x, self.y, self.c, self.max_iter).T

    def replot(self):
        self.ax.clear()
        maps = self.ax.pcolorfast(self.x, self.y, np.log10(self.out), cmap=self.cmap)
        self.cbar.update_normal(maps)

    def init_plot_interactive(self) -> None:
        self.recalculate()
        self.fig, self.ax = plt.subplots(1, 1, figsize=(9, 7))
        self.ax.axis("equal")
        self.fig.canvas.mpl_connect("key_press_event", self.enter_press)
        self.fig.canvas.mpl_connect("button_release_event", self.on_button_press)
        maps = self.ax.pcolorfast(self.x, self.y, np.log10(self.out), cmap=self.cmap)
        self.cbar = self.fig.colorbar(maps)

    def redraw_centered(self):
        x0, y0 = get_x0_y0(self.ax)
        ylim = self.ax.get_ylim()
        pixelwidth = (ylim[1] - ylim[0]) / self.resy
        self.x = np.linspace(
            x0 - pixelwidth * (self.resx - 1) / 2,
            x0 + pixelwidth * (self.resx - 1) / 2,
            self.resx,
        )
        self.y = np.linspace(
            y0 - pixelwidth * (self.resy - 1) / 2,
            y0 + pixelwidth * (self.resy - 1) / 2,
            self.resy,
        )
        self.recalculate()
        print(self.x, self.y, "\n", x0, y0, pixelwidth)
        # self.save_toimage()

    def save_toimage(self):
        print("TODO - SAVE IMAGE")
        out = np.flip(self.out.T, axis=1)
        # out = self.out.T
        out = np.ma.masked_where(out == 0, out)
        out = np.log10(out.T)
        out = (out - np.min(out)) / (np.max(out) - np.min(out))
        out = np.uint8(255 * self.cmap(out))
        img = Image.fromarray((out))
        img.save(self.impath)

    def update_canvas(self):
        xr, yr = get_ax_size(self.fig, self.ax)
        self.x = np.linspace(*self.ax.get_xlim(), int(xr))
        self.y = np.linspace(*self.ax.get_ylim(), int(yr))
        self.recalculate()
        self.replot()

    def on_button_press(self, event):
        self.update_canvas()

    def enter_press(self, event):
        if event.key == "enter":
            self.redraw_centered()
            self.save_toimage()
            x0, y0 = get_x0_y0(self.ax)
            print(x0, y0)
        elif event.key == "h":
            self.update_canvas()


class JuliaPlot(FractalPlot):
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.method = fractals.julia
        # self.c = c


class MandelbrotPlot(FractalPlot):
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.method = fractals.mandelbrot


class FractionalMandelbrotPlot(FractalPlot):
    def __init__(self, *args, pow=4, fac=0.63, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.method = fractals.mandelbrot_fractional
        self.pow = pow
        self.fac = fac

    def recalculate(self):
        self.out = self.method(
            self.x, self.y, self.c, self.max_iter, self.pow, self.fac
        ).T
