from flask import Flask, request, jsonify, send_from_directory
# from flask_marshmallow import Marshmallow
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS
from models import initialize_db, EMD, emdSchema,  DRUG, drugSchema, LAB, labSchema, Radiology, radSchema , END, endSchema, Urology , uroSchema
import openai
from sqlalchemy import func



import os

# test1
app = Flask(__name__)

# Initialize the database with the app instance
initialize_db(app)

CORS(app)
app.app_context().push()

openai.api_type = "azure"
openai.api_version = "2023-05-15"
# Your Azure OpenAI resource's endpoint value.
openai.api_base = "https://shplayground2.openai.azure.com/"
openai.api_key = "fefc20d1c3ee4046b446c239f96e4fc4"


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

end_schema = endSchema()
ends_schema = endSchema(many=True)

uro_schema = uroSchema()
uros_schema = uroSchema(many=True)

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
    

@app.route('/end', methods=['GET'])
def get_ends():
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
            all_ends = END.query.order_by(
                END.Authored_Date.desc(), END.Document_Item_Description).all()
        else:
            all_ends = END.query.filter_by(Case_No=Case_No).order_by(
                END.Authored_Date.desc(), END.Document_Item_Description)
        if Patient_ID is not None:
            all_ends = all_ends.filter_by(Patient_ID=Patient_ID).order_by(
                END.Authored_Date.desc(), END.Document_Item_Description)
        if Institution_Code is not None:
            all_ends = all_ends.filter_by(Institution_Code=Institution_Code).order_by(
                END.Authored_Date.desc(), END.Document_Item_Description)
        if Document_Name is not None:
            all_ends = all_ends.filter_by(Document_Name=Document_Name).order_by(
                END.Authored_Date.desc(), END.Document_Item_Description)
        if Document_Item_Name_Long is not None:
            all_ends = all_ends.filter_by(
                Document_Item_Name_Long=Document_Item_Name_Long).order_by(END.Authored_Date.desc(), END.Document_Item_Description)
        if Left_Label is not None:
            all_ends = all_ends.filter_by(Left_Label=Left_Label).order_by(
                END.Authored_Date.desc(), END.Document_Item_Description)
        result = ends_schema.dump(all_ends)
        return jsonify(result) 

@app.route('/uro', methods=['GET'])
def get_uros():
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
            all_uros = Urology.query.order_by(
                Urology.Authored_Date.desc(), Urology.Document_Item_Description).all()
        else:
            all_uros = Urology.query.filter_by(Case_No=Case_No).order_by(
                Urology.Authored_Date.desc(), Urology.Document_Item_Description)
        if Patient_ID is not None:
            all_uros = all_uros.filter_by(Patient_ID=Patient_ID).order_by(
                Urology.Authored_Date.desc(), Urology.Document_Item_Description)
        if Institution_Code is not None:
            all_uros = all_uros.filter_by(Institution_Code=Institution_Code).order_by(
                Urology.Authored_Date.desc(), Urology.Document_Item_Description)
        if Document_Name is not None:
            all_uros = all_uros.filter_by(Document_Name=Document_Name).order_by(
                Urology.Authored_Date.desc(), Urology.Document_Item_Description)
        if Document_Item_Name_Long is not None:
            all_uros = all_uros.filter_by(
                Document_Item_Name_Long=Document_Item_Name_Long).order_by(Urology.Authored_Date.desc(), Urology.Document_Item_Description)
        if Left_Label is not None:
            all_uros = all_uros.filter_by(Left_Label=Left_Label).order_by(
                Urology.Authored_Date.desc(), Urology.Document_Item_Description)
        result = uros_schema.dump(all_uros)
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
                DRUG.Drug_Dispensed_Date_To.desc(), DRUG.Generic_Drug_Name).all()
        else:
            all_drug = DRUG.query.filter_by(Case_No=Case_No).order_by(
                DRUG.Drug_Dispensed_Date_To.desc(), DRUG.Generic_Drug_Name)
        if Patient_ID is not None:
            all_drug = all_drug.filter_by(Patient_ID=Patient_ID).order_by(
                DRUG.Drug_Dispensed_Date_To.desc(), DRUG.Generic_Drug_Name)
        if Institution_Code is not None:
            all_drug = all_drug.filter_by(Institution_Code=Institution_Code).order_by(
                DRUG.Drug_Dispensed_Date_To.desc(), DRUG.Generic_Drug_Name)
        if Drug_Name is not None:
            all_drug = all_drug.filter_by(Drug_Name=Drug_Name).order_by(
                DRUG.Drug_Dispensed_Date_To.desc(), DRUG.Generic_Drug_Name)
        if Generic_Drug_Name is not None:
            all_drug = all_drug.filter_by(
                Generic_Drug_Name=Generic_Drug_Name).order_by(DRUG.Drug_Dispensed_Date_To.desc(), DRUG.Generic_Drug_Name)
        if Discharge_Indicator is not None:
            all_drug = all_drug.filter_by(
                Discharge_Indicator=Discharge_Indicator).order_by(DRUG.Drug_Dispensed_Date_To.desc(), DRUG.Generic_Drug_Name)
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
        engine="432",
        messages=[
            {"role": "system",
                "content": "You are medical Assistant that can generate medical reports based on the given patient's medical data."},
            {"role": "user", "content": user_message}
        ] , temperature=0.3,top_p=1 
    )
    return jsonify(response['choices'][0]['message'])

@app.route('/compare', methods=['POST'])
def get_comparision_response():
    user_message = request.json.get('prompt')
    response = openai.ChatCompletion.create(
        # The deployment name you chose when you deployed the GPT-35-Turbo or GPT-4 model.
        engine="432",
        messages=[
            {"role": "system",
                "content": "Extract the list of entities and their values from the provided Source Data and Medical Report in tabular format with 3 columns named as Entity ,Source Data value, Medical Report Value .\n\nAn Entity is:\n- Relevant: to the main story.\n- Specific: descriptive yet concise (5 words or fewer).\n- Faithful: present in the provided data.\n- Anywhere: Located anywhere in provided data."},
            {"role": "user", "content": user_message}
        ] , temperature=0.3,top_p=1 
    )
    return jsonify(response['choices'][0]['message'])

@app.route('/format_transcript', methods=['POST'])
def get_format_transcript():
    user_message = request.json.get('transcript')
    response = openai.ChatCompletion.create(
        # The deployment name you chose when you deployed the GPT-35-Turbo or GPT-4 model.
        engine="432",
        messages=[
            {"role": "system",
                "content": "You will be provided with a transcript of a conversation between a doctor and a patient in either of English , Mandarin , Indonesian or Tamil language. You need to re format the transcript in English in a way that it is easy to read and understand.Please ensure to do proper tagging as Doctor , Patient. You can use any format provided in Sample Transcript below. Do not add any additional information to the transcript. \n\nSample Transcript:\nDoctor: Hello, how are you?\nPatient: I am fine, thank you.\nDoctor: What brings you here today?\nPatient: I have a headache.\nDoctor: How long have you had it?\nPatient: For about a week."},
            {"role": "assistant", "content": user_message}
        ] , temperature=0.2,top_p=1 
    )
    return jsonify(response['choices'][0]['message'])

@app.route('/summarize_transript', methods=['POST'])
def get_summarize_transcript():
    user_message = request.json.get('transcript')
    response = openai.ChatCompletion.create(
        # The deployment name you chose when you deployed the GPT-35-Turbo or GPT-4 model.
        engine="432",
        messages=[
            {"role": "system",
                "content": "You will be provided with a transcript of a conversation between a doctor and a patient in either of English , Mandarin , Indonesian or Tamil language. You need to summarize the transcript in English in a way that it is easy to read and understand. Summary should include Problem, Medical history, Medications, Allergies, Family history, Social history, Physical exam, Assessment, Plan. \n\nSample Summary: \nProblem: \nPatient has a headache for about a week. \n\nMedical history: \nPatient has no medical history. \n\nMedication:\n Patient is not taking any medications. \n\nAllergies:\n Patient has no allergies. Patient has no family history. \n\nFamily history:\n Patient has no social history. \n\nPhysical examination:\n Patient has no physical exam. \n\nAssessment:\n Patient has no assessment. \n\nPlan:\n Patient has no plan."},
            {"role": "assistant", "content": user_message}
        ] , temperature=0.2,top_p=1 
    )
    return jsonify(response['choices'][0]['message'])

@app.route('/solve-mystery', methods=['POST'])
def solve_mystery():
    user_input = request.json['text']
    initial_context = """You are a database of evidence that will be used to solve the mystery of the missing merlion. Detectives will ask you questions to retrieve the evidence. Use the following guidelines when giving answers:

Answer questions in less than 50 words.
If asked for the clues or evidence, reply with a random Singapore fun fact.
If the answer cannot be found, create a random story.
If the question is irrelevant, reply with a random Singapore fun fact.

Evidence

Merlion Sightings: The merlion was last seen by credible sources at 1:30am on 2 Jan 2024.

Site investigations:
 -Only nuts and bolts were left scattered around the scene.
 -The floor was undamaged and there are no signs of the Merlion being forcefully removed.
 -Skidding marks were seen towards the direction of the river.

Surveillance footage:
 -A medium-sized box truck was seen entering the Merlion park on 2 Jan 1:58am. The truck left the park at 3:12am.
 -The license plate on the truck is GBF 2546 J.
 -The truck is registered to “Lion Construction Company”.

Lion Construction Company
 -The company is headquartered in Paya Lebar industrial estate and is a licensed contractor for the merlion maintenance.
 -The company was requested by STB to conduct an unscheduled maintenance on 2 Jan, with instructions to leave the equipment on-site after maintenance.
 -Bob was rostered to conduct the merlion maintenance on 2 Jan early morning.
 -Preliminary investigations show Bob to be an animal lover with the lion as his favourite animal.

Singapore Tourism Board (STB)
 -STB oversees scheduling the merlion maintenance.
 -The maintenance schedule is publicly available on the STB website.
 -John is the manager in charge of scheduling maintenance for tourist attractions.
 -John instructed Lion Construction Company to leave the equipment at the site after conducting maintenance.

John
 -John has been working at STB for 5 years.
 -John is a patron of the arts and is active on social media promoting up-and-coming artist.
 -Just before the merlion disappearance, there were unusual telephone logs to an unknown number.

Interviews from Members of the Public
 -Prior to the disappearance, visitors interviewed mentioned that the merlion did not seem securely fastened to the base and would wobble when winds were strong.

Maritime Logs on 2 Jan
 -There were many boats moored along the Singapore River that night.
 -The only active boat during the night was Bumboat “X19545B”.
 -3:20am: Bumboat “X19545B” was in the vicinity of the merlion.
 -4:10am: Bumboat “X19545B” was in the vicinity of the Keppel Bay.

Barge “X19545B”
 -20m long vessel belonging to “Boating Forever Club”
 -Rented by Singapore Art Forever Society from 1 Jan to 3 Jan.
 -The rental company noted that the boat was returned with 10m of heavy-duty sailing rope left on the deck.

Singapore Art Forever Society
 -The society was founded in 1995 by 48-year-old Sally
 -The society owns Warehouse 21 along Keppel Bay
 -The society is known to attract struggling avant-garde sculptors.

Warehouse 21
 -Preliminary visits to the warehouse show that it is locked with the windows blacked out. Investigators were unable to view the contents inside.
 -Interviews from neighbouring warehouses state that heavy machine noises have been heard recently.

Sally
 -Sally is a pet lover with 5 cats, 3 dogs and a goldfish.
 -Past posts on IG shows her frustration with the governments lack of funding for the local arts scene.
 -Recently posted on IG that she will unveiling a surprise sculpture on Chinese New Year eve. The post was liked by John."""

    try:
        response = openai.ChatCompletion.create(
            engine="432",
            messages=[
                {"role": "system", "content": initial_context},
                {"role": "assistant", "content": user_input}
            ], temperature=0.2, top_p=1 
        )
        interpreted_query = response['choices'][0]['message']['content']
    except Exception as e:
        return jsonify({"error": str(e)})
    
    return jsonify({"response": interpreted_query})



# Run Server
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
