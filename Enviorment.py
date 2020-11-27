################
# Environement #
################
# Import Packages Needed
import pandas as pd
import os
import glob

# Directory
# wd = os.chdir('F:') # Set working directory
cwd = os.getcwd() # Get current working directory
file_ls = os.listdir(cwd) # File List under the path 
x_datapath = glob.glob('*X_ray*.xlsx') # Files contains the specific character
c_datapath = glob.glob('Clinical*.csv')
i_datapath = glob.glob('*IMAGENO*.csv')
d_datapath = glob.glob('*dicomhead*.csv')
print("Current Working Directory %s\nImage Reports: %s\nClinical Information: %s\nImage Information: %s\nDICOM: %s" 
      %(cwd, x_datapath, c_datapath, i_datapath, d_datapath)) # List out only file needed

# Setting
pd.set_option('display.max_columns', None) # To display the entire columns without ...
pd.set_option('display.max_colwidth', None) # To display the entire columns' value

# Preselect Columns (Variable) Required, because of Hardware Limitation
x_cols = ['歸戶代號', '收件日期', 'CONTENT']
c_cols = ['歸戶代號', '性別', '年齡', '住院日期', '診斷類別名稱1', '診斷類別名稱2', '診斷類別名稱3', '診斷類別名稱4', 
          '診斷類別名稱5', '診斷類別名稱6', '診斷類別名稱7', '診斷類別名稱8', '診斷類別名稱9', '診斷類別名稱10']
i_cols = ['歸戶代號', 'image_no']
d_cols = ['PatientID', 'fullpath', 'StudyDate', 'Modality', 'AccessionNumber', 'Manufacturer', 'PatientBirthDate']

################
# Data Loading #
################
# Read as Pandas DataFrames
## Source 1: X_ray report
x_ls = [] # Create empty list for append reading files
for filename in x_datapath:
    tmp = pd.read_excel(os.path.join(cwd, filename), # read_excel for xlsx(excel files) 
                        usecols = x_cols) # Read specific columns only
    x_ls.append(tmp)
x_ray = pd.concat(x_ls) # Concatenate Result

## Source 2: Clinical Information
clinfo = pd.read_csv(os.path.join(cwd, 'Clinical_Info.csv'), # read_csv for csv
                     engine = 'python', # Parser engine is default as 'c', which is faster,
                                         # but not suitable for files with chinese word.
                     encoding = 'utf-8' , # The common encoder of chinese characters
                     usecols = c_cols)

## Source 3: Image Information
imginfo = pd.read_csv(os.path.join(cwd, 'STROKE_IMAGENO.csv'), engine = 'python', encoding = 'utf-8', usecols = i_cols)

## Source 4: DICOM
dicom = pd.read_csv(os.path.join(cwd, 'dicomhead.csv'), engine = 'python', encoding = 'utf-8', usecols = d_cols)

# Present source shape
print('Shape of X ray report: %s\nShape of Clinical Information: %s\nShape of Image Information: %s\nShape of DICOM: %s' 
      %(x_ray.shape, clinfo.shape, imginfo.shape, dicom.shape)) # (row number, column number)

#############################
# DICOM + Image Information #
#############################
# Integrate Image Series Number & Data Path
## DICOM
print('DICOM\n%s' %dicom.columns)
dicom.head()

## Image Information
print('Image Information\n%s' %imginfo.columns)
imginfo.head()

# Integration
imginfo = imginfo.rename(columns = {'image_no': 'AccessionNumber', # Rename Key Columns' to achieve Merging
                                    '歸戶代號': 'PatientID'})

img = pd.merge(imginfo, # pd.merge for Combining 2 DataFrames
               dicom, # Second DataFrame
               how = 'inner', # Inner presend Intersection of both DataFrame
               on = ['AccessionNumber', 'PatientID']) # Key Columns
# img = imginfo.merge(dicom, how = 'inner', on = ['AccessionNumber', 'PatientID']) # Same as Above
print('DICOM + Image Info\n%s\nShape: %s' %(img.columns, img.shape)) # Remain Rows Size
img.head() # Show Five Rows of the DataFrame

##################
# Image + Report #
##################
# Report Overview
print('Image report\n%s' %x_ray.columns) # List out the columns and dtype
x_ray.head() # Show five rows from the table

# Integration
x_ray = x_ray.rename(columns = {'歸戶代號': 'PatientID', '收件日期': 'StudyDate', 'CONTENT': 'Content'})
img = pd.merge(img, x_ray, how = 'inner', on = ['PatientID', 'StudyDate'])
print('Final Image Information\n%s\nShape: %s' %(img.columns, img.shape)) # Remain Rows Size
img.head()

##################
# Clean & Output #
##################
# Missing Value
## NA Counting
print('Image Information NA Counting\n%s' %img.isna().sum()) # Check NA Detected from Each Column

## Drop NA
img = img.dropna() # Drop Rows Having NA
print('Image Information Rows After NA Dropped:', img.shape) # 9294 (-4) = 9288

# Filter CT & MR Series
## CT
print('Row Count by Modality\n', img.groupby('Modality')['Modality'].count()) # Original Data having OT / XA Modality
ct = img[img['Modality'] == 'CT'] # Series Modality of CT
ct = ct[ct['Content'].str.contains('CT')] # Report Content Contains 'CT' word
print('\nCT Modality + CT Report:', ct.shape) # 

## MR
mr = img[img['Modality'] == 'MR']
mr = mr[mr['Content'].str.contains('MR')]
print('MR Modality + MR Report:', mr.shape) 

# Concatenate
ctmr = pd.concat([ct, mr])
print('CTMR:', ctmr.shape)

# Duplicate Rows/Value
ctmr = ctmr.drop_duplicates(subset = ['AccessionNumber']) # Image Number Must be Unique
print('Final CTMR:', ctmr.shape)

# Match Data Path
path = os.path.join(cwd, 'CGRD') # Location of DICOM Image
files = os.listdir(path) # File List among the Path
print('Image Files Matched by Path:', ctmr[ctmr['fullpath'].isin(files)].shape)

# Export Image Result
ctmr.to_csv('CTMR.csv', # File name
            index = False, # Ignore DataFrame Index
            encoding = 'utf-8') # For Chinese Word

# Clinical Information
print('Clinical Information\n%s' %clinfo.columns)
clinfo.head()

# Combine Columns as one
clinfo['History'] = clinfo[['診斷類別名稱1', '診斷類別名稱2', '診斷類別名稱3', '診斷類別名稱4', '診斷類別名稱5', '診斷類別名稱6', 
                            '診斷類別名稱7', '診斷類別名稱8', '診斷類別名稱9', 
                            '診斷類別名稱10']].astype(str).agg(' '.join, # str type adding, separate with ' ' (space)
                                                         axis = 1)
clinfo['History'] = clinfo['History'].str.replace('nan', '') # Replace nan characters to None
clinfo['History'] = clinfo['History'].str.replace('\s+', ' ') # Replace Multiple blank space to one
clinfo['History'].head()

# Columns Rename
clinfo = clinfo.rename(columns = {'歸戶代號': 'ID', '性別': 'Gender', '年齡': 'Age'})
clinfo = clinfo[['ID', 'Gender', 'Age', 'History']] # Select Columns Needed
print('Clinical Information\n%s\nShape: %s' %(clinfo.columns, clinfo.shape)) # Remain Rows Size
clinfo.head()

# Intersect with Image Patient ID
df = clinfo[clinfo.ID.isin(ctmr['PatientID'])]
df = df.sort_values(by = ['ID', 'Age']) # Sort Values by ID, and the Age
print('Clinical Information Shape:', df.shape)
df.head()

# Remain Unique Patiet Information
df2 = df.drop_duplicates(subset = ['ID'], keep = 'last') # Keep the Last Repeated ID
print('Unique Clinical Information Shape:', df2.shape)
df2.head()

# Output
df.to_csv('Clinfo.csv', index = False, encoding = 'utf-8')
df2.to_csv('uni_Clinfo.csv', index = False, encoding = 'utf-8')
'''


'''ls_project = session.select('/project').get()

## Subjects Under the Path
### ls_subject = session.select.projects().subjects().get()
ls_subject = session.select('/project/subject').get()

print('Project List: %s\nSubject List: %s' %(ls_project, ls_subject))