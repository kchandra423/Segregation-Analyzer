import json
import os

from census import Census
from dotenv import load_dotenv
from pymongo import MongoClient

POPULATION = 'P1_001N'
HISPANIC = 'P2_002N'
HISPANIC_ADULT = 'P4_002N'
BLACK_NOT_HISPANIC = 'P2_006N'
BLACK_NOT_HISPANIC_ADULT = 'P4_006N'
# hispanic + non hispanic black = black or hispanic

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
# MONGO_PSWRD = os.getenv('MONGO_PASSWORD')
c = Census(KEY)

number = 0
iso_distribution = []
div_distribution = []
chi_distribution = []
residentdiv =[]
residentiso=[]
# client = MongoClient(
#     f"mongodb+srv://kumar:{MONGO_PSWRD}@segregationdata.porcl.mongodb.net/DemographicData?retryWrites=true&w=majority")
# client = MongoClient("mongodb://localhost:27017")
def export(data, name: str):
    with open(f'data/{name}.json', 'w') as fp:
        json.dump(data, fp)