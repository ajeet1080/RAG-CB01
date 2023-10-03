import os
from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse, abort
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy import false
import urllib.parse


app = Flask(__name__)
params = urllib.parse.quote_plus(
    "Driver={ODBC Driver 18 for SQL Server};Server=tcp:shs-genai-sql-01.database.windows.net,1433;Database=shs-genai-omr-01;Uid=sqldba;Pwd=P2ssw0rd!;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;")
app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc:///?odbc_connect=%s" % params
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)
app.app_context().push()

# Product class/model


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=False)
    description = db.Column(db.String(200), unique=False)
    price = db.Column(db.Float, unique=False)
    qty = db.Column(db.Integer, unique=False)
    date_created = db.Column(db.DateTime, default=datetime.now)
    date_updated = db.Column(
        db.DateTime, default=datetime.now, onupdate=datetime.now)

    def __init__(self, name, description, price, qty):
        self.name = name
        self.description = description
        self.price = price
        self.qty = qty

# Product Schema


class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'price',
                  'qty', 'date_created', 'date_updated')


# Init Schema
product_schema = ProductSchema(strict=True)
products_schema = ProductSchema(many=True, strict=True)

#create route for post


# Run Server
if __name__ == '__main__':
    app.run(debug=True)
