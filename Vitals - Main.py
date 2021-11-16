import time
import sys
import os
from os import path
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


##############  Script Toggles and Settings  #######################
testMode = False
fireREDACTEDAOnly = False
fireREDACTEDpcOnly = False
killafter = 25   # Kills the below loop after x many iterations
userInputAfterVitalsEntry = False    # If true, will require key press before saving vitals. If False, will pause three seconds and proceed
proceedIfNotFound = False    #  doesn't prompt for correct patient in REDACTED, just skipps to next patient.

# Setting initial variables
firstRun = True
skipPatientsList = []
successfullyCompletedPatients = []   # Growing list. Appended to after successful save.
breakmainloop = False
####################################################################


##############  Credentials ########################################
REDACTEDUsername = 'REDACTED'
REDACTEDPassword = 'REDACTED'
REDACTED2Username = 'REDACTED'
REDACTED2Password = 'REDACTED'
####################################################################


######  FUNCTIONS ##################################################

def promptVitalsDate():                                # Prompts for user to enter vitals date
    global vitalsDate
    print('\n'+
            '============================================================='+'\n' +
            '========= Vitals Automator by https://github.com/mjadgit/==='+'\n' +
            '============================================================='+'\n')
    # Asking for Vitals Date. 't' = todays date | 'n' = exit
    vitalsDate = input('Please enter vitals date (in format MM/DD/YYYY)' + '\n' + 
                    "(Enter 't' to use todays date): ")
    if vitalsDate == 't':           # If user enter's 't', use today's date
        vitalsDate = date.today().strftime("%m/%d/%Y")
    vitalsDateConfirm = input('\n' + 'Date Entered: ' + vitalsDate + '\n\n' +
                      "If correct, enter 'y' to continue. If not, enter 'n' to exit: " + '\n\n')
    if  vitalsDateConfirm == 'n':   # Allows exit on fat-fingered date entry
        print('\n' + 'Invalid date. Exiting ...' + '\n')
        sys.exit()
    print('\n'+'Will be entering vitals for the date of ' + vitalsDate + ' ...' + '\n')


def fireREDACTEDpc():                                         # Opens REDACTED site and logs in to search page
    global REDACTEDdriver
    global REDACTEDwait

    REDACTEDdriver = webdriver.Chrome()
    REDACTEDdriver.get('REDACTED/AppsCentral.aspx')
    REDACTEDwait = WebDriverWait(REDACTEDdriver, 10)
#commented out indented block due to REDACTEDpc login error, need to manually log in.
                            # # REDACTEDpcdriver.switch_to_frame('content')  # old switch_to_frame - not in use
                            # # REDACTEDpcdriver.switch_to_frame('credentials')
                            # # REDACTEDpcdriver.switch_to.frame('content')
                            # # time.sleep(0.5)
                            # # REDACTEDpcdriver.switch_to.frame('credentials')
                            # # time.sleep(0.5)

                            # # Switches to proper frame to enter credentials
                            # REDACTEDpcwait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, 'content')))
                            # REDACTEDpcwait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, 'credentials')))


                            # # Finds all relevant elements on page
                            # # REDACTEDpcUsernameField = REDACTEDpcdriver.find_element(By.XPATH, '/html/body/form[1]/table/tbody/tr[1]/td/table/tbody/tr[1]/td[2]/input')
                            # # REDACTEDpcPasswordField = REDACTEDpcdriver.find_element_by_xpath('/html/body/form[1]/table/tbody/tr[1]/td/table/tbody/tr[2]/td[2]/input')
                            # # REDACTEDpcLoginButton = REDACTEDpcdriver.find_element_by_xpath('/html/body/form[1]/table/tbody/tr[1]/td/table/tbody/tr[3]/td/input')
                            # # #REDACTEDpcPasswordField = REDACTEDpcdriver.find_element_by_name('Ecom_Password')
                            # REDACTEDpcUsernameField = REDACTEDpcwait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/form[1]/table/tbody/tr[1]/td/table/tbody/tr[1]/td[2]/input')))
                            # REDACTEDpcPasswordField = REDACTEDpcwait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/form[1]/table/tbody/tr[1]/td/table/tbody/tr[2]/td[2]/input')))
                            # REDACTEDpcLoginButton = REDACTEDpcwait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/form[1]/table/tbody/tr[1]/td/table/tbody/tr[3]/td/input')))

                            # REDACTEDpcUsernameField.send_keys(REDACTEDpcUsername)
                            # time.sleep(0.25)
                            # REDACTEDpcPasswordField.send_keys(REDACTEDpcPassword)

                            # REDACTEDpcLoginButton.click()
    REDACTEDerrorwait = input("REDACTED login error, waiting for manual login. Please press any key to continue after loggins in...")
    REDACTEDdriver.get('https://REDACTED')

    #REDACTEDpcdriver.maximize_window()
    #REDACTEDpcdriver.quit()


def fireREDACTEDA():                                      # Opens REDACTED Browser and logs in to right before loadTodaysAppointments()
    global REDACTEDAdriver
    global REDACTEDwait

    REDACTEDAdriver = webdriver.Chrome()
    #REDACTEDAdriver.maximize_window()
    REDACTEDAdriver.get('https://REDACTEDA.com')
    REDACTEDwait = WebDriverWait(REDACTEDAdriver, 10)

    # REDACTEDAUserField = REDACTEDAdriver.find_element_by_xpath(".//*[@id='USERNAME']")
    # REDACTEDAPassField = REDACTEDAdriver.find_element_by_xpath(".//*[@id='PASSWORD']")
    REDACTEDAUserField = REDACTEDwait.until(EC.element_to_be_clickable((By.XPATH, ".//*[@id='USERNAME']")))
    REDACTEDAPassField = REDACTEDwait.until(EC.element_to_be_clickable((By.XPATH, ".//*[@id='PASSWORD']")))
    REDACTEDAUserField.send_keys(REDACTEDAUsername)
    REDACTEDAPassField.send_keys(REDACTEDAPassword)
    REDACTEDwait.until(EC.element_to_be_clickable((By.XPATH, ".//*[@id='loginbutton']"))).click()  #Clicks to Login

    
    ##### DEPARTMENT SELECTION ##############
    # departmentSelection = Select(REDACTEDAdriver.find_element_by_xpath('.//*[@id="DEPARTMENTID"]'))
    # departmentSelection.select_by_value('2041') # Selects proper office just in case
    # REDACTEDAdriver.find_element(By.ID, 'loginbutton').click() # final login after confirming office
    departmentSelection = Select(REDACTEDwait.until(EC.element_to_be_clickable((By.XPATH, './/*[@id="DEPARTMENTID"]'))))
    departmentSelection.select_by_value('3') # Selects proper office just in case
    REDACTEDwait.until(EC.element_to_be_clickable((By.ID, 'loginbutton'))).click() # final login after confirming office
    # Lands on page with calendar BAR


def loadTodaysAppointments():                          # Navigates to starting REDACTEDA page, loads todays appointments page, stops
    # Proceedes to Today's Appointments
    print('\n\n' + '===============================================================')
    print('\n'+ "Navigating to Today's Calender ..." + '\n')
    time.sleep(0.3)
    REDACTEDAdriver.get('https://REDACTED/globalframeset.esp')
    time.sleep(0.3)
    REDACTEDAdriver.switch_to.frame('GlobalNav')
    time.sleep(0.25)
    calendarButton = REDACTEDAdriver.find_element(By.ID, "calendarmenucomponent")
    time.sleep(0.25)
    calendarButton.click()
    time.sleep(0.25)
    REDACTEDAdriver.switch_to.default_content()                                             #Exits GlobalNav calendar frame to top frame
    time.sleep(0.25)
    todaysApp = REDACTEDAdriver.find_element(By.ID, '466ca8d')      #ID of Today's Appointments button within Calendar menu
    time.sleep(0.25)
    todaysApp.click()    # Clicks on 'Todays Appointments' button (inside 'Calendar' menu)
    time.sleep(0.25)
    
    #Focus table frame to work Calendar and Patient Table
    focusTableFrame()
    
    # Attempting to enter vitalsDate
    print('\n\n' +"Attempting to enter date ..." + '\n\n')
    appDate = REDACTEDwait.until(EC.element_to_be_clickable((By.NAME, 'APPOINTMENTDATE')))
    time.sleep(0.5)
    appDate.clear()
    time.sleep(0.25)
    print("Cleared field, sending keys..")
    appDate.send_keys(vitalsDate)                                                       # Sends vitalsDate
    goButton = REDACTEDwait.until(EC.element_to_be_clickable((By.NAME, 'SUBMIT')))
    goButton.click()                                                                    # Should now be at looking at table of Today's Appointments
    print("Done.")


def refreshTable():                                    # Main patient parser
    global patientTable
    global patientTableRows
    global parsedPatientList
    global readyStaffPatientList
    global removePatientList
    global totalVitalsPatients
    print('\n\n' +
            '==============  Parsing Fresh Table Rows ...  =================' + '\n\n')
    patientTable = REDACTEDAdriver.find_element(By.ID, 'providerschedule')
    print('Working Table ID: ' + patientTable.get_attribute('id'))
    patientTableRows = patientTable.find_elements(By.XPATH, "//tr[contains(@class, '_M') and @title]")
    print('Total Patients found in table: ' + str(len(patientTableRows)))
    print('Printing original rows ...' +'\n')
    # for patient in patientTableRows:
    #     print(patient)
    #     print(patient.get_attribute('title') + '\n')
    print('==============================================================='+'\n\n\n'+
        'Parsed list loading ...')
    # Printing some patient information
    # Goes over list of today's patients and removes ones vith vitals already entered
    parsedPatientList = []
    removePatientList = []
    readyStaffPatientList = []
    for patient in patientTableRows:   
        title = patient.get_attribute('title')
        if 'Checked Out' in title:
            print('Removing Patient, Checked Out:')
            #print(title + '\n')
            # print(patient.get_attribute('class'))
            removePatientList.append(patient)
        elif 'With Provider' in title:
            print('Removing Patient, With Provider:')
            #print(title + '\n')
            # print(patient.get_attribute('class'))
            removePatientList.append(patient)
        elif 'Ready For Provider' in title:
            print('Removing Patient, Ready For Provider:')
            #print(title + '\n')
            # print(patient.get_attribute('class'))
            removePatientList.append(patient)
        elif 'Ready For Staff' in title:
            print('Removing Patient, apparently started atypically (yellow in table):')
            #print(title + '\n')
            # print(patient.get_attribute('class'))
            readyStaffPatientList.append(patient)
        else:
            parsedPatientList.append(patient)


    # Printing table and found patient information
    print('Removed Patient list length:' + str(len(removePatientList)) + '\n\n\n')
    print('===============  Main set of patients for today  =====================================' +  '\n\n\n')
    print('New Parsed Patient list length:' + str(len(parsedPatientList)))
    print('Ready For Staff Patient list length: ' + str(len(readyStaffPatientList)) + '\n')
    print('There are ' + str(len(parsedPatientList)+len(readyStaffPatientList)) + ' outstanding patients found' + '\n')
    for patient in parsedPatientList:
        print(patient.get_attribute('title'))
    for patient in readyStaffPatientList:
        print(patient.get_attribute('title'))
    print('==============================================================================' +  '\n\n\n')
    totalVitalsPatients = len(parsedPatientList) + len(readyStaffPatientList)


def navAndRefreshTable():                              # Combo of loadTodaysAppointments() and refreshTable()
    # Load Today's Appointments
    loadTodaysAppointments()  # Focuses on table iframe - via focusTableFrame() function - within to successfully enter date
    time.sleep(0.2)

    # Parses fresh copy of Patient Table 
    refreshTable()
    time.sleep(0.2)


def processPatient(patient):
    global title
    global patientLastName
    global patientFirstName
    global patientID

    title = patient.get_attribute('title')
    titleSplit = title.split()
    patientLastName = str(titleSplit[0].rstrip(','))
    patientFirstName = str(titleSplit[1])
    patientID = patientLastName + patientFirstName
    print('======================================================================='+'\n'
        "Current Patient :" + patientLastName + ', '  + patientFirstName + '\n\n')


def focusTableFrame():
    # Switches to iframe containing Today's Patients once function loadTodaysAppointments is run
    # #backup block
    # print("Running focusTableFrame() ...")
    # print('\n'+ "Switching to Main frame ...")
    # REDACTEDAdriver.switch_to.default_content()
    # time.sleep(0.3)
    # print("Switching to frame GlobalWrapper ...")
    # REDACTEDAdriver.switch_to.frame('GlobalWrapper')
    # time.sleep(0.3)
    # print("Switching to frame frameContent ...")
    # REDACTEDAdriver.switch_to.frame('frameContent')
    # time.sleep(0.3)
    # print("Switching to frame frScheduleNav ...")
    # REDACTEDAdriver.switch_to.frame('frScheduleNav')
    # time.sleep(0.3)
    # print('Done' + '\n\n')   

    print("Running focusTableFrame() ...")
    print('\n'+ "Switching to Main frame ...")
    REDACTEDAdriver.switch_to.default_content()
    #selenium.webdriver.support.expected_conditions.frame_to_be_available_and_switch_to_it
    print("Switching to frame GlobalWrapper ...")
    REDACTEDwait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, 'GlobalWrapper')))
    print("Switching to frame frameContent ...")
    REDACTEDwait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, 'frameContent')))
    print("Switching to frame frScheduleNav ...")
    REDACTEDwait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, 'frScheduleNav')))
    print('Done' + '\n\n')   


def focusMainPatientWindow():    
    # old code block
    # print("Running focusMainPatientWindow() ...")
    # print('\n' + 'Switching to Main frame ...')
    # REDACTEDAdriver.switch_to.default_content()
    # time.sleep(0.3)
    # print("Switching to frame GlobalWrapper ...")
    # REDACTEDAdriver.switch_to.frame('GlobalWrapper')
    # time.sleep(0.3)
    # print("Switching to frame frameContent ...")
    # REDACTEDAdriver.switch_to.frame('frameContent')
    # time.sleep(0.3)
    # print("Switching to frame frMain ...")
    # REDACTEDAdriver.switch_to.frame('frMain')
    # time.sleep(0.3)
    # print('Done' + '\n\n')

    print("Running focusMainPatientWindow() ...")
    print('\n' + 'Switching to Main frame ...')
    REDACTEDAdriver.switch_to.default_content()
    time.sleep(0.3)
    print("Switching to frame GlobalWrapper ...")
    REDACTEDwait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, 'GlobalWrapper')))
    print("Switching to frame frameContent ...")
    REDACTEDwait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, 'frameContent')))
    print("Switching to frame frMain ...")
    REDACTEDwait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, 'frMain')))
    print('Done' + '\n\n')


def focusStartIntakeButton():
    # # old code block
    # print(" Running focusStartIntakeButton() ...")
    # print('\n'+'Switching to Main frame ...')
    # REDACTEDAdriver.switch_to.default_content()
    # time.sleep(0.3)
    # print("Switching to frame simplemodal-data ...")
    # REDACTEDAdriver.switch_to.frame('simplemodal-data')
    # time.sleep(0.3)
    # print('Done' + '\n\n')

    print(" Running focusStartIntakeButton() ...")
    print('\n'+'Switching to Main frame ...')
    REDACTEDAdriver.switch_to.default_content()
    print("Switching to frame simplemodal-data ...")
    REDACTEDwait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, 'simplemodal-data')))
    print('Done' + '\n\n')


def doTheThing():                                      # Main Vitals Transfer Function. Start from REDACTEDA on calendar page and table refreshed
    global totalVitalsPatients
    global parsedPatientList
    global successfullyCompletedPatients
    global skipPatientsList
    global killafter
    global firstRun
    global breakmainloop
    global userInputAfterVitalsEntry


    # Skips navigating to and refreshing patient table on first run since available on initial load.
    if firstRun:
        pass
    else:
        navAndRefreshTable()

    ############################################################################################################################################################################################
    # Processing Initial Patient for First/Last name and skipPatientID to be used in future runs
    if  len(readyStaffPatientList) == 0:
        patient = parsedPatientList[0]
    else:
        patient = readyStaffPatientList[0]    
    processPatient(patient)
   
    # # Checks if patient in skipped list  ------- works for 2 skips
    # if patientID not in skipPatientsList:
    #     pass
    # else:
    #     index = 0
    #     print('First skipped patient found ... Skipping ' + patientID)

    #     # Assign and process next after skipped patient    
    #     patient = parsedPatientList[1]
    #     processPatient(patient)
  
    while patientID in skipPatientsList:
        print(str('\n' + 'Patient ID {} found in skipPatienList ... attempting to skip patient ...'.format(patientID) + '\n'))

        if 'Ready For Staff' in patient.get_attribute('title'):
            readyStaffPatientList.remove(patient)
            if len(readyStaffPatientList) == 0:
                patient = parsedPatientList[0]  # Reselects new first patient after removal from list, from parsed list if the removal makes the Ready For Staff table empty.
            processPatient(patient)
        parsedPatientList.remove(patient)
        if len(parsedPatientList) == 0:
            print('Skipped all available patients. Printing exit message and exiting...')
            exitMessage()
            sys.exit()
        patient = parsedPatientList[0]
        processPatient(patient)
    else:
        pass

    


    # Search for by Last name and click on Patient link, entering Patient's page
    link = patient.find_elements(By.PARTIAL_LINK_TEXT, patientLastName)
    REDACTEDAdriver.execute_script('arguments[0].click();', link[0])
    print('Entering patient page ...'+'\n')
    

    # Focus on main page
    focusMainPatientWindow()
    print('\n' + "Focused onto main patient window ..." + '\n')


    # Collect REDACTEDA ID and DOB
    REDACTEDADOB = REDACTEDwait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="patientworkflowheading"]/div/ul[1]/li[2]'))) #Xpath to date of birth
    REDACTEDADOB = REDACTEDADOB.text
    REDACTEDADOBMonth = REDACTEDADOB.split('-')[0]
    REDACTEDADOBDay = REDACTEDADOB.split('-')[1]
    REDACTEDADOBYear = REDACTEDADOB.split('-')[2]
    patientREDACTEDAID = REDACTEDwait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="patientworkflowheading"]/div/ul[1]/li[3]')))  #Xpath to REDACTEDAID
    patientREDACTEDAID = patientREDACTEDAID.text
    REDACTEDADOBKey = REDACTEDADOBMonth + REDACTEDADOBDay + REDACTEDADOBYear
    print('Collecting REDACTEDA DOB information ...')
    print('Patient REDACTEDA ID is: ' + patientREDACTEDAID)
    print('Patient REDACTEDA DOB: ' + REDACTEDADOB)
    
        
    # Start REDACTEDpc Search
    print('Starting patient REDACTEDpc search ...'+'\n')
    searchREDACTEDpc = REDACTEDpcdriver.find_element(By.ID, 'searchField')
    searchREDACTEDpc.send_keys(patientLastName)
    searchREDACTEDpc.send_keys(Keys.RETURN)
    print('\n' + 'Finding Patient ...' + '\n')
    time.sleep(1)


    # Checking to see if on valid patient page, allowing for exit or addition to skipPatientList[]
    patientNotFoundAlert = ('\n\n'+'============= ALERT ==========================='+'\n' +
                            '============================================='+'\n\n' +
                            'REDACTEDpc Browser NOT on valid patient page. Please navigate to the correct patient page.' + '\n\n' + 
                            '       Press any key to continue ...' + '\n' + '(n = exit script, d = No found patient or discharged)'
                            + '\n\n' +
                            '================================='+'\n\n')
    if REDACTEDpcdriver.title != "Clinical Profile":
        if proceedIfNotFound:
            raise Exception('Patient Not Found and Proceed-If-Not-Found toggle is TRUE. Skipping patient.')   #  raising exception to break try/except and therefore proceed to next patient
        else:
            patientNotFoundAlert = input(patientNotFoundAlert)
        
    if patientNotFoundAlert == 'n':
        print('\n' + 'Exiting Script ...')
        sys.exit()
    if patientNotFoundAlert == 'd':
        print("You indicated 'd' for Patient Discharged / No patient found. Skipping patient ...")
        firstRun = False
        raise Exception('Patient not found/discharged. Looping through patients again')
    print('Continuing ...')    


    #################################################################
    # Gathering REDACTEDpc DOB and Vitals Values
    #################################################################
    
    try:
        # Gathering DOB
        REDACTEDpcDOB = REDACTEDpcdriver.find_element(By.XPATH, '/html/body/table[4]/tbody/tr/td[1]/p[2]')  # DOB on REDACTEDpc page
        time.sleep(0.25)
        REDACTEDpcDOB = REDACTEDpcDOB.text
        REDACTEDpcDOB = REDACTEDpcDOB.split()[3]
        REDACTEDpcDOBMonth = REDACTEDpcDOB.split('/')[0]
        REDACTEDpcDOBDay = REDACTEDpcDOB.split('/')[1]
        REDACTEDpcDOBYear = REDACTEDpcDOB.split('/')[2]
        # Adding leading zeros to REDACTEDpc DOB months and days
        if int(REDACTEDpcDOBDay) < 10:
            REDACTEDpcDOBDay = '0'+ REDACTEDpcDOBDay
        if int(REDACTEDpcDOBMonth) < 10:
            REDACTEDpcDOBMonth = '0' + REDACTEDpcDOBMonth
        REDACTEDpcDOBKey = REDACTEDpcDOBMonth + REDACTEDpcDOBDay + REDACTEDpcDOBYear
        REDACTEDpcDOB = REDACTEDpcDOBMonth + '/' +  REDACTEDpcDOBDay + '/' +  REDACTEDpcDOBYear

        # Gathering Weight
        REDACTEDpcVitalWeight = REDACTEDpcdriver.find_element(By.XPATH, '//*[@id="vitals"]/tbody/tr[2]/td[4]/div[2]/div[1]')   # Weight on REDACTEDpc page
        time.sleep(0.25)
        REDACTEDpcVitalWeight = REDACTEDpcVitalWeight.text
        if REDACTEDpcVitalWeight == 'Weight:': # problem if equal to just that string. means empty weight value on the page
            REDACTEDpcVitalWeight = 'Error' 
        else:
            REDACTEDpcVitalWeight = REDACTEDpcVitalWeight.split()[1]
        # if type(REDACTEDpcVitalWeight) == int or type(REDACTEDpcVitalWeight) == float:

            # raise Exception('Problem with the weight number found ...')

        # Gathering Blood Pressure
        REDACTEDpcVitalBPElement = REDACTEDpcdriver.find_element(By.XPATH, '//*[@id="vitals"]/tbody/tr[2]/td[1]/div[2]/div') # BP on REDACTEDpc page
        time.sleep(0.25)
        REDACTEDpcVitalBPElement =REDACTEDpcVitalBPElement.text
        REDACTEDpcVitalBPElement =REDACTEDpcVitalBPElement.split()[1]
        REDACTEDpcVitalBPUpper = REDACTEDpcVitalBPElement.split('/')[0]
        REDACTEDpcVitalBPLower = REDACTEDpcVitalBPElement.split('/')[1]

        # Gathering Pulse
        REDACTEDpcVitalPulse = REDACTEDpcdriver.find_element(By.XPATH, '//*[@id="vitals"]/tbody/tr[2]/td[3]/div[2]/div[1]')   # Pulse on REDACTEDpc page
        time.sleep(0.25)
        REDACTEDpcVitalPulse = REDACTEDpcVitalPulse.text
        REDACTEDpcVitalPulse = REDACTEDpcVitalPulse.split()[1]

        # Gathering Resp Rate
        REDACTEDpcVitalRR = REDACTEDpcdriver.find_element(By.XPATH, '//*[@id="vitals"]/tbody/tr[3]/td[1]/div[2]/div[1]')   # RR on REDACTEDpc page
        time.sleep(0.25)
        REDACTEDpcVitalRR = REDACTEDpcVitalRR.text
        REDACTEDpcVitalRR = REDACTEDpcVitalRR.split()[1]

        # Gathering O2
        REDACTEDpcVitalO2 = REDACTEDpcdriver.find_element(By.XPATH, '//*[@id="vitals"]/tbody/tr[3]/td[3]/div[2]/div[1]')   # O2 on REDACTEDpc page
        time.sleep(0.25)
        REDACTEDpcVitalO2 = REDACTEDpcVitalO2.text
        REDACTEDpcVitalO2 = REDACTEDpcVitalO2.split()[1]


        # Gathering Temp
        REDACTEDpcVitalTemp = REDACTEDpcdriver.find_element(By.XPATH, '//*[@id="vitals"]/tbody/tr[2]/td[2]/div[2]/div[1]')   # Temp on REDACTEDpc page
        time.sleep(0.25)
        REDACTEDpcVitalTemp = REDACTEDpcVitalTemp.text
        REDACTEDpcVitalTemp = REDACTEDpcVitalTemp.split()[0].split(':')[1]


        # Gathering Glucose - not working yet
        REDACTEDpcVitalGlucose = REDACTEDpcdriver.find_element(By.XPATH, '//*[@id="vitals"]/tbody/tr[3]/td[2]/div[2]/div[1]')   # Glucose on REDACTEDpc page
        time.sleep(0.25)
        REDACTEDpcVitalGlucose = REDACTEDpcVitalGlucose.text
        REDACTEDpcVitalGlucose = REDACTEDpcVitalGlucose.split()[1]
        if REDACTEDpcVitalGlucose == 'BS:':
            REDACTEDpcVitalGlucose = 'NoEntry'
    except:
        print('Exception reading vitals from REDACTEDpc ... attempting to continue to next patient ...')
    #################################################################


    # Starting DOB Check
    print('=================================================')
    print('Patient REDACTEDpc Date of Birth: '+ REDACTEDpcDOB +'\n')
    print('REDACTEDpcDOBKey: ' + REDACTEDpcDOBKey)
    print('REDACTEDADOBKey: ' + REDACTEDADOBKey + '\n')
    if REDACTEDpcDOBKey == REDACTEDADOBKey:
        print('DOB Keys Match! Proper patient record confirmed' + '\n')
    else:
        print('DOB Keys do not match. Critical error, exiting script ...' + '\n')
        sys.exit()


    # Print all Patient Vitals
    print('=====================================================================' + '\n' +
        'Printing Vitals for Patient: ' + patientLastName + ', ' + patientFirstName + '\n' +
        '=====================================================================' + '\n')
    print('REDACTEDpc DOB: ' + REDACTEDpcDOB +'\n')
    print('Weight: ' + REDACTEDpcVitalWeight +'\n')
    print('Blood Pressure: ' + REDACTEDpcVitalBPUpper + '/' + REDACTEDpcVitalBPLower + '\n')
    print('RR: ' + REDACTEDpcVitalRR +'\n')
    print('Pulse: ' + REDACTEDpcVitalPulse +'\n')
    print('O2: ' + REDACTEDpcVitalO2 +'\n')
    print('Temp: ' + REDACTEDpcVitalTemp +'\n')
    print('Glucose: ' + REDACTEDpcVitalGlucose + '\n')



    #################################################################
    #  Start Intake Process
    #################################################################

    # # Confirming start checkin
    # proceedCheckin = input('\n' + 'Continue with Checkin? (n= system exit) : '+ '\n')
    # if proceedCheckin == 'n':
    #     print('Skipping Checkin process. Exiting Script ...')
    #     sys.exit()


    # Click first 'Start Checkin' button on bottom bar for patients in parsed list
    if 'Ready For Staff' in title:
        pass
    else:
        print("Clicking Start Checkin on main window ...")
        #REDACTEDAdriver.find_element(By.ID, 'SUBMITVALUE').click() #Clicks the actual Start Checkin button
        startCheckinButton = REDACTEDwait.until(EC.element_to_be_clickable((By.ID, 'SUBMITVALUE')))
        startCheckinButton.click() #Clicks the actual Start Checkin button
        #time.sleep(3)
        print('Done.')
        print('\n\n' + '============================================' + '\n\n')
        print('Starting Checking for '+ patientLastName + ', ' + patientFirstName + ' ...' + '\n')

                                                                # print('\n' + 'Cancelling check-in ...' + '\n')
                                                                # cancelCheckin = REDACTEDAdriver.find_elements(By.PARTIAL_LINK_TEXT, 'Cancel Check-in')
                                                                # time.sleep(1)
                                                                # cancelCheckin[0].click()  # Clicks cancel checkin


    # Click Intake under DOB (REDACTEDA site)
    print("Clicking 'Intake' under DOB ..."+ '\n')
    #intakeUnderDOB = REDACTEDAdriver.find_element(By.XPATH, '//*[@id="stagespan_INTAKE"]')
    #time.sleep(0.25)
    intakeUnderDOB = REDACTEDwait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="stagespan_INTAKE"]')))
    intakeUnderDOB.click()
    print('Done.' + '\n\n')
    time.sleep(1)


    # Check for Patient Portal Registration.
    try:
        portalDeclineButton = WebDriverWait(REDACTEDAdriver,3).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="declineportalinvitehardstoplink"]')))
        if portalDeclineButton.is_displayed():
            print("Declining Patient Portal Registration ...")
            portalDeclineButton.click()
            reason = Select(REDACTEDwait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="declinehardstopreason"]'))))
            reason.select_by_value('DECLINEDPORTAL')  # Selects Decline reason 'Does not want a portal account
            submitButton = REDACTEDwait.until(EC.element_to_be_clickable((By.XPATH, '//button[@class ="declinehardstopbuttons submitbutton" and @value="Submit"]')))
            submitButton.click()
            time.sleep(0.25)
    except:
        print('In Patient Portal Exception loop. Didnt find Patient Portal Registration ...')
        pass

    
    ###########################3

    # Check for and Click 'Start Intake' POPUP BOX
    if 'Ready For Staff' in title:
        pass
    else:
        try:
            focusStartIntakeButton()
            startIntakePopUp = REDACTEDwait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="YESBUTTON"]')))
            if startIntakePopUp.is_displayed():
                print("Found and clicking on 'Start Intake' popup box ...")
                startIntakePopUp.click()
                time.sleep(1)
                focusMainPatientWindow()
            else:
                print("Didnt find 'Start Intake popup box ...")
                pass
        except:
            print('In Start Intake POPUP BOX Exception loop. Didnt find the popup ...')
            pass
    time.sleep(2)



    # Click GREEN 'Go To Intake' button on right side after checkin
    print('\n' + 'Clicking GREEN Go To Intake button ...' + '\n')
    # GoToIntakeButton = REDACTEDAdriver.find_element(By.XPATH, '//button[@data-stage = "intake" and contains(text(), "Go to Intake")]')    # old find method
    time.sleep(2.5)
    GoToIntakeButton = REDACTEDwait.until(EC.element_to_be_clickable((By.XPATH, '//button[@data-stage = "intake" and contains(text(), "Go to Intake")]')))
    print('Green Intake button found and clickable.')
    GoToIntakeButton.click()
    print('Done.' + '\n')
    time.sleep(3) # let the page load

    # Clicking 'Vitals' on Left Bar
    try:
        print('\n' + "Clicking 'Vitals' on the left bar ..." + '\n')
        #vitalsButton = REDACTEDAdriver.find_element(By.XPATH, '//*[@id="page-container"]/div[6]/nav/ul/li[3]/div')
        #time.sleep(2.5)
        #time.sleep(2.5)  #waiting for page to load up
        
        vitalsButton = REDACTEDwait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="page-container"]/div[5]/nav/ul/li[3]/div')))  # original, i think for when green intake actually works
        #vitalsButton = REDACTEDwait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="page-container"]/div[5]/div[5]/div[1]/ul/li[6]')))  # value found if green intake is skipped?


        print('Found, attempting click..')
        time.sleep(1)
        vitalsButton.click()
        print('Done.' + '\n')
        time.sleep(1.75) # let the page load
    except:
        print('Eror clicking Vitals button. In excption, , looping..')
        raise Exception('Error clicking Vitals button ...')

    # Gathering REDACTEDA Vitals webElements 
    focusMainPatientWindow()
    print('Gathering REDACTEDA Vitals webElements ...' + '\n')
    REDACTEDAVitalWeight = REDACTEDwait.until(EC.element_to_be_clickable((By.XPATH, '//input[@data-clinical-element-id="VITALS:WEIGHT"]')))
    REDACTEDAVitalBPUpper = REDACTEDwait.until(EC.element_to_be_clickable((By.XPATH, '//input[@data-clinical-element-id="VITALS:BLOODPRESSURE:SYSTOLIC"]')))
    REDACTEDAVitalBPLower = REDACTEDwait.until(EC.element_to_be_clickable((By.XPATH, '//input[@data-clinical-element-id="VITALS:BLOODPRESSURE:DIASTOLIC"]')))
    REDACTEDAVitalPulse = REDACTEDwait.until(EC.element_to_be_clickable((By.XPATH, '//input[@data-clinical-element-id="VITALS:PULSE:RATE"]'))) 
    REDACTEDAVitalRR = REDACTEDwait.until(EC.element_to_be_clickable((By.XPATH, '//input[@data-clinical-element-id="VITALS:RESPIRATIONRATE"]')))  
    REDACTEDAVitalO2 = REDACTEDwait.until(EC.element_to_be_clickable((By.XPATH, '//input[@data-clinical-element-id="VITALS:O2SATURATION"]')))
    REDACTEDAVitalTemp = REDACTEDwait.until(EC.element_to_be_clickable((By.XPATH, '//input[@data-clinical-element-id="VITALS:TEMPERATURE"]')))  
    print('Done.' + '\n')


    # First Clearing and Plugging in vitals information into REDACTEDA
    print('Plugging in vitals information into REDACTEDA ...')
    if REDACTEDpcVitalWeight != 'Error':
        REDACTEDAVitalWeight.clear()
        time.sleep(0.5)
        REDACTEDAVitalWeight.send_keys(REDACTEDpcVitalWeight)
        #REDACTEDAVitalWeight.send_keys(Keys.TAB)
    time.sleep(0.5)
    REDACTEDAVitalBPUpper.clear()
    time.sleep(0.3)
    REDACTEDAVitalBPUpper.send_keys(REDACTEDpcVitalBPUpper)
    #REDACTEDAVitalBPUpper.send_keys(Keys.TAB)
    time.sleep(0.5)
    REDACTEDAVitalBPLower.clear()
    time.sleep(0.3)
    REDACTEDAVitalBPLower.send_keys(REDACTEDpcVitalBPLower)
    #REDACTEDAVitalBPLower.send_keys(Keys.TAB)
    time.sleep(0.5)
    REDACTEDAVitalPulse.clear()
    time.sleep(0.3)
    REDACTEDAVitalPulse.send_keys(REDACTEDpcVitalPulse)
    #REDACTEDAVitalPulse.send_keys(Keys.TAB)
    time.sleep(0.5)
    REDACTEDAVitalRR.clear()
    time.sleep(0.3)
    REDACTEDAVitalRR.send_keys(REDACTEDpcVitalRR)
    #REDACTEDAVitalRR.send_keys(Keys.TAB)
    time.sleep(0.5)
    REDACTEDAVitalO2.clear()
    time.sleep(0.3)
    REDACTEDAVitalO2.send_keys(REDACTEDpcVitalO2)
    #REDACTEDAVitalO2.send_keys(Keys.TAB)
    time.sleep(0.5)
    REDACTEDAVitalTemp.clear()
    time.sleep(0.3)
    REDACTEDAVitalTemp.send_keys(REDACTEDpcVitalTemp)
    time.sleep(0.3)

    
    # Pausing to allow user to look over page before proceeding. Vitals probably locked in from here
    # if input('\n\n' + "Pausing to look over entered vitals. Press 'n' to exit, or any other key to continue ..." + '\n') == 'n':
    #     print("Exiting script ...")
    #     sys.exit()
    if userInputAfterVitalsEntry == True:
        resp = input('\n\n' + "Pausing to look over entered vitals. Press 'n' to exit, or any other key to continue ..." + '\n')
        if resp == 'n':
            print("Exiting script ...")
            sys.exit()
    else:
        print('\n\n' + 'Pausing for 3 seconds to glace at vitals...')
        time.sleep(1.5)
        print('Proceeding.')


    # # this seems to fail if there is a popup on next screen
    # # Clicking 'Next' button to ensure vitals plugged in
    # print('\n' + "Clicking 'Next' in upper corner - vitals should be saved..." + '\n')
    # nextButton = REDACTEDwait.until(EC.element_to_be_clickable((By.XPATH, '//button[@class = "navigation-button button-large next-button call-to-action" and contains(text(), "Next")]')))
    # if testMode is True:
    #     pass
    #     print('\n' + "Test Mode is ON. Not Clicking 'Next', passing ...")
    # else:
    #     nextButton.click()
    # time.sleep(0.1)


    # Clicking Patient Preferences button on left menu to ensure vitals plugged in
    print('\n' + "Clicking 'Patient Preferences' in upper corner - vitals should be saved..." + '\n')
        # Patient Preferences button on left menu.
    if testMode is True:
        print('\n' + "Test Mode is ON. Passing click to lock in patient info ...")
        pass
    else:
        patientPref = REDACTEDwait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="page-container"]/div[5]/nav/ul/li[2]/div')))
        time.sleep(0.7)
        patientPref.click()
        time.sleep(0.7)

    
    # Final Click - Done With Intake / Intake Complete -----------------------------------------------------------------
    # #doneWithIntakeButton = REDACTEDAdriver.find_element(By.XPATH, '//*[@id="intake-complete"]')
    # #time.sleep(0)
    # this test mode code below does not work. fails.
    # while testMode == True: # If True, doesn't save Vitals info
    #     print('\n' + "**** Test Mode is ON. ****' + '\n' + 'NOT actually clicking 'Intake Complete'. Exiting current patient loop.")
    #     continue
    try:
        print("Clicking 'Done with Intake' (Intake Complete) ..." + '\n')
        doneWithIntakeButton = REDACTEDwait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="intake-complete"]')))
        time.sleep(0.7)
        doneWithIntakeButton.click()
        time.sleep(0.7)
        print('Done.')
    except: # Runs when can't click Done intake button
        print ('Exception clicking Done With Intake button ...')
        skipPatientsList.append(patientID)
        pass
    # else:
    #     try: # Trying First Click of Done Button
    #         doneWithIntakeButton = REDACTEDwait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="intake-complete"]')))
    #         doneWithIntakeButton.click()
    #         # Check for possible 'Leave Page' Alert
    #         try: #Attempts to find alert and Cancel it. Pauses and passes if not found
    #             WebDriverWait(REDACTEDAdriver,3).until(EC.alert_is_present())
    #             alert = REDACTEDAdriver.switch_to.alert()
    #             alert.cancel()
    #         except: # Pauses
    #             input('\n'+ 'Possible Problem with Alert. Clear it and press any key to continue ...')
    #             pass
    #         time.sleep(0.1)
    #         print('Done.' + '\n')
    #         # Future Code to check if dumped onto exited page? to be entered below.
    #         print("First Click Success, Vitals successfully entered for " + patientLastName + ', ' + patientFirstName + '\n')
    #     except: # Exception if first click failed
    #         try:  # trying to click again in case no more alerts
    #             doneWithIntakeButton = REDACTEDwait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="intake-complete"]')))
    #             doneWithIntakeButton.click()
    #             print("Second Click Success (first failed), Vitals successfully entered for " + patientLastName + ', ' + patientFirstName + '\n')
    #         except:
    #             print('There must REALLY be a problem. Tried clicking done with intake Twice. Exiting')
    #             raise  Exception('\n'+ 'Looping to next patient ...')
    #             # print ('Exception attenmpting to click Intake Complete ... Exiting script ...')
    #             # sys.exit()
    # -------   End of Click Done code    -------------------------------------------------------------------------
    # End of loop  -------------------------------------------------------
    # Checks for iteration limit set in beginning of script
    # Proceedes to start loop with new patient 


    # Successful Patient Wrap-up. Check for killswitch
    totalVitalsPatients = totalVitalsPatients - 1
    print('Adding patient to successfullCompletedPatients table ...')
    successfullyCompletedPatients.append(patientID)
    print('Done.' + '\n')
    totalCompleted = 'Completed a total of {} patients so far ...'.format(str(len(successfullyCompletedPatients)))
    print(totalCompleted)
    print('Done.' + '\n')

    # Checks if loop limit killafter has been reached. Exists scipt if yes
    print('Getting to killafter loop')

    killafter = killafter - 1
    #print('killafter: ' + str(killafter))
    if killafter == 0:
        #REDACTEDAdriver.quit()
        print('\n' + '===========  ALERT  ==================')
        print('\n' + 'KILLAFTER limit triggered. Exiting script ...' + '\n')
        print('Breaking out of main loop...')
        breakmainloop = True
    
    else:
        pass
    print('Looped successfully past killafter. Proceeding to next patient ...')
    time.sleep(2)  # longer sleep to let page load as next loop starts...
    

def exitMessage():
    global successfullyCompletedPatients
    global totalVitalsPatients
    global skipPatientsList

    exitMessage = str('\n\n' + '======================  EXITING ... =======================' + '\n' +
        'Finished Processing' + '\n' +
        'There are {} totalVitalPatients left.'.format(str(totalVitalsPatients)) + '\n'+
        'There were {} skipped patients'.format(len(skipPatientsList)) + '\n' +
        'Processed {} patients during this script run.'.format(str(len(successfullyCompletedPatients))) + '\n' +
        'Exiting Script ... Goodbye!' + '\n' +
        '===========================================================' + '\n\n')
    print(exitMessage)
    print('Printing skipped patients: ')
    for skipped in skipPatientsList:
        print(skipped)
        print('\n\n')


####################################################################


####################################################################
############ MAIN PROGRAM ##########################################
####################################################################

# Take a timestamp now


# Fire only REDACTEDA or REDACTEDpc if Script toggles true
if (fireREDACTEDAOnly or fireREDACTEDpcOnly):
    if fireREDACTEDAOnly:
        fireREDACTEDA()
        time.sleep(0.1)
        navAndRefreshTable()
    if fireREDACTEDpcOnly:
        fireREDACTEDpc()
    print('Fired only browser drivers due to script toggles ...' + '\n')
    sys.exit()
else:
    pass


#Prompt for vitals date
promptVitalsDate()


# Fire Up REDACTEDA Browser
print('\n\n'+'Loading REDACTEDA Browser ...' + '\n')
fireREDACTEDA()
time.sleep(2)


# Navigate to Today's Appointments and Refresh Patient Calender
navAndRefreshTable()
originalPatientCount = totalVitalsPatients


# Fire up REDACTEDpc Browser if patients found
if totalVitalsPatients > 0:
    print('\n\n'+ 'Loading REDACTEDpc Browser ...' + '\n')
    fireREDACTEDpc()
    time.sleep(2)
else:
    print('Total vitals candidates found is 0. Exiting script ...')
    sys.exit()


# Check if proceeding to enter vitals. Last pause point before main loop
quitques = input('\n\n' + '====================================================================' + '\n' +
          'Proceed to entering main vitals loop? (y / n=exits script): '+ '\n\n' +
          '====================================================================' + '\n\n')
if quitques == 'n':
    #REDACTEDAdriver.quit()
    #REDACTEDpcdriver.quit()
    print('\n'+'Exiting script ...')
    breakmainloop = True  # doesn't come into play, but doesn't hurt
    sys.exit()


# MAIN Vitals Loop and Program Exit (within 'else' clause)
print('====================== Beginning Vitals Main Loop ... =======================')


while len(parsedPatientList) > 0 and breakmainloop == False:  # and (totalVitalsPatients != len(skipPatientsList)):   # Keeps looping until out of found patients, loop deliberately broken, or all available patients are skipped patients
    try: 
        # Crunch main patient processes...
        doTheThing()

        # Flags subsequent runs as not being first
        firstRun = False

        # End of the function loop. If last patient, removes 1 count from patient list to get to 0 and break out of 'while' loop
        print('Total Vitals Patients Left: ' + str(totalVitalsPatients))
        if len(parsedPatientList) == 1:
            print('\n'+"This is the last patient. Removing patientID from list, onto exit message...")
            parsedPatientList.remove(patientID)
    except: # Exception skips the patient and keeps going
        firstRun = False
        skipPatientsList.append(patientID)
        print('\n' + 'Something failed completing patient or patient indicated dischared. In main while-try-except ... attempting to continue to next patient ... ' +'\n')
else: # Real program ending and stats
    # Program Ending. Wrapping up 
    # REDACTEDAdriver.quit()
    # REDACTEDpcdriver.quit()
    exitMessage()
    resp = input('Proceed to process skipped patients? (y / n = exit script) ...' + '\n\n')
    if resp == 'n':
        print('Exiting ...')
        sys.exit()
    else:
        while len(skipPatienList) > 0:
            try:
                doTheThing()
                skipPatientList.remove(patientID)
            except:
                continue
        print('skipPatientList is now empty. Script is exiting ...' + '\n\n')
        sys.exit()
