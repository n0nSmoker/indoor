from app.devices.utils import save_device, save_contact
from app.locations.utils import save_city, save_location
from app.publishers.utils import save_publisher
from lib.utils import get_random_str


def add_city(name=None):
    return save_city(name=name or get_random_str())


def add_location(city_name=None, address=None):
    city = add_city(name=city_name)
    return save_location(
        address=address or get_random_str(),
        city_id=city.id
    )


def add_device(uid_token=None, **kwargs):
    return save_device(uid_token=uid_token or get_random_str(), **kwargs)


def add_contact(name=None, tel=None, comment=None):
    return save_contact(
        name=name or get_random_str(),
        tel=tel or get_random_str(),
        comment=comment or get_random_str(),
    )


def add_publisher(name=None, comment=None, airtime=None, created_by=None):
    return save_publisher(
        name=name or get_random_str(),
        comment=comment,
        airtime=airtime,
        created_by=created_by
    )
