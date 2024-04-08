BIN = ./bin
SRC = ./src
BLD = ./bld
PRF = ./prf

NAME = mandelbrot_f

.PHONY : build draw_2d

all: draw_2d

build: $(SRC)/mandelbrot.f90
	python -m numpy.f2py -c --f90flags='-Wno-tabs -fopenmp -O2' -lgomp -m $(NAME) $<
	mv $(NAME).cpython* ./$(SRC)/

draw_2d: 
	python3 -m src.draw_2d

draw_3d: 
	python3 ./$(SRC)/draw_3d.py
