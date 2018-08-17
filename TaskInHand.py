import pandas as pd
import numpy as np
#first make sure timestamps are readable formats, data should be pre cleaned to this point
df = pd.read_excel('TiH.xlsx') 
dfc = df[df.notnull().values]

vil = df[df.Facility == 'Village']
fh = df[df.Facility == 'Farmington Hill']
#Start and End times are in TimeStamp Format  

#need to figure out means and std deviation of actual data, theoritical data in order to create a normal curve
#at minimum should look at distibution of each type, take a look at what unique tasks there are first

#checking acuity of buildings, function will return a list of counts of failure to clock out task

#used to clean data 
def clean(df):
    temp = df[df['Total Sec'] <= 5400]
    return temp
    

def acuity(df):
    print("Number of unfinished tasks: "+str(df.isnull().sum().sum()))
    temp = df[df.isnull().values]
    return temp['Facility'].groupby(temp["Aide"]).count().sort_values(ascending = False)

#funtion chechking which employees use the system most accuratley and most often

def goodUsers(df):
    temp =df[df.notnull().values]
    return temp['Facility'].groupby(temp["Aide"]).count().sort_values(ascending = False)

#checks how many care requests were done by each aide:
def careGiven(df):
    temp=df['Facility'].groupby(df['Aide']).count().sort_values(ascending = False)
    x = pd.DataFrame()
    x['names'] =temp.index
    x['care_no '] = temp.values
    x['facility'] = ""
    for i in range(len(x['names'])):
        x['facility'][i] = df.loc[df['Aide'] == x['names'][i], 'Facility'].iloc[0]
    return x
#client information

#Will return count of care incidents per client & which facility they are located at
def careRequests(df):
    temp=df['Facility'].groupby(df['Client']).count().sort_values(ascending = False)
    x = pd.DataFrame()
    x['names'] =temp.index
    x['care_no '] = temp.values
    x['facility'] = ""
    for i in range(len(x['names'])):
        x['facility'][i] = df.loc[df['Client'] == x['names'][i], 'Facility'].iloc[0]
    return x

#recurring problem isn't instant hits, its long time hits
def nOutlier(df, service):
    temp= clean(df)
    temp =df[df.notnull().values]
    temp =  df[df.Care == service]
    avg = np.mean(temp['Total Sec'])
    std = np.std(temp['Total Sec'])
    low = avg-(2*std)
    high = avg+(2*std)
    lower= temp[temp['Total Sec'] < low]
    higher = temp[temp['Total Sec'] < high]
    return lower.append(higher)

def avgSeconds(df,service):
    temp =  df[df.notnull().values]
    temp =  df[df.Care == service]
    return  np.mean(temp['Total Sec'])

def summary(df):
    for i in df['Care'].unique():
        print ('Average time for '+i+" is "+str(avgSeconds(df,i)/60)+' min.')
    print()
    print('The number of null tasks for this facility by aide is:')
    acuity(df)
    