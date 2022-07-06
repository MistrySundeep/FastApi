from sqlalchemy import Float, Column, String, Integer, Boolean
from App.db import Base, engine


class Address(Base):
    __tablename__ = 'address'

    id = Column(Integer, primary_key=True)
    outcode = Column(String)
    incode = Column(String)
    addresskey = Column(String)
    locality = Column(String)
    thoroughfarekey = Column(String)
    thoroughfaredescriptorkey = Column(String)
    dependentthoroughfarekey = Column(String)
    dependentthoroughfaredescriptorkey = Column(String)
    buildingnumber = Column(String)
    buildingnamekey = Column(String)
    subbuildingnamekey = Column(String)
    numberofhouseholds = Column(Float)
    organisationkey = Column(String)
    postcodetype = Column(String)
    concatenationindicator = Column(String)
    deliverypointsuffix = Column(String)
    smalluserorganisationindicator = Column(String)
    poboxnumber = Column(String)
    fullpostcode = Column(String)


class BuildingNames(Base):
    __tablename__ = 'buildingnames'

    buildingnamekey = Column(String, primary_key=True)
    buildingname = Column(String)


class Localities(Base):
    __tablename__ = 'localities'

    localitykey = Column(String, primary_key=True)
    filler1 = Column(String)
    filler2 = Column(String)
    posttown = Column(String)
    dependentlocality = Column(String)
    doubledependentlocality = Column(String)


class MailSort(Base):
    __tablename__ = 'mailsort'

    outcode = Column(String, primary_key=True)
    sector = Column(String)
    residualidentifier = Column(String)
    directwithinresidualindicator = Column(String)


class Organisations(Base):
    __tablename__ = 'organisations'

    organisationkey = Column(String, primary_key=True)
    postcodetype = Column(String)
    organisationame = Column(String)
    departmentname = Column(String)
    filler = Column(String)


class SubBuildingNames(Base):
    __tablename__ = 'subbuildingnames'

    subbuildingnamekey = Column(String, primary_key=True)
    subbuildingname = Column(String)


class Thoroughfares(Base):
    __tablename__ = 'thoroughfares'

    thoroughfarekey = Column(String, primary_key=True)
    thoroughfarename = Column(String)


class ThoroughfareDescriptor(Base):
    __tablename__ = 'thoroughfaredescriptors'

    thoroughfaredescriptorkey = Column(String, primary_key=True)
    thoroughfaredescriptor = Column(String)
    approvedabbreviation = Column(String)


class APIUsers(Base):
    __tablename__ = 'apiusers'

    userid = Column(Integer, primary_key=True)
    companyid = Column(Integer)
    authemail = Column(String)
    authkey = Column(String)
    enabled = Column(Boolean)


Base.metadata.create_all(engine)
