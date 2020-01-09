fw =  bnx2x-e1-7.13.1.0.fw bnx2x-e1h-7.13.1.0.fw bnx2x-e2-7.13.1.0.fw

firmware: $(fw)

install: $(fw)
	for f in $+; do \
		install -m 644 -D $$f $(INSTALL_PATH)/lib/firmware/$$f; \
	done

%:: %.ihex
	objcopy -Iihex -Obinary $< $@

%.fw: %.HEX ihex2fw
	./ihex2fw $< $@

%.fw: %.H16 ihex2fw
	./ihex2fw -w $< $@

ihex2fw: ihex2fw.c
	gcc -o $@ $<
