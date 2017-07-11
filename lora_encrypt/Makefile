CC=gcc
EXE=LoRaMacCrypto_test
SHARE_LIB=libloraCrypto.so
mkfile_path := $(shell dirname $(abspath $(lastword $(MAKEFILE_LIST))))

$(EXE): main.o  
	@echo $(mkfile_path)
	$(CC) -o $@ $^  -L$(mkfile_path)  -lloraCrypto

so: aes.o cmac.o LoRaMacCrypto.o
	$(CC) --share -fPIC -o $(SHARE_LIB) $^ 

%.o: %.c
	$(CC) -c -fPIC $< -D HAVE_UINT_32T

clean:
	rm *.o $(EXE) 
