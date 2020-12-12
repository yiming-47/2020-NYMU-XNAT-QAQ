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


if __name__ == '__main__':
    img_path = read_CTMR(path)
    session = xnat.connect('http://120.126.47.114', user='admin', password='admin123')
    for i, patientID in enumerate(img_path):
        time.sleep(180) #3mins
        try:
            zip_dir(patientID)
            df = pd.read_csv(path + '/CTMR.csv')
            print(i,patientID)
            prearchive_session = session.services.import_(patientID + '.zip', project='109_TM', subject=df['fullpath'][i], destination='/prearchive')
            #print(prearchive_session)
            #session.prearchive.sessions()
            prearchive_session = session.prearchive.sessions()[0]
            experiment = prearchive_session.archive(subject=df['fullpath'][i], experiment=df['fullpath'][i])
             
        except:
            print('error')  
            pass
        continue
    session.disconnect()

    ##------------------------------------------------------------------------------------------------------
    # session.disconnect()
    # for filename in os.listdir(path):
    #    zip_dir(path + '/' + filename)
    #zip_dir(path)
    # session = pyxnat.Interface('http://120.126.47.114', user='admin', password='admin')
    # project = session.select.project('109_translation_medical')
    # project.create(
    #project.create()
    # session.disconnect()
    '''os.chdir('D:/XNat/CGRD')
    # session = xnat.connect('http://120.126.47.114', user='admin', password='admin123')
    for i in glob.glob('*.zip'):
        # try:
        os.remove('D:/XNat/CGRD/' + i)
    #         patient_name = i[0:len(i) - 4]
    #         print(patient_name)
    #         print('./' + i)
    #         prearchive_session = session.services.import_('./' + i, project='109_translation_medical', subject=patient_name, destination='/prearchive')
    #         #print(prearchive_session)
    #         #session.prearchive.sessions()
    #         prearchive_session = session.prearchive.sessions()[0]
    #         print(prearchive_session)
    #         experiment = prearchive_session.archive(subject=patient_name, experiment=patient_name)
    #         print(experiment)
    #     except:
    #         print('error')
    #         pass
    #     continue
    
    # session.disconnect()'''
