
from ast import Call
from typing import Coroutine, Callable, Awaitable, Union, List
import uuid
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from uoishelpers.resolvers import create1NGetter, createEntityByIdGetter, createEntityGetter, createInsertResolver, createUpdateResolver
from uoishelpers.resolvers import putSingleEntityToDb

from gql_facilities.DBDefinitions import BaseModel

## Nasleduji funkce, ktere lze pouzit jako asynchronni resolvery

###########################################################################################################################
#
# zde si naimportujte sve SQLAlchemy modely
#
###########################################################################################################################

from gql_facilities.DBDefinitions import FacilityTypeModel, FacilityModel

###########################################################################################################################
#
# zde definujte sve resolvery s pomoci funkci vyse
# tyto pouzijete v GraphTypeDefinitions
#
###########################################################################################################################

#facility resolvers
resolveFacilityById = createEntityByIdGetter(FacilityModel)
resolveFacilityPage = createEntityGetter(FacilityModel)
resolveUpdateFacility = createUpdateResolver(FacilityModel)
resolveInsertFacility = createInsertResolver(FacilityModel)

#facility type resolvers
resolveFacilityTypeById = createEntityByIdGetter(FacilityTypeModel)
resolveFacilityTypeAll = createEntityGetter(FacilityTypeModel)
resolveUpdateFacilityType = createUpdateResolver(FacilityTypeModel)
resolveInsertFacilityType = createInsertResolver(FacilityTypeModel)


