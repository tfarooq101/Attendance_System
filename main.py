import rp2
from rp2 import PIO
from machine import Pin
from neopixel import NeoPixel
from Button import *
from Buttonhandler import *
from Buzzer import *
import utime
from Displays import *

@rp2.asm_pio(out_init=[PIO.OUT_LOW]*8, sideset_init=[PIO.OUT_LOW]*4)
def sevseg():
    wrap_target()
    label("0")
    pull(noblock)           .side(0)      # 0
    mov(x, osr)             .side(0)      # 1
    out(pins, 8)            .side(1)      # 2
    out(pins, 8)            .side(2)      # 3
    out(pins, 8)            .side(4)      # 4
    out(pins, 8)            .side(8)      # 5
    jmp("0")                .side(0)      # 6
    wrap()

sm = rp2.StateMachine(0, sevseg, freq=2000, out_base=Pin(2), sideset_base=Pin(10))
sm.active(1)

digits = [
    0b11000000,  # 0
    0b11111001,  # 1
    0b10100100,  # 2 
    0b10110000,  # 3
    0b10011001,  # 4
    0b10010010,  # 5
    0b10000010,  # 6
    0b11111000,  # 7
    0b10000000,  # 8
    0b10011000   # 9
]

def segmentize(num):
    return (
        digits[num % 10] | digits[num // 10 % 10] << 8
        | digits[num // 100 % 10] << 16
        | digits[num // 1000 % 10] << 24
    )

# Create an instance of the Button class
green_button = Button(pin=1, name="green_button")
red_button = Button(pin=22, name="red_button")

def play_song(song, buzzer):
    buzzer.playsong(song)

def main():
    counting = 0
    running = False
    led_lights_running = False

    # Create an instance of the ButtonHandler class
    button_handler = Buttonhandler()

    # Set the button handler for the green and red buttons
    green_button.setHandler(button_handler)
    red_button.setHandler(button_handler)

    # creating a PIR object, setting it as IN
    pir = Pin(26, Pin.IN)

    # Set pins for LED Lights 
    pixels = NeoPixel(Pin(28), 16)

    #Create an instance of the SevenSegmentDisplay class
    # display = SevenSegmentDisplay()

    # Create an instance of the LCDDisplay class
    lcd_display = LCDDisplay()
    lcd_display.showText('Welcome to Class ISM6106!')

    # Initialize PWM (aka pulse width modulation) on Pin 27 and assign it to the variable buzzer.
    buzzer = PassiveBuzzer(27)

    song = ["E5", "G5", "A5", "P", "E5", "G5", "B5", "A5", "P", "E5", "G5", "A5", "P", "G5", "E5"]

    rainbow = [
        (126, 1, 0), (114, 13, 0), (102, 25, 0), (90, 37, 0), (78, 49, 0), (66, 61, 0), (54, 73, 0), (42, 85, 0),
        (30, 97, 0), (18, 109, 0), (6, 121, 0), (0, 122, 5), (0, 110, 17), (0, 98, 29), (0, 86, 41), (0, 74, 53),
        (0, 62, 65), (0, 50, 77), (0, 38, 89), (0, 26, 101), (0, 14, 113), (0, 2, 125), (9, 0, 118), (21, 0, 106),
        (33, 0, 94), (45, 0, 82), (57, 0, 70), (69, 0, 58), (81, 0, 46), (93, 0, 34), (105, 0, 22), (117, 0, 10)
    ]

    try:
        while True:
            if pir.value() == 1:
                print(f"Status: Attendance Recorded! for Tag: XXXX, Student: John Doe, Class: ISM6106\n Added to Database, woohoo!!")
                if not led_lights_running:
                    led_lights_running = True
                    play_song(song, buzzer)
                    # for i in range(16):
                    #     pixels[i] = rainbow[i]
                    #     pixels.write()
                    #     utime.sleep_ms(100)  # Delay between each LED light and note
            else:
                print(f"Status: Please Scan Tag For Attendeance...:)")
                if led_lights_running:
                    led_lights_running = False
                    pixels.fill((0, 0, 0))
                    pixels.write()

            if green_button.isPressed():
                running = True
                sm.put(segmentize(counting))
                if not led_lights_running:
                    led_lights_running = True
                    # for i in range(16):
                    #     pixels[i] = rainbow[i]
                    #     pixels.write()
                    #     utime.sleep_ms(100)  # Delay between each LED light
                button_handler.buttonPressed("green_button")

            elif red_button.isPressed():
                print(f" Status: Invalid Tag Bro, Scan it again!! xD")
                play_song(song, buzzer)
                if running:
                    running = False
                    button_handler.buttonReleased("green_button")
                    counting = 0
                else:
                    counting = 0
                    sm.put(segmentize(counting))
                    button_handler.buttonReleased("red_button")
                    button_handler.buttonPressed("red_button")

            if running:
                counting += 1
                sm.put(segmentize(counting))

            utime.sleep_ms(100)  # Delay between each iteration of the loop

    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
