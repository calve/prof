OCAMLC = ocamlc
CFLAGS = -I +curl curl.cma str.cma
OBJS=connection

.PHONY : all clean
all: $(OBJS)

%.cmi : %.mli
	$(OCAMLC) $(CFLAGS) $< -c
%:	%.ml %.cmi
	$(OCAMLC) $(CFLAGS) $< -o $@

clean:
	$(RM) -Rdv *.cmi *.cmo $(OBJS)
