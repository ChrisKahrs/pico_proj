MAX_5_BIT = (2 ** 5) - 1
MAX_6_BIT = (2 ** 6) - 1
MAX_8_BIT = (2 ** 8) - 1

import binascii
    
def rgb888_to_brg565(hex_color):
    """
    converts a 24-bit RGB hex (e.g. #FFFFFF colour to the 16bit brg colour used by the waveshare LCD.
    
    hex_color should be a value, like 0x00FF00 or 0b000000001111111100000000. I guess any value form will work if it's >= 0 and <= 2^32 - 1
    """
    
    # get the first 8 bits from the 24 bit value. The left is padded with 0 so no need to mask
    red_8_bit = hex_color >> 16
    # get the second 8 bits from the 24 bit value. The left will have 8 valid bits still so mask
    green_8_bit = (hex_color >> 8) & 0b00000000_11111111
    # get the third 8 bits from the 24 bit value. the left will have 16 valid bits still so mask
    blue_8_bit = hex_color & 0b00000000_00000000_11111111
    
    # debug
    #print(f"R: {red_8_bit}, G: {green_8_bit}, B: {blue_8_bit}")
    
    # map each from 0 to 255 to 0 to whatever their max is
    blue_mapped = round((MAX_5_BIT / MAX_8_BIT) * blue_8_bit)
    red_mapped = round((MAX_6_BIT / MAX_8_BIT) * red_8_bit)
    green_mapped = round((MAX_5_BIT / MAX_8_BIT) * green_8_bit)
    
    # shift them to their bit positions in BRG565 and recombine them
    blue_shifted = blue_mapped << 11
    red_shifted = red_mapped << 5
    # green is already all the way to the right
    
    combined = blue_shifted | red_shifted | green_mapped
    
    return combined

print(int(rgb888_to_brg565(0xff0000)))
