import pandas as pd
from datetime import datetime as dt
import numpy as np
#read in data frame
df = pd.read_excel('Aides_7_31_2018.xlsx')

#full copy of df
full_copy = df


#ignore orientation numbers
df = df[df['RegRate'] >= 9.25]
df = df[df['DaysWorked'] >= 60]

#active/inactive subsets
active = df[df['Status'] == 'Active']
inactive = df[df['Status'] == 'Inactive']

#average Total rate by building
a = df['RegRate'].groupby(df['Facility']).mean()


#count of aides
b = df['RegRate'].groupby(df['Facility']).count()

#average rate per skill type overall
for i in df['SkillName'].unique():
    temp = df[df['SkillName']==i]
    print(i)
    print(temp.RegRate.mean())

#average rate per skill type for each facility

avg = pd.DataFrame()

for i in df['SkillName'].unique():
    temp2 = df[df['SkillName']==i]
    avg[i] = temp2['RegRate'].groupby(temp2['Facility']).mean()
    
    
#checking overtime pay, pay by age, turnover rate, and filtering out unecessary data
     
c = df['RegRate'].groupby(df['City']).count()
df = df.reset_index()

df['age'] = ""
for i in range(len(df)):    
    df['age'][i] = np.rint((dt.now()-df["BirthDate"][i]).days/365)

d = df['RegRate'].groupby(df['age']).mean()    
    