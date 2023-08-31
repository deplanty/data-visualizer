class Color:
    """
    A color is a tuple with R, G, B from [0.0 - 1.0].
    It has an alpha value from [0.0 - 1.0].
    """

    def __init__(self, rgb:tuple=(1.0, 1.0, 1.0), alpha:float=1, max_int_byte=1):
        self._rgb = rgb
        self._alpha = alpha
        self._max_int_byte = max_int_byte
        self._max_int_value = 2**(8 * self._max_int_byte) - 1

    # Properties

    @property
    def r(self):
        return self._rgb[0]

    @property
    def r_int(self):
        return self.__to_int(self.r)

    @property
    def g(self):
        return self._rgb[1]

    @property
    def g_int(self):
        return self.__to_int(self.g)

    @property
    def b(self):
        return self._rgb[2]

    @property
    def b_int(self):
        return self.__to_int(self.b)

    @property
    def a(self):
        return self._alpha

    @property
    def a_int(self):
        return self.__to_int(self.a)

    @property
    def rgb(self):
        return (self.r, self.g, self.b)

    @property
    def rgb_int(self):
        return (self.r_int, self.g_int, self.b_int)

    @property
    def rgba(self):
        return (self.r, self.g, self.b, self.a)

    @property
    def rgba_int(self):
        return (self.r_int, self.g_int, self.b_int, self.a_int)

    @property
    def hex(self) -> str:
        return "#" + "".join(self.__to_hex(x) for x in (self.r, self.g, self.b))

    @property
    def ahex(self) -> str:
        return "#" + "".join(self.__to_hex(x) for x in (self.a, self.r, self.g, self.b))

    @property
    def hexa(self) -> str:
        return "#" + "".join(self.__to_hex(x) for x in (self.r, self.g, self.b, self.a))

    # Methods

    def from_int(self, rgb:tuple[int]=(255, 255, 255), alpha:int=255):
        self._rgb = tuple(self.__to_float(x) for x in rgb)
        self._alpha = self.__to_float(alpha)

    # Tools

    def __to_int(self, value:float) -> int:
        return int(value * self._max_int_value)

    def __to_float(self, value:int) -> float:
        return value / self._max_int_value

    def __to_hex(self, value:float) -> str:
        return f"{self.__to_int(value):02x}"


def new(rgb:tuple=(1.0, 1.0, 1.0), alpha:float=1, max_int_byte=1):
    return Color(rgb, alpha, max_int_byte)


def from_rgba_int(rgba:tuple[int]=(255, 255, 255, 255), max_int_byte=1):
    color = Color(max_int_byte=max_int_byte)
    *rgb, alpha = rgba
    color.from_int(rgb, alpha)
    return color



RED = Color((1, 0, 0))
GREEN = Color((0, 1, 0))
BLUE = Color((0, 0, 1))
YELLOW = Color((1, 1, 0))
PURPLE = Color((1, 0, 1))
CYAN = Color((0, 1, 1))



if __name__ == '__main__':
    color = Color((1.0, 0.75, 0.5))
    assert color.rgb == (1.0, 0.75, 0.5)
    assert color.rgb_int == (255, 191, 127)
    assert color.rgba == (1.0, 0.75, 0.5, 1.0)
    assert color.rgba_int == (255, 191, 127, 255)

    assert color.a == 1.0
    assert color.a_int == 255
    assert color.r == 1.0
    assert color.r_int == 255
    assert color.g == 0.75
    assert color.g_int == 191
    assert color.b == 0.5
    assert color.b_int == 127

    assert color.hex == "#ffbf7f"
    assert color.ahex == "#ffffbf7f"
    assert color.hexa == "#ffbf7fff"

    color = Color((0.66, 0.32, 0.75), alpha=0.5, max_int_byte=2)
    assert color.rgba_int == (43_253, 20_971, 49_151, 32_767)
