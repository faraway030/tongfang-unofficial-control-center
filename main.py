#!/usr/bin/python3
# main.py

import sys
import argparse, textwrap
from handler import DeviceHandler
            
class Controller(DeviceHandler):
    def __init__(self, vendor_id, product_id):
        super(Controller, self).__init__(vendor_id, product_id)
    
    brightness_map = {
    1: 0x08,
    2: 0x16,
    3: 0x24,
    4: 0x32
    }
        
    def get_rgb(self, color):
        colors = {
            "white":    "FFFFFF",
            "red":      "FF0000",
            "blue":     "0000C8",
            "teal":     "0064C8",
            "green":    "006400",
            "yellow":   "FFFF66",
            "orange":   "ff2800",
            "gold":     "ff4600",
            "cyan":     "00FFFF",
            "pink":     "FF00C8",
            "purple":   "8800C8",
        }
        
        color = colors[color]
        
        r = int(color[:2],16)
        g = int(color[2:4],16)
        b = int(color[-2:],16)
            
        return [r, g, b]
    
    def setup(self, program=0x01, speed=0x05, brightness=0x32, direction=0x00, save=0x01):
        # Byte  Purpose     Notes
        # 0     ???         0x08 to issue commands?
        # 1     ???         0x02 to issue commands? 
        # 2     Program     The 'effect' in use
        # 3     Speed       0x0?: 1,2,3,4,5,6,7,8,9,a (fastest to slowest)
        # 4     Brightness  0x08, 0x16, 0x24, 0x32
        # 5     ???         0x08
        # 6     Direction   0x0?: 0 for None, 1 for right, 2 for left
        # 7     save changes (00 for no, 01 for yes)
        ######################################################################
        # Programs:
        #   Name            Command     Colors required
        #
        #   Static          0x01        4
        #   Breathing       0x02        7
        #   Wave            0x03        7
        #   Rainbow         0x04        0
        #   Mix             0x13        7
        #   Flash           0x12        7
        
        self.ctrl_write(0x08, 0x02, program, speed, brightness, 0x08, direction, save)

    def set_area(self, area, color):
        self.rgb = self.get_rgb(color)
        self.ctrl_write(0x14, 0x00, area, self.rgb[0], self.rgb[1], self.rgb[2], 0x00, 0x00)
    
    def set_brightness(self, brightness=None):
        if brightness:
            self.ctrl_write(0x08, 0x02, 0x01, 0x05, self.brightness_map[brightness], 0x08, 0x00, 0x00)
        else:    
            self.set_brightness(4)
            
    def send_end(self):
        self.ctrl_write(0x14, 0x00, 0x05, 0x00, 0x00, 0xc8, 0x00, 0x00)
        self.ctrl_write(0x14, 0x00, 0x06, 0x00, 0x64, 0xc8, 0x00, 0x00)
        self.ctrl_write(0x14, 0x00, 0x07, 0x00, 0x64, 0x00, 0x00, 0x00)
        self.ctrl_write(0x08, 0x02, 0x01, 0x05, 0x32, 0x08, 0x00, 0x00)

    def set_mono_color(self, color):
        for i in range(1,5,1):
            self.set_area(i,color)
 	

def main():
    control = Controller(vendor_id=0x048d, product_id=0xce00)

    parser = argparse.ArgumentParser(
        description=textwrap.dedent('''
            Supply at least one of the options [-a|-c|-b|-d].
                
            Colors available:
            [red|green|blue|teal|pink|purple|white|yellow|orange|olive|maroon|brown|gray|skyblue|navy|crimson|darkgreen|lightgreen|gold|violet] '''),
        formatter_class=argparse.RawDescriptionHelpFormatter)
    
    parser.add_argument(
        '-a', '--area', help='Select an area. (1-4)', type=int, choices=range(1,5))
    parser.add_argument(
        '-c', '--color', help='Select a color for a specific area or all keys.')
    parser.add_argument(
        '-b', '--brightness', help='Set brightness, 1 is minimum, 4 is maximum.', type=int, choices=range(1, 5))
    #parser.add_argument('-s', '--style',
    #                    help='One of (rainbow, marquee, wave, raindrop, aurora, random, reactive, breathing, ripple, reactiveripple, reactiveaurora, fireworks). Additional single colors are available for the following styles: raindrop, aurora, random, reactive, breathing, ripple, reactiveripple, reactiveaurora and fireworks. These colors are: Red (r), Orange (o), Yellow (y), Green (g), Blue (b), Teal (t), Purple (p). Append those styles with the start letter of the color you would like (e.g. rippler = Ripple Red')
    parser.add_argument('-d', '--disable', action='store_true',
                        help='Turn keyboard backlight off'),

    parsed = parser.parse_args()
    if parsed.disable:
        control.disable_keyboard()
    else :
        if parsed.color:
            if parsed.area:
                control.set_area(parsed.area, parsed.color)
            else:
                control.set_mono_color(parsed.color)
        if parsed.brightness:
            control.set_brightness(parsed.brightness)
        else :
            pass
            #print("Invalid or absent command")

    sys.exit(1)

if __name__ == "__main__":
    main()
