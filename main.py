import json

# c = Census('60602aa74fd360f49c530acf9b65cc20408c1512')
# POPULATION = 'B02001_001E'
WHITE = 'B02001_002E'
BLACK = 'B02001_003E'
NATIVE = 'B02001_004E'
ASIAN = 'B02001_005E'
PACIFIC_ISLANDER = 'B02001_005E'
# block_group = c.acs5.state_county(('NAME', WHITE, BLACK, NATIVE, ASIAN, PACIFIC_ISLANDER, POPULATION), states.CA.fips,
#                                   '*')
# pprint(block_group)
# with open("California.json", "w") as outfile:
#     json.dump(block_group, outfile)
black_total = 0
white_total = 0
data: dict
with open('California.json', 'r') as f:
    data = json.load(f)
for county in data:
    black_total += county[BLACK]
    white_total += county[WHITE]
print(black_total)
print(white_total)
index = 0
for county in data:
    index += abs(county[WHITE] / white_total - county[BLACK] / black_total)
index *= 0.5*100
print(index)
