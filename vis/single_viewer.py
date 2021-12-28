import numpy as np
from math import log10, ceil
from PIL import Image, ImageDraw, ImageFont
from generators.planet_generator import (Celestial, GasGiantPlanet, RockyPlanet,
                                         Star, Blackhole, Asteroid,
                                         PLANET_RADIUS_RANGE, ROCKY_COLOR, GAS_COLOR)

DRAW_FONT = ImageFont.truetype("/Library/fonts/Arial.ttf", 16)

# lower and upper limit of planet drawing sizes in pixel
PLANET_BOUND = (50, 400)
PLANET_BOUND_SAFE_MARGIN = 0.05
# helper variables for planet size calculation
pbound_l = PLANET_BOUND[0] * (1 + PLANET_BOUND_SAFE_MARGIN)
pbound_h = PLANET_BOUND[1] * (1 - PLANET_BOUND_SAFE_MARGIN)
# linear conversion and mapping scale
PK = (pbound_h -pbound_l) / (log10(PLANET_RADIUS_RANGE[1] - log10(PLANET_RADIUS_RANGE[0])))
PB = pbound_l - PK * log10(PLANET_RADIUS_RANGE[0])
def acquire_planet_size(radius: float):
    """Returns diameter of normalzied size.
    """
    return PK * log10(radius) + PB


class CelestialImageDrawer:
    def __init__(self, cele: Celestial):
        self.image = None
        if isinstance(cele, GasGiantPlanet):
            self.image = self.draw_gas(cele)
        elif isinstance(cele, RockyPlanet):
            self.image = self.draw_rocky(cele)
        elif isinstance(cele, Star):
            self.image = self.draw_star(cele)
        elif isinstance(cele, Blackhole):
            self.image = self.draw_blackhole(cele)
        elif isinstance(cele, Asteroid):
            self.image = self.draw_asteroid(cele)
        else:
            raise NotImplementedError('Unknown type parsed for drawing: ' + str(type(cele)))
    
    @staticmethod
    def draw_round_object(diameter: int, color: tuple, info: str = ''):
        im = Image.new('RGBA', (diameter + 1, diameter + 1), (0, 0, 0, 0))
        draw = ImageDraw.Draw(im)
        draw.ellipse((0, 0, diameter, diameter), fill=color, outline=None)
        draw.text((diameter // 2, diameter // 2), info, (255,255,255), font=DRAW_FONT)
        return im

    
    @staticmethod
    def draw_rocky(planet):
        diameter = ceil(acquire_planet_size(planet.radius))
        color = ROCKY_COLOR[planet.surface]
        info = 'Rocky\n' + str(planet.surface)
        return CelestialImageDrawer.draw_round_object(diameter, color, info)

    @staticmethod
    def draw_gas(planet):
        diameter = ceil(acquire_planet_size(planet.radius))
        color = GAS_COLOR[planet.content]
        info = 'Gas\n' + str(planet.content)
        return CelestialImageDrawer.draw_round_object(diameter, color, info)
