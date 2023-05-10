from doctest import master
from functools import cache
from gql_facilities.DBDefinitions import BaseModel, FacilityModel, FacilityTypeModel, UserModel

import uuid
import random
import itertools

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

def randomFacilityName():
    names = ["Rohlik", "Kounicovka", "Zeme Oz", "Zemeplocha", "Mordor"]
    return random.choice(names)

def randomFacilityAddress():
    names = ["Adresa1", "Adresa2", "Adresa3", "Adresa4", "Adresa5"]
    return random.choice(names)

def randomFacilityLabel():
    names = ["Label1", "Label2", "Label3", "Label4", "Label5"]
    return random.choice(names)

def randomCapacity():
    capacity=random.randint(1,100)
    return capacity

def randomFacilityGeometry():
    names = ["Geometry1", "Geometry2", "Geometry3", "Geometry4", "Geometry5"]
    return random.choice(names)

def randomFacilityGeolocation():
    names = ["Geolocation1", "Geolocation2", "Geolocation3", "Geolocation4", "Geolocation5"]
    return random.choice(names)

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

facilitytypesIDs = randomUUID(4)
def determineFacilityTypes():
    """Definuje typy facilities"""
    facilityTypes = [ 
        {'id': facilitytypesIDs[0], 'name':'Areal', },
        {'id': facilitytypesIDs[1], 'name':'Budova'},
        {'id': facilitytypesIDs[2], 'name':'Patro'},
        {'id': facilitytypesIDs[3], 'name':'Mistnost'},
    ]
    return facilityTypes

areaUUIDs= randomUUID(2)
buildingUUIDs=randomUUID(4)
floorUUIDs=randomUUID(8)
roomUUID=randomUUID(16)



def randomSubArea(id, master_id, facility_type):
    """asembly of random facility     

        Parameters
        ----------
        id: UUID
            id of facility
        master_id: UUID
            id of master facility
        facility_type: UUID
            id of type of facility

        Returns
        ---------
        1 random facility    
    """
    return {
        'id':id,
        'name':randomFacilityName(),
        'address':randomFacilityAddress(),
        'label':randomFacilityLabel(),
        'capacity':randomCapacity(),
        'geometry':randomFacilityGeometry(),
        'geolocation':randomFacilityGeolocation(),
        'facilitytype_id':facilitytypesIDs[facility_type],
        'manager_id':randomManagerID(),
        'lastchange':randomLastChange(),
        'valid': True,
        'startdate':randomStartDate(),
        'enddate':randomEndDate(),
        'master_facility_id':master_id
        }


def createDataStructureFacilities():
    """creates list of facilities
        Returns
        ---------
        32 random facilities by deafult
    """
    areas=[]
    areasindex=0
    buildings=[]
    indexbuilding=0
    floors=[]
    indexfloors=0
    rooms=[]
    indexrooms=0
    for id in areaUUIDs:
        areas.append(randomSubArea(id, id,0))
        for x in range(2):
            buildings.append(randomSubArea(buildingUUIDs[indexbuilding], areaUUIDs[areasindex],1))
            for x in range(2):
                floors.append(randomSubArea(floorUUIDs[indexfloors],buildingUUIDs[indexbuilding],2))
                for x in range(2):
                    rooms.append(randomSubArea(roomUUID[indexrooms], floorUUIDs[indexfloors], 3))
                    indexrooms+=1
                indexfloors+=1
            indexbuilding+=1
        areasindex+=1
    facilities=[]
    facilities=areas+buildings+floors+rooms
    return facilities

def createDataStructureFacilityTypes():
    """creates random facility type list     

        Returns
        ---------
        4 random facility types
    """
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
    