from simple_salesforce import Salesforce
import easygui as ui
# import csv

msg = "LMS Reporting.\nEnter LMS ID. Tool Returns Record ID"
title = "LMS Record ID"
fieldNames = ["LMS ID:"]
fieldValue = []
fieldValue = ui.multenterbox(msg, title, fieldNames)


sforg1 = Salesforce(username='REDACTED', password='REDACTED',
                    security_token='REDACTED')


LMS_query = "SELECT Stage__c, Id FROM Project__c WHERE LMS_Id__c = '" + str(fieldValue[0]) + "'"
# print(LMS_query)
or1_record_id = sforg1.query(LMS_query)

print(or1_record_id)

ui.msgbox(or1_record_id)

raise SystemExit
