# Headless build of the MAIANA transponder firmware, mirroring the Eclipse CDT
# configurations in .cproject. Default: L412-NewBreakouts-Bootloader (board 12.0.x).
#
#   make                       # build/L412-NewBreakouts-Bootloader/maiana-transponder.bin
#   make CONFIG=L412-NewBreakouts

CONFIG ?= L412-NewBreakouts-Bootloader

ifeq ($(CONFIG),L412-NewBreakouts-Bootloader)
  DEFS   := STM32L412xx VECT_TAB_OFFSET=0x2000 LEGACY_BREAKOUTS=0
  LDSCRIPT := STM32L412_64k-Bootloader.ld
  STARTUP  := startup/startup_stm32l412xx.S
else ifeq ($(CONFIG),L412-NewBreakouts)
  DEFS   := STM32L412xx VECT_TAB_OFFSET=0x0 LEGACY_BREAKOUTS=0
  LDSCRIPT := STM32L412_64k.ld
  STARTUP  := startup/startup_stm32l412xx.S
else
  $(error Unsupported CONFIG=$(CONFIG))
endif

PREFIX  ?= $(HOME)/opt/xpack-arm-none-eabi-gcc-15.2.1-1.1/bin/arm-none-eabi-
CC      := $(PREFIX)gcc
CXX     := $(PREFIX)g++
OBJCOPY := $(PREFIX)objcopy
SIZE    := $(PREFIX)size

BUILD := build/$(CONFIG)
TARGET := $(BUILD)/maiana-transponder

INCS := Inc Inc/bsp Drivers/CMSIS/Include Drivers/CMSIS/Device/ST/STM32L4xx/Include \
        Drivers/STM32L4xx_HAL_Driver/Inc

ARCH  := -mcpu=cortex-m4 -mthumb -mfloat-abi=hard -mfpu=fpv4-sp-d16
OPT   := -Os -fmessage-length=0 -fsigned-char -ffunction-sections -fdata-sections \
         -fsingle-precision-constant -flto -Wall
FLAGS := $(ARCH) $(OPT) $(addprefix -D,$(DEFS)) $(addprefix -I,$(INCS)) -MMD -MP
CFLAGS   := $(FLAGS) -std=gnu11
CXXFLAGS := $(FLAGS) -std=gnu++11 -fno-rtti -fno-exceptions -fno-use-cxa-atexit -fno-threadsafe-statics
LDFLAGS  := $(ARCH) $(OPT) -T $(LDSCRIPT) -Xlinker --gc-sections -s --specs=nano.specs \
            --specs=rdimon.specs -Wl,-Map,$(TARGET).map

# Same source set as Eclipse: everything under Src/ and Drivers/, minus the excluded files
SRCS := $(wildcard Src/*.c Src/*.cpp Src/bsp/*.cpp Drivers/STM32L4xx_HAL_Driver/Src/*.c) $(STARTUP)
SRCS := $(filter-out Src/printf.c Src/main.c Src/bsp/bsp_6_0_bad.cpp,$(SRCS))
OBJS := $(addprefix $(BUILD)/,$(addsuffix .o,$(basename $(SRCS))))

all: $(TARGET).bin

$(TARGET).elf: $(OBJS) $(LDSCRIPT)
	$(CXX) $(LDFLAGS) -o $@ $(OBJS)
	$(SIZE) --format=sysv $@ | tail -n +3 | head -n 4

$(TARGET).bin: $(TARGET).elf
	$(OBJCOPY) -O binary $< $@
	@ls -l $@

$(BUILD)/%.o: %.c
	@mkdir -p $(dir $@)
	$(CC) $(CFLAGS) -c $< -o $@

$(BUILD)/%.o: %.cpp
	@mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) -c $< -o $@

$(BUILD)/%.o: %.S
	@mkdir -p $(dir $@)
	$(CC) $(FLAGS) -x assembler-with-cpp -c $< -o $@

clean:
	rm -rf build

.PHONY: all clean
-include $(OBJS:.o=.d)
