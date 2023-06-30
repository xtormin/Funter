import os, sys
from pymongo import MongoClient
from bson.objectid import ObjectId
from mongoengine import connect, disconnect, DynamicDocument, StringField, ReferenceField
from pathlib import Path
from dotenv import load_dotenv

# DATABASE MODELS

class Project(DynamicDocument):
    """
    This class represents a project document in the database.
    Each project has a unique name.
    """

    meta = {'collection': 'project',  # Explicitly specify collection name
            'indexes': ['name']}  # Adding an index on the 'name' field

    name = StringField(
        required=True,
        max_length=200,
        unique=True,
        help_text="The unique name of the project"
    )


class Scope(DynamicDocument):
    """
    This class represents a scope document in the database.
    Each scope has a unique name and is associated with a project.
    """
    meta = {'collection': 'scope',  # Explicitly specify collection name
            'indexes': ['name']}  # Adding an index on the 'name' field

    name = StringField(
        required=True,
        max_length=200,
        unique=True,
        help_text="The unique name of the scope"
    )

    project_reference = ReferenceField(
        Project,
        required=True,
        help_text="Reference to the associated project"
    )

class Form(DynamicDocument):
    """
    This class represents a form document in the database.
    It stores information about a form, including its URL, name,
    action, method, input_name, type, value, and options.
    """
    meta = {
        'collection': 'form',  # Explicitly specify collection name
        'indexes': ['url_name', 'form_name']  # Example of adding indexes
    }

    url_name = StringField(
        max_length=200,
        help_text="The URL name of the form"
    )

    form_name = StringField(
        max_length=200,
        help_text="The name of the form"
    )

    action = StringField(
        max_length=200,
        help_text="The action attribute of the form"
    )

    method = StringField(
        max_length=200,
        choices=['GET', 'POST'],  # Example of adding validation for the method field
        help_text="The method of the form (e.g., GET, POST)"
    )

    input_name = StringField(
        max_length=200,
        help_text="The input name of the form"
    )

    input_type = StringField(  # Renamed 'type' to 'input_type' for clarity
        max_length=200,
        help_text="The input type of the form"
    )

    value = StringField(
        max_length=500,
        help_text="The value attribute of the form's input"
    )

    options = StringField(
        max_length=200,
        help_text="The options for the form's input"
    )