from flask_sqlalchemy import SQLAlchemy
import urllib.parse
from flask_marshmallow import Marshmallow


def initialize_db(app):
    # Connection to Azure SQL Database
    params = urllib.parse.quote_plus(
        "Driver={ODBC Driver 18 for SQL Server};Server=tcp:shs-genai-sql-01.database.windows.net,1433;Database=shs-genai-omr-01;Uid=sqldba;Pwd=P2ssw0rd!;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;")
    app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc:///?odbc_connect=%s" % params
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)


db = SQLAlchemy()
ma = Marshmallow()

# Define Model


class EMD(db.Model):
    EMD_ID = db.Column(db.Integer, primary_key=True)
    Patient_ID = db.Column("Patient ID", db.String(10), unique=False)
    Institution_Code = db.Column(
        'Institution Code', db.String(50), unique=False)
    Case_No = db.Column("Case No", db.String(10), unique=False)
    Document_Name = db.Column("Document Name", db.String, unique=False)
    Document_Item_Name_Long = db.Column(
        "Document Item Name Long", db.String, unique=False)
    Document_Item_Description = db.Column(
        "Document Item Description", db.String, unique=False)
    Left_Label = db.Column("Item Left Label", db.String, unique=False)
    Right_Label = db.Column("Item Right Label", db.String, unique=False)
    Authored_Date = db.Column(
        "Authored Date (YYYYMMDD)", db.String, unique=False)
    Value_Text = db.Column("Value Text cleaned", db.String, unique=False)

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

class END(db.Model):
    END_ID = db.Column(db.Integer, primary_key=True)
    Patient_ID = db.Column("Patient ID", db.String(10), unique=False)
    Institution_Code = db.Column(
        'Institution Code', db.String(50), unique=False)
    Case_No = db.Column("Case No", db.String(10), unique=False)
    Document_Name = db.Column("Document Name", db.String, unique=False)
    Document_Item_Name_Long = db.Column(
        "Document Item Name Long", db.String, unique=False)
    Document_Item_Description = db.Column(
        "Document Item Description", db.String, unique=False)
    Left_Label = db.Column("Item Left Label", db.String, unique=False)
    Right_Label = db.Column("Item Right Label", db.String, unique=False)
    Authored_Date = db.Column(
        "Authored Date (YYYYMMDD)", db.String, unique=False)
    Value_Text = db.Column("Value Text cleaned", db.String, unique=False)


    def __init__(self, END_ID, Patient_ID, Institution_Code, Case_No, Document_Name, Document_Item_Name_Long, Document_Item_Description, Left_Label, Right_Label, Authored_Date, Value_Text):
        self.END_ID = END_ID
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


class Urology(db.Model):
    URO_ID = db.Column(db.Integer, primary_key=True)
    Patient_ID = db.Column("Patient ID", db.String(10), unique=False)
    Institution_Code = db.Column(
        'Institution Code', db.String(50), unique=False)
    Case_No = db.Column("Case No", db.String(10), unique=False)
    Document_Name = db.Column("Document Name", db.String, unique=False)
    Document_Item_Name_Long = db.Column(
        "Document Item Name Long", db.String, unique=False)
    Document_Item_Description = db.Column(
        "Document Item Description", db.String, unique=False)
    Left_Label = db.Column("Item Left Label", db.String, unique=False)
    Right_Label = db.Column("Item Right Label", db.String, unique=False)
    Authored_Date = db.Column(
        "Authored Date (YYYYMMDD)", db.String, unique=False)
    Value_Text = db.Column("Value Text cleaned", db.String, unique=False)


    def __init__(self, URO_ID, Patient_ID, Institution_Code, Case_No, Document_Name, Document_Item_Name_Long, Document_Item_Description, Left_Label, Right_Label, Authored_Date, Value_Text):
        self.URO_ID = URO_ID
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
 

# Model DRUG with Columns  Drug_ID as Primary Key,  Institution Code,  Case No,Drug Form,Drug Name, Generic Drug Name,Drug Dispensed Date From,Drug Dispensed Date To,Duration Unit (from Dispensed),Discharge Indicator,Instructions (from Ordered),Instructions (from Dispensed),Duration (from Dispensed), Case Start Date,Case Type Description


class DRUG(db.Model):
    Drug_ID = db.Column(db.Integer, primary_key=True)
    Institution_Code = db.Column(
        'Institution Code', db.String(50), unique=False)
    Case_No = db.Column("Case No", db.String(10), unique=False)
    Drug_Form = db.Column("Drug Form", db.String, unique=False)
    Drug_Name = db.Column("Drug Name", db.String, unique=False)
    Generic_Drug_Name = db.Column("Generic Drug Name", db.String, unique=False)
    Drug_Dispensed_Date_From = db.Column(
        "Drug Dispensed Date From", db.String, unique=False)
    Drug_Dispensed_Date_To = db.Column(
        "Drug Dispensed Date To", db.String, unique=False)
    Duration_Unit_from_Dispensed = db.Column(
        "Duration Unit (from Dispensed)", db.String, unique=False)
    Discharge_Indicator = db.Column(
        "Discharge Indicator", db.String, unique=False)
    Instructions_from_Ordered = db.Column(
        "Instructions (from Ordered)", db.String, unique=False)
    Instructions_from_Dispensed = db.Column(
        "Instructions (from Dispensed)", db.String, unique=False)
    Duration_from_Dispensed = db.Column(
        "Duration (from Dispensed)", db.String, unique=False)
    Case_Start_Date = db.Column("Case Start Date", db.String, unique=False)
    Case_Type_Description = db.Column(
        "Case Type Description", db.String, unique=False)

    def __init__(self, Drug_ID, Institution_Code, Case_No, Drug_Form, Drug_Name, Generic_Drug_Name, Drug_Dispensed_Date_From, Drug_Dispensed_Date_To, Duration_Unit_from_Dispensed, Discharge_Indicator, Instructions_from_Ordered, Instructions_from_Dispensed, Duration_from_Dispensed, Case_Start_Date, Case_Type_Description):
        self.Drug_ID = Drug_ID
        self.Institution_Code = Institution_Code
        self.Case_No = Case_No
        self.Drug_Form = Drug_Form
        self.Drug_Name = Drug_Name
        self.Generic_Drug_Name = Generic_Drug_Name
        self.Drug_Dispensed_Date_From = Drug_Dispensed_Date_From
        self.Drug_Dispensed_Date_To = Drug_Dispensed_Date_To
        self.Duration_Unit_from_Dispensed = Duration_Unit_from_Dispensed
        self.Discharge_Indicator = Discharge_Indicator
        self.Instructions_from_Ordered = Instructions_from_Ordered


# create Model LAB with columns as Lab_ID as Primary key,Patient ID as Foriegn Key with relation to EMD table, Institution Code,Case No,Reported Date,Lab Test Code,Lab Test Description,Lab Resulted Order Test Code,Lab Resulted Order Test Description,Result Value,Reference Ranges,Units of Measurement
class LAB(db.Model):
    Lab_ID = db.Column(db.Integer, primary_key=True)
    Patient_ID = db.Column("Patient ID", db.String(10), unique=False)
    Institution_Code = db.Column(
        'Institution Code', db.String(50), unique=False)
    Case_No = db.Column("Case No", db.String(10), unique=False)
    Reported_Date = db.Column("Reported Date", db.String, unique=False)
    Lab_Test_Code = db.Column("Lab Test Code", db.String, unique=False)
    Lab_Test_Description = db.Column(
        "Lab Test Description", db.String, unique=False)
    Lab_Resulted_Order_Test_Code = db.Column(
        "Lab Resulted Order Test Code", db.String, unique=False)
    Lab_Resulted_Order_Test_Description = db.Column(
        "Lab Resulted Order Test Description", db.String, unique=False)
    Result_Value = db.Column("Result Value", db.String, unique=False)
    Reference_Ranges = db.Column("Reference Ranges", db.String, unique=False)
    Units_of_Measurement = db.Column(
        "Units of Measurements", db.String, unique=False)

    def __init__(self, Lab_ID, Patient_ID, Institution_Code, Case_No, Reported_Date, Lab_Test_Code, Lab_Test_Description, Lab_Resulted_Order_Test_Code, Lab_Resulted_Order_Test_Description, Result_Value, Reference_Ranges, Units_of_Measurement):
        self.Lab_ID = Lab_ID
        self.Patient_ID = Patient_ID
        self.Institution_Code = Institution_Code
        self.Case_No = Case_No
        self.Reported_Date = Reported_Date
        self.Lab_Test_Code = Lab_Test_Code
        self.Lab_Test_Description = Lab_Test_Description
        self.Lab_Resulted_Order_Test_Code = Lab_Resulted_Order_Test_Code
        self.Lab_Resulted_Order_Test_Description = Lab_Resulted_Order_Test_Description
        self.Result_Value = Result_Value
        self.Reference_Ranges = Reference_Ranges
        self.Units_of_Measurement = Units_of_Measurement


# Create Model RAD with column as Rad_ID as primary key, Institution Code,Case No,Visit Date,Exam Start Date,Performed Date Time,Order Name,Procedure Name,Report_cleaned
class Radiology(db.Model):
    Rad_ID = db.Column(db.Integer, primary_key=True)
    Institution_Code = db.Column(
        'Institution Code', db.String(50), unique=False)
    Case_No = db.Column("Case No", db.String(10), unique=False)
    Visit_Date = db.Column("Visit Date", db.String, unique=False)
    Exam_Start_Date = db.Column("Exam Start Date", db.String, unique=False)
    Performed_Date_Time = db.Column(
        "Performed Date Time", db.String, unique=False)
    Order_Name = db.Column("Order Name", db.String, unique=False)
    Procedure_Name = db.Column("Procedure Name", db.String, unique=False)
    Report_cleaned = db.Column("Report_cleaned", db.String, unique=False)

    def __init__(self, Rad_ID, Institution_Code, Case_No, Visit_Date, Exam_Start_Date, Performed_Date_Time, Order_Name, Procedure_Name, Report_cleaned):
        self.Rad_ID = Rad_ID
        self.Institution_Code = Institution_Code
        self.Case_No = Case_No
        self.Visit_Date = Visit_Date
        self.Exam_Start_Date = Exam_Start_Date
        self.Performed_Date_Time = Performed_Date_Time
        self.Order_Name = Order_Name
        self.Procedure_Name = Procedure_Name
        self.Report_cleaned = Report_cleaned


# Define Schema for EMD
class emdSchema(ma.Schema):
    class Meta:
        fields = ('EMD_ID', 'Patient_ID', 'Institution_Code', 'Case_No', 'Document_Name', 'Document_Item_Name_Long',
                  'Document_Item_Description', 'Left_Label', 'Right_Label', 'Authored_Date', 'Value_Text')
        
# Define Schema for END
class endSchema(ma.Schema):
    class Meta:
        fields = ('END_ID', 'Patient_ID', 'Institution_Code', 'Case_No', 'Document_Name', 'Document_Item_Name_Long',
                  'Document_Item_Description', 'Left_Label', 'Right_Label', 'Authored_Date', 'Value_Text') 

# Define Schema for URO
class uroSchema(ma.Schema):
    class Meta:
        fields = ('URO_ID', 'Patient_ID', 'Institution_Code', 'Case_No', 'Document_Name', 'Document_Item_Name_Long',
                  'Document_Item_Description', 'Left_Label', 'Right_Label', 'Authored_Date', 'Value_Text')


# Define Schema for DRUG


class drugSchema(ma.Schema):
    class Meta:
        fields = ('Drug_ID', 'Institution_Code', 'Case_No', 'Drug_Form', 'Drug_Name', 'Generic_Drug_Name', 'Drug_Dispensed_Date_From', 'Drug_Dispensed_Date_To', 'Duration_Unit_from_Dispensed',
                  'Discharge_Indicator', 'Instructions_from_Ordered', 'Instructions_from_Dispensed', 'Duration_from_Dispensed', 'Case_Start_Date', 'Case_Type_Description')

# Define Schema for LAB


class labSchema(ma.Schema):
    class Meta:
        fields = ('Lab_ID', 'Patient_ID', 'Institution_Code', 'Case_No', 'Reported_Date', 'Lab_Test_Code', 'Lab_Test_Description', 'Lab_Resulted_Order_Test_Code',
                  'Lab_Resulted_Order_Test_Description', 'Result_Value', 'Reference_Ranges', 'Units_of_Measurement')


# Define Schema for RAD
class radSchema(ma.Schema):
    class Meta:
        fields = ('Rad_ID', 'Institution_Code', 'Case_No', 'Visit_Date', 'Exam_Start_Date',
                  'Performed_Date_Time', 'Order_Name', 'Procedure_Name', 'Report_cleaned')
