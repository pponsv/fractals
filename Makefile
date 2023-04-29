BIN = ./bin
SRC = ./src
BLD = ./bld
PRF = ./prf

NAME = mandelbrot

.PHONY : build draw_2d

all: draw_2d

build: $(SRC)/mandelbrot.f90
	f2py3 -c --f90flags='-Wno-tabs -fopenmp -O2' -lgomp -m $(NAME) $<
	mv $(NAME).cpython* ./$(SRC)/

draw_2d: 
	python3 ./$(SRC)/draw_2d.py

draw_3d: 
	python3 ./$(SRC)/draw_3d.py