from sqlalchemy.exc import IntegrityError

from lib.factory import db
from lib.utils import setattrs

from .models import Location, City, LocationException, CityException


def save_city(instance=None, **kwargs):
    """
    Creates or updates existing city
    :param instance: Instance of City to update
    :param kwargs:
    :return: City
    """
    if instance:
        setattrs(instance, **kwargs, ignore_nulls=True)
    else:
        instance = City(**kwargs)

    db.session.add(instance)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        if City.query.filter_by(name=instance.name).first():
            raise CityException('Duplicate name')
        raise
    return instance


def save_location(instance=None, **kwargs):
    """
    Creates or updates location
    :param instance: Instance of location to update
    :param kwargs:
    :return: Location
    """
    if instance:
        setattrs(instance, **kwargs, ignore_nulls=True)
    else:
        instance = Location(**kwargs)

    db.session.add(instance)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        if Location.query.filter_by(city_id=instance.city_id, address=instance.address):
            raise LocationException('Duplicate location')
        raise
    return instance
