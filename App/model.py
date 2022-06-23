from sqlalchemy import Float, Column, String, Integer
from App.db import Base, engine


class Address(Base):
    __tablename__ = 'Address'

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
    smalluserorganisationinidicator = Column(String)
    poboxnumber = Column(String)
    fullpostcode = Column(String)


Base.metadata.create_all(engine)
