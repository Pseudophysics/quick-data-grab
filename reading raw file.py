import pandas as pd
from pathlib import Path
import numpy as np


with open(Path(__file__).parent / 'rawmovedata.txt', 'r') as file:
    data = file.read().rsplit('\n\t\t')

g = pd.DataFrame(data)
g[1] = g[0].str.replace('\t', '')
g[2] = g[1].str.replace('\n', '')
t = ''.join(g[2].to_list())
t = t.replace(',]', ']')
t = t.replace(',}', '}')
f = t.split('}')
f2 = pd.DataFrame(f)
f3 = f2[f2[0].str.contains('learnset') & f2[0].str.contains('9')]
f3[0] = f3[0].str.replace('^,', '', regex=True)
f3 = f3[0].str.split('{learnset: ', expand=True)

f3[0]=f3[0].str.replace(":",'')
t = f3[1].str.split('],', expand=True)
for i in t.keys():
    mask = t[i].str.contains('"9')
    t[i].mask(~mask.fillna(False), '', inplace=True)
    t.loc[:, i] = t[i].str.findall('([a-zA-Z]*.): ').str.join('')

t.set_index(f3[0].values, inplace=True)
t.replace(r'^\s*$', np.nan, regex=True,inplace=True)
t.dropna(axis=0, how='all',inplace=True)
t.to_csv('NamesToMoves.csv')
print()