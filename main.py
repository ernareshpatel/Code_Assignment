import sys
import pandas as pd
import numpy as np
import json
from datetime import datetime, date

filename = sys.argv[1]

# Read Data
df = pd.read_csv(filename,
                 delimiter="|",
                 header=None,
                 names=[
                     'FirstName', 'LastName', 'Company', 'BirthDate', 'Salary',
                     'Address', 'Suburb', 'State', 'Post', 'Phone', 'Mobile',
                     'Email'
                 ],
                 dtype={
                     'FirstName': str,
                     'LastName': str,
                     'Company': str,
                     'BirthDate': int,
                     'Salary': float,
                     'Address': str,
                     'Suburb': str,
                     'State': str,
                     'Post': int,
                     'Phone': int,
                     'Mobile': int,
                     'Email': str
                 })

# Transformation

df['BirthDate'] = df['BirthDate'].apply(
    lambda x: pd.to_datetime(str(x), format='%d%m%Y'))

df['BirthDate'] = df['BirthDate'].dt.strftime('%d/%m/%Y')

df['SalaryBucket '] = np.where(df['Salary'] < 50.000, 'A',
                      np.where((df['Salary'] >= 50.000) & (df['Salary'] <= 100.000), 'B',
                      np.where(df['Salary'] > 100.000, 'C','')))                      

df['Salary'] = '$' + df["Salary"].map('{:,.2f}'.format)

df['FirstName'] = df['FirstName'].map(lambda x: x.strip())
df['LastName'] = df['FirstName'].map(lambda x: x.strip())

df["FullName"] = df["FirstName"].astype(str) + ' ' + df["LastName"].astype(str)


# converts given date to age
def age(born):
  born = datetime.strptime(born, "%d/%m/%Y").date()
  #today = date.today()
  today = pd.to_datetime('01/03/2024')
  return today.year - born.year - (
      (today.month, today.day) < (born.month, born.day))


df['Age'] = df['BirthDate'].apply(age)

#drop columns
df = df.drop('FirstName', axis=1)
df = df.drop('LastName', axis=1)

#print(df)

# Convert DataFrame to a list of dictionaries
dict_list = df.to_dict('records')
#print(dict_list)


# write output to json file
with open('result.json', 'w') as fp:
    json.dump(dict_list, fp)
