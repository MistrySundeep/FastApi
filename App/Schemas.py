from pydantic import BaseModel


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



class Address(AddressBase):
    class Config:
        orm_mode = True