from sqlalchemy import UniqueConstraint

from lib.factory import db


class Location(db.Model):
    __tablename__ = 'locations'
    __table_args__ = (
        UniqueConstraint('address', 'city_id'),
    )

    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(2048), index=True)

    city_id = db.Column(db.Integer, db.ForeignKey('cities.id', ondelete='CASCADE'))
    city = db.relationship('City', foreign_keys=[city_id], uselist=False, lazy='joined', cascade="all, delete")


class City(db.Model):
    __tablename__ = 'cities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, index=True)


class CityException(Exception):
    pass


class LocationException(Exception):
    pass
