import os

from census import Census
from dotenv import load_dotenv
from pymongo import MongoClient

POPULATION = 'B02001_001E'
HISPANIC = 'B03002_012E'
BLACK_HISPANIC = 'B03002_014E'
BLACK = 'B02001_003E'

# black +  hispanic - black and hispanic
# black or hispanic

# mongo structure
# us
# info
# key to each state
# states
# info
# each has a key to its counties
# counties
# info
# each has a key to its tracts
# tracts
# info
load_dotenv()
KEY = os.getenv('API_KEY')
MONGO_PSWRD = os.getenv('MONGO_PASSWORD')
c = Census(KEY)

client = MongoClient(
    f"mongodb+srv://kumar:{MONGO_PSWRD}@segregationdata.porcl.mongodb.net/DemographicData?retryWrites=true&w=majority")
db = client.get_database('Test')

counties = db.get_collection("Counties")

states = db.get_collection('States')

blocks_groups = db.get_collection('Block Groups')

united_states = db.get_collection('United States')