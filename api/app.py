from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import urllib.parse
from flask_swagger_ui import get_swaggerui_blueprint




app = Flask(__name__)

params = urllib.parse.quote_plus(
    "Driver={ODBC Driver 18 for SQL Server};Server=tcp:shs-genai-sql-01.database.windows.net,1433;Database=shs-genai-omr-01;Uid=sqldba;Pwd=P2ssw0rd!;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;")
app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc:///?odbc_connect=%s" % params
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)
app.app_context().push()

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

#Create route to upload file
UPLOAD_FOLDER = 'uploads'

@app.route('/uploads/<path:filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

#Add code snippet to include Swagger docs route for API
SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
API_URL = '/static/swagger.json'  # Our API url (can of course be a local resource)

# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "SingHealth Medical Report Generator"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


API_KEYS = {
    "client1": "api_key_1",
    "client2": "sgsgenaiapikey123098",
    # Add more clients and API keys as needed
}

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


#Create route to get all records with optional  query parameter for any Patient_ID, Case_No, Institution_Code , Document_Name,Document_Item_Name_Long and Left_Label . Also create api_key for authentication
@app.route('/emd', methods=['GET'])
def get_emds():
    api_key = request.headers.get('x-api-key')
   #fetch authentication api_key value from request as api_key 
    Case_No = request.args.get('Case_No')
    Patient_ID = request.args.get('Patient_ID')
    Institution_Code = request.args.get('Institution_Code')
    Document_Name = request.args.get('Document_Name')
    Document_Item_Name_Long = request.args.get('Document_Item_Name_Long')
    Left_Label = request.args.get('Left_Label')
    if api_key is None:
        return jsonify(error="Missing API key"), 400

    # Check if the provided API key is valid
    if api_key not in API_KEYS.values():
        return jsonify(error="Invalid API key"), 403  
    else: 
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
    

#@app.route('/swagger.json')
#def spec():
#    swag = swagger(app)
#    swag['info']['version'] = "1.0"
#    swag['info']['title'] = "SingHealth Medical Records API"
#    return jsonify(swag)


# Run Server
if __name__ == '__main__':
    app.run(debug=True)
