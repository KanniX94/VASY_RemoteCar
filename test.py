import pygame

from digi.xbee.devices import XBeeDevice, RemoteXBeeDevice, XBee64BitAddress
from digi.xbee.models.options import XBeeLocalInterface
import time

PORT = "COM11"
BAUD_RATE = 9600

def main():
    pygame.init()
    pygame.display.set_caption(u'Keyboard events')
    pygame.display.set_mode((400, 400))
    
    device = XBeeDevice(PORT, BAUD_RATE)

    try:
               
        # Instantiate an XBee device object.
        device.open()
        
        remote_device = RemoteXBeeDevice(device, XBee64BitAddress.from_hex_string("0013A20041981831"))
        
        print("Control car with W/A/S/D, close with F")
        #message = ""
        run = True
        while run == True:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                break
    
            if event.type in (pygame.KEYDOWN, pygame.KEYUP):
                key_name = pygame.key.name(event.key).upper()
                if event.type == pygame.KEYDOWN: # Key down
                    print(key_name + " pressed")
                    device.send_data(remote_device, key_name + ",1")
                       
                elif event.type == pygame.KEYUP: # Key release
                    print(key_name + " released")
                    device.send_data(remote_device, key_name + ",0")
                    
    finally:
        print("Remote control closed")
        if device is not None and device.is_open():
            device.close()
            
    # finalizes Pygame
    pygame.quit()
        

if __name__ == '__main__':
    main()