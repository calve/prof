OCAMLC = ocamlc
CFLAGS = -I +curl curl.cma str.cma

OCAMLOPT = ocamlopt
OFLAGS = -I +curl curl.cmxa str.cmxa

#.cmo files needed to build the executable
OBJS=libprof.cmo
COMPILED=libprof.cmx
OUT=prof

.PHONY : all clean
all: $(OUT)

$(OUT) : $(OBJS)
	$(OCAMLC) $(CFLAGS) $(OBJS) $@.ml -o $@

#How to build a cmi file from a mli file
%.cmi : %.mli
	$(OCAMLC) $(CFLAGS) $< -c

#How to build a cmo file from one ml and one cmi file
%.cmo:	%.ml %.cmi
	$(OCAMLC) $(CFLAGS) $< -c

%.cmx : %.ml
	$(OCAMLOPT) $(OFLAGS) $< -c

clean:
	$(RM) -Rdv *.cmi *.cmo $(OBJS) $(OUT)
