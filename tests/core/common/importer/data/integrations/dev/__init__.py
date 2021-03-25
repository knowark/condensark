from .graphql.empty import *
from .graphql.query import Solution, DroidSolution
from .graphql.dataloaders import DroidLoader, EpisodeLoader
from .rest.location import Location


SOLUTIONS = [
    Solution,
    DroidSolution()
]

DATALOADERS = [
    DroidLoader,
    EpisodeLoader
]

LOCATIONS = [
    Location
]
