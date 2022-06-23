from sqlalchemy.orm import Session
import App.model


def get_postcode(db: Session, postcode: str):
    return db.query(App.model.Address).filter(App.model.Address.fullpostcode == postcode.upper()).all()


def get_postcode_from_outcode(db: Session, o: str):
    return db.query(App.model.Address).filter(App.model.Address.fullpostcode.contains(f'{o.upper()}%')).offset(0).limit(30).all()

# % at the start: anything before it but must have term
# % at the end: has to start with this
# % Both ends: don't care where the data is in the term
