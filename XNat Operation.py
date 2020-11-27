######################
# Database Operation #
######################
# 1. Creating Project
name_p = 'project_test_10' # Name a new project
test_project = session.select.project(name_p)
print('Project Exists: %s' %test_project.exists()) # Return False if project unfounded
test_project.create() # Return True if project detected
print('After Created: %s' %test_project.exists())
test_project.set_accessibility('public') # Default Accesibility: Protected

# 2. Creating Subject
## Similar to Project Create
name_s = 'subject_test4' # Name a new subject
test_subject = session.select.project(name_p).subject(name_s)
print('Subject Exists: %s' %test_subject.exists()) # Return False if project unfounded
test_subject.create()
print('After Created: %s' %test_subject.exists())

ls = ['ID_1', 'ID_2']
test_project_n = session.select.project('777')
test_project_n.create()
for i in ls:
      sub = session.select.project('777').subject(i)
      sub.create()
      sub.attrs.mset({
        'xnat:subjectData/demographics[@xsi:type=xnat:demographicData]/gender': 'Male',
        'xnat:subjectData/demographics[@xsi:type=xnat:demographicData]/handedness':'Right'}) # set attribute: gender, handedness
subject = test_project_n.subject('ID_1')
print(subject)
    


subjects = session.select.project('test2').subjects().get()
print(subjects)
test_subject.attrs.mset({
    'xnat:subjectData/demographics[@xsi:type=xnat:demographicData]/gender': 'Male',
    'xnat:subjectData/demographics[@xsi:type=xnat:demographicData]/handedness':'Right'}) # set attribute: gender, handedness

test_subject.attrs.mget({
    'xnat:subjectData/demographics[@xsi:type=xnat:demographicData]/gender',
    'xnat:subjectData/demographics[@xsi:type=xnat:demographicData]/handedness'}) # get attribute: gender, handedness

session.get("https://central.xnat.org/schemas/xnat/xnat.xsd")

session.inspect.datatypes('xnat::subjectData/demographics[@xsi:type=xnat:demographicData]/')
test_subject.attrs.mset({'xnat::subjectData/GENDER_TEXT': 'Male',
                        'xnat::subjectData/demographics[@xsi:type=xnat:demographicData]/handedness':'Right'})'''