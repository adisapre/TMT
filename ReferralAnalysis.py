#imports
import pandas as pd
from datetime import datetime as dt
from datetime import timedelta
#reading in data file...
byPhys = pd.read_excel('MarketerPhysiciansNew2017-2018.xlsx')
byRef = pd.read_excel('MarketerReferralsNew2017-2018.xlsx')
MktTable = pd.DataFrame()
PhysTable = pd.DataFrame()
RefTable = pd.DataFrame()
#Marketer Operations
#two files seem to have different numbers, doing operations on both seperately to see where the change is occuring

MktList = byPhys['Marketer'].unique()

byPhys['Date'].groupby(byPhys['Marketer']).count().sort_values(ascending = False)

#counts of referrals by marketers in total
'''
Marketer
Taranto, Jerome                   517
Hatfield, Donnell                 510
Adams, Lauralee                   312
Picou, Debbie                     259
No Marketer Assigned              133
Marketing, No Liaison Assigned     35
'''
 
byRef['Date'].groupby(byRef['Marketer']).count()

#phys total is higher, will use that one as it seems more updated/recent

 

for i in MktList:
    ind = byPhys[byPhys['Marketer'] == i]
    x = ind['Marketer'].groupby(ind['Date']).count().sort_index()
    MktTable = MktTable.append(x, ignore_index = True)

##Final Table, NAN = No data for said month.   
MktTable.insert(loc = 0, column = "Marketer", value = MktList)    

# Physicians  Operations

#Total # of referrals sent to physicians
byPhys['Date'].groupby(byPhys['Physician']).count().sort_values(ascending = False)

'''
Top Physicians:
Henry, Russell (M.D.)           66
Walker, Patrick (M.D.)          64
Abou-Issa, Fadi (MD)            57
Ellender, Patrick (M.D.)        38
Chaisson, Thomas (M.D.)         36
Espinoza, Andrea (MD)           32
Wade, Craig (MD)                28
Chesnut, Alain (MD)             26
Huddleston, Jamie (MD)          26
Cinnater, Ray (M.D.)            26
Scott, Jarelle M (MD)           26
...(more available)
'''
#unique physician values
PhysList = byPhys['Physician'].unique()

#coutning and sorting into proper months
for i in PhysList:
    ind = byPhys[byPhys['Physician'] == i]
    q = ind['Physician'].groupby(ind['Date']).count().sort_index()
    PhysTable = PhysTable.append(q, ignore_index = True)

#adding physicians labels    
PhysTable.insert(loc = 0, column = "Physician", value = PhysList)
 
# Referral Souce Operations

#datetime change for other spreadsheet
for i in range(len(byRef)):
    byRef['Date'][i] = dt.strptime(byRef['Date'][i],'%m/%Y')

byPhys['Date'].groupby(byPhys['Physician']).count().sort_values(ascending = False)

#find unique referral values
RefList = byRef['Referrer'].unique()   

#total number of refererals per source
byRef['Date'].groupby(byRef['Referrer']).count().sort_values(ascending = False)

#Most Popular Sources
'''
Mollere, Megan (Terrebonne General Medical Center)                     49
Nguyen, Sandra (CM) (West Jefferson Medical Center)                    38
Townsend, Chantel (LPN) (Terrebonne General Medical Center)            36
Boudreaux, Kayley (Terrebonne General Medical Center)                  33
Blanchard, Victor (Ochsner Leonard J. Chabert Medical Center)          32
Bibbins, Deborah (RN) (Veterans Administration)                        29
Sheila (Thibodaux Regional Medical Center)                             27
Gautreaux, Jodie (LPN) (Terrebonne General Medical Center)             26
Sheila (TRMC)                                                          25
Robinson, Sylvia (CM) (Ochsner Main)                                   23
Washington, Tania (LMSW) (Thibodaux Regional Medical Center)           22
Euleka (Patrick Walker)                                                22
Anders, Debra (RN) (VA)                                                22
Cantrelle, Kimberley (LPN) (Terrebonne General Medical Center)         21
...(more available)
'''

#coutning and sorting into proper months
for i in RefList:
    ind = byRef[byRef['Referrer'] == i]
    q = ind['Referrer'].groupby(ind['Date']).count().sort_index()
    RefTable = RefTable.append(q, ignore_index = True)

#adding physicians labels    
RefTable.insert(loc = 0, column = "Referrer", value = RefList)

#writing to excel sheet (Commented out due to extra analysis done on sheet. Uncomment for a new sheet)

#writer =  pd.ExcelWriter('ReferralAnalysis.xlsx')
# 
#MktTable.to_excel(writer,'MarketerToReferrals')
#PhysTable.to_excel(writer,'PhysicianToReferrals')
#RefTable.to_excel(writer,'ReferralSource')
#
#writer.save()


##############################################################################
# Other Relevant Data Analysis
##############################################################################

#What is the average amount of referrals in the past 3 months only, per person?

mos = byPhys[byPhys['Date'] > dt.today()-timedelta(days = 90)]

totalRecentList = mos['Date'].groupby(mos['Marketer']).count().sort_values(ascending=False)

totalRecentList = totalRecentList/3

totalRecentList

'''
Marketer
Taranto, Jerome         29.333333
Hatfield, Donnell       22.666667
Adams, Lauralee         14.000000
Picou, Debbie           11.333333
No Marketer Assigned     6.666667
Name: Date, dtype: float64
'''
#Extra analysis done on Excel Sheet attatched, inlcuding monthly averages, total graphs over time.

