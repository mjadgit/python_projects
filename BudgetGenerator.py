# Budget Generator

import csv

with open('appliances.csv', newline='') as applcsv:
    applcsvread = csv.reader(applcsv, delimiter=',', dialect='excel')
    next(applcsvread, None)  # Skips header
    appliances = []
    for row in applcsvread:
        if len(row) != 0:
            appliances = appliances + [row]

applcsv.close()  # closing file loaded in memory


with open('budget.csv', 'w', newline='') as tempwrite:
    writer = csv.writer(tempwrite, delimiter=',', dialect='excel')
    writer.writerow(['REDACTED__c'])
    # Budget File headers below, not Product Load headers
    headers = ['Record ID', 'Account', 'Budget', 'Category', 'Code', 'Cost', 'Desc', 'Item', 'Preferred Product', 'Product', 'Region',
               'Retail', 'Subcategory', 'Tax Rate']
    writer.writerow(headers)

    for appliance in appliances:

        accounts = ['REDACTED']
        States = ['GA', 'AL', 'MN', 'MA', 'CT', 'NH', 'NJ', 'NY', 'IL']

        for account in accounts:
            for state in States:

                MainColumns = ['New', account, '', appliance[3], appliance[5], appliance[9], appliance[5], appliance[
                    1], 'FALSE', appliance[0], '', appliance[9], 'Other', '', appliance[15], appliance[16], 'FALSE', 'FALSE', state]
                #MainColumns.append(state)
                writer.writerow(MainColumns)
                #MainColumns.remove(MainColumns[18])

tempwrite.close()
raise SystemExit

# writer.writerow(MainColumns, 'GA')
# writer.writerow([MainColumns, 'AL'])
# writer.writerow([MainColumns, 'MN'])
# writer.writerow([MainColumns, 'MA'])
# writer.writerow([MainColumns, 'CT'])
# writer.writerow([MainColumns, 'NH'])
# writer.writerow([MainColumns, 'NJ'])
# writer.writerow([MainColumns, 'NY'])
# writer.writerow([MainColumns, 'IL'])

# writer.writerow([account, ProductFamily, ProductCode, MSRP, ProductCode,'GA'])
# writer.writerow([account, ProductFamily, ProductCode, MSRP, ProductCode,'AL'])
# writer.writerow([account, ProductFamily, ProductCode, MSRP, ProductCode,'MN'])
# writer.writerow([account, ProductFamily, ProductCode, MSRP, ProductCode,'MA'])
# writer.writerow([account, ProductFamily, ProductCode, MSRP, ProductCode,CT'])
# writer.writerow([account, ProductFamily, ProductCode, MSRP, ProductCode,'NH'])
# writer.writerow([account, ProductFamily, ProductCode, MSRP, ProductCode,'NJ'])
# writer.writerow([account, ProductFamily, ProductCode, MSRP, ProductCode,'NY'])
# writer.writerow([account, ProductFamily, ProductCode, MSRP, ProductCode,'IL'])


# print(len(appliances[0]))
# lastrow = (appliances[len(appliances)-1])
# print(lastrow[3])


# with open('budget.csv', 'a') as budget:
#     budgetwriter = csv.writer(budget)
#     for appliance in appliances:
#
# import csv
# applfile = open('appliances.csv')
# csv_file = csv.reader(applfile)

# for row in csv_file:
#     print(row)
# applfile.close()
