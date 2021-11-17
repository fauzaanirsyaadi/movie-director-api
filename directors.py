"""
This is the people module and supports all the REST actions for the director data
"""

from flask import make_response, abort
from config import db
from models import Director, DirectorSchema, Movie

def read_all():
    """
    This function responds to a request for /api/director with the complete lists of director
    :return:        json string of list of people
    """
    # Create the list of director from our data
    director = Director.query.order_by(Director.id).all()

    # Serialize the data for the response
    director_schema = DirectorSchema(many=True)
    data = director_schema.dump(director)
    return data

def read_offset_limit(offset,limit):
    """
    This function responds to a request for /api/director/{offset}/{limit} with the complete lists of people
    :param offset:      Index where to get data
    :param limit:       number of data to get
    :return:            json string of list of director
    """
    # Create the list of director from our data
    director = Director.query.order_by(Director.id).slice(offset,limit)

    # Serialize the data for the response
    director_schema = DirectorSchema(many=True)
    data = director_schema.dump(director)
    return data

def read_one(director_id):
    """
    This function responds to a request for /api/director/{director_id} with one matching director
    :param director_id:     Id of director to find
    :return:                director matching id
    """
    # Build the initial query
    director = (
        Director.query.filter(Director.id == director_id)
        .outerjoin(Movie)
        .one_or_none()
    )

    # Did we find a director?
    if director is not None:

        # Serialize the data for the response
        director_schema = DirectorSchema()
        data = director_schema.dump(director)
        return data

    # Otherwise, nope, didn't find that director
    else:
        abort(404, f"Director not found for Id: {director_id}")

def create(director):
    """
    This function creates a new director based on the passed in director data
    :param director:    director to create in director structure
    :return:            201 on success, 406 on director exists
    """
    uid = director.get("uid")
    gender = director.get("gender")
    name = director.get("name")
    department = director.get("department")

    # Create a director instance using the schema and the passed in director
    schema = DirectorSchema()
    new_director = schema.load(director, session=db.session)

    try:
        assert new_director.gender in [0,1,2]
    except AssertionError:
        abort(404, "Gender not valid, must be 1 = Male or 2 = Female or 0")

    # Add the director to the database
    db.session.add(new_director)
    db.session.commit()

    # Serialize and return the newly created director in the response
    data = schema.dump(new_director)

    return data, 201


def update(director_id, director):
    """
    This function updates an existing director
    :param director_id:     Id of the director to update
    :param director:        director data to replace
    :return:                updated director structure
    """
    # Get the director requested from the db into session
    update_director = Director.query.filter(
        Director.id == director_id
    ).one_or_none()

    # Did we find an existing director?
    if update_director is not None:

        # turn the passed in director into a db object
        schema = DirectorSchema()
        update = schema.load(director, session=db.session)

        try:
            assert update.gender in [0,1,2]
        except AssertionError:
            abort(404, "Gender not valid, must be 1 = Male or 2 = Female")

        # Set the id to the director we want to update
        update.id = update_director.id

        # merge the new object into the old and commit it to the db
        db.session.merge(update)
        db.session.commit()

        # return updated director in the response
        data = schema.dump(update_director)

        return data, 200

    # Otherwise, nope, didn't find that director
    else:
        abort(404, f"Director not found for Id: {director_id}")

def delete(director_id):
    """
    This function deletes a director from the director structure
    :param director_id:     Id of the director to delete
    :return:                200 on successful delete, 404 if not found
    """
    # Get the director requested
    director = Director.query.filter(Director.id == director_id).one_or_none()

    # Did we find a director?
    if director is not None:
        db.session.delete(director)
        db.session.commit()
        return make_response(f"Director {director.name} with id: {director_id} deleted", 200)

    # Otherwise, nope, didn't find that director
    else:
        abort(404, f"Director not found for Id: {director_id}")
