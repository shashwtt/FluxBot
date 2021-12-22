colors = [
    0x60FF60,  # light green
    0xFFFF00,  # yellow
    0x00FFFF,  # cyan
    0xA641CB,  # purple
    0xECE3ED,  # off white
    0xFFFF4E,  # pale yellow
    0x1A1FC6,  # almost royal blue
    0x479B9E,  # turquoise
    0xCAFD7C,  # yellow green
    0x60C1E8   # baby blue
]

red = 0xFF0000
l_red = 0xFF3E3E
m_red = 0xEC5858
green = 0x00FF00
d_green = 0x274E13
l_green = 0x60FF60
yellow = 0xFFFF00
l_yellow = 0xFFFF4E
blue = 0x0000FF
cyan = 0x00FFFF
l_blue = 0x60C1E8

colors_but_in_a_dictionary = {
    'red': 0xFF0000,
    'l_red': 0xFF3E3E,
    'm_red': 0xEC5858,
    'green': 0x00FF00,
    'd_green': 0x274E13,
    'l_green': 0x60FF60,
    'yellow': 0xFFFF00,
    'l_yellow': 0xFFFF4E,
    'blue': 0x0000FF,
    'cyan': 0x00FFFF,
    'l_blue': 0x60C1E8
}


def get_color(color_name):
    return colors_but_in_a_dictionary[str(color_name)]