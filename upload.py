import xnat
session = xnat.connect('http://120.126.47.114', user='admin', password='admin')
prearchive_session = session.services.import_('D:/XNat/upload/1.2.528.1.1001.200.10.4573.2021.3754721344.20190923031739775.zip', project='109_translational_medical', subject='subject_6', destination='/prearchive')
#print(prearchive_session)
#session.prearchive.sessions()
prearchive_session = session.prearchive.sessions()[0]
experiment = prearchive_session.archive(subject='subject_6', experiment='subject_6')
print(experiment)