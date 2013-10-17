OCAMLC = ocamlc
CFLAGS = -I +curl curl.cma str.cma
OUT=prof
SRCDIR=src

.PHONY : all clean
all: $(OUT)

$(OUT):
	make -C $(SRCDIR) $(OUT)
	mv $(SRCDIR)/$(OUT) .

clean:
	make -C $(SRCDIR) clean
	$(RM) -Rdv $(OUT)
