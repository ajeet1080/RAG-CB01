from flask import Flask, request, jsonify, send_from_directory
# from flask_marshmallow import Marshmallow
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS
from models import initialize_db, EMD, emdSchema,  DRUG, drugSchema, LAB, labSchema, Radiology, radSchema
import openai

# test
app = Flask(__name__)

# Initialize the database with the app instance
initialize_db(app)

CORS(app)
app.app_context().push()

openai.api_type = "azure"
openai.api_version = "2023-05-15"
# Your Azure OpenAI resource's endpoint value.
openai.api_base = "https://singhealth-openai.openai.azure.com/"
openai.api_key = "8878aae71e9d425ca35e7a2c70d8f9af"


@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)


# Create route to upload file
UPLOAD_FOLDER = 'uploads'


@app.route('/uploads/<path:filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)


# Add code snippet to include Swagger docs route for API
SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
# Our API url (can of course be a local resource)
API_URL = '/static/swagger.json'

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


# Init Schema
emd_schema = emdSchema()
emds_schema = emdSchema(many=True)

lab_schema = labSchema()
labs_schema = labSchema(many=True)

drug_schema = drugSchema()
drugs_schema = drugSchema(many=True)

rad_schema = radSchema()
rads_schema = radSchema(many=True)

# Create route to get all records with optional  query parameter for any Patient_ID, Case_No, Institution_Code , Document_Name,Document_Item_Name_Long and Left_Label . Also create api_key for authentication


@app.route('/emd', methods=['GET'])
def get_emds():
    api_key = request.headers.get('x-api-key')
   # fetch authentication api_key value from request as api_key
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
            all_emds = EMD.query.order_by(
                EMD.Authored_Date.desc(), EMD.Document_Item_Description).all()
        else:
            all_emds = EMD.query.filter_by(Case_No=Case_No).order_by(
                EMD.Authored_Date.desc(), EMD.Document_Item_Description)
        if Patient_ID is not None:
            all_emds = all_emds.filter_by(Patient_ID=Patient_ID).order_by(
                EMD.Authored_Date.desc(), EMD.Document_Item_Description)
        if Institution_Code is not None:
            all_emds = all_emds.filter_by(Institution_Code=Institution_Code).order_by(
                EMD.Authored_Date.desc(), EMD.Document_Item_Description)
        if Document_Name is not None:
            all_emds = all_emds.filter_by(Document_Name=Document_Name).order_by(
                EMD.Authored_Date.desc(), EMD.Document_Item_Description)
        if Document_Item_Name_Long is not None:
            all_emds = all_emds.filter_by(
                Document_Item_Name_Long=Document_Item_Name_Long).order_by(EMD.Authored_Date.desc(), EMD.Document_Item_Description)
        if Left_Label is not None:
            all_emds = all_emds.filter_by(Left_Label=Left_Label).order_by(
                EMD.Authored_Date.desc(), EMD.Document_Item_Description)
        result = emds_schema.dump(all_emds)
        return jsonify(result)


@app.route('/lab', methods=['GET'])
def get_lab():
    api_key = request.headers.get('x-api-key')
   # fetch authentication api_key value from request as api_key
    Case_No = request.args.get('Case_No')
    Patient_ID = request.args.get('Patient_ID')
    Institution_Code = request.args.get('Institution_Code')
    Lab_Test_Code = request.args.get('Lab_Test_Code')
    Lab_Resulted_Order_Test_Code = request.args.get(
        'Lab_Resulted_Order_Test_Code')
    Units_of_Measurement = request.args.get('Units_of_Measurement')
    if api_key is None:
        return jsonify(error="Missing API key"), 400

    # Check if the provided API key is valid
    if api_key not in API_KEYS.values():
        return jsonify(error="Invalid API key"), 403
    else:
        if Case_No is None:
            all_lab = LAB.query.order_by(
                LAB.Reported_Date.desc(), LAB.Lab_Resulted_Order_Test_Description).all()
        else:
            all_lab = LAB.query.filter_by(Case_No=Case_No).order_by(
                LAB.Reported_Date.desc(), LAB.Lab_Resulted_Order_Test_Description)
        if Patient_ID is not None:
            all_lab = all_lab.filter_by(Patient_ID=Patient_ID).order_by(
                LAB.Reported_Date.desc(), LAB.Lab_Resulted_Order_Test_Description)
        if Institution_Code is not None:
            all_lab = all_lab.filter_by(Institution_Code=Institution_Code).order_by(
                LAB.Reported_Date.desc(), LAB.Lab_Resulted_Order_Test_Description)
        if Lab_Test_Code is not None:
            all_lab = all_lab.filter_by(Lab_Test_Code=Lab_Test_Code).order_by(
                LAB.Reported_Date.desc(), LAB.Lab_Resulted_Order_Test_Description)
        if Lab_Resulted_Order_Test_Code is not None:
            all_lab = all_lab.filter_by(
                Lab_Resulted_Order_Test_Code=Lab_Resulted_Order_Test_Code).order_by(LAB.Reported_Date.desc(), LAB.Lab_Resulted_Order_Test_Description)
        if Units_of_Measurement is not None:
            all_lab = all_lab.filter_by(
                Units_of_Measurement=Units_of_Measurement).order_by(LAB.Reported_Date.desc(), LAB.Lab_Resulted_Order_Test_Description)
        result = labs_schema.dump(all_lab)
        return jsonify(result)


@app.route('/drugs', methods=['GET'])
def get_drugs():
    api_key = request.headers.get('x-api-key')
   # fetch authentication api_key value from request as api_key
    Case_No = request.args.get('Case_No')
    Patient_ID = request.args.get('Patient_ID')
    Institution_Code = request.args.get('Institution_Code')
    Drug_Name = request.args.get('Drug_Name')
    Generic_Drug_Name = request.args.get(
        'Generic_Drug_Name')
    Discharge_Indicator = request.args.get('Discharge_Indicator')
    if api_key is None:
        return jsonify(error="Missing API key"), 400

    # Check if the provided API key is valid
    if api_key not in API_KEYS.values():
        return jsonify(error="Invalid API key"), 403
    else:
        if Case_No is None:
            all_drug = DRUG.query.order_by(
                DRUG.Case_Start_Date.desc(), DRUG.Generic_Drug_Name).all()
        else:
            all_drug = DRUG.query.filter_by(Case_No=Case_No).order_by(
                DRUG.Case_Start_Date.desc(), DRUG.Generic_Drug_Name)
        if Patient_ID is not None:
            all_drug = all_drug.filter_by(Patient_ID=Patient_ID).order_by(
                DRUG.Case_Start_Date.desc(), DRUG.Generic_Drug_Name)
        if Institution_Code is not None:
            all_drug = all_drug.filter_by(Institution_Code=Institution_Code).order_by(
                DRUG.Case_Start_Date.desc(), DRUG.Generic_Drug_Name)
        if Drug_Name is not None:
            all_drug = all_drug.filter_by(Drug_Name=Drug_Name).order_by(
                DRUG.Case_Start_Date.desc(), DRUG.Generic_Drug_Name)
        if Generic_Drug_Name is not None:
            all_drug = all_drug.filter_by(
                Generic_Drug_Name=Generic_Drug_Name).order_by(DRUG.Case_Start_Date.desc(), DRUG.Generic_Drug_Name)
        if Discharge_Indicator is not None:
            all_drug = all_drug.filter_by(
                Discharge_Indicator=Discharge_Indicator).order_by(DRUG.Case_Start_Date.desc(), DRUG.Generic_Drug_Name)
        result = drugs_schema.dump(all_drug)
        return jsonify(result)


@app.route('/radiology', methods=['GET'])
def get_radiology():
    api_key = request.headers.get('x-api-key')
   # fetch authentication api_key value from request as api_key
    Case_No = request.args.get('Case_No')
    Institution_Code = request.args.get('Institution_Code')
    Order_Name = request.args.get('Order_Name')
    Procedure_Name = request.args.get(
        'Procedure_Name')
    if api_key is None:
        return jsonify(error="Missing API key"), 400

    # Check if the provided API key is valid
    if api_key not in API_KEYS.values():
        return jsonify(error="Invalid API key"), 403
    else:
        if Case_No is None:
            all_rads = Radiology.query.order_by(
                Radiology.Exam_Start_Date.desc(), Radiology.Order_Name).all()
        else:
            all_rads = Radiology.query.filter_by(Case_No=Case_No).order_by(
                Radiology.Exam_Start_Date.desc(), Radiology.Order_Name)
        if Institution_Code is not None:
            all_rads = all_rads.filter_by(Institution_Code=Institution_Code).order_by(
                Radiology.Exam_Start_Date.desc(), Radiology.Order_Name)
        if Order_Name is not None:
            all_rads = all_rads.filter_by(Order_Name=Order_Name).order_by(
                Radiology.Exam_Start_Date.desc(), Radiology.Order_Name)
        if Procedure_Name is not None:
            all_rads = all_rads.filter_by(
                Procedure_Name=Procedure_Name).order_by(Radiology.Exam_Start_Date.desc(), Radiology.Order_Name)
        result = rads_schema.dump(all_rads)
        return jsonify(result)

# Create Post route called /generate to call azure open ai api to ask question and get answer. Use deployment shhqllm01


@app.route('/generate', methods=['POST'])
def get_openai_response():
    user_message = request.json.get('prompt')
    response = openai.ChatCompletion.create(
        # The deployment name you chose when you deployed the GPT-35-Turbo or GPT-4 model.
        engine="shhqllm01",
        messages=[
            {"role": "system",
                "content": "Assistant can generate medical reports based on the given patient's medical data."},
            {"role": "user", "content": user_message}
        ] , temperature=0.3,top_p=1
    )
    return jsonify(response['choices'][0]['message'])


# Run Server
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
