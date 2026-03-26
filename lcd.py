import smbus
import time

I2C_BUS = 1
LCD_ADDR = 0x27 

bus = smbus.SMBus(I2C_BUS)

LCD_WIDTH = 16     
LCD_CHR = 1        
LCD_CMD = 0        

LCD_LINE_1 = 0x80  
LCD_LINE_2 = 0xC0  

LCD_BACKLIGHT = 0x08
ENABLE = 0b00000100

def lcd_write(bits, mode):
    bits_high = mode | (bits & 0xF0) | LCD_BACKLIGHT
    bits_low = mode | ((bits << 4) & 0xF0) | LCD_BACKLIGHT

    bus.write_byte(LCD_ADDR, bits_high)
    lcd_toggle_enable(bits_high)

    bus.write_byte(LCD_ADDR, bits_low)
    lcd_toggle_enable(bits_low)

def lcd_toggle_enable(bits):
    time.sleep(0.0005)
    bus.write_byte(LCD_ADDR, (bits | ENABLE))
    time.sleep(0.0005)
    bus.write_byte(LCD_ADDR, (bits & ~ENABLE))
    time.sleep(0.0005)

def lcd_init():
    lcd_write(0x33, LCD_CMD)  # Initialize
    lcd_write(0x32, LCD_CMD)  # Set to 4-bit mode
    lcd_write(0x06, LCD_CMD)  # Cursor move direction
    lcd_write(0x0C, LCD_CMD)  # Turn cursor off
    lcd_write(0x28, LCD_CMD)  # 2 line display
    lcd_write(0x01, LCD_CMD)  # Clear display
    time.sleep(0.005)

def lcd_string(message, line):
    message = message.ljust(LCD_WIDTH)
    lcd_write(line, LCD_CMD)
    for char in message:
        lcd_write(ord(char),LCD_CHR)

lcd_init()
lcd_string("Rbsfboshini!", LCD_LINE_1)
lcd_string("Shreyaa, Hrithviii", LCD_LINE_2)
