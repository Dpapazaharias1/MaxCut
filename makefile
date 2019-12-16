SRCPATH	  = ./src
BINPATH	  = ./bin
DATPATH   = ./dat
DATFILES  = $(shell find $(DATPATH) -name 'Graph_*.dat')

all:
	$(foreach var,$(DATFILES), python $(SRCPATH)/main.py $(var);)

IP:
	$(foreach var,$(DATFILES), python $(SRCPATH)/main.py IP $(var);)

LP:
	$(foreach var,$(DATFILES), python $(SRCPATH)/main.py LP $(var);)

LD:
	$(foreach var,$(DATFILES), python $(SRCPATH)/main.py LD $(var);)

ellipsoid:
	$(foreach var,$(DATFILES), python $(SRCPATH)/main.py ellipsoid $(var);)

heuristic:
	$(foreach var,$(DATFILES), python $(SRCPATH)/main.py heuristic $(var);)
