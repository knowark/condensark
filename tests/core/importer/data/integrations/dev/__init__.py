from .graphql.empty import *
from .graphql.query import Solution
from .graphql.dataloaders import DroidLoader, EpisodeLoader
from .rest.location import Location


SOLUTIONS = [
    Solution
]

DATALOADERS = [
    DroidLoader,
    EpisodeLoader
]

LOCATIONS = [
    Location
]
