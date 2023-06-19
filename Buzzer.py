"""
# Buzzer.py - Object-oriented implementation of active and passive buzzers
# Author: Arijit Sengupta
"""

import time
from machine import Pin, PWM
from utime import sleep

class Buzzer:
    """
    A simple buzzer class - use it to play and pause different sounds
    ranging from fequencies 10 through 10000
    default volume is half volume - set it between 0 and 10
    """ 
    
    def beep(self, tone=500, duration=150):
        print(f"Beeping the buzzer at {tone}hz for {duration} ms")
        self.play(tone)
        time.sleep(duration / 1000)
        self.stop()
    
class ActiveBuzzer(Buzzer):
    """
    An active buzzer has an internal oscillator that plays a fixed tone when power is applied
    Cannot control the tone. Only turn on and off.
    """
    
    def __init__(self, pin):
        self._buz = Pin(pin, Pin.OUT)
   
    def play(self, tone=500):
        """ Play sound. Tone is ignored. """
        
        self._buz.value(1)
        
    def stop(self):
        """ Stop the sound. """
        
        self._buz.value(0)
    
class PassiveBuzzer(Buzzer):
    """
    A passive buzzer does not have an internal oscillator. MC needs to send a PWM signal
    to play tones. The tone is controlled by the frequency of the PWM, and the volume level
    is controlled by the duty cycle. Setting duty cycle to 0 stops sound.
    """
    
    def __init__(self, pin,tone=500):
        print("PassiveBuzzer: constructor")
        self._buz = PWM(Pin(pin))
        self._volume = 5
        self._playing = False
        self.stop()

    def play(self, tone=500):
        """ play the supplied tone. """
        
        print(f"PassiveBuzzer: playing tone {tone}")
        self._buz.freq(tone)
        self._buz.duty_u16(self._volume * 100)
        self._playing = True

    def stop(self):
        """ Stop playing sound """
        
        print("PassiveBuzzer: stopping tone")
        self._buz.duty_u16(0)
        self._playing = False

    def setVolume(self, volume=5):
        """ Change the volume of the sound currently playing and future plays """
        
        print(f"PassiveBuzzer: changing volume to {volume}")
        self._volume = volume
        if (self._playing):
            self._buz.duty_u16(self._volume * 100)
    
    def playtone(frequency):
        buzzer.duty_u16(1000)
        buzzer.freq(frequency)

    def bequiet():
        buzzer.duty_u16(0)

    def playsong(self, song):
        tones = {
        "B0": 31, "C1": 33, "CS1": 35, "D1": 37, "DS1": 39, "E1": 41, "F1": 44, "FS1": 46, "G1": 49, "GS1": 52,
        "A1": 55, "AS1": 58, "B1": 62, "C2": 65, "CS2": 69, "D2": 73, "DS2": 78, "E2": 82, "F2": 87, "FS2": 93,
        "G2": 98, "GS2": 104, "A2": 110, "AS2": 117, "B2": 123, "C3": 131, "CS3": 139, "D3": 147, "DS3": 156,
        "E3": 165, "F3": 175, "FS3": 185, "G3": 196, "GS3": 208, "A3": 220, "AS3": 233, "B3": 247, "C4": 262,
        "CS4": 277, "D4": 294, "DS4": 311, "E4": 330, "F4": 349, "FS4": 370, "G4": 392, "GS4": 415, "A4": 440,
        "AS4": 466, "B4": 494, "C5": 523, "CS5": 554, "D5": 587, "DS5": 622, "E5": 659, "F5": 698, "FS5": 740,
        "G5": 784, "GS5": 831, "A5": 880, "AS5": 932, "B5": 988, "C6": 1047, "CS6": 1109, "D6": 1175, "DS6": 1245,
        "E6": 1319, "F6": 1397, "FS6": 1480, "G6": 1568, "GS6": 1661, "A6": 1760, "AS6": 1865, "B6": 1976,
        "C7": 2093, "CS7": 2217, "D7": 2349, "DS7": 2489, "E7": 2637, "F7": 2794, "FS7": 2960, "G7": 3136,
        "GS7": 3322, "A7": 3520, "AS7": 3729, "B7": 3951, "C8": 4186, "CS8": 4435, "D8": 4699, "DS8": 4978
        }
        for note in song:
            if note == "P":
                self._buz.duty_u16(0)  # Turn off the buzzer
            else:
                frequency = tones[note]
                self._buz.freq(frequency)  # Set the frequency
                self._buz.duty_u16(32768)  # Set the duty cycle for a 50% square wave
                sleep(0.5)  # Play each note for 0.5 seconds

        self._buz.duty_u16(0)  # Turn off the buzzer at the end of the song

