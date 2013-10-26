OUT=prof
SRCDIR=src

.PHONY : all clean
all: $(OUT)

#We'll compile in $(SRCDIR), and then we retrive then binary
$(OUT):
	make -C $(SRCDIR) $(OUT)
	mv $(SRCDIR)/$(OUT) .

clean:
	make -C $(SRCDIR) clean
	$(RM) -Rdv $(OUT)
