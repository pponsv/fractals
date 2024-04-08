import numpy as np
import sys
import os
import subprocess

from . import draw_2d, random_fractals
from . import mandelbrot_f as mb_f


DIRPATH = os.path.dirname(os.path.abspath(__file__))
IMPATH = f"{DIRPATH}/../mandelbrot.png"
sys.path.append(DIRPATH)


def main(resx=3440, resy=1440, plot=False, impath=IMPATH):
    pow, fac = 5, 0.5
    # mb.random_fractals.random_julia_bw_far()
    k = np.random.randint(1, 5)
    # k = 2
    if k == 1:
        print("Mandelbrot fractional")
        random_fractals.random_fractal(
            cmap="plasma",
            resx=resx,
            resy=resy,
            plot=plot,
            minvar=8,
            method=mb_f.fractals.mandelbrot_fractional,
            max_iter=500,
            impath=impath,
            pow=pow,
            fac=fac,
        )
    elif k == 2:
        print("Julia")
        random_fractals.random_fractal(
            cmap="plasma",
            resx=resx,
            resy=resy,
            plot=plot,
            minvar=8,
            method=mb_f.fractals.julia,
            max_iter=500,
            impath=impath,
        )
    elif k == 3:
        print("Mandelbrot")
        random_fractals.random_fractal(
            cmap="plasma",
            resx=resx,
            resy=resy,
            plot=plot,
            minvar=8,
            method=mb_f.fractals.mandelbrot,
            max_iter=500,
            impath=impath,
        )
    elif k == 4:
        print("Julia black and white")
        random_fractals.random_julia_far(resx=resx, resy=resy, impath=impath)
    if plot:
        random_fractals.plt.show()


if __name__ == "__main__":
    main()
    os.system(f"DISPLAY=:0 feh --bg-fill {IMPATH}")
    # plt.show()
# mb.random_fractals.random_julia_far(cmap='gray')
# mb.random_fractals.plt.show()
