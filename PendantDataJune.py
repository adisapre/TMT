#package imports
import time
import pandas as pd  
#read in data as data frame
df = pd.read_excel('ah_monthly_events_jun.xlsx')

t0 = time.time()

#drop unnecessary data
df.drop('event_id', axis=1, inplace=True)
df.drop('zone_id', axis=1, inplace=True)
df.drop('cs_no', axis=1, inplace=True)

#drop "broken" fields

'''
4/28/2017 12:04:44 PM
 
''' 

#convert all event dates to datetime format for easy removal
#possible optimization with mapply function although strptime requires 2 parameters
#for i in range(len(df)):
#    df['event_date'][i] = dt.strptime(df['event_date'][i],'%m/%d/%Y %I:%M:%S %p')
  
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
df = df[df['apartment']!='Medical Team Acknowledgment.']
df = df[df['apartment']!='unassinged']
df = df[df['apartment']!='Lost']
df = df[df['apartment']!='Mailed out 4/10/18']
df = df[df['apartment']!='VACANT/LOST']
df = df[df['apartment']!='Apt A-9 VACANT APT']
df = df[df['apartment']!='Medical Team Acknowledgement']

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
                
#total call volume: 18279 Calls made VIA pendant
#spammed button count: 26962
#slow responses: 6919 

cpp = len(df)/len(df_names)


#around 20 calls per person in a month across all facilites

#take a look at which facilities had the most calls
w =df['event_date'].groupby(df['facility']).count().sort_values(ascending = False)


    

'''
American House Sterling II         1562
American House Southland           1440
American House Livonia 2           1337
American House Sterling I          1284
American House Stone               1171
American House Riverview           1093
American House Westland 3          1070
American House Westland Venoy        
American House Westland- Joy Rd     937
American House West Bloomfield      854
American House Oakland              734
American House Elmwood              647
American House Hazel Park           622
American House Carpenter            597
American House Farmington Hills     577
American House Lloyds Bayou         564
American House Lakeside I           435
American House Milford              418
American House Lakeside II          413
American House Terrace              333
American House Troy                 332
American House Bld 1 and 2          332
American House The Villiages        252
American House Grand Blanc          252
American House Southgate             58
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
Apt 7 Dolores Kolle            245
Apt 39 Steven Pawlyk           216
Apt 112 Lillian Galazka        212
Apt 14 Francis Talley          210
Apt 226 Patricia Richards      207
Apt 210 Gilbert Lauhoff        201
Apt 212 Clara Halatsis         189
Apt 105 Caterine Neal          182
Apt 202 Liz Verplank           182
Apt 308 Gerald Stann           175
Apt 36 Shirey Bauman           165
Apt 120 Mable Michaels         160
Apt 102 Jonathan Bishoff       155
Apt 25 Rose Jay                150
Apt 9 Kathyn Clemans           149
Apt 10 Majorie Durand          146
Apt 203 Janet Scott            141
Apt 101 Juanita Marentette     141
Apt 230 Albert Jackson         132
Apt 119 Charles Montana         
Apt 103 Margo Crimo            131

Apt 113 Ernest Semak           130
Apt 130 Dorothy Vardy          128
Apt 321 Mary Debien            125
Apt 80 Irene Rosnowsky         122
Apt T-13 Cheryl Cirk           121
Apt 212 Charles Knight         117
Apt 52 Carol Casey             117
Apt 223 Ben Pearlman           116
'''

# which facilities are the slowest to respond to calls ?

p= slo_df['slow'].groupby(slo_df['facility']).sum().sort_values(ascending = False)

'''
American House Bld 1 and 2         570
American House Carpenter           219
American House Elmwood              12
American House Oakland               0
American House Farmington Hills      0
American House Grand Blanc           0
American House Hazel Park            0 
American House Lakeside I            0
American House Lakeside II           0
American House Livonia 2             0
American House Lloyds Bayou          0
American House Milford               0
American House Westland- Joy Rd      0
American House Westland Venoy        0
American House Southgate             0
American House Southland             0
American House Sterling I            0
American House Sterling II           0
American House Stone                 0
American House Terrace               0
American House The Villiages         0
American House Troy                  0
American House West Bloomfield       0
American House Westland 3            0
American House Riverview             0
'''
t1 = time.time()

total = t1-t0

print(total/60)
