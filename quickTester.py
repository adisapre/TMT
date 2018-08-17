import pandas as pd
import numpy as np

verizon = pd.read_excel('verizon.xlsx')
comp = pd.read_excel('comp.xlsx')

l1=verizon['User name'].str.lower()
l2= comp.Names.str.lower()

for i in l2:
    if i not in l2:
        print(i)
        
