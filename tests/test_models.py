import pytest
from src.electronics.models import NetworkObject, Country
from faker import Faker
from django_countries import countries
from random import choice, randrange


def get_random_word(max_size):
    word = Faker().word().capitalize()
    while len(word) >= max_size:
        word = Faker().word().capitalize()
    return word


def random_country():
    return Country.objects.create(
        country=choice(list(countries))
    )


@pytest.mark.django_db
def test_save_networkobject():
    """
    Check if there is possible to create a wrong order
    of objects.
    """
    for i in range(3):
        object_factory = NetworkObject(
            type=i,
            name=get_random_word(50),
            mail='test@maiil.ru',
            location_country=random_country(),
            location_street=get_random_word(250),
            location_house=randrange(1, 100),
            debt=randrange(0, 100),
        )
        if i != 0:
            object_factory.supplier = NetworkObject.objects.filter(type=i-1)[0]
        object_factory.save()
    assert NetworkObject.objects.all().count() == 3

    with pytest.raises(ValueError):
        object_factory_wrong = NetworkObject(
            type=0,
            name=get_random_word(50),
            mail='test@maiil.ru',
            location_country=random_country(),
            location_street=get_random_word(250),
            location_house=randrange(1, 100),
            supplier=NetworkObject.objects.filter(type=1)[0],
            debt=randrange(0, 100),
        )
        object_factory_wrong.save()


