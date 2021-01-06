import xnat
import os 
import glob
import pyxnat
import pandas as pd
# coding: utf-8
import zipfile
import time
path = "D:/XNat"
# zipfile example
def zip_dir(path):
    zf = zipfile.ZipFile('{}.zip'.format(path), 'w', zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk(path):
        for file_name in files:
            zf.write(os.path.join(root, file_name))

def read_CTMR(path):
    df = pd.read_csv(path + '/CTMR.csv')
    img_path = path + '/CGRD/' + df['fullpath']
    return img_path


def read_CT_and_MR(path,df,df2):
    x,y = df2.shape
    CT = 0
    MR = 0
    for i in range(x):
        try:
            subject_ct = df2[df2['ID'].str.match(df2['ID'][i])]
            name_s = subject_ct.iloc[0]['ID'] # Name a new subjectn

            ID = df[df['PatientID'].str.match(name_s)]
            ID_name = ID.iloc[0]['PatientID']
            if ID_name:
                Modality = ID.iloc[0]['Modality']
                if Modality == 'CT':
                    CT = CT + 1
                else:
                    MR = MR + 1

            '''prearchive_session = session.services.import_(patientID + '.zip', project=name_p, subject=df['fullpath'][i], destination='/prearchive')
            prearchive_session = session.prearchive.sessions()[0]
            experiment = prearchive_session.archive(subject=df['fullpath'][i], experiment=df['fullpath'][i])'''

        except:
            print('error')  
            pass
    return CT,MR
if __name__ == '__main__':
    img_path = read_CTMR(path)
    df = pd.read_csv(path + '/CTMR.csv') 
    uniclinical = pd.read_excel(path + '/uniclinical.xlsx',encoding = 'utf-8') 
    session = xnat.connect('http://120.126.47.114', user='admin', password='admin123')
    session2 = pyxnat.Interface('http://120.126.47.114', # Connect to Server (website https / IP)
                           user = 'admin', # Username Registered
                           password = 'admin123') # Password
    #CT, MR =read_CT_and_MR(path,df,uniclinical)
                          
    name_p = '109_TM'
    for i, patientID in enumerate(img_path):
        #time.sleep(180) #3mins
        try:
            zip_dir(patientID)
            df = pd.read_csv(path + '/CTMR.csv')
            print(i,patientID)
            subject_ct = df[df['fullpath'].str.match(df['fullpath'][i])]
            name_s = subject_ct.iloc[0]['PatientID'] # Name a new subjectn
            ID = uniclinical[uniclinical['ID'].str.match(name_s)]
            prearchive_session = session.services.import_(patientID + '.zip', project=name_p, subject=df['fullpath'][i], destination='/prearchive')
            prearchive_session = session.prearchive.sessions()[0]
            experiment = prearchive_session.archive(subject=df['fullpath'][i], experiment=df['fullpath'][i])
        except:
            print('error')  
            pass
        subject_ct = df[df['fullpath'].str.match(df['fullpath'][i])]
        name_sb = df['fullpath'][i]
        name_sb = name_sb.replace('.', '_')
        name_s = subject_ct.iloc[0]['PatientID'] # Name a new subjectn
        ID = uniclinical[uniclinical['ID'].str.match(name_s)]
        subject = session2.select.project(name_p).subject(name_sb)
        subject_c = uniclinical[uniclinical['ID'].str.match(name_s)]
        get_exp = session2.select.project(name_p).subject(name_sb).experiments().get() 
        
        if len(get_exp) != 0:
            try:
                subject.attrs.mset({
                        'xnat:subjectData/demographics[@xsi:type=xnat:demographicData]/gender': subject_c.iloc[0]['Gender'],
                        'xnat:subjectData/demographics[@xsi:type=xnat:demographicData]/age': str(subject_c.iloc[0]['Age']),
                        'xnat:subjectData/demographics[@xsi:type=xnat:demographicData]/dob': str(subject_ct.iloc[0]['PatientBirthDate'])})
                print(subject.attrs.mget({
                        'xnat:subjectData/demographics[@xsi:type=xnat:demographicData]/gender',
                        'xnat:subjectData/demographics[@xsi:type=xnat:demographicData]/age',
                        'xnat:subjectData/demographics[@xsi:type=xnat:demographicData]/dob'}))
            except:
                print('123')
        
            report = subject_ct.iloc[0]['Content']
            #subject = session2.select('/projects/' + name_p + '/subjects/%s'% (name_s))
            #print(subject)
            print(len(subject_ct.iloc[0]['Content']))
            if len(subject_ct.iloc[0]['Content']) < 1400:
                
                experiment = subject.experiment('%s'%(get_exp[0]))
                experiment.attrs.set('xnat:experimentData/note',report)
                experiment.attrs.get('xnat:experimentdata/Note')
                print(experiment.attrs.get('xnat:experimentdata/Note'))
            # set experiment attribute 'note'''
    
    session.disconnect()
    session2.disconnect()

    
