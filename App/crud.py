from fastapi import Request
from sqlalchemy.orm import Session

import App.model as model


# Returns all data on the chosen postcode from the results of autocomplete
def get_data_on_postcode(db: Session, postcode: str):
    return db.query(model.Address.buildingnumber,
                    model.BuildingNames.buildingname,
                    model.SubBuildingNames.subbuildingname,
                    model.Thoroughfares.thoroughfarename,
                    model.ThoroughfareDescriptor.thoroughfaredescriptor,
                    model.Localities.posttown,
                    model.Localities.dependentlocality,
                    model.Localities.doubledependentlocality,
                    model.Address.outcode,
                    model.Address.incode,
                    model.Address.fullpostcode) \
        .outerjoin(model.Localities, model.Address.locality == model.Localities.localitykey) \
        .outerjoin(model.Thoroughfares, model.Address.thoroughfarekey == model.Thoroughfares.thoroughfarekey) \
        .outerjoin(model.ThoroughfareDescriptor,
                   model.Address.thoroughfaredescriptorkey == model.ThoroughfareDescriptor.thoroughfaredescriptorkey) \
        .outerjoin(model.BuildingNames, model.Address.buildingnamekey == model.BuildingNames.buildingnamekey) \
        .outerjoin(model.SubBuildingNames,
                   model.Address.subbuildingnamekey == model.SubBuildingNames.subbuildingnamekey) \
        .filter(model.Address.fullpostcode == postcode.upper()).order_by(model.Address.buildingnumber,
                                                                         model.BuildingNames.buildingname,
                                                                         model.SubBuildingNames.subbuildingname).distinct().first()


def autocomplete(db: Session, o: str):
    return db.query(model.Address).filter(model.Address.fullpostcode.like(f'{o.upper()}%')).limit(20).all()

    # % at the start: anything before it but must have term
    # % at the end: has to start with this
    # % Both ends: don't care where the data is in the term


# Used in autocomplete to find postcodes that contain the current string in the text field, limits results to 10
def get_potential_address(db: Session, postcode: str):
    return db.query(model.Address.buildingnumber,
                    model.BuildingNames.buildingname,
                    model.Thoroughfares.thoroughfarename,
                    model.ThoroughfareDescriptor.thoroughfaredescriptor,
                    model.Localities.posttown,
                    model.Localities.dependentlocality) \
        .outerjoin((model.Localities, model.Address.locality == model.Localities.localitykey),
                   (model.Thoroughfares, model.Address.thoroughfarekey == model.Thoroughfares.thoroughfarekey),
                   (model.ThoroughfareDescriptor,
                    model.Address.thoroughfaredescriptorkey == model.ThoroughfareDescriptor.thoroughfaredescriptorkey),
                   (model.BuildingNames, model.Address.buildingnamekey == model.BuildingNames.buildingnamekey)).filter(
        model.Address.fullpostcode == postcode.upper()).distinct().all()


def authentication(request: Request, db: Session):
    # Get email/key from request header
    email = request.headers.get('Auth-Email')
    key = request.headers.get('Auth-Key')
    # Do a check to see if those pieces of information exist
    auth_obj = db.query(model.APIUsers.authemail, model.APIUsers.authkey, model.APIUsers.enabled).filter(
        model.APIUsers.authemail == email).first()
    # Then check to see if enabled == True (return this part)
    if auth_obj[0] == email and auth_obj[1] == key and auth_obj[2] is True:
        return True

