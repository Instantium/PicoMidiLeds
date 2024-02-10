# The Default Colors that are shown when the device is powered on or when note_display_default was played
# Values from 0-127 inclusive
default_colors = [
    50,     # Red
    127,    # Green
    50,     # Blue
    0,      # Red
    90,     # Green
    127     # Blue
]

# Displays the default color (Does not reset the global brightness changed by pitch bend)
note_display_default = 15
# Sets all LEDS to 0 (Does not reset the global brightness changed by pitch bend)
note_clear_all = 13

# When no message was received for timeout in seconds the default colors will be shown
# A value of -1 equals no timeout
timeout = -1

# Midi notes that correspong to the Led-channels
note_mapping = [
    12,
    14,
    16,
    17,
    19,
    21
]