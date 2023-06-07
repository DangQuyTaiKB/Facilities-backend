from doctest import master
from functools import cache
from DBDefinitions import BaseModel, FacilityModel, FacilityTypeModel, UserModel

import uuid
import random
import json
import os

# Lấy đường dẫn tuyệt đối của tệp Python hiện tại
current_directory = os.path.dirname(os.path.abspath(__file__))

# Kết hợp đường dẫn tuyệt đối với tên tệp JSON
json_file_path_1 = os.path.join(current_directory, 'kasarnaCP.geojson')
json_file_path_2 = os.path.join(current_directory, 'kasarnaCP.geojson')

# Đọc dữ liệu từ tệp JSON
with open (json_file_path_1,"r") as file:
    kasarnaCP= json.load(file)
with open (json_file_path_2,"r") as f:
    kasarnaJB= json.load(f)
    
database=[kasarnaCP,kasarnaJB]

from functools import cache
from sqlalchemy.future import select
from datetime import date, timedelta

def singleCall(asyncFunc):
    """Dekorator, ktery dovoli, aby dekorovana funkce byla volana (vycislena) jen jednou. Navratova hodnota je zapamatovana a pri dalsich volanich vracena.
       Dekorovana funkce je asynchronni.
    """
    resultCache = {}
    async def result():
        if resultCache.get('result', None) is None:
            resultCache['result'] = await asyncFunc()
        return resultCache['result']
    return result

###########################################################################################################################
#
# zde definujte sve funkce, ktere naplni random data do vasich tabulek
#
###########################################################################################################################
def randomUUID(limit):
    random_uuid = [uuid.uuid4() for _ in range(limit)]
    return random_uuid

def randomFacilityAddress():
    names = ["Adresa1", "Adresa2", "Adresa3", "Adresa4", "Adresa5"]
    return random.choice(names)

def randomCapacity():
    capacity=random.randint(1,100)
    return capacity

def randomLastChange():
    base = date(2025, 1, 1)
    return base + timedelta(days=random.randint(1,30))

def randomStartDate():
    base = date(2023, 1, 1)
    return base + timedelta(days=random.randint(1,30))

def randomEndDate():
    base = date(2024, 1, 1)
    return base + timedelta(days=random.randint(1,30))

def randomManagerID():
    managerUUID="7d6d341e-02fe-45dd-b103-b3c15a903fb8"
    return managerUUID

facilitytypesIDs = randomUUID(2)
def determineFacilityTypes():
    """Definuje typy facilities"""
    facilityTypes = [ 
        {'id': facilitytypesIDs[0], 'name':'Areal'},
        {'id': facilitytypesIDs[1], 'name':'Budova'}
    ]
    return facilityTypes

def CreateSubArea(master_id, facility_type,feature):
    return {
        'id':feature["id"],
        'name':feature["properties"]["name"],
        'address':randomFacilityAddress(),
        'label':feature["properties"]["building"],
        'capacity':randomCapacity(),
        'geometry':feature["geometry"]["type"],
        'geolocation':feature["geometry"]["coordinates"],
        'facilitytype_id':facilitytypesIDs[facility_type],
        'manager_id':randomManagerID(),
        'lastchange':randomLastChange(),
        'valid': True,
        'startdate':randomStartDate(),
        'enddate':randomEndDate(),
        'master_facility_id':master_id
        }


def createDataStructureFacilities():
    
    areas=[]
    buildings=[]
    
    for i in range(2):
        data=database[i]
        areas.append(CreateSubArea(data["features"][0]["id"],0,data["features"][0]))
        for j in range(1,len(data["features"])):
            buildings.append(CreateSubArea(data["features"][0]["id"],1,data["features"][j]))
           
    facilities=[]
    facilities=areas+buildings
    return facilities

def createDataStructureFacilityTypes():
    facilityTypes=determineFacilityTypes()
    return facilityTypes

async def randomDataStructure(session):
    """asembly of facilities data for query      
    """
    facilityTypes = createDataStructureFacilityTypes()
    facilityTypesToAdd=[FacilityTypeModel(**record) for record in facilityTypes]
    async with session.begin():
        session.add_all(facilityTypesToAdd)
    await session.commit()

    facilities = createDataStructureFacilities()
    facilitiesToAdd=[FacilityModel(**record)for record in facilities]
    async with session.begin():
        session.add_all(facilitiesToAdd)
    await session.commit()
    

