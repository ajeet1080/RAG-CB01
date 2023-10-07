from flask import Flask, request, jsonify, send_from_directory
# from flask_marshmallow import Marshmallow
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS
from models import initialize_db, EMD, emdSchema

# test
app = Flask(__name__)

# Initialize the database with the app instance
initialize_db(app)

CORS(app)
app.app_context().push()


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
            all_emds = all_emds.filter_by(
                Document_Item_Name_Long=Document_Item_Name_Long)
        if Left_Label is not None:
            all_emds = all_emds.filter_by(Left_Label=Left_Label)
        result = emds_schema.dump(all_emds)
        return jsonify(result)


# Run Server
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
