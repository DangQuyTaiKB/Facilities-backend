from typing import List, Union, Optional
import typing
from unittest import result
import strawberry as strawberryA
import uuid
import datetime
from contextlib import asynccontextmanager


@asynccontextmanager
async def withInfo(info):
    asyncSessionMaker = info.context['asyncSessionMaker']
    async with asyncSessionMaker() as session:
        try:
            yield session
        finally:
            pass

def AsyncSessionFromInfo(info):
    return info.context['session'] 

def AsyncSessionMakerFromInfo(info):
    return info.context['asyncSessionMaker']

###########################################################################################################################
#
# zde definujte sve GQL modely
# - nove, kde mate zodpovednost
# - rozsirene, ktere existuji nekde jinde a vy jim pridavate dalsi atributy
#
###########################################################################################################################
#FACILITIES
from gql_facilities.GraphResolvers import resolveFacilityById, resolveFacilityPage, resolveInsertFacility, resolveUpdateFacility
@strawberryA.federation.type(description="""Type for query root""")
class FacilityGQLModel:
    """class representing facility model
    
    Attributes
    ----------
    id: UUID
        id of facility
    name: str
        name of facility
    address: str
        address of facility
    label: str
        label of facility
    capacity: int
        capacity of  facility
    geometry: str
        geometry  of  facility
    geolocation: str
        geolocation of  facility
    facilityType: FacilityTypeGQLModel
        facility type  of  facility
    manager_id: UserGQLModel
        manager ID  of  facility
    lastchange: datetime.datetime
        lastchange  of  facility
    valid: bool
        is facility still valid?
    startdate: datetime.datetime
        when was facility created
    enddate: datetime.datetime
        when was facility ended
    editor: FacilityEditorGQLModel
        editor for facility
    """
    #id
    @strawberryA.field(description="""primary key/facility id""")
    def id(self) -> strawberryA.ID:
        return self.id
    #name
    @strawberryA.field(description="""Facility name""")
    def name(self) -> str:
        return self.name
    #address
    @strawberryA.field(description="""Facility address""")
    def address(self) -> str:
        return self.address
    #label
    @strawberryA.field(description="""Facility label""")
    def label(self) -> str:
        return self.label  
    #capacity
    @strawberryA.field(description="""Facility capacity""")
    def capacity(self) -> int:
        return self.capacity   
    #geometry
    @strawberryA.field(description="""Facility geometry""")
    def geometry(self) -> str:
        return self.geometry  
    #geolocation
    @strawberryA.field(description="""Facility geolocation""")
    def geolocation(self) -> str:
        return self.geolocation 
    #facilitytype_id->facilitytype table
    @strawberryA.field(description="""Project type of project""")
    async def facilityType(self, info: strawberryA.types.Info) -> 'FacilityTypeGQLModel':
        async with withInfo(info) as session:
            result = await resolveFacilityTypeById(session, self.facilityType_id)
            return result
    #manager_id->user table  ????je správně
    @strawberryA.field(description="""user model from ug_container""")
    async def manager_id(self) -> 'UserGQLModel':
        return UserGQLModel(id=self.user_id)
    #master_facility_id->??správně když foreign
    @strawberryA.field(description="""master-facility id""")
    def master_facility_id(self) -> strawberryA.ID:
        return self.master_facility_id
    #lastchange
    @strawberryA.field(description="""is the membership still valid""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange
    #valid
    @strawberryA.field(description="""is the facility still valid""")
    def valid(self) -> bool:
        return self.valid
    #startdate
    @strawberryA.field(description="""is the membership still valid""")
    def startdate(self) -> datetime.datetime:
        return self.startdate
    #enddate
    @strawberryA.field(description="""is the membership still valid""")
    def enddate(self) -> datetime.datetime:
        return self.enddate
    #editor
    @strawberryA.field(description="""Returns facility editor""")
    async def editor(self, info: strawberryA.types.Info) -> Union['FacilityEditorGQLModel', None]:
        return self
    
#FACILITY UPDATE
@strawberryA.input(description="""Entity representing a facility update""")
class FacilityUpdateGQLModel:
    """class representing facility model
    
    Attributes
    ----------
    name: str
    address: str
    label: str
    capacity: int
    geometry: str
    geolocation: str
    facilityType: FacilityTypeGQLModel
    manager_id: UserGQLModel
    lastchange: datetime.datetime
    valid: bool
    startdate: datetime.datetime
    enddate: datetime.datetime
    editor: FacilityEditorGQLModel
    """
    lastchange: datetime.datetime
    name:  Optional[str] = None
    address:  Optional[str] = None
    label:  Optional[str] = None
    capacity:  Optional[int] = None
    geometry:  Optional[str] = None
    geolocation:  Optional[str] = None
    facilitytype_id: Optional[uuid.UUID] = None
    manager_id: Optional[uuid.UUID] = None
    valid: Optional[bool] = None
    start_date: Optional[datetime.date] = None 
    end_date: Optional[datetime.date] = None 
    master_facility_id: Optional[uuid.UUID] = None

#FACILITY EDITOR
@strawberryA.federation.type(keys=["id"], description="""Entity representing an editable facility""")
class FacilityEditorGQLModel:
    """class representing facility update model
    
    Attributes
    ----------
    id: UUID
        id of facility to edit
    result: str
        was edit succesfull?

    Methods
    -------
    resolve_reference(class, info:strawberry.type.Info, id:strawberry.ID)
        resolves refence and pasees execution context
    facility(self, info: strawberryA.types.Info)
        resolves facility by its id
    update(self, info: strawberryA.types.Info, data: FacilityUpdateGQLModel)
        updates facility
    invalidate_facility(self, info: strawberryA.types.Info)
        invalidates facility
    """
    id: strawberryA.ID = None
    result: str = None

    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        async with withInfo(info) as session:
            result = await resolveFacilityById(session, id)
            result._type_definition = cls._type_definition # little hack :)
            return result

    @strawberryA.field(description="""Entity primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""Result status of update operation""")
    def result(self) -> str:
        return self.result 

    @strawberryA.field(description="""Result of update operation""")
    async def facility(self, info: strawberryA.types.Info) -> FacilityGQLModel:
        async with withInfo(info) as session:
            result = await resolveFacilityById(session, id)
            return result

    @strawberryA.field(description="""Updates the facility data""")
    async def update(self, info: strawberryA.types.Info, data: FacilityUpdateGQLModel) -> 'FacilityEditorGQLModel':
        lastchange = data.lastchange
        async with withInfo(info) as session:
            await resolveUpdateFacility(session, id=self.id, data=data)
            if lastchange == data.lastchange:
                # no change
                resultMsg = "ok"
            else:
                resultMsg = "fail"
            result = FacilityEditorGQLModel()
            result.id = self.id
            result.result = resultMsg
            return result    

    @strawberryA.field(description="""Invalidate facility""")
    async def invalidate_facility(self, info: strawberryA.types.Info) -> 'FacilityGQLModel':
        async with withInfo(info) as session:
            facility = await resolveFacilityById(session, self.id)
            facility.valid = False
            await session.commit()
            return facility
    
        
   
#FACILITY TYPE    
from gql_facilities.GraphResolvers import resolveFacilityTypeById, resolveFacilityTypeAll, resolveInsertFacilityType, resolveUpdateFacilityType
@strawberryA.federation.type(keys=["id"], description="""Type for query root""")
class FacilityTypeGQLModel:
    """class representing facility update model
    
    Attributes
    ----------
    id: UUID
        id of facility type
    name: str
        name of facility tape
    """
    #id
    @strawberryA.field(description="""primary key/facility type id""")
    def id(self) -> strawberryA.ID:
        return self.id
    
    #type name
    @strawberryA.field(description="""Facility type name""")
    def name(self) -> str:
        return self.name

#USER
@strawberryA.federation.type(extend=True, keys=["id"])
class UserGQLModel:
    """class representing facility update model
    
    Attributes
    ----------
    id: UUID
        id of facility to edit

    Methods
    -------
    resolve_reference(class,  id:strawberry.ID)
        resolves refence to user
    """

    id: strawberryA.ID = strawberryA.federation.field(external=True)

    @classmethod
    def resolve_reference(cls, id: strawberryA.ID):
        return UserGQLModel(id=id)
    


###########################################################################################################################
#
# zde definujte svuj Query model
#
###########################################################################################################################
#from gql_facilities.GraphResolvers import resolveFacilityById, resolveFacilityPage
from gql_facilities.DBFeeder import randomDataStructure
@strawberryA.type(description="""Type for query root""")
class Query:
    """class representing query
    
    Methods
    -------
    say_hello(self, info: strawberryA.types.Info, id: uuid.UUID)
        just to test things out
    facility_by_id(self, info: strawberryA.types.Info, id: uuid.UUID)
        query for facility by id and its atributes
    facility_page(self, info: strawberryA.types.Info)
        list of facilities, default limit 1000
    facility_type_page(self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10)
        list of facility types, default start on 0 and for 10 entries
    randomFacility(self, name: str, info: strawberryA.types.Info)
        feeds semi-random data
    """
       
    @strawberryA.field(description="""Finds an workflow by their id""")
    async def say_hello(self, info: strawberryA.types.Info, id: uuid.UUID) -> Union[str, None]:
        
        result = f'Hello {id}'
        return result

    @strawberryA.field(description="""Finds an facility by id""")
    async def facility_by_id(self, info: strawberryA.types.Info, id: uuid.UUID) -> FacilityGQLModel:
        
        result = await resolveFacilityById(AsyncSessionFromInfo(info), id )
        return result

    @strawberryA.field(description="""List of facilities""")
    async def facility_page(self, info: strawberryA.types.Info) -> List[FacilityGQLModel]:
        result = await resolveFacilityPage(AsyncSessionFromInfo(info),0,1000)
        return result

    @strawberryA.field(description="""List of facility types""")
    async def facility_type_page(self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10) -> List[FacilityTypeGQLModel]:
        async with withInfo(info) as session:
            result = await resolveFacilityTypeAll(session, skip, limit)
            return result

    @strawberryA.field(description="""Random facility""")
    async def randomFacility(self, name: str, info: strawberryA.types.Info) -> str:
        newId = await randomDataStructure(AsyncSessionFromInfo(info))#tady druhy arg name
        return "ok"