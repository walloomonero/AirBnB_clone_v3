#!/usr/bin/python3
"""
The User Class from Models Module
"""
import os
from models.base_model import BaseModel, Base
from hashlib import md5
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Float

storage_type = os.environ.get('HBNB_TYPE_STORAGE')


class User(BaseModel, Base):
    """User class that handles all application users"""
    if storage_type == "db":
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column("password", String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)

        places = relationship('Place', backref='user', cascade='delete')
        reviews = relationship('Review', backref='user', cascade='delete')
    else:
        email = ''
        password = ''
        first_name = ''
        last_name = ''

    def __init__(self, *args, **kwargs):
        """
        initializes User Model, inherits from BaseModel
        """
        super().__init__(*args, **kwargs)

    @property
    def password(self):
        """
        The getter for password
        :return: The password (hashed)
        """
        return self.__dict__.get("password")

    @password.setter
    def password(self, password):
        """
        The Password setter, with md5 hasing
        :parameter password: password
        :return: nothing
        """
        self.__dict__["password"] = md5(password.encode('utf-8')).hexdigest()
