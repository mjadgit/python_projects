import easygui as g
import pyautogui as auto
import webbrowser
import os
import time
import pyperclip

testing_mode = 1  # 0 to turn off, 1 to turn on

if testing_mode == 1:
    g.msgbox('Testing mode is on.', "B2B Flooring Order Creator - Created by https://github.com/mjadgit/")

msg = "B2B Flooring Order Creator. Please enter the following information:"
title = "B2B Flooring Order Creator - Created by https://github.com/mjadgit/"
fieldNames = ["Store #:", "Phone #:", "SKU #:", "Par % (4, 5, 8, 10):",
              "Invoice Total:", "Street 1:", "Street 2:", "Zip Code:", "Job Name:", "Special Instructions:",
               "Stage for payment? (y/n):", "Multi-SKU order? (y/n)"]
entryform = []
entryform = g.multenterbox(msg, title, fieldNames)
if entryform is None:
    g.msgbox('Goodbye!', 'Exiting')
    raise SystemExit

# Editable variables:
stageemail = 'REDACTED'
esvsnote = 'REDACTED: **DO NOT COPY, CANCEL OR MODIFY** AWAITING PAYMENT** If you should have any questions regarding this order, please call REDACTED. Thanks.'
auto.PAUSE = 0.01
auto.FAILSAFE = True
maxsearchloops = 15  # Create and maintain search independently modified.
storeloadwaittime = 10  # in seconds.


# Variables created from user entryform input
storenum = entryform[0]
phonenum = entryform[1]
skunum = entryform[2]
parpercent = int(entryform[3])
invtotal = entryform[4]
street1 = entryform[5]
street2 = entryform[6]
zipcode = entryform[7]
jobname = entryform[8]
specinstr = entryform[9]
stage = entryform[10]
multiSKUorder = entryform[11]

# Multi SKU entry form and variable creation
if multiSKUorder is 'y' or multiSKUorder is 'Y':
    secondSKUentry = g.multenterbox('Please enter all second SKU information:', title, ['Second SKU #:', 'Second Invoice Total:', "Second Special Instructions:", "More than 2 SKUs? (y/n):"])
    if secondSKUentry is None:
        g.msgbox('Goodbye!', 'Exiting')
        os._exit(1)
    skunum2 = secondSKUentry[0]
    invtotal2 = secondSKUentry[1]
    specinstr2 = secondSKUentry[2]
    more2sku = secondSKUentry[3]
else:
    pass

# Screenshot image variables corresponding to filenames in root folder
createmaintimg = 'createmaint.png'
phoneentryimg = 'phoneentry.png'
skuentryimg = 'skuentry.png'
measurepopupimg = 'measurepopup.png'
greenarrowimg = 'greenarrow.png'
servicesiteimg = "servicesite.png"
continuebuttonimg = 'continuebutton.png'
lookupimg = 'lookup.png'
jobdescriptimg1 = 'jobdescript1.png'
jobdescriptimg2 = 'jobdescript2.png'
addnotesimg = 'addnotes.png'
saveandexitimg = 'saveandexit.png'
printimg = 'print.png'
emailimg = 'email.png'
donotprintimg = 'donotprint.png'
acceptbuttonimg = 'acceptbutton.png'
relatedinstallimg = 'relatedinstall.png'
parboxblueimg = 'parboxblue.png'

if parpercent == 4:
    parimg1 = 'par4orange.png'
    parimg2 = 'par4orange.png'
elif parpercent == 5:
    parimg1 = 'par5orange.png'
    parimg2 = 'par5white.png'
elif parpercent == 8:
    parimg1 = 'par8orange.png'
    parimg2 = 'par8white.png'
elif parpercent == 10:
    parimg1 = 'par10orange.png'
    parimg2 = 'par10white.png'


#############################
# Define functions
#############################

def searchcreatemaint():
    try:
        global reply
        global search
        reply = None
        search = auto.locateCenterOnScreen(createmaintimg)
        loopcount = 0
        while search is None:
            search = auto.locateCenterOnScreen(createmaintimg)
            if search is None and loopcount >= 40:
                reply = g.indexbox('Create and maintain not found', 'B2B Flooring', choices=[
                                   'Continue Searching', 'Attempt phone search', 'Exit'])
                if reply == 0:
                    reply = None
                    pass
                elif reply == 1:
                    break
                elif reply == 2:
                    os._exit(1)
            loopcount = loopcount + 1
            time.sleep(0.1)
    except:
        g.msgbox("Exception: searchcreatemaint(). Exiting")
        os._exit(1)


def clickoncreatemaint():
    try:
        global reply
        global search
        if reply is None:
            auto.moveTo(search[0], search[1])
            auto.click()
        elif reply == 1:
            pass
    except:
        g.msgbox("Exception: clickoncreatemaint(). Exiting")
        os._exit(1)


def findphoneentry():
    try:
        global reply
        global search
        reply = None
        search = auto.locateCenterOnScreen(phoneentryimg)
        loopcount = 0
        while search is None:
            search = auto.locateCenterOnScreen(phoneentryimg)
            if search is None and loopcount >= maxsearchloops:
                reply = g.indexbox('Phone entry not found', 'B2B Flooring', choices=[
                                   'Continue Searching', 'Pause for customer selection', 'Exit'])
                if reply == 0:
                    reply = None
                    pass
                elif reply == 1:
                    break
                elif reply == 2:
                    os._exit(1)
            loopcount = loopcount + 1
            time.sleep(0.1)
    except:
        g.msgbox("Exception: findphoneentry(). Exiting")
        os._exit(1)


def enterphone():
    try:
        global reply
        global search
        if reply is None:
            auto.moveTo(search[0], search[1])
            auto.click()
            time.sleep(0.7)
            auto.typewrite(phonenum, interval=0.1)
            auto.press('enter')
        elif reply == 1:
            pass
    except:
        g.msgbox("Exception: enterphone(). Exiting")
        os._exit(1)


def searchskuentry():
    try:
        global reply
        global search
        reply = None
        search = auto.locateCenterOnScreen(skuentryimg)
        loopcount = 0
        while search is None:
            search = auto.locateCenterOnScreen(skuentryimg)
            if search is None and loopcount >= maxsearchloops:
                reply = g.indexbox('SKU entry not found', 'B2B Flooring', choices=[
                                   'Continue Searching', 'Find measure popup', 'Exit'])
                if reply == 0:
                    reply = None
                    pass
                elif reply == 1:
                    break
                elif reply == 2:
                    os._exit(1)
            loopcount = loopcount + 1
            time.sleep(0.1)
    except:
        g.msgbox("Exception: searchskuentry(). Exiting")
        os._exit(1)


def entersku():
    try:
        global reply
        global search
        if reply is None:
            auto.moveTo(search[0], search[1])  # move to image location
            auto.moveRel(0, 34)  # move to field entry position on screen, relative to found image
            auto.click()
            time.sleep(0.5)
            auto.typewrite(skunum, interval=0.1)
            auto.press('enter')
        elif reply == 1:
            pass
    except:
        g.msgbox("Exception: entersku(). Exiting")
        os._exit(1)


def searchmeasurepopup():
    try:
        global reply
        global search
        reply = None
        search = auto.locateCenterOnScreen(measurepopupimg)
        loopcount = 0
        while search is None:
            search = auto.locateCenterOnScreen(measurepopupimg)
            if search is None and loopcount >= maxsearchloops:
                reply = g.indexbox('Measure popup not found', 'B2B Flooring', choices=[
                                   'Continue Searching', 'Proceed within install line', 'Exit'])
                if reply == 0:
                    reply = None
                    pass
                elif reply == 1:
                    break
                elif reply == 2:
                    os._exit(1)
            loopcount = loopcount + 1
            time.sleep(0.1)
    except:
        g.msgbox("Exception: searchmeasurepopup(). Exiting")
        os._exit(1)


def clickmeasureok():
    try:
        global reply
        global search
        if reply is None:
            auto.moveTo(search[0], search[1])  # move to image location
            auto.moveRel(0, 39)  # move down to ok button, relative to found image
            auto.click()
        elif reply == 1:
            pass
    except:
        g.msgbox("Exception: clickmeasureok(). Exiting")
        os._exit(1)


def searchgreenarrow():
    try:
        global reply
        global search
        reply = None
        search = auto.locateCenterOnScreen(greenarrowimg)
        loopcount = 0
        while search is None:
            search = auto.locateCenterOnScreen(greenarrowimg)
            if search is None and loopcount >= maxsearchloops:
                reply = g.indexbox('Green arrow not found', 'B2B Flooring', choices=[
                                   'Continue Searching', 'Pass', 'Exit'])
                if reply == 0:
                    reply = None
                    pass
                elif reply == 1:
                    break
                elif reply == 2:
                    os._exit(1)
            loopcount = loopcount + 1
            time.sleep(0.1)
    except:
        g.msgbox("Exception: searchgreenarrow(). Exiting")
        os._exit(1)


def clickgreenarrow():
    try:
        global reply
        global search
        if reply is None:
            auto.moveTo(search[0], search[1])  # move to image location
            auto.click()
        elif reply == 1:
            pass
    except:
        g.msgbox("Exception: clickgreenarrow(). Exiting")
        os._exit(1)


def searchservicesite():
    try:
        global reply
        global search
        reply = None
        search = auto.locateCenterOnScreen(servicesiteimg)
        loopcount = 0
        while search is None:
            search = auto.locateCenterOnScreen(servicesiteimg)
            if search is None and loopcount >= maxsearchloops:
                reply = g.indexbox('Service Site not found', 'B2B Flooring', choices=[
                                   'Continue Searching', 'Pass', 'Exit'])
                if reply == 0:
                    reply = None
                    pass
                elif reply == 1:
                    break
                elif reply == 2:
                    os._exit(1)
            loopcount = loopcount + 1
            time.sleep(0.1)
    except:
        g.msgbox("Exception: searchservicesite(). Exiting")
        os._exit(1)


def fillservicesite():
    try:
        global reply
        global search
        if reply is None:
            auto.moveTo(search[0], search[1])   # move to image location
            auto.moveRel(140, 0)  # moveRel into box
            auto.click()  # Clicks into Name Field
            auto.press('tab')  # Enter Company field
            auto.press('tab')  # Enter Home Number field
            auto.typewrite(phonenum, interval=0.05)
            time.sleep(0.008)
            auto.press('tab')  # Enter Work Number field
            time.sleep(0.008)
            auto.typewrite(phonenum, interval=0.05)
            auto.press('tab')  # Enter Cell filed
            auto.press('tab')  # Enter Ext Field
            auto.press('tab')  # Enter Address 1 Field
            auto.typewrite(street1, interval=0.05)
            auto.press('tab')  # Enter Address 2 field
            auto.typewrite(street2, interval=0.05)
            auto.press('tab')  # Enter Cross St1 field
            auto.press('tab')  # Enter Cross St2 field
            auto.press('tab')  # Enter City field
            auto.press('tab')  # Enter State field
            auto.press('tab')  # Enter Zip field
            auto.typewrite(zipcode, interval=0.05)
            auto.press('tab')  # Enter County
        elif reply == 1:
            pass
    except:
        g.msgbox("Exception: fillservicesite(). Exiting")
        os._exit(1)


def searchparimg():
    try:
        global reply
        global search
        reply = None
        search = auto.locateCenterOnScreen(parimg1)
        loopcount = 0
        while search is None:
            search = auto.locateCenterOnScreen(parimg1)
            if search is None:
                search = auto.locateCenterOnScreen(parimg2)
            if search is None and loopcount >= maxsearchloops:
                reply = g.indexbox('Par Image not found', 'B2B Flooring', choices=[
                                   'Continue Searching', 'Pass', 'Exit'])
                if reply == 0:
                    reply = None
                    pass
                elif reply == 1:
                    break
                elif reply == 2:
                    os._exit(1)
            loopcount = loopcount + 1
            time.sleep(0.1)
    except:
        g.msgbox("Exception: searchparimg(). Exiting")
        os._exit(1)


def selectpar_entervalue():
    try:
        global reply
        global search
        loopcount = 0
        if reply is None:
            auto.moveTo(search[0], search[1])  # move to PARx image location
            auto.click()  # Clicks proper PAR line
            # Searches for blue checkbox
            time.sleep(1)  # Waits for any other blue check boxes to disappear
            search = auto.locateCenterOnScreen(parboxblueimg)
            while search is None:
                search = auto.locateCenterOnScreen(parboxblueimg)
                if search is None and loopcount >= maxsearchloops:
                    reply = g.indexbox('Checkbox not found', 'B2B Flooring', choices=[
                                       'Continue Searching', 'Pass', 'Exit'])
                    if reply == 0:
                        reply = None
                        pass
                    elif reply == 1:
                        break
                    elif reply == 2:
                        os._exit(1)
                loopcount = loopcount + 1
                time.sleep(0.1)
            auto.moveTo(search[0], search[1])  # Moves to found blue box image
            auto.click()
            time.sleep(0.1)
            auto.typewrite(invtotal, interval=0.05)
            auto.press('enter')
        elif reply == 1:
            pass
    except:
        g.msgbox("Exception: selectpar_entervalue(). Exiting")
        os._exit(1)


def searchcontinuebutton():
    try:
        global reply
        global search
        reply = None
        search = auto.locateCenterOnScreen(continuebuttonimg)
        loopcount = 0
        while search is None:
            search = auto.locateCenterOnScreen(continuebuttonimg)
            if search is None and loopcount >= maxsearchloops:
                reply = g.indexbox('Continue button not found', 'B2B Flooring', choices=[
                                   'Continue Searching', 'Pass', 'Exit'])
                if reply == 0:
                    reply = None
                    pass
                elif reply == 1:
                    break
                elif reply == 2:
                    os._exit(1)
            loopcount = loopcount + 1
            time.sleep(0.1)
    except:
        g.msgbox("Exception: searchcontinuebutton(). Exiting")
        os._exit(1)


def clickcontinue():
    try:
        global reply
        global search
        if reply is None:
            auto.moveTo(search[0], search[1])  # move to image location
            auto.click()
        elif reply == 1:
            pass
    except:
        g.msgbox("Exception: clickcontinue(). Exiting")
        os._exit(1)


def searchlookupimg():
    try:
        global reply
        global search
        reply = None
        search = auto.locateCenterOnScreen(lookupimg)
        loopcount = 0
        while search is None:
            search = auto.locateCenterOnScreen(lookupimg)
            if search is None and loopcount >= maxsearchloops:
                reply = g.indexbox('Look-up/Continue button not found', 'B2B Flooring', choices=[
                                   'Continue Searching', 'Pass', 'Exit'])
                if reply == 0:
                    reply = None
                    pass
                elif reply == 1:
                    break
                elif reply == 2:
                    os._exit(1)
            loopcount = loopcount + 1
            time.sleep(0.1)
        search = auto.locateCenterOnScreen(continuebuttonimg)  # Search for continue button again, after finding 'Look-up' image
    except:
        g.msgbox("Exception: searchlookupimg(). Exiting")


def searchjobdescription():
    try:
        global reply
        global search
        reply = None
        search = auto.locateCenterOnScreen(jobdescriptimg1)
        loopcount = 0
        while search is None:
            search = auto.locateCenterOnScreen(jobdescriptimg1)
            if search is None:
                search = auto.locateCenterOnScreen(jobdescriptimg2)
            if search is None and loopcount >= maxsearchloops:
                reply = g.indexbox('Job Description not found', 'B2B Flooring', choices=[
                                   'Continue Searching', 'Pass', 'Exit'])
                if reply == 0:
                    reply = None
                    pass
                elif reply == 1:
                    break
                elif reply == 2:
                    os._exit(1)
            loopcount = loopcount + 1
            time.sleep(0.1)
    except:
        g.msgbox("Exception: searchjobdescription(). Exiting")
        os._exit(1)


def enterjobdesc():
    try:
        global reply
        global search
        if reply is None:
            auto.moveTo(search[0], search[1])
            time.sleep(0.02)
            auto.click()
            time.sleep(0.1)
            # auto.hotkey('ctrl', 'a')
            # pyperclip.copy(jobname)
            # auto.hotkey('ctrl', 'v')
            # pyperclip.copy('')
            auto.typewrite(jobname, interval=0.01)
            auto.press('tab')
            time.sleep(0.02)
        elif reply == 1:
            pass
    except:
        g.msgbox("Exception: enterjobdesc(). Exiting")
        os._exit(1)


def searchaddnotes():
    try:
        global reply
        global search
        reply = None
        search = auto.locateCenterOnScreen(addnotesimg)
        loopcount = 0
        while search is None:
            search = auto.locateCenterOnScreen(addnotesimg)
            if search is None and loopcount >= maxsearchloops:
                reply = g.indexbox('Add Notes not found', 'B2B Flooring', choices=[
                                   'Continue Searching', 'Pass', 'Exit'])
                if reply == 0:
                    reply = None
                    pass
                elif reply == 1:
                    break
                elif reply == 2:
                    os._exit(1)
            loopcount = loopcount + 1
            time.sleep(0.1)
    except:
        g.msgbox("Exception: searchaddnotes(). Exiting")
        os._exit(1)


def clickandtypenotes():
    try:
        global reply
        global search
        loopcount = 0
        if reply is None:
            auto.moveTo(search[0], search[1])  # move to found Add Notes image location
            auto.click()
            search = auto.locateCenterOnScreen(saveandexitimg)
            while search is None:  # whie looop searches for save and exit button. This is how it knows note screen has loaded
                search = auto.locateCenterOnScreen(saveandexitimg)
                if search is None and loopcount >= maxsearchloops:
                    reply = g.indexbox('Add Note Entry  not found', 'B2B Flooring', choices=[
                                       'Continue Searching', 'Pass', 'Exit'])
                    if reply == 0:
                        reply = None
                        pass
                    elif reply == 1:
                        break
                    elif reply == 2:
                        os._exit(1)
#            auto.moveTo(search[0], search[1])
#            auto.moveRel(-450, -150)
#            auto.click()
#            time.sleep(0.4)
#            pyperclip.copy(esvsnote)
#            auto.hotkey('ctrl', 'v')
#            pyperclip.copy('')
            auto.typewrite(esvsnote, interval=0.01)  # Types out esvs note
            auto.press('tab')
            time.sleep(0.2)
            auto.press('down')
            auto.press('enter')  # sets FYI designation
            auto.moveTo(search[0], search[1])
            auto.click()  # Clicks Save and Exit, saving note
        elif reply == 1:
            pass
    except:
        g.msgbox("Exception: clickandtypenotes(). Exiting")
        os._exit(1)


def searchprint():
    try:
        global reply
        global search
        reply = None
        search = auto.locateCenterOnScreen(printimg)
        loopcount = 0
        while search is None:
            search = auto.locateCenterOnScreen(printimg)
            if search is None and loopcount >= maxsearchloops:
                reply = g.indexbox('Print button not found', 'B2B Flooring', choices=[
                                   'Continue Searching', 'Pass', 'Exit'])
                if reply == 0:
                    reply = None
                    pass
                elif reply == 1:
                    break
                elif reply == 2:
                    os._exit(1)
            loopcount = loopcount + 1
            time.sleep(0.1)
    except:
        g.msgbox("Exception: searchprint(). Exiting")
        os._exit(1)


def fillemailcsa():
    try:
        global reply
        global search
        loopcount = 0
        if reply is None:
            auto.moveTo(search[0], search[1])  # move to found Print button image location
            auto.click()

            search = auto.locateCenterOnScreen(emailimg)
            while search is None:  # whie looop searches for 'email' imgage. This is how it knows print screen has loaded
                search = auto.locateCenterOnScreen(emailimg)
                if search is None and loopcount >= maxsearchloops:
                    reply = g.indexbox('Email field not found', 'B2B Flooring', choices=[
                                       'Continue Searching', 'Pass', 'Exit'])
                    if reply == 0:
                        reply = None
                        pass
                    elif reply == 1:
                        break
                    elif reply == 2:
                        os._exit(1)
            auto.moveTo(search[0], search[1])
            auto.click()  # Clicks 'email'
            auto.hotkey('ctrl', 'a')
            auto.typewrite(stageemail, interval=0.02)  # Types out emai address

            search = auto.locateCenterOnScreen(donotprintimg)
            while search is None:  # whie looop searches for 'do not print' imgage.
                search = auto.locateCenterOnScreen(donotprintimg)
                if search is None and loopcount >= maxsearchloops:
                    reply = g.indexbox('Do Not Print button not found', 'B2B Flooring', choices=[
                                       'Continue Searching', 'Pass', 'Exit'])
                    if reply == 0:
                        reply = None
                        pass
                    elif reply == 1:
                        break
                    elif reply == 2:
                        os._exit(1)
            auto.moveTo(search[0], search[1])
            auto.click()  # Clicks 'do not print'

            search = auto.locateCenterOnScreen(acceptbuttonimg)
            while search is None:  # whie looop searches for 'accept' button imgage.
                search = auto.locateCenterOnScreen(acceptbuttonimg)
                if search is None and loopcount >= maxsearchloops:
                    reply = g.indexbox('Accept button not found', 'B2B Flooring', choices=[
                                       'Continue Searching', 'Pass', 'Exit'])
                    if reply == 0:
                        reply = None
                        pass
                    elif reply == 1:
                        break
                    elif reply == 2:
                        os._exit(1)
            auto.moveTo(search[0], search[1])
            auto.click()  # Clicks 'accept' button
    except:
        g.msgbox("Exception: fillemailcsa(). Exiting")
        os._exit(1)


def searchrelatedinstall():
    try:
        global reply
        global search
        reply = None
        search = auto.locateCenterOnScreen(relatedinstallimg)
        loopcount = 0
        while search is None:
            search = auto.locateCenterOnScreen(relatedinstallimg)
            if search is None and loopcount >= maxsearchloops:
                reply = g.indexbox('Related Install not found', 'B2B Flooring', choices=[
                                   'Continue Searching', 'Pass', 'Exit'])
                if reply == 0:
                    reply = None
                    pass
                elif reply == 1:
                    break
                elif reply == 2:
                    os._exit(1)
            loopcount = loopcount + 1
            time.sleep(0.1)
    except:
        g.msgbox("Exception: searchrelatedinstall(). Exiting")
        os._exit(1)


def clickrelatedinstallcheckbox():
    try:
        global reply
        global search
        if reply is None:
            auto.moveTo(search[0], search[1])  # move to image location
            auto.moveRel(0, 146)  # move down to checkbox, relative to found image
            auto.click()
        elif reply == 1:
            pass
    except:
        g.msgbox("Exception: clickrelatedinstallcheckbox(). Exiting")
        os._exit(1)


def find_click_accept():
    search = auto.locateCenterOnScreen(acceptbuttonimg)
    loopcount = 0
    while search is None:  # whie looop searches for 'accept' button imgage.
        search = auto.locateCenterOnScreen(acceptbuttonimg)
        if search is None and loopcount >= maxsearchloops:
            reply = g.indexbox('Accept button not found', 'B2B Flooring', choices=[
                               'Continue Searching', 'Pass', 'Exit'])
            if reply == 0:
                reply = None
                pass
            elif reply == 1:
                break
            elif reply == 2:
                os._exit(1)
    auto.moveTo(search[0], search[1])
    auto.click()  # Clicks 'accept' button


#############################
# Executing
#############################

if testing_mode == 1:
    stageemail = 'testing@nat3stingna.com'
    esvsnote = 'Test order. Please disregard and cancel if needed.'
    invtotal = '2345.67'
    invtotal2 = '3456.78'
    street1 = '123 Testing Street'
    street2 = 'PO Testing'
    zipcode = '90210'
    jobname = 'Test Order. Please Cancel'
    specinstr = 'This is a test order. Please cancel if needed.'
    specinstr2 = 'This is a test order. Second SKU spec instruct. Please cancel.'
else:
    pass

# Open browser to correct store
url = 'REDACTED' % storenum
ie = webbrowser.get(webbrowser.iexplore)
ie.open(url)

# Wait for store to load before starting first search
time.sleep(storeloadwaittime)

searchcreatemaint()
clickoncreatemaint()

findphoneentry()
enterphone()

#  User will need to select proper customer here

searchskuentry()
entersku()

searchmeasurepopup()
clickmeasureok()

searchgreenarrow()  # Begins inside install line
clickgreenarrow()

searchservicesite()
fillservicesite()

# Pause for city/county selection
time.sleep(3)

searchgreenarrow()
clickgreenarrow()

# Get through 'Basic' screen
time.sleep(1)
auto.hotkey('shift', 'tab')
auto.press('enter')

searchparimg()
selectpar_entervalue()

searchgreenarrow()
clickgreenarrow()

time.sleep(0.4)
auto.click()  # Clicks through 'Custom' screen

time.sleep(0.4)
auto.hotkey('ctrl', 'a')
auto.typewrite(specinstr, interval=0.01)
time.sleep(0.4)

auto.click()
time.sleep(0.04)
auto.moveRel(35, 0)  # Move over to save button
auto.click()  # Saves and exits install line

searchcontinuebutton()
clickcontinue()

searchlookupimg()  # Search for presence of 'Look-up' image to see if can enter SKU

if multiSKUorder is 'y' or multiSKUorder is 'Y':
    if testing_mode == 1:
        pass
    else:
        skunum = skunum2

    invtotal = invtotal2

    searchskuentry()
    entersku()

    searchrelatedinstall()
    clickrelatedinstallcheckbox()

    find_click_accept()

    searchmeasurepopup()
    clickmeasureok()

    searchgreenarrow()  # Begins inside install line
    clickgreenarrow()  # 1 into service site , 3rd click lands on PAR
    time.sleep(1)
    auto.click()  # 2 into Basic screen , 3rd click lands on PAR
    time.sleep(1)
    auto.click()  # Now in PAR screen
#    searchservicesite()
#    fillservicesite()#

#    # Pause for city/county selection
#    time.sleep(3)#

#    searchgreenarrow()
#    clickgreenarrow()#

#    # Get through 'Basic' screen
#    time.sleep(1)
#    auto.hotkey('shift', 'tab')
#    auto.press('enter')

    searchparimg()
    selectpar_entervalue()

    searchgreenarrow()
    clickgreenarrow()

    time.sleep(0.4)
    auto.click()  # Clicks through 'Custom' screen
    time.sleep(0.4)

    auto.hotkey('ctrl', 'a')
    auto.typewrite(specinstr2, interval=0.01)
    time.sleep(0.4)

    auto.click()
    time.sleep(0.04)
    auto.moveRel(35, 0)  # Move over to save button
    auto.click()  # Saves and exits install line

    if more2sku is 'y' or more2sku is 'Y':
        g.msgbox('Pausing for additional SKU Entry. Please click OK when ready to proceed.')

    searchcontinuebutton()
    clickcontinue()

    searchlookupimg()
    clickcontinue()
else:
    clickcontinue()

searchjobdescription()
enterjobdesc()

searchaddnotes()
clickandtypenotes()

searchprint()
fillemailcsa()

pyperclip.copy(jobname)

g.msgbox('Order Complete. Exiting', "B2B Flooring")

# if stage is 'y' or stage is 'Y':
#     g.msgbox('Staging order...')
#     pass
# elif stage is 'n' or stage is 'N':
#     g.msgbox('Not staging order...')
#     pass


raise SystemExit
os._exit(1)
