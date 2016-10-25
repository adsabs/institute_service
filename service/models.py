'''
Created on October 20, 2016

@author: ehenneken
'''
from flask import current_app, request
from flask.ext.sqlalchemy import SQLAlchemy
import sys

db = SQLAlchemy()


class Institute(db.Model):
    __bind_key__ = 'institutes'
    __tablename__ = 'institute'
    id = db.Column(db.Integer, primary_key=True)
    canonical_name = db.Column(db.String)
    city = db.Column(db.String)
    street = db.Column(db.String)
    state = db.Column(db.String)
    country = db.Column(db.String)
    ringgold_id = db.Column(db.Integer)
    ads_id = db.Column(db.String)

    def __repr__(self):
        return '<Insitute, name: {0}, Ringgold ID: {1}, ADS ID: {2}>'\
            .format(self.canonical_name, self.ringgold_id, self.ads_id)

class Library(db.Model):
    __bind_key__ = 'institutes'
    __tablename__ = 'library'
    id = db.Column(db.Integer, primary_key=True)
    libserver = db.Column(db.String)
    iconurl   = db.Column(db.String)
    libname   = db.Column(db.String)
    institute = db.Column(db.Integer, db.ForeignKey('institute.id'))

    def __repr__(self):
        return '<Library, name: {0}, OpenURL server: {1}, OpenURL icon: {2}>'\
            .format(self.libname,  self.libserver, self.iconurl)
