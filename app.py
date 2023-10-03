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


class EMD(db.Model):
    
    EMD_ID = db.Column(db.Integer, primary_key=True)
    Patient_ID = db.Column("Patient ID", db.String(10), unique=False)
    Institution_Code = db.Column('Institution Code', db.String(50), unique=False)
    Case_No = db.Column("Case No",db.String(10), unique=False)
    Document_Name = db.Column("Document Name", db.String, unique=False)
    Document_Item_Name_Long = db.Column("Document Item Name Long", db.String, unique=False)
    Document_Item_Description = db.Column("Document Item Description", db.String, unique=False)
    Left_Label = db.Column("Item Left Label", db.String, unique=False)
    Right_Label = db.Column("Item Right Label",db.String, unique=False)
    Authored_Date = db.Column("Authored Date (YYYYMMDD)", db.String, unique=False)
    Value_Text = db.Column("Value Text cleaned",db.String, unique=False)

    def __init__(self, EMD_ID, Patient_ID, Institution_Code, Case_No, Document_Name, Document_Item_Name_Long, Document_Item_Description, Left_Label, Right_Label, Authored_Date, Value_Text):
        
        self.EMD_ID = EMD_ID
        self.Patient_ID = Patient_ID
        self.Institution_Code = Institution_Code
        self.Case_No = Case_No
        self.Document_Name = Document_Name
        self.Document_Item_Name_Long = Document_Item_Name_Long
        self.Document_Item_Description = Document_Item_Description
        self.Left_Label = Left_Label
        self.Right_Label = Right_Label
        self.Authored_Date = Authored_Date
        self.Value_Text = Value_Text




# create emd Schema
class emdSchema(ma.Schema):
    class Meta:
        fields = ('EMD_ID','Patient_ID', 'Institution_Code', 'Case_No', 'Document_Name', 'Document_Item_Name_Long',
                  'Document_Item_Description', 'Left_Label', 'Right_Label', 'Authored_Date', 'Value_Text')


# Init Schema
emd_schema = emdSchema()
emds_schema = emdSchema(many=True)


#Create route to get all records with optional  query parameter for any Patient_ID, Case_No, Institution_Code , Document_Name,Document_Item_Name_Long and Left_Label 
@app.route('/emd', methods=['GET'])
def get_emds():
    Case_No = request.args.get('Case_No')
    Patient_ID = request.args.get('Patient_ID')
    Institution_Code = request.args.get('Institution_Code')
    Document_Name = request.args.get('Document_Name')
    Document_Item_Name_Long = request.args.get('Document_Item_Name_Long')
    Left_Label = request.args.get('Left_Label')
    if Case_No is None:
        all_emds = EMD.query.all()
    else:
        all_emds = EMD.query.filter_by(Case_No=Case_No)
    if Patient_ID is not None:
        all_emds = all_emds.filter_by(Patient_ID=Patient_ID)
    if Institution_Code is not None:
        all_emds = all_emds.filter_by(Institution_Code=Institution_Code)
    if Document_Name is not None:
        all_emds = all_emds.filter_by(Document_Name=Document_Name)
    if Document_Item_Name_Long is not None:
        all_emds = all_emds.filter_by(Document_Item_Name_Long=Document_Item_Name_Long)
    if Left_Label is not None:
        all_emds = all_emds.filter_by(Left_Label=Left_Label)
    result = emds_schema.dump(all_emds)
    return jsonify(result)





# Run Server
if __name__ == '__main__':
    app.run(debug=True)
