
import math
import random

import pytest
from faker import Faker
from flask import url_for
from flask_jwt_extended import create_access_token
from werkzeug.datastructures import Headers
from werkzeug.security import check_password_hash

from src.i18n.models import i18n_create, I18NLocale, I18NKey, I18NValue
from src.people.models import Person
# from src.people.test_people import create_multiple_people

from .. import db

from .models import Attribute, AttributeSchema, PersonAttribute, PersonAttributeSchema, EnumeratedValue, EnumeratedValueSchema


class RandomLocaleFaker:
    """Generate multiple fakers for different locales."""

    def __init__(self, *locales):
        self.fakers = [Faker(loc) for loc in locales]

    def __call__(self):
        """Return a random faker."""
        return random.choice(self.fakers)


rl_fake = RandomLocaleFaker('en_US', 'es_MX')
fake = Faker()  # Generic faker; random-locale ones don't implement everything.

# ---- Attribute


def flip():
    """Return true or false randomly."""
    return random.choice((True, False))


def add_attribute_type(name, sqla, locale_code):
    type_i18n = f'attribute.type.{name}'

    if not sqla.query(I18NLocale).get(locale_code):
        sqla.add(I18NLocale(code=locale_code, desc='English US'))

    if not sqla.query(I18NKey).get(type_i18n):
        i18n_create(type_i18n, 'en-US',
                    name, description=f"Type {name}")


def add_i18n_code(name, sqla, locale_code, name_i18n):

    if not sqla.query(I18NLocale).get(locale_code):
        sqla.add(I18NLocale(code=locale_code, desc=''))

    try:
        i18n_create(name_i18n, locale_code,
                    name, description=f"Type {name}")
    except:
        # entry is already in value table
        pass

    return name_i18n


def attribute_factory(sqla, name, locale_code='en-US', active=1):
    """Create a fake attribute."""
    name_i18n = f'attribute.name'
    add_i18n_code(name, sqla, locale_code, name_i18n)
    attributes = sqla.query(Attribute).all()
    add_attribute_type('radio', sqla, 'en-US')
    add_attribute_type('check', sqla, 'en-US')
    add_attribute_type('dropdown', sqla, 'en-US')
    add_attribute_type('float', sqla, 'en-US')
    add_attribute_type('integer', sqla, 'en-US')
    add_attribute_type('string', sqla, 'en-US')
    add_attribute_type('date', sqla, 'en-US')

    attribute = {
        'nameI18n': name_i18n,
        'typeI18n': random.choice(Attribute.available_types()),
        'seq': random.randint(5, 15),
        'active': active
    }
    return attribute


def enumerated_value_factory(sqla):
    """Create a fake enumerated value."""
    count = random.randint(5, 15)
    create_multiple_attributes(sqla, 3, 1)
    attributes = sqla.query(Attribute).all()

    value_string = rl_fake().name()
    value_i18n = f'enumerated.{value_string}'

    locale_code = 'en-US'
    if not sqla.query(I18NLocale).get(locale_code):
        sqla.add(I18NLocale(code=locale_code, desc='English US'))

    if not sqla.query(I18NKey).get(value_i18n):
        i18n_create(value_i18n, locale_code,
                    value_string, description=f"Enum Value {value_string}")

    enumerated_value = {
        'attributeId': random.choice(attributes).id,
        'valueI18n': value_i18n,
        'active': flip()
    }
    return enumerated_value


def person_attribute_enumerated_factory(sqla):
    """Create a fake person attribute that is enumerated."""
    # create_multiple_people(sqla, 17)
    create_multiple_attributes(sqla, 5, 1)
    create_multiple_enumerated_values(sqla, 10)
    people = sqla.query(Person).all()
    current_person = random.choice(people)
    enumerated_values = sqla.query(EnumeratedValue).all()
    current_enumerated_value = random.choice(enumerated_values)
    person_attribute = {
        'personId': current_person.id,
        'attributeId': current_enumerated_value.attribute_id,
        'enumValueId': current_enumerated_value.id
    }
    return person_attribute


def person_attribute_string_factory(sqla):
    """Create a fake person attribute that is enumerated."""
    # create_multiple_people(sqla, 17)
    create_multiple_attributes(sqla, 5, 1)
    people = sqla.query(Person).all()
    current_person = random.choice(people)
    nonenumerated_values = sqla.query(Attribute).all()
    current_nonenumerated_value = random.choice(nonenumerated_values)
    person_attribute = {
        'personId': current_person.id,
        'attributeId': current_nonenumerated_value.id,
        'stringValue': rl_fake().first_name()
    }
    return person_attribute


def create_multiple_attributes(sqla, n, active=1):
    """Commit `n` new attributes to the database. Return their IDs."""
    attribute_schema = AttributeSchema()
    new_attributes = []
    for i in range(n):
        valid_attribute = attribute_schema.load(
            attribute_factory(sqla, 'name', 'en-US'))
        new_attributes.append(Attribute(**valid_attribute))
    sqla.add_all(new_attributes)
    sqla.commit()


def create_multiple_enumerated_values(sqla, n):
    """Commit `n` new enumerated values to the database. Return their IDs."""
    enumerated_value_schema = EnumeratedValueSchema(exclude=['id'])
    new_enumerated_value = []
    for i in range(n):
        valid_enumerated_value = enumerated_value_schema.load(
            enumerated_value_factory(sqla))
        new_enumerated_value.append(EnumeratedValue(**valid_enumerated_value))
    sqla.add_all(new_enumerated_value)
    sqla.commit()


def create_multiple_person_attribute_strings(sqla, n):
    """Commit `n` new person attributes that have a string type to the database. Return their IDs."""
    person_attribute_schema = PersonAttributeSchema()
    new_person_attribute = []
    for i in range(n):
        valid_person_attribute = person_attribute_schema.load(
            person_attribute_string_factory(sqla))
        new_person_attribute.append(PersonAttribute(**valid_person_attribute))
    sqla.add_all(new_person_attribute)
    sqla.commit()


def create_multiple_person_attribute_enumerated(sqla, n):
    """Commit `n` new person attributes that have an enumerated type to the database. Return their IDs."""
    person_attribute_schema = PersonAttributeSchema()
    new_person_attribute = []
    for i in range(n):
        valid_person_attribute = person_attribute_schema.load(
            person_attribute_enumerated_factory(sqla))
        new_person_attribute.append(PersonAttribute(**valid_person_attribute))
    sqla.add_all(new_person_attribute)
    sqla.commit()


def prep_database(sqla):
    """Prepare the database with a random number of attributes, some of which are enumerated, some are string.
    Returns list of IDs of the new attributes.
    """
    create_multiple_attributes(sqla, random.randint(5, 15))
    create_multiple_enumerated_values(sqla, random.randint(5, 15))
    create_multiple_person_attribute_enumerated(sqla, random.randint(5, 15))
    create_multiple_person_attribute_strings(sqla, random.randint(5, 15))
    return [attribute.id for attribute in sqla.query(Attribute.id).all()]


# ---- Attribute

@pytest.mark.smoke
def test_create_attribute(auth_client):
    # GIVEN an empty database
    count = random.randint(5, 15)
    # WHEN we create a random number of new attributes
    for i in range(count):
        resp = auth_client.post(url_for('attributes.create_attribute'), json={"attribute": attribute_factory(auth_client.sqla, 'name', 'en-US'), "enumeratedValues":[]})
        assert resp.status_code == 201
    # THEN we end up with the proper number of attributes in the database
    assert auth_client.sqla.query(Attribute).count() == count

@pytest.mark.smoke
def test_create_enumerated_attribute(auth_client):
    # GIVEN an empty database
    count = random.randint(5, 15)
    # WHEN we create a random number of new attributes
    for i in range(count):
        resp = auth_client.post(url_for('attributes.create_attribute'), json={"attribute": attribute_factory(auth_client.sqla, 'name', 'en-US'), "enumeratedValues":[]})
        assert resp.status_code == 201
    # THEN we end up with the proper number of attributes in the database
    assert auth_client.sqla.query(Attribute).count() == count


def test_read_one_attributes(auth_client):
    # GIVEN a DB with a collection of attributes.
    count = random.randint(3, 11)
    create_multiple_attributes(auth_client.sqla, count)

    # WHEN we ask for them all
    attributes = auth_client.sqla.query(Attribute).all()
    # THEN we exepct the same number
    assert len(attributes) == count

    # WHEN we request each of them from the server
    for attribute in attributes:
        resp = auth_client.get(
            url_for('attributes.read_one_attribute', attribute_id=attribute.id))
        # THEN we find a matching attribute
        assert resp.status_code == 200
        assert resp.json['nameI18n'] == attribute.name_i18n
        assert resp.json['typeI18n'] == attribute.type_i18n

@pytest.mark.slow
def test_read_all_attributes(auth_client):
    # GIVEN a DB with a collection of attributes.
    count = random.randint(3, 11)
    create_multiple_attributes(auth_client.sqla, count, 1)
    assert count > 0

    attributes = auth_client.sqla.query(Attribute).all()

    # WHEN we request all attributes from the server
    resp = auth_client.get(url_for('attributes.read_all_attributes', locale='en-US'))
    # THEN the count matches the number of entries in the database
    assert resp.status_code == 200
    assert len(resp.json) == count


def test_update_attribute(auth_client):
    # GIVEN a DB with an attribute.
    create_multiple_attributes(auth_client.sqla, 1)
    attribute_id = auth_client.sqla.query(Attribute.id).first().id

    # WHEN we update its fields
    payload = {}

    payload['nameI18n'] = 'updated_name'
    payload['typeI18n'] = 'updated_type'
    payload['seq'] = 0
    payload['active'] = False
    resp = auth_client.patch(url_for(
        'attributes.update_attribute', attribute_id=attribute_id), json={'attribute': payload, 'enumeratedValues': []})
    assert resp.status_code == 200

    updated_attribute = auth_client.sqla.query(
        Attribute).filter_by(id=attribute_id).first()
    assert updated_attribute is not None
    assert updated_attribute.name_i18n == payload['nameI18n']
    assert updated_attribute.type_i18n == payload['typeI18n']
    assert updated_attribute.seq == payload['seq']
    assert updated_attribute.active == payload['active']


def test_deactivate_attribute(auth_client):
    # GIVEN a DB with an attribute.
    create_multiple_attributes(auth_client.sqla, 1)
    attribute_id = auth_client.sqla.query(Attribute.id).first().id

    # WHEN we call deactivate
    resp = auth_client.patch(url_for(
        'attributes.deactivate_attribute', attribute_id=attribute_id))
    assert resp.status_code == 200

    updated_attribute = auth_client.sqla.query(
        Attribute).filter_by(id=attribute_id).first()
    assert updated_attribute is not None
    assert updated_attribute.active == False


def test_activate_attribute(auth_client):
    # GIVEN a DB with an attribute.
    create_multiple_attributes(auth_client.sqla, 1, 0)
    attribute_id = auth_client.sqla.query(Attribute.id).first().id

    # WHEN we call deactivate
    resp = auth_client.patch(url_for(
        'attributes.activate_attribute', attribute_id=attribute_id))
    assert resp.status_code == 200

    updated_attribute = auth_client.sqla.query(
        Attribute).filter_by(id=attribute_id).first()
    assert updated_attribute is not None
    assert updated_attribute.active == True


# ---- EnumeratedValue


def create_multiple_enumerated_values(sqla, n):
    """Commit `n` new enumerated values to the database. Return their IDs."""
    enumerated_value_schema = EnumeratedValueSchema(exclude=['id'])
    new_enumerated_values = []
    for i in range(n):
        valid_enumerated_values = enumerated_value_schema.load(
            enumerated_value_factory(sqla))
        new_enumerated_values.append(
            EnumeratedValue(**valid_enumerated_values))
    sqla.add_all(new_enumerated_values)
    sqla.commit()


def test_create_enumerated_value(auth_client):
    # GIVEN an empty database
    count = random.randint(5, 15)
    # WHEN we create a random number of new enumerated values
    for i in range(count):
        resp = auth_client.post(
            url_for('attributes.create_enumerated_value'), json=enumerated_value_factory(auth_client.sqla))
        assert resp.status_code == 201
    # THEN we end up with the proper number of enumerated values in the database
    assert auth_client.sqla.query(EnumeratedValue).count() == count


def test_read_one_enumerated_values(auth_client):
    # GIVEN a DB with a collection of enumerated values.
    count = random.randint(3, 11)
    create_multiple_enumerated_values(auth_client.sqla, count)

    # WHEN we ask for them all
    enumerated_values = auth_client.sqla.query(EnumeratedValue).all()
    # THEN we exepct the same number
    assert len(enumerated_values) == count

    # WHEN we request each of them from the server
    for enumerated_value in enumerated_values:
        resp = auth_client.get(
            url_for('attributes.read_one_enumerated_value', enumerated_value_id=enumerated_value.id))
        # THEN we find a matching enumerated_value
        assert resp.status_code == 200
        assert resp.json['valueI18n'] == enumerated_value.value_i18n
        assert resp.json['active'] == enumerated_value.active


@pytest.mark.slow
def test_read_all_enumerated_values(auth_client):
    # GIVEN a DB with a collection of enumerated values.
    count = random.randint(3, 11)
    create_multiple_enumerated_values(auth_client.sqla, count)
    assert count > 0

    # WHEN we request all enumerated values from the server
    resp = auth_client.get(url_for('attributes.read_all_enumerated_values', locale='en-US'))
    # THEN the count matches the number of entries in the database
    assert resp.status_code == 200
    assert len(resp.json) == count


def test_update_enumerated_value(auth_client):
    # GIVEN a DB with an enumerated value.
    count = random.randint(3, 11)
    create_multiple_enumerated_values(auth_client.sqla, count)
    enumerated_value_id = auth_client.sqla.query(
        EnumeratedValue.id).first().id

    # WHEN we update its fields
    payload = {}

    payload['valueI18n'] = 'updated_name'
    payload['active'] = False
    resp = auth_client.patch(url_for(
        'attributes.update_enumerated_value', enumerated_value_id=enumerated_value_id), json=payload)
    assert resp.status_code == 200

    updated_enumerated_value = auth_client.sqla.query(
        EnumeratedValue).filter_by(id=enumerated_value_id).first()
    assert updated_enumerated_value is not None
    assert updated_enumerated_value.value_i18n == payload['valueI18n']
    assert updated_enumerated_value.active == payload['active']


def test_deactivate_enumerated_value(auth_client):
    # GIVEN a DB with an enumerated_value.
    create_multiple_enumerated_values(auth_client.sqla, 1)
    enumerated_value_id = auth_client.sqla.query(
        EnumeratedValue.id).first().id

    # WHEN we call deactivate
    resp = auth_client.patch(url_for(
        'attributes.deactivate_enumerated_value', enumerated_value_id=enumerated_value_id))
    assert resp.status_code == 200

    updated_enumerated_value = auth_client.sqla.query(
        EnumeratedValue).filter_by(id=enumerated_value_id).first()
    assert updated_enumerated_value is not None
    assert updated_enumerated_value.active == False


def test_activate_enumerated_value(auth_client):
    # GIVEN a DB with an enumerated_value.
    create_multiple_enumerated_values(auth_client.sqla, 1)
    enumerated_value_id = auth_client.sqla.query(
        EnumeratedValue.id).first().id

    # WHEN we call deactivate
    resp = auth_client.patch(url_for(
        'attributes.activate_enumerated_value', enumerated_value_id=enumerated_value_id))
    assert resp.status_code == 200

    updated_enumerated_value = auth_client.sqla.query(
        EnumeratedValue).filter_by(id=enumerated_value_id).first()
    assert updated_enumerated_value is not None
    assert updated_enumerated_value.active == True

@pytest.mark.smoke
def test_repr_attribute(auth_client):
    attribute = Attribute()
    attribute.__repr__()

@pytest.mark.smoke
def test_repr_enumerated_value(auth_client):
    enumerated_value = EnumeratedValue()
    enumerated_value.__repr__()

@pytest.mark.smoke
def test_repr_person_attribute(auth_client):
    person_attribute = PersonAttribute()
    person_attribute.__repr__()


