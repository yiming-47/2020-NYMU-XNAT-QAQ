import xnat
import os 
import glob
import pyxnat
# coding: utf-8
import zipfile

path = './CGRD'
# zipfile example
def zip_dir(path):
    zf = zipfile.ZipFile('{}.zip'.format(path), 'w', zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk(path):
        for file_name in files:
            zf.write(os.path.join(root, file_name))


if __name__ == '__main__':
    #for filename in os.listdir(path):
    #    zip_dir(path + '/' + filename)
    #zip_dir(path)
    # session = pyxnat.Interface('http://120.126.47.114', user='admin', password='admin')
    # project = session.select.project('109_translation_medical')
    # project.create(
    #project.create()
    # session.disconnect()
    os.chdir('D:/XNat/CGRD')
    for i in glob.glob('*.zip'):
        try:
            #os.remove('D:/XNat/CGRD/' + i)
            patient_name = i[0:len(i) - 4]
            print(patient_name)
            session = xnat.connect('http://120.126.47.114', user='admin', password='admin')
            print('./' + i)
            prearchive_session = session.services.import_('./' + i, project='109_translation_medical', subject=patient_name, destination='/prearchive')
            #print(prearchive_session)
            #session.prearchive.sessions()
            prearchive_session = session.prearchive.sessions()[0]
            print(prearchive_session)
            experiment = prearchive_session.archive(subject=patient_name, experiment=patient_name)
            print(experiment)
        except:
            print('error')
            pass
        session.disconnect()
        continue
