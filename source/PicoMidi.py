import board
import time
import pwmio
import busio
import adafruit_midi
import usb_midi
import config
from adafruit_midi.note_on import NoteOn
from adafruit_midi.control_change import ControlChange

CC_MODULATION = 1

# Midi output settings
midi_channel = 1  # Target midi channel to write to
usb_midi = adafruit_midi.MIDI(midi_in=usb_midi.ports[0], debug=True)
# UART Midi device on pin 6
uart = busio.UART(tx=board.GP16, rx=board.GP17, baudrate=31250, timeout=0.001)
uart_midi = adafruit_midi.MIDI(midi_out=uart, midi_in=uart, debug=True)

led_pins = [
    board.GP6,
    board.GP7,
    board.GP8,
    board.GP10,
    board.GP11,
    board.GP12,
]

last_message_at = 0
is_default_showing = True
global_brightness_factor = 1


def processMidiMessage(message):
    global last_message_at
    global is_default_showing
    global global_brightness_factor

    if isinstance(message, NoteOn):
        last_message_at = time.time()

        if message.note == config.note_display_default:
            displayDefault()
            return

        if message.note == config.note_clear_all:
            for i in range(len(led_colors)):
                led_colors[i] = 0
            return

        if is_default_showing:
            for led in leds:
                led.duty_cycle = 0
            is_default_showing = False

        try:
            led_index = config.note_mapping.index(message.note)

            print("index:")
            print(led_index)
            print(message.velocity)

            led_colors[led_index] = message.velocity

        except ValueError:
            print("not interested in note")

    elif isinstance(message, ControlChange) and message.control == CC_MODULATION:
        global_brightness_factor = abs(message.value) % 128 / 127


def update_leds():
    for led, color in zip(leds, led_colors):
        color_factor = min(color / 127, 1)

        led.duty_cycle = int(
            pow(65535, color_factor * global_brightness_factor))


def displayDefault():
    global is_default_showing
    global led_colors
    led_colors = [color for color in config.default_colors]
    is_default_showing = True


# Setup
displayDefault()
leds = [pwmio.PWMOut(lp, frequency=1000, duty_cycle=0) for lp in led_pins]
print("Init done")

# main loop
while True:
    in_message = usb_midi.receive()
    if in_message is not None:
        print("Received USB message")
        print(in_message)

        # uart_midi.send(in_message)

        # BEWARE: channel is always 0
        processMidiMessage(in_message)

    in_message = uart_midi.receive()
    if in_message is not None:
        print("Received uart message")
        print(in_message)
        # BEWARE: channel is always 0
        processMidiMessage(in_message)

    if config.timeout > 0 and time.time() - last_message_at > config.timeout:
        displayDefault()

    update_leds()
