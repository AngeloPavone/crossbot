from math import ceil, log, floor
import re

from PIL import Image, ImageDraw
import numpy as np


SHARE_CODE = ''
WIDTH = 361
HEIGHT = 271
CENTER_X = WIDTH / 2
CENTER_Y = HEIGHT / 2


class Crosshair:
    style               =  0
    has_center_dot      =  0
    size                =  0.0
    thickness           =  0.0
    gap                 =  0.0
    fixed_gap           =  0
    has_outline         =  0
    outline_thickness   =  0.0
    red                 =  0
    green               =  0
    blue                =  0
    has_alpha           =  0
    alpha               =  0
    split_distance      =  0
    inner_split_alpha   =  0
    outer_split_alpha   =  0
    split_size_ratio    =  0
    is_t_style          =  0
    use_weapon_gap      =  0


    def code_to_bytes(self, SHARE_CODE: str) -> list:

        crosshair_code = SHARE_CODE[4:].replace('-','')

        DICTIONARY = "ABCDEFGHJKLMNOPQRSTUVWXYZabcdefhijkmnopqrstuvwxyz23456789"
        MATCH = re.search("^CSGO(-?[\\w]{5}){5}$", SHARE_CODE)

        if not MATCH:
            print('Not a Valid Crosshair Code!')
            exit(1)

        big = 0
        for char in list(reversed(crosshair_code)):
            big = (big * len(DICTIONARY)) + DICTIONARY.index(char)

        def bytes_needed(n):
            return 1 if n == 0 else int(log(n, 256)) + 1

        bytes_required = bytes_needed(big)
        bytes = list(big.to_bytes(bytes_required, 'little'))

        if len(bytes) == 18:
            bytes.append(0x00)

        return list(reversed(bytes))


    def uint8toint8(self, input: int) -> int:
        return input if input < 128 else input - 256


    def __init__(self, raw_bytes=None) -> None:
        raw_bytes = self.code_to_bytes(SHARE_CODE)
        self.gap                =   (self.uint8toint8(raw_bytes[3]) / 10.0)
        self.outline_thickness  =   (raw_bytes[4] / 2)
        self.red                =   (raw_bytes[5])
        self.green              =   (raw_bytes[6])
        self.blue               =   (raw_bytes[7])
        self.alpha              =   (raw_bytes[8])
        self.split_distance     =   (float(raw_bytes[9]))
        self.fixed_gap          =   (self.uint8toint8((raw_bytes[10]) / 10.0))
        self.color              =   (raw_bytes[11] & 7)
        self.has_outline        =   (1 if (raw_bytes[11] & 8) != 0 else 0)
        self.inner_split_alpha  =   (raw_bytes[11] >> 4) / 10.0
        self.outer_split_alpha  =   (raw_bytes[12] & 0xF) / 10.0
        self.split_size_ratio   =   (raw_bytes[12] >> 4) / 10.0
        self.thickness          =   (raw_bytes[13] / 10.0)
        self.has_center_dot     =   (1 if ((raw_bytes[14] >> 4) & 1) != 0 else 0)
        self.use_weapon_gap     =   (1 if ((raw_bytes[14] >> 4) & 2) != 0 else 0)
        self.has_alpha          =   (1 if ((raw_bytes[14] >> 4) & 4) != 0 else 0)
        self.is_t_style         =   (1 if ((raw_bytes[14] >> 4) & 8) != 0 else 0)
        self.style              =   (raw_bytes[14] & 0xF) >> 1
        self.size               =   (raw_bytes[15] / 10.0)


    def get_crosshair_settings(self) -> str:
        settings = str(
                f'cl_crosshairstyle {self.style};\n'
                f'cl_crosshairsize {self.size};\n'
                f'cl_crosshairthickness {self.thickness};\n'
                f'cl_crosshairgap {self.gap};\n'
                f'cl_crosshair_drawoutline {self.has_outline};\n'
                f'cl_crosshair_outlinethickness {self.outline_thickness};\n'
                f'cl_crosshaircolor {self.color};\n'
                f'cl_crosshaircolor_r {self.red};\n'
                f'cl_crosshaircolor_g {self.green};\n'
                f'cl_crosshaircolor_b {self.blue};\n'
                f'cl_crosshairusealpha {self.has_alpha};\n'
                f'cl_crosshairalpha {self.alpha};\n'
                f'cl_crosshairdot {self.has_center_dot};\n'
                f'cl_crosshair_t {self.is_t_style};\n'
                f'cl_crosshairgap_useweaponvalue {self.use_weapon_gap};\n'
                f'cl_crosshair_dynamic_splitdist {self.split_distance};\n'
                f'cl_fixedcrosshairgap {self.fixed_gap};\n'
                f'cl_crosshair_dynamic_splitalpha_innermod {self.inner_split_alpha};\n'
                f'cl_crosshair_dynamic_splitalpha_outermod {self.outer_split_alpha};\n'
                f'cl_crosshair_dynamic_maxdist_splitratio {self.split_size_ratio};\n'
                )
        print(settings)
        return settings

class generate_crosshair_coordinates:
    def left(self, THICKNESS: float, SIZE: float, GAP: float) -> tuple:
        X1 = ceil(CENTER_X - (SIZE + (GAP / 2)))
        Y1 = CENTER_Y + (THICKNESS / 2)
        X2 = ceil(CENTER_X - (GAP / 2))
        Y2 = CENTER_Y - (THICKNESS / 2)
        left = tuple([X1, Y1, X2, Y2])
        return left


    def top(self, THICKNESS: float, SIZE: float, GAP: float) -> tuple:
        X1 = CENTER_X - (THICKNESS / 2)
        Y1 = ceil(CENTER_Y - (SIZE + (GAP / 2)))
        X2 = CENTER_X + (THICKNESS / 2)
        Y2 = ceil(CENTER_Y - (GAP / 2))
        top = tuple([X1, Y1, X2, Y2])
        return top


    def right(self, THICKNESS: float, SIZE: float, GAP: float) -> tuple:
        X1 = floor(CENTER_X + (GAP / 2))
        Y1 = CENTER_Y + (THICKNESS / 2)
        X2 = floor(CENTER_X + (SIZE + (GAP / 2)))
        Y2 = CENTER_Y - (THICKNESS / 2)
        right = tuple([X1, Y1, X2, Y2])
        return right


    def bottom(self, THICKNESS: float, SIZE: float, GAP: float) -> tuple:
        X1 = CENTER_X - (THICKNESS / 2)
        Y1 = floor(CENTER_Y + (GAP / 2))
        X2 = CENTER_X + (THICKNESS / 2)
        Y2 = floor(CENTER_Y + (SIZE + (GAP / 2)))
        bottom = tuple([X1, Y1, X2, Y2])
        return bottom


    def dot(self, THICKNESS: float) -> tuple:
        X1 = CENTER_X - (THICKNESS / 2)
        Y1 = CENTER_Y - (THICKNESS / 2)
        X2 = CENTER_X + (THICKNESS / 2)
        Y2 = CENTER_Y + (THICKNESS / 2)
        dot = tuple([X1, Y1, X2, Y2])
        return dot

    def left_outline(self, THICKNESS: float, SIZE: float, GAP: float) -> tuple:
        X1 = ceil(CENTER_X - (SIZE + (GAP / 2))) - 1
        Y1 = CENTER_Y + (THICKNESS / 2) + 1
        X2 = ceil(CENTER_X - (GAP / 2)) + 1
        Y2 = CENTER_Y - (THICKNESS / 2) - 1
        left = tuple([X1, Y1, X2, Y2])
        return left


    def top_outline(self, THICKNESS: float, SIZE: float, GAP: float) -> tuple:
        X1 = CENTER_X - (THICKNESS / 2) - 1
        Y1 = ceil(CENTER_Y - (SIZE + (GAP / 2))) - 1
        X2 = CENTER_X + (THICKNESS / 2) + 1
        Y2 = ceil(CENTER_Y - (GAP / 2)) + 1
        top = tuple([X1, Y1, X2, Y2])
        return top


    def right_outline(self, THICKNESS: float, SIZE: float, GAP: float) -> tuple:
        X1 = floor(CENTER_X + (GAP / 2)) - 1
        Y1 = CENTER_Y + (THICKNESS / 2) + 1
        X2 = floor(CENTER_X + (SIZE + (GAP / 2))) + 1
        Y2 = CENTER_Y - (THICKNESS / 2) - 1
        right = tuple([X1, Y1, X2, Y2])
        return right


    def bottom_outline(self, THICKNESS: float, SIZE: float, GAP: float) -> tuple:
        X1 = CENTER_X - (THICKNESS / 2) - 1
        Y1 = floor(CENTER_Y + (GAP / 2)) - 1
        X2 = CENTER_X + (THICKNESS / 2) + 1
        Y2 = floor(CENTER_Y + (SIZE + (GAP / 2))) + 1
        bottom = tuple([X1, Y1, X2, Y2])
        return bottom


    def dot_outline(self, THICKNESS: float) -> tuple:
        X1 = CENTER_X - (THICKNESS / 2) - 1
        Y1 = CENTER_Y - (THICKNESS / 2) - 1
        X2 = CENTER_X + (THICKNESS / 2) + 1
        Y2 = CENTER_Y + (THICKNESS / 2) + 1
        dot = tuple([X1, Y1, X2, Y2])
        return dot

def map_gap_value(x: int | float) -> float:
    if x > -5:
        return float(x -(-5))
    elif x < -5:
        return float((x + 5) * -1)
    else:
        return float(0)


def round_up_to_odd(f: int | float) -> float:
    f = int(np.ceil(f))
    return float(f + 1 if f % 2 == 0 else f)


def default_colors(c: Crosshair) -> None:
    if c.color == 1:
        c.blue = 0
        c.red = 0
        c.green = 255
    if c.color == 2:
        c.blue = 0
        c.red = 255
        c.green = 255
    if c.color == 3:
        c.blue = 255
        c.red = 0
        c.green = 0
    if c.color == 4:
        c.blue = 255
        c.red = 0
        c.green = 255


def create_image(c: Crosshair) -> object:
    img = Image.new('RGBA', (WIDTH, HEIGHT), (255, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    g = generate_crosshair_coordinates()

    if c.color != 5:
        default_colors(c)

    if c.thickness < 1:
        c.thickness = 1

    SIZE = 2 * c.size
    THICKNESS = round(2 * c.thickness) // 2
    GAP = 2 * map_gap_value(c.gap)
    GAP = round_up_to_odd(GAP)
    SIZE = round_up_to_odd(SIZE)
    THICKNESS = floor(round_up_to_odd(THICKNESS))

    if c.has_outline:
        draw.rectangle((g.left_outline(THICKNESS, SIZE, GAP)), fill=('black'))
        draw.rectangle((g.top_outline(THICKNESS, SIZE, GAP)), fill=('black'))
        draw.rectangle((g.right_outline(THICKNESS, SIZE, GAP)), fill=('black'))
        draw.rectangle((g.bottom_outline(THICKNESS, SIZE, GAP)), fill=('black'))
        draw.rectangle((g.dot_outline(THICKNESS)), fill=('black')) if c.has_center_dot else None

    draw.rectangle((g.left(THICKNESS, SIZE, GAP)), fill=(c.red, c.green, c.blue, c.alpha))
    draw.rectangle((g.top(THICKNESS, SIZE, GAP)), fill=(c.red, c.green, c.blue, c.alpha))
    draw.rectangle((g.right(THICKNESS, SIZE, GAP)), fill=(c.red, c.green, c.blue, c.alpha))
    draw.rectangle((g.bottom(THICKNESS, SIZE, GAP)), fill=(c.red, c.green, c.blue, c.alpha))
    draw.rectangle((g.dot(THICKNESS)), fill=(c.red, c.green, c.blue, c.alpha)) if c.has_center_dot else None

    img.save('crosshair.png', 'PNG')
    return img


def main():
    c = Crosshair()
    create_image(c)


if __name__ == '__main__':
    main()