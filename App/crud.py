from sqlalchemy.orm import Session
import App.model


def get_postcode(db: Session, postcode: str):
    return db.query(App.model.Address).filter(App.model.Address.fullpostcode == postcode.upper()).all()


def get_data_on_postcode(db: Session, postcode: str):
    return db.query(App.model.Address.id, App.model.Address.outcode, App.model.Address.incode,
                    App.model.Address.addresskey,
                    App.model.Address.locality, App.model.Address.thoroughfarekey,
                    App.model.Address.thoroughfaredescriptorkey,
                    App.model.Address.dependentthoroughfarekey, App.model.Address.dependentthoroughfaredescriptorkey,
                    App.model.Address.buildingnumber,
                    App.model.Address.buildingnamekey, App.model.Address.subbuildingnamekey,
                    App.model.Address.numberofhouseholds,
                    App.model.Address.organisationkey,
                    App.model.Address.postcodetype, App.model.Address.concatenationindicator,
                    App.model.Address.deliverypointsuffix,
                    App.model.Address.smalluserorganisationinidicator,
                    App.model.Address.poboxnumber, App.model.Address.fullpostcode).filter(App.model.Address.fullpostcode == postcode.upper()).one()


def get_postcode_from_outcode(db: Session, o: str):
    return db.query(App.model.Address).filter(App.model.Address.fullpostcode.contains(f'{o.upper()}%')).offset(0).limit(
        50).all()

# % at the start: anything before it but must have term
# % at the end: has to start with this
# % Both ends: don't care where the data is in the term
