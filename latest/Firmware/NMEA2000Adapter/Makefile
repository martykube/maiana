# Headless build of the MAIANA NMEA 2000 adapter firmware (maiana-n2k), mirroring the
# Eclipse CDT configuration "Board7.0-L432" in .cproject.
# The 8.1 adapter (STM32L432KB) uses the Board 7.0 BSP: same MCU pins (SPI1 PA2/5/6/7 to
# the MCP2515, USART1 PA9/PA10 to the transponder UART, NMEA_RX PA3, NMEA_RX_EN PB0).
#
#   make                 # build/Board7.0-L432/maiana-n2k.bin  (flash at 0x08000000)

CONFIG ?= Board7.0-L432

ifeq ($(CONFIG),Board7.0-L432)
  DEFS     := STM32 STM32L432xx
  LDSCRIPT := STM32L432KBUX_FLASH.ld
  BSP      := Core/Src/bsp/board_7.0.cpp
else
  $(error Unsupported CONFIG=$(CONFIG))
endif

PREFIX  ?= $(HOME)/opt/xpack-arm-none-eabi-gcc-15.2.1-1.1/bin/arm-none-eabi-
CC      := $(PREFIX)gcc
CXX     := $(PREFIX)g++
OBJCOPY := $(PREFIX)objcopy
SIZE    := $(PREFIX)size

BUILD  := build/$(CONFIG)
TARGET := $(BUILD)/maiana-n2k

INCS := Core/Inc Core/Inc/bsp mcp_can ais n2k_mcp nmea2000 Drivers/CMSIS/Include \
        Drivers/CMSIS/Device/ST/STM32L4xx/Include Drivers/STM32L4xx_HAL_Driver/Inc

ARCH  := -mcpu=cortex-m4 -mthumb -mfloat-abi=hard -mfpu=fpv4-sp-d16
OPT   := -Os -fmessage-length=0 -fsigned-char -ffunction-sections -fdata-sections -Wall
FLAGS := $(ARCH) $(OPT) $(addprefix -D,$(DEFS)) $(addprefix -I,$(INCS)) -MMD -MP
CFLAGS   := $(FLAGS) -std=gnu11
CXXFLAGS := $(FLAGS) -include cstdint -std=gnu++11 -fno-rtti -fno-exceptions -fno-use-cxa-atexit -fno-threadsafe-statics
LDFLAGS  := $(ARCH) $(OPT) -T $(LDSCRIPT) -Xlinker --gc-sections -s --specs=nano.specs \
            --specs=nosys.specs -Wl,-Map,$(TARGET).map

# Same source set as Eclipse: the L432 config compiles startup_stm32l422xx.S (l431 excluded),
# skips stm32l4xx_hal_msp.c, the other BSPs and ActisenseReader.cpp.
SRCS := $(wildcard Core/Src/*.cpp Core/Src/*.c Drivers/STM32L4xx_HAL_Driver/Src/*.c \
          ais/*.cpp mcp_can/*.cpp n2k_mcp/*.cpp nmea2000/*.cpp) $(BSP) startup/startup_stm32l422xx.S
SRCS := $(filter-out Core/Src/stm32l4xx_hal_msp.c nmea2000/ActisenseReader.cpp,$(SRCS))
OBJS := $(addprefix $(BUILD)/,$(addsuffix .o,$(basename $(SRCS))))

all: $(TARGET).bin

$(TARGET).elf: $(OBJS) $(LDSCRIPT)
	$(CXX) $(LDFLAGS) -o $@ $(OBJS)
	$(SIZE) --format=berkeley $@

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
