from simple_salesforce import Salesforce
import easygui as ui
import csv

# sample org1 account = REDACTED
# sample org2 account = REDACTED

# Get Account Record ID from user
msg = "This tool transfers existing accounts from REDACTED.\nEnter REDACTED Account Record ID."
title = "SF Org Account Migrator"
fieldNames = ["Account Record ID:"]
fieldValue = []
fieldValue = ui.multenterbox(msg, title, fieldNames)


sforg1 = Salesforce(username='REDACTED', password='REDACTED',
                    security_token='REDACTED')
# Returned dictionary with all values for account in org1
org1account = sforg1.Account.get(fieldValue[0])

# Check for Org1 record type being SP
if org1account['RecordTypeId'] == 'REDACTED':
    org2_recordtype = 'REDACTED'  # SP recordtype
else:
    org2_recordtype = 'REDACTED'  # Client record type

########################################################
# Anticipating blank REDACTED, prevent exception on NoneType

if org1account['REDACTED'] is None:
    org1_REDACTED_acc_ID = org1account['REDACTED']
else:
    org1_REDACTED_acc_ID = '{:,}'.format(int(org1account['REDACTED']))

if org1account['REDACTED_Acct_ID__c'] is None:
    org1_REDACTED_acc_ID = org1account['REDACTED_Acct_ID__c']
else:
    org1_REDACTED_acc_ID = int(org1account['REDACTED_Acct_ID__c'])

########################################################

# Assigning Or2 fields using Org1 values
org2accountload = {'Name': org1account['Name'],
                   'Phone': org1account['Phone'],
                   'Fax': org1account['Fax'],
                   'Website': org1account['Website'],
                   'REDACTED': org1account['REDACTED__c'],
                   'REDACTED': org1account['REDACTED'],
                   'REDACTED': org1account['REDACTED'],
                   'REDACTED': org1REDACTED,
                   'REDACTED__c': org1account['REDACTED__c'],
                   'REDACTED': REDACTED,
                   'BillingStreet': org1account['BillingStreet'],
                   'BillingCity': org1account['BillingCity'],
                   'BillingState': org1account['BillingState'],
                   'BillingPostalCode': org1account['BillingPostalCode'],
                   'RecordTypeId': org2_recordtype}
# 'Onboarding_Status__c': org1account['Status__c']


sforg2 = Salesforce(username='REDACTED', password='REDACTED',
                    security_token='REDACTED')


org2return = sforg2.Account.create(org2accountload)
print(org2return)


with open('log.csv', 'a', newline='') as log:
    logwriter = csv.writer(log, delimiter=',', dialect='excel')
    logwriter.writerow(['Load Status:', 'Success'])
    logwriter.writerow([org2return.items()])
    for val, key in org2accountload.items():
        logwriter.writerow([val, key])
    logwriter.writerow(["'========================================="])

completemsg = 'Account Mirroring Successfull\n', org2return
ui.msgbox(completemsg, 'Load Success')

raise SystemExit
