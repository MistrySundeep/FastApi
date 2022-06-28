from pydantic import BaseModel


# BASE CLASSES
class AddressBase(BaseModel):
    id: int
    outcode: str
    incode: str
    addresskey: str
    locality: str
    thoroughfarekey: str
    thoroughfaredescriptorkey: str
    dependentthoroughfarekey: str
    dependentthoroughfaredescriptorkey: str
    buildingnumber: str
    buildingnamekey: str
    subbuildingnamekey: str
    numberofhouseholds: float
    organisationkey: str
    postcodetype: str
    concatenationindicator: str | None = None
    deliverypointsuffix: str
    smalluserorganisationindicator: str | None = None
    poboxnumber: str | None = None
    fullpostcode: str


class BuildingNameBase(BaseModel):
    buildingnamekey: str
    buildingname: str


class LocalitiesBase(BaseModel):
    localitykey: str
    filler1: str | None = None
    filler2: str | None = None
    posttown: str
    dependentlocality: str
    doubledependentlocality: str


class MailSortBase(BaseModel):
    outcode: str
    sector: str
    residualidentifier: str
    directwithinresidualindicator: str


class OrganisationsBase(BaseModel):
    organisationkey: str
    postcodetype: str
    organisationname: str
    departmentname: str
    filler: str


class SubBuildingNamesBase(BaseModel):
    subbuildingnamekey: str
    subbuildingname: str


class ThoroughfaresBase(BaseModel):
    thoroughfarekey: int
    thoroughfarename: str


class ThoroughfareDescriptorBase(BaseModel):
    thoroughfaredescriptorkey: str
    thoroughfaredescriptor: str
    approvedabbreviation: str


# Class Configs
class Address(AddressBase):
    class Config:
        orm_mode = True


class BuildingName(BuildingNameBase):
    class Config:
        orm_mode = True


class Localities(LocalitiesBase):
    class Config:
        orm_mode = True


class MailSort(MailSortBase):
    class Config:
        orm_mode = True


class Organisations(OrganisationsBase):
    class Config:
        orm_mode = True


class SubBuildingNames(SubBuildingNamesBase):
    class Config:
        orm_mode = True


class ThoroughfareDescriptor(ThoroughfareDescriptorBase):
    class Config:
        orm_mode = True


class Thoroughfare(ThoroughfaresBase):
    class Config:
        orm_mode = True
