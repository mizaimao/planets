from abc import ABC, abstractmethod
from dataclasses import dataclass
import numpy as np
from math import pi


PLANET_MASS_RANGE = (7.34767309e22, 2.46766e28) # moon to jupyter x 13
PLANET_MASS_MEAN = 1.8982e+25
PLANET_MASS_STD = 1.0e26
PLANET_MASS_SPLIT = 2.38888e+25 # four times of Earth

PLANET_RADIUS_RANGE = (1737.4, 559288) # moon to jupyter x 8
PLANET_RADIUS_SPLIT = 25484.
PLANET_TYPE = ['GasGiant', 'Rocky']

PLANET_RADIUS_MEAN = (139822., 38226.) # jupyter; 6 times Earth
PLANET_RADIUS_STD = (69911, 19113.) # jupyter; 3 times Earth

ROCKY_PLANET_SURFACES = ['water', 'rock', 'sulfer', 'ammonia']
ROCKY_PLANET_SURFACES_W = [1] * len(ROCKY_PLANET_SURFACES)
ROCKY_PLANET_SURFACES_W_NORM = np.array(ROCKY_PLANET_SURFACES_W) / sum(ROCKY_PLANET_SURFACES_W)


@dataclass
class Celestial(ABC):
    mass: int = 1   # in ton
    radius: int = 1 # in km
    volume = (4/3)*pi*(radius**2)
    density = mass / volume


@dataclass
class Star(Celestial):
    surface_temp: int = 1
    core_temp: int = 1
    def __init__(self, seed):
        self.rng = np.random.RandomState(seed)


@dataclass
class Blackhole(Celestial):
    eh_radius: int = 1


@dataclass
class Asteroid(Celestial):
    def __init__(self, seed):
        self.rng = np.random.RandomState(seed)


@dataclass
class Planet(Celestial):
    surface_temp: int = 1
    core_temp: int = 1
        

@dataclass
class GasGiantPlanet(Planet):
    def __init__(self, content, **kwargs):
        super(Planet, self).__init__(**kwargs)
        self.content = content


@dataclass
class RockyPlanet(Planet):
    def __init__(self, surface, atmosphere, **kwargs):
        super(Planet, self).__init__(**kwargs)
        self.surface = surface
        self.atmosphere = atmosphere


class PlanetGenerator:
    def __init__(self, seed: int = None):
        mass = 1
        radius = 1
        self.rng = np.random.RandomState(seed)
        while not PLANET_MASS_RANGE[0] <= mass <= PLANET_MASS_RANGE[1]:
            mass = self.rng.normal(PLANET_MASS_MEAN, PLANET_MASS_STD)
            
        if mass >= PLANET_MASS_SPLIT:  # gas gaint
            self.built_planet = self.build_gas(mass)
        else:   # rocky
            self.built_planet = self.build_rocky(mass)

            
    def build_rocky(self, mass):
        # radius
        radius = 1
        while not PLANET_RADIUS_RANGE[0] <= radius <= PLANET_RADIUS_SPLIT:
            radius = self.rng.normal(PLANET_RADIUS_MEAN[1], PLANET_RADIUS_MEAN[1])
        # surface
        surface = self.rng.choice(ROCKY_PLANET_SURFACES, p=ROCKY_PLANET_SURFACES_W_NORM)
        # atmosphere
        print(mass)

        return RockyPlanet(mass=mass, radius=radius, surface=surface, atmosphere='chicken atm')


    def build_gas(self, mass):
        # radius
        radius = 1
        while not PLANET_RADIUS_SPLIT <= radius <= PLANET_RADIUS_RANGE[1]:
            print(radius)
            radius = self.rng.normal(PLANET_RADIUS_MEAN[0], PLANET_RADIUS_MEAN[0])

        return GasGiantPlanet(mass=mass, radius=radius, content='chicken')

    def get(self):
        return self.built_planet
