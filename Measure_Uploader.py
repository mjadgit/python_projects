# from simple_salesforce import SalesforceLogin
# from simple_salesforce import SFType
from simple_salesforce import Salesforce
import easygui as ui
import sys
import os
import requests
import base64
import json
# import csv
# from datetime import datetime

####################### TESTING MODE##############
testing_mode = 0  # 0 or 1

if testing_mode is 0:
    file_paths = sys.argv[1:]
    path = os.path.abspath(file_paths[0])
    file_name = os.path.basename(file_paths[0])
    print("\n\n" + "Measure Uploader by https://github.com/mjadgit/" + "\n\n")
    print("Path:", path)
    print("Filename:", file_name, "\n")
    # returns the first part of the filename, the measure number before
    # underscore
    measure_number = os.path.basename(file_name).split('_')[0]
    os.startfile(file_paths[0])  # Opens the PDF file for human analysis
if testing_mode is 1:
    file_paths = "REDACTED"
    file_name = "REDACTED"
    # os.startfile(file_paths)
    measure_number = 12759999  # hardcoded measure number for testing.
####################### TESTING MODE##############


# session_id, instance = SalesforceLogin(
#     username='REDACTED',
#     password='REDACTED',
#     security_token='REDACTED',
#     sandbox=False)

# model = SFType('Model__c', session_id,
#                'REDACTED')

sforg2 = Salesforce(username='REDACTED', password='REDACTED',
                    security_token='REDACTED')
sessionId = sforg2.session_id


query_string_model = "SELECT Id, Name, REDACTED__c, Description__c, Property__c FROM Model__c WHERE REDACTED__c = '{}'".format(
    measure_number)
query_return = sforg2.query(query_string_model)

model_id = query_return['records'][0]['Id']
model_name = query_return['records'][0]['Name']
model_desc = query_return['records'][0]['Description__c']
model_prop = query_return['records'][0]['Property__c']

query_string_prop = "SELECT Street_Address__c, Community__c, Account__c FROM Property__c WHERE Id = '{}'".format(
    model_prop)
query_return_prop = sforg2.query(query_string_prop)

street_address = query_return_prop['records'][0]['Street_Address__c']

print("Model:", model_name)
print("Description:", model_desc)
print("Property:", street_address)

enterbox_msg = "Enter new description below...\nIf no changes, click OK to continue. \
Cancel to exit.\n\nProperty: {}\n\nName: {}\nMeasure Number: {}\nDescription: {}".format(street_address, model_name, measure_number, model_desc)
enterbox_return = ui.enterbox(msg=enterbox_msg, title="Measure Uploader - https://github.com/mjadgit/")

if enterbox_return is None:
    try:
        os.system('TASKKILL /F /IM AcroRd32.exe')
    except:
        pass
    raise SystemExit
if enterbox_return is "":
    pass
else:
    sforg2.Model__c.update(model_id, {'Description__c': enterbox_return})


try:
    os.system('TASKKILL /F /IM AcroRd32.exe')
except:
    pass

# ui.msgbox(enterbox_return)


######################
# Uploading Attachment
######################

url = "REDACTED"
bearer = "Bearer " + sessionId
header = {'Content-Type': 'application/json', 'Authorization': bearer}


body = ""
with open(path, "rb") as upload:
    body = base64.b64encode(upload.read()).decode('UTF-8')
data = json.dumps({
                   'ParentId': model_id,
                   'Name': file_name,
                   'body': body
                  })
response = requests.post(url, headers=header, data=data)

new_attachment_id = response.json()["id"]

print(response.text)
print(response.json()["id"])

measure_link = 'REDACTED/servlet/servlet.FileDownload?file={}'.format(new_attachment_id)

sforg2.Model__c.update(model_id, {'Measurement_Link__c': measure_link, 'REDACTED_Status__c': 'In Progress'})

ui.msgbox(msg="PDF attached. Exiting.", title="Measure Uploader - https://github.com/mjadgit/")
raise SystemExit
