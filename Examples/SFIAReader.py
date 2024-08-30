import pandas as pd


from sfia import SFIA



data = SFIA('sfiaskills.6.3.en.1.xlsx')

entry = data[('DESN', 1, 'Description')]


print(entry)