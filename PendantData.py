#package imports
import time
import pandas as pd
from datetime import datetime as dt
#read in data as data frame
t0 = time.time()

df = pd.read_csv('ah_monthly_events.csv') 

#drop unnecessary data
df.drop('event_id', axis=1, inplace=True)
df.drop('zone_id', axis=1, inplace=True)
df.drop('cs_no', axis=1, inplace=True)

#drop "broken" fields
df = df.drop(df.index[45772:45789])
'''
4/28/2017 12:04:44 PM

'''

#convert all event dates to datetime format for easy removal
#possible optimization with mapply function although strptime requires 2 parameters
for i in range(len(df)):
    df['event_date'][i] = dt.strptime(df['event_date'][i],'%m/%d/%Y %I:%M:%S %p')
  
#drop unnecessary VACANT fields   
df = df[df['apartment']!='VACANT/DAMAGED']
df = df[df['apartment']!='MEDICAL TEAM ABORT']
df = df[df['apartment']!='Med Team Abort button']
df = df[df['apartment']!='UNASSIGNED']
df = df[df['apartment']!='Unassigned']
df = df[df['apartment']!='Vacant']
df = df[df['apartment']!='vacant']
df = df[df['apartment']!='unaddigned']
df = df[df['apartment']!='VACANT']
df = df[df['apartment']!='BROKEN']
df = df[df['apartment']!='LOST']
df = df[df['apartment']!='broken']
df = df[df['apartment']!='Broken']
df = df[df['apartment']!='Broken Pendant']
df = df[df['apartment']!='unassigned']

#There are 830 unique apartments/users, need to weed out repeat calls for accurate timings

# weeding out of repeat hits and count of slow calls and new calls
df['slow'] = 0
df_names =  df['apartment'].unique()
spam_count = 0
slow_count = 0
ct = 0
slo_df = df
for i in range(len(df_names)):
    person = df[df['apartment']==df_names[i]]
    presses = person.event_date
    indx = presses.index
    for j in range(len(indx)-1):
        delt = presses.loc[indx[j+1]]-presses.loc[indx[j]]
        delt = delt.total_seconds()
        if delt <= 300:          
            ##df.drop(df.index[indx[j]])
            df = df.drop(indx[j])
            spam_count += 1
            #person = person.drop(indx[j])
        if delt > 300:
            if delt < 1500:
                slo_df['slow'][j] = 1
                slow_count+=1
                df = df.drop(indx[j])
                

# df is now a comprehensive list of every call incident, not inlcuding slow response times
# or repeat calls.
                
#total call volume: 15513 Calls made VIA pendant
#spammed button count: 19481
#slow responses: 287

cpp = 15707/830

#around 18 calls per person in a month across all facilites

#take a look at which facilities had the most calls
p= df['event_date'].groupby(df['facility']).count().sort_values(ascending = False)

'''
Most incidents (should cross reference with data size)
American House Riverview           1437
American House Stone               1317
American House Oakland             1274
American House Sterling II         1257
American House Westland Venoy      1174
American House Troy                1048
American House Westland- Joy Rd     812
American House Lakeside I           734
American House Elmwood              729
American House West Bloomfield      709
American House The Villiages        693
American House Farmington Hills     646
American House Sterling I           591
American House Westland 3           571
American House Carpenter            525
American House Bld 1 and 2          434
American House Terrace              421
American House Hazel Park           402
American House Grand Blanc          348
American House Lakeside II          174
American House Milford              169
American House Lloyds Bayou          44
American House Livonia 2              4
'''

#which patients took the most calls?
l = df['event_date'].groupby(df['apartment']).count().sort_values(ascending = False)

n = pd.DataFrame()

n['names'] = l.index
n['calls'] = l.values
n['facility'] = ""

for i in range(len(n['names'])):
    n['facility'][i] = df.loc[df['apartment'] == n['names'][i], 'facility'].iloc[0]

'''
Apt 108 Carole Gillikin         299
Apt 9 Ruth Schirman             252
Apt 118 Sally Schoonover        243 
Apt 318 Pasquale Presti         216
Apt C-1 Marilyn Taylor          214
Apt C-9 Nancy Campbell          205
Apt 212 Clara Halatsis          197
Apt 123 Bruce Spencer           196
Apt 45 Betty Burgeson           188
Apt 36 Shirley Bauman           187
Apt 320 Ursula Crampton         186
Apt 12 Sarah Prell              183
Apt 60 Patricia Friegruber      180
Apt 38 Cecile Abduel-Massiah    179
Apt C-12 Mark Clark             175
Apt 104 Beverly Wright          174
Apt 114 Annette Peters          171
Apt A-12 James Weubel           168
Apt 210 Gilbert Lahoff          158
Apt 301 Mary Bertelsen          151
'''


# which facilities are the slowest to respond to calls ?

w = slo_df['slow'].groupby(slo_df['facility']).sum().sort_values(ascending = False)

t1 = time.time()

total = t1-t0

print(total/60)
