import pandas as pd
def convert_to_datetime(year: int, month: int, day:int):
     return pd.to_datetime(10000 * year + 100 * month + day, format='%Y%m%d')
