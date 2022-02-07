ifdef PISTE_STD_LIB_PATH
STD_LIB_PATH := $(PISTE_STD_LIB_PATH)
else
STD_LIB_PATH := $(HOME)/.piste/lib
endif

.PHONY: std

std: 
	mkdir -p $(STD_LIB_PATH)
	cp std/* $(STD_LIB_PATH)/
