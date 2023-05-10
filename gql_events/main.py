from typing import List
from urllib.request import Request

import typing
import strawberry as strawberryB

def randomEvent(id = 1):
    return {'id': id, 'name': f'Event({id})', 'users': [{'id': "3edba4da-d136-42d8-9f65-2e63e3e9d3f4"}]}

def randomUser(id = 1):
    return {'id': id, 'name': 'John', 'surname': 'Leon', 'groups': [{'id': 1}]}

def resolveDictField(self, info: strawberryB.types.Info) -> str:
    return self[info.field_name]



def randomCampus(id=1):
    return{'id':id, 'name':'Campus_one','adress':'CampusOne_adress','managerID':'1'} 

def randomBuilding(id=1):
    return{'id':id, 'campusID':'1', 'name':'Building_one','managerID':'1'} 

def randomFloor(id=1):
    return{'id':id,'buildingID':'1', 'name':'Floor_one','managerID':'1'} 

def randomRoom(id=1):
    return{'id':id,'floorID':'1', 'name':'Room_one','managerID':'1'} 
 

"""testy22"""
""" @strawberryB.federation.type(extend=True, keys=["id"])
class UserGQLModel:

    id: strawberryB.ID = strawberryB.federation.field(external=True)

    @strawberryB.field
    def events(self) -> typing.List['EventGQLModel']:
        return [randomEvent(id) for id in range(10)]

#    @classmethod
#    def resolve_reference(cls, id: strawberryB.ID):
        # here we could fetch the book from the database
        # or even from an API
#        return UserGQLModel(id=id)

@strawberryB.federation.type(keys=["id"])
class EventGQLModel:

    @strawberryB.field
    def id(self) -> str:
        return self['id']

    @strawberryB.field
    def name(self) -> str:
        return self['name']

    @strawberryB.field
    def users(self) -> typing.List['UserGQLModel']:
        return [randomUser(user['id']) for user in self['users']] """


""" return{'id':id, 'name':'Campus_one','adress':'CampusOne_adress','managerID':'1'} """
@strawberryB.federation.type(keys=["id"])
class CampusGQLModel:

    @strawberryB.field
    def id(self) -> str:
        return self['id']

    @strawberryB.field
    def name(self) -> str:
        return self['name']

    @strawberryB.field
    def adress(self) -> str:
        return self['adress']
    
    @strawberryB.field
    def managerID(self) -> str:
        return self['managerID']

""" return{'id':id, 'campusID':'1', 'name':'Building_one','managerID':'1'} """
@strawberryB.federation.type(keys=["id"])
class BuildingGQLModel:

    @strawberryB.field
    def id(self) -> str:
        return self['id']

    @strawberryB.field
    def campusID(self) -> str:
        return self['campusID']

    @strawberryB.field
    def name(self) -> str:
        return self['name']
    
    @strawberryB.field
    def managerID(self) -> str:
        return self['managerID']


"""return{'id':id,'buildingID':'1', 'name':'Floor_one','managerID':'1'} """
@strawberryB.federation.type(keys=["id"])
class FloorGQLModel:

    @strawberryB.field
    def id(self) -> str:
        return self['id']

    @strawberryB.field
    def buildingID(self) -> str:
        return self['buildingID']

    @strawberryB.field
    def name(self) -> str:
        return self['name']
    
    @strawberryB.field
    def managerID(self) -> str:
        return self['managerID']

"""return{'id':id,'floorID':'1', 'name':'Room_one','managerID':'1'}  """
@strawberryB.federation.type(keys=["id"])
class RoomGQLModel:

    @strawberryB.field
    def id(self) -> str:
        return self['id']

    @strawberryB.field
    def floorID(self) -> str:
        return self['floorID']

    @strawberryB.field
    def name(self) -> str:
        return self['name']
    
    @strawberryB.field
    def managerID(self) -> str:
        return self['managerID']
   







@strawberryB.type
class Query:
    _service: typing.Optional[str]
    
    """ @strawberryB.field
    def event_by_id(self, id: str) -> 'EventGQLModel':
        return randomEvent(id) """

    @strawberryB.field
    def campus_by_id(self, id: str) -> 'CampusGQLModel':
        return randomCampus(id)

    @strawberryB.field
    def building_by_id(self, id: str) -> 'BuildingGQLModel':
        return randomBuilding(id)

    @strawberryB.field
    def floor_by_id(self, id: str) -> 'FloorGQLModel':
        return randomFloor(id)

    @strawberryB.field
    def room_by_id(self, id: str) -> 'RoomGQLModel':
        return randomRoom(id)    



from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

def myContext():
    return {'session': None}

graphql_app = GraphQLRouter(
    strawberryB.federation.Schema(query=Query, types=[ CampusGQLModel, BuildingGQLModel, FloorGQLModel, RoomGQLModel]), 
    graphiql = True,
    allow_queries_via_get = True,
    root_value_getter = None,
    context_getter = myContext#None #https://strawberry.rocks/docs/integrations/fastapi#context_getter
)

app = FastAPI()
#app.add_middleware(MyMiddleware)
app.include_router(graphql_app, prefix="/gql")

print('All initialization is done')

@app.get('api/ug_gql')
def hello():
    return {'hello': 'world'}


