from flask import Flask, render_template, request, jsonify
import requests
import xml.etree.ElementTree as ET
from io import BytesIO
import os
from xml.dom import minidom

app = Flask(__name__)
TRANSLATOR_SUBSCRIPTION_KEY = os.getenv("TRANSLATOR_SUBSCRIPTION_KEY")
TRANSLATOR_REGION ='uaenorth'

def create_xml(data):
 # Define variables
    id_value = "BSG_DEMO_TEST"
    type_value = "XML"
    sequence_value = data.get("sequence")
    delta_record_flag = "Y"
    subject_name = data.get("subject_name")

    # Create XML structure
    root = ET.Element("Message")

    id_elem = ET.SubElement(root, "Id")
    id_elem.text = id_value

    type_elem = ET.SubElement(root, "Type")
    type_elem.text = type_value

    sequence_elem = ET.SubElement(root, "Sequence")
    sequence_elem.text = sequence_value
    data_elem = ET.SubElement(root, "Data")
    cdata_content = f"""
    <txn>
        <delta_record_flag>{delta_record_flag}</delta_record_flag>
        
        <subject_name>{subject_name}</subject_name>
        
    </txn>
    """
    data_elem.text = ET.CDATA(cdata_content) if hasattr(ET, 'CDATA') else cdata_content

    # Generate pretty XML
    rough_string = ET.tostring(root, encoding="utf-8")
    parsed_string = minidom.parseString(rough_string)
    pretty_xml = parsed_string.toprettyxml(indent="  ")
    
    return pretty_xml
   

@app.route('/', methods=['GET', 'POST'])
def form():
    nr_result = None 
    translation = None
    response_body = None
    new_xml = None
    subject_name = None
    pretty_xml =None
    if request.method == 'POST':
        form_data = request.form.to_dict()
        subject_name = form_data.get("subject_original_name")

        # Translate subject_name using Microsoft Translator API
        translator_url = "https://api.cognitive.microsofttranslator.com/translate?api-version=3.0&to=en&toScript=Latn"
        headers = {
            'Ocp-Apim-Subscription-Key': TRANSLATOR_SUBSCRIPTION_KEY,
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Region': TRANSLATOR_REGION 
        }
        body = [{"Text": subject_name}]
        translator_response = requests.post(translator_url, headers=headers, json=body)

        if translator_response.status_code == 200:
            translation = translator_response.json()[0]['translations'][0]['text']
            form_data['subject_name'] = translation

            # Create a new XML
            new_xml = create_xml(form_data)
            
            base_url = form_data.get("base_url")
            # Get token from NetReveal
            token_url = base_url + "/netreveal/rest-external/oauth/token"
            token_data = {"grant_type": "client_credentials"}
            token_headers = {
                'Authorization': 'Basic YWRtaW46c2VjcmV0',  # Replace with Base64 encoded credentials
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            token_response = requests.post(token_url, data=token_data, headers=token_headers, verify=False)
            
            if token_response.status_code == 200:
                token = token_response.json().get("access_token")

                # Call the processMessage API
                process_url = base_url + "/netreveal/rest-external/eim-services/v1.0.0/servicesmanager/processMessage"
                process_headers = {
                    'Authorization': f'Bearer {token}',
                    'Content-Type': 'application/xml'
                }
                process_response = requests.post(process_url, headers=process_headers, data=new_xml, verify=False)
                response_body = process_response.text

    # Render form
    if response_body is not None: 
        x= ET.fromstring (response_body)
        value_elem = x.findall(".//value")
        # Remove CDATA if necessary
        
        if len(value_elem) >= 1 : 
            if value_elem[0].text.strip()=="NOHIT" :
                response_body = "No Hit!"
            elif value_elem[0].text.strip()=="HIT":
                response_body = value_elem[2].text.strip()
                
                parsed_string = minidom.parseString(response_body)
                response_body = parsed_string.toprettyxml(indent="  ")
            else :
                response_body = "No reply"
               
    return render_template('form.html', original_name = subject_name ,translation = translation, response_body=response_body)
   
if __name__ == '__main__':
    app.run(port=50001)