'''
###### Output Empty List when Connection Failed (or Workspace without Project/Subject) ######'''      


###############
# Environment #
###############
#!pip install pyxnat
#!pip install xnat # XNATpy
import pyxnat
import xnat
import os
import glob 
from datetime import date # Display Today's Date
print('Current Date: %s\npyXNAT version: %s\nXNATpy version: %s'
      %(date.today(), pyxnat.__version__, xnat.__version__))

#####################
# Server Connection #
#####################
# Session Implementation
session = pyxnat.Interface('http://120.126.47.114', # Connect to Server (website https / IP)
                           user = 'admin', # Username Registered
                           password = 'admin123') # Password

projectID = input('plz input Project ID: ') #input project id
subjects = session.select.project(projectID).subjects().get() #how many subjects
print(subjects)
allSessions = []

for i, subject in enumerate(subjects):
      label = session.select.project(projectID).subject(subject).label() # Subject name = e.g. Test2 -> Test
      print (label),('%i/%i' % (i+1, len(subjects)))
      sessions = session.select.project(projectID).subjects(subject).experiments().get() #how many data in this Subject(include accession)
      allSessions.append(sessions) # append Subject Accession

dirName = os.path.join(r'D:\XNat\XNatDownload', projectID) #download path
if not os.path.exists(dirName):
      os.mkdir(dirName)
      print("Directory " , dirName ,  " Created ")
else:    
      print("Directory " , dirName ,  " already exists")

Results_Dir = dirName
number_subjects = 0
subjectCounter = 0 
for s, subjectID in enumerate(subjects):  # s: number n ,subjectID : number n subjectID
      subjectLabel = session.select.project(projectID).subject(subjectID).label() #subject Name
      for experimentID in allSessions[s]:
            scansNum = session.select.project(projectID).subject(subjectID).experiments(experimentID).scans() #scan all data(subject)

            ################# from subject test2 ##################
            ##Date 	      Experiment 	Project 	Label     ###
            ##2002-02-18	CT Session	 test     Test_CT_1   ###
            #######################################################
            scanIDs = scansNum.get() #get data num
            coll = session.select.project(projectID).subject(subjectID).experiments(experimentID)
            
            for ese in coll:
                  explab = ese.attrs.get('label') #get experiment label(Test_CT_1)
            
            # Check if data has already been pulled
            dataCheck = glob.glob(Results_Dir + "/" + subjectLabel + "/*" + explab ) 
            dataCheck = ''.join(dataCheck) # covert list to string
            if not os.path.exists(dataCheck):
                print("Downloading:", explab)        
                number_subjects+=1
            
                if len(scanIDs) == 0:
                    print("There are no scans to download for", explab)
                else:
                    filenames = session.select.project(projectID).subject(subjectID).experiment(experimentID).scans()
                    filenames.download(Results_Dir, type='ALL', extract=False, removeZip=True)   
                    
            else:
                print(explab + " already pulled")
print ("The total number of scanning sessions downloaded is = " + str(number_subjects))
session.disconnect()
