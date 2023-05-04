import numpy as np
import sys
import os
import subprocess
import fractals as mb_f


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
        mb_f.random_fractals.random_fractal(
            cmap="plasma",
            resx=resx,
            resy=resy,
            plot=plot,
            minvar=8,
            method=mb_f.random_fractals.mb_f.fractals.mandelbrot_fractional,
            max_iter=500,
            impath=impath,
            pow=pow,
            fac=fac,
        )
    elif k == 2:
        print("Julia")
        mb_f.random_fractals.random_fractal(
            cmap="plasma",
            resx=resx,
            resy=resy,
            plot=plot,
            minvar=8,
            method=mb_f.random_fractals.mb_f.fractals.julia,
            max_iter=500,
            impath=impath,
        )
    elif k == 3:
        print("Mandelbrot")
        mb_f.random_fractals.random_fractal(
            cmap="plasma",
            resx=resx,
            resy=resy,
            plot=plot,
            minvar=8,
            method=mb_f.random_fractals.mb_f.fractals.mandelbrot,
            max_iter=500,
            impath=impath,
        )
    elif k == 4:
        print("Julia black and white")
        mb_f.random_fractals.random_julia_far(resx=resx, resy=resy, impath=impath)
    if plot:
        mb_f.random_fractals.plt.show()


if __name__ == "__main__":
    main()
    os.system(f"DISPLAY=:0 feh --bg-fill {IMPATH}")
# mb.random_fractals.random_julia_far(cmap='gray')
# mb.random_fractals.plt.show()
