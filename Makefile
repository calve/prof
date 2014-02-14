OUT=prof
SRCDIR=src
DESTDIR=/usr/bin

.PHONY : all clean
all: $(OUT)

#We'll compile in $(SRCDIR), and then we retrive the binary
$(OUT):
	make -C $(SRCDIR) $(OUT)
	mv $(SRCDIR)/$(OUT) .

clean:
	make -C $(SRCDIR) clean
	$(RM) -Rdv $(OUT)

install: all
	cp $(OUT) $(DESTDIR)
