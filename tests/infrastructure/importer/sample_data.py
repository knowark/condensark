# Taken from: https://graphql-core-next.readthedocs.io/en/latest/
# usage/resolvers.html

# Humans

luke = dict(
    id='1000', name='Luke Skywalker', homePlanet='Tatooine',
    friends=['1002', '1003', '2000', '2001'], appearsIn=[4, 5, 6])

vader = dict(
    id='1001', name='Darth Vader', homePlanet='Tatooine',
    friends=['1004'], appearsIn=[4, 5, 6])

han = dict(
    id='1002', name='Han Solo', homePlanet=None,
    friends=['1000', '1003', '2001'], appearsIn=[4, 5, 6])

leia = dict(
    id='1003', name='Leia Organa', homePlanet='Alderaan',
    friends=['1000', '1002', '2000', '2001'], appearsIn=[4, 5, 6])

tarkin = dict(
    id='1004', name='Wilhuff Tarkin', homePlanet=None,
    friends=['1001'], appearsIn=[4])

human_data = {
    '1000': luke, '1001': vader, '1002': han, '1003': leia, '1004': tarkin}

# Droids

threepio = dict(
    id='2000', name='C-3PO', primaryFunction='Protocol',
    friends=['1000', '1002', '1003', '2001'], appearsIn=[4, 5, 6])

artoo = dict(
    id='2001', name='R2-D2', primaryFunction='Astromech',
    friends=['1000', '1002', '1003'], appearsIn=[4, 5, 6])

droid_data = {
    '2000': threepio, '2001': artoo}
