from simple_salesforce import Salesforce
from simple_salesforce import SFType
import easygui as ui
import requests
import json
import base64
from time import sleep

# import pycurl
# import certifi

# import csv
# from time import sleep
# from datetime import datetime
# from simple_salesforce import Salesforce


# fieldNames = ["Property ID:",
#               "Requested Date (YYYY-MM-DD):",
#               "Scheduled Date (YYYY-MM-DD):"]
# fieldValue = []
# fieldValue = ui.multenterbox(msg, title, fieldNames)

# if fieldValue is None:
#     # ui.msgbox('Goodbye', 'Quitting')
#     raise SystemExit

# prop_id = fieldValue[0]
# req_date = fieldValue[1]
# sched_date = fieldValue[2]

# Hardcoded values for ease of testing:
# prop_id = 'REDACTED'
# req_date = 'REDACTED'
# sched_date = 'REDACTED'

# if len(str(prop_id)) is not 15:
#     completemsg = 'Please re-check the property ID. Exiting...'
#     ui.msgbox(completemsg, 'Exiting')
#     raise SystemExit
# else:
#     pass

print('\nEstablishing Salesforce connection...\n')

# session_id, instance = SalesforceLogin(
#     username='REDACTED',
#     password='REDACTED',
#     security_token='REDACTED',
#     sandbox=True)

sf = Salesforce(
    username='REDACTED',
    password='REDACTED',
    security_token='REDACTED',
    sandbox=True)
session_id = sf.session_id

sf_instance = 'REDACTED.my.salesforce.com'

# print(session_id)

# contract = SFType('Contract', session_id,
#                   'REDACTED.my.salesforce.com')

# print('\n{}\n'.format(session_id))

print("Connection established.\n\n")

# contract_return = contract.get('REDACTED')

# for key, val in contract_return.items():
#   # print(key, " = ", val)
#   print('{} = {}'.format(key, val))

# print(contract_return.get('StatusCode'))

attachment = SFType('Attachment', session_id,
                    sf_instance)

parent_ID = 'REDACTED'  # UAT Test Contract

attachment_text = sf.query(
    "SELECT Id, Name, Body FROM Attachment WHERE ParentID = '{}'".format(parent_ID))

# attachment_text = sf.get()

print(attachment_text['records'][0]['Name'])
print(attachment_text['records'][0]['Body'])
for i in attachment_text['records']:
    print(i['Name'])

###########################################################
# requests.get attempt to download attachment
###########################################################
bearer_token = 'Bearer {}'.format(session_id)
url = "https://{}{}".format(sf_instance, attachment_text['records'][0]['Body'])
headers = {'Content-Type': 'application/json', 'Authorization': bearer_token}
body = requests.get(url, headers=headers, stream=True)  # stream=true

data = body.raw.read(decode_content=True)
data64 = base64.encode(data)

# print(body.headers)
# if body.status_code == 200:
#     with open(body, 'wb') as f:
#         for chunk in body:
#             f.write(chunk)

# body64 = base64.b64encode(body)
# # print(body)
###########################################################
# Uploading Above attachment
###########################################################
post_url = "https://{}/services/data/v29.0/sobjects/Attachment/".format(
    sf_instance)
name_up = str(attachment_text['records'][0]['Name'])
response = requests.post(post_url, headers=headers, data=json.dumps(
    {'ParentId': 'REDACTED',
     'Name': name_up,
     'body': data64}))

###########################################################
# Attempting with curl
###########################################################
# c = pycurl.Curl()
# url = "https://{}{}-H 'Authorization: Bearer {}'".format(sf_instance, attachment_text['records'][0]['Body'], session_id)
# c.setopt(c.URL, url)
# c.setopt(pycurl.CAINFO, certifi.where())
# body = c.perform()
# print(body)
#
#
# curl https://REDACTED/body
# -H "Authorization: Bearer token"
############################################################
# try:
#     with open('unitinfo.csv', newline='') as unitcsv:
#         unitcsvread = csv.reader(unitcsv, delimiter=',', dialect='excel')
#         next(unitcsvread, None)  # Skips header
#         for row in unitcsvread:
#             if len(row) != 0:
#                 model_load = {'REDACTED'}
#                 model_return = model.create(model_load)
#                 print(model_return)
#                 sleep(0.1)  # Delay to slow down load rate.
# except:
#     ui.msgbox(
#         "Failed loading models.\nPlease ensure date is in the correct YYYY-MM-DD format.", "Exception")
#     raise SystemExit

# print("\n\nModels Loaded.\n")

# unitcsv.close()  # closing file loaded in memory

completemsg = 'Success'
ui.msgbox(completemsg, 'Success')

raise SystemExit
