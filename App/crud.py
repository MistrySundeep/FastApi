from sqlalchemy.orm import Session

import App.model


# Used for testing purposes, will be removed at a later point
def get_postcode(db: Session, postcode: str):
    return db.query(App.model.Address).filter(App.model.Address.fullpostcode == postcode.upper()).all()


# Returns all data on the chosen postcode from the results of autocomplete
def get_data_on_postcode(db: Session, postcode: str):
    return db.query(App.model.Address.buildingnumber, App.model.BuildingNames.buildingname,
                    App.model.SubBuildingNames.subbuildingname, App.model.Thoroughfares.thoroughfarename,
                    App.model.ThoroughfaresDescriptor.thoroughfaredescriptor, App.model.Localities.posttown,
                    App.model.Localities.dependentlocality, App.model.Localities.doubledependentlocality,
                    App.model.Address.outcode, App.model.Address.outcode, App.model.Address.fullpostcode).outerjoin(
        App.model.Localities, App.model.Address.locality == App.model.Localities.localitykey).outerjoin(
        App.model.Thoroughfares,
        App.model.Address.thoroughfarekey == App.model.Thoroughfares.thoroughfarekey).outerjoin(
        App.model.ThoroughfaresDescriptor,
        App.model.Address.thoroughfaredescriptorkey == App.model.ThoroughfaresDescriptor.thoroughfaredescriptorkey).outerjoin(
        App.model.BuildingNames, App.model.Address.buildingnamekey == App.model.BuildingNames.buildingname).outerjoin(
        App.model.SubBuildingNames,
        App.model.Address.subbuildingnamekey == App.model.SubBuildingNames.subbuildingnamekey).filter(
        App.model.Address.fullpostcode == postcode.upper()).order_by(App.model.Address.buildingnumber,
                                                                     App.model.BuildingNames.buildingname,
                                                                     App.model.SubBuildingNames.subbuildingname).distinct().first()


# Used in autocomplete to find postcodes that contain the current string in the text field, limits results to 50
def get_postcode_from_outcode(db: Session, o: str):
    return db.query(App.model.Address).filter(App.model.Address.fullpostcode.contains(f'{o.upper()}%')).offset(
        0).limit(
        50).all()

    # % at the start: anything before it but must have term
    # % at the end: has to start with this
    # % Both ends: don't care where the data is in the term

# return db.query(App.model.Address.outcode, App.model.Address.incode,
#                 App.model.Address.addresskey,
#                 App.model.Address.locality, App.model.Address.thoroughfarekey,
#                 App.model.Address.thoroughfaredescriptorkey,
#                 App.model.Address.dependentthoroughfarekey, App.model.Address.dependentthoroughfaredescriptorkey,
#                 App.model.Address.buildingnumber,
#                 App.model.Address.buildingnamekey, App.model.Address.subbuildingnamekey,
#                 App.model.Address.numberofhouseholds,
#                 App.model.Address.organisationkey,
#                 App.model.Address.postcodetype, App.model.Address.concatenationindicator,
#                 App.model.Address.deliverypointsuffix,
#                 App.model.Address.smalluserorganisationindicator,
#                 App.model.Address.poboxnumber, App.model.Address.fullpostcode).filter(App.model.Address.fullpostcode == postcode.upper()).first()
