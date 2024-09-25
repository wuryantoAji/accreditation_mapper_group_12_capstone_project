import pandas as pd


from sfia import SFIA



data = SFIA('sfia_v8_custom.xlsx')

entry = data[('DESN', 1, 'Description')]


print(entry)