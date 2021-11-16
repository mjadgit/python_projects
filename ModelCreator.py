from simple_salesforce import SalesforceLogin
from simple_salesforce import SFType
import easygui as ui
import csv
from time import sleep
# from datetime import datetime
# from simple_salesforce import Salesforce

# Get
msg = "This tool creates flooring models for a specified property.\nPlease make sure CSV file contains new unit and measure information.\n\nUser: REDACTED"
title = "Model Creator - by https://github.com/mjadgit/"
fieldNames = ["Property ID:",
              "Requested Date (YYYY-MM-DD):",
              "Scheduled Date (YYYY-MM-DD):"]
fieldValue = []
fieldValue = ui.multenterbox(msg, title, fieldNames)

if fieldValue is None:
    # ui.msgbox('Goodbye', 'Quitting')
    raise SystemExit

prop_id = fieldValue[0]
req_date = fieldValue[1]
sched_date = fieldValue[2]

# Hardcoded values for ease of testing:
# prop_id = 'REDACTED'
# req_date = 'REDACTED'
# sched_date = 'REDACTED'

if len(str(prop_id)) is not 15:
    completemsg = 'Please re-check the property ID. Exiting...'
    ui.msgbox(completemsg, 'Exiting')
    raise SystemExit
else:
    pass

print('\nEstablishing Salesforce connection...\n')

# session_id, instance = SalesforceLogin(
#     username='REDACTED',
#     password='REDACTED',
#     security_token='REDACTED',
#     sandbox=False)

session_id, instance = SalesforceLogin(
    username='REDACTED',
    password='REDACTED',
    security_token='REDACTED',
    sandbox=False)

model = SFType('Model__c', session_id,
               'REDACTED')
# print('\n{}\n'.format(session_id))

print("Connection established.\n\nAttmepting CSV open...\n\n\n")

try:
    with open('unitinfo.csv', newline='') as unitcsv:
        unitcsvread = csv.reader(unitcsv, delimiter=',', dialect='excel')
        next(unitcsvread, None)  # Skips header
        for row in unitcsvread:
            if len(row) != 0:
                model_load = {'Property__c': prop_id,
                              'Description__c': row[0],
                              'REDACTED__c': row[1],
                              'Requested_Date__c': req_date,
                              'Scheduled_Date__c': sched_date,
                              'REDACTED__c': 'Requested'}
                model_return = model.create(model_load)
                print(model_return)
                sleep(0.1)  # Delay to slow down load rate.
except:
    ui.msgbox(
        "Failed loading models.\nPlease ensure date is in the correct YYYY-MM-DD format.", "Exception")
    raise SystemExit

print("\n\nModels Loaded.\n")

unitcsv.close()  # closing file loaded in memory

completemsg = 'Models have been created'
ui.msgbox(completemsg, 'Load Success')

raise SystemExit
