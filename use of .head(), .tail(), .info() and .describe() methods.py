import pandas as pd

data = {'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eva'],
        'Age': [24, 27, 22, 32, 29],
        'City': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix']}
df = pd.DataFrame(data)

print("First 3 rows using head():")
print(df.head(3))

print("\nLast 2 rows using tail():")
print(df.tail(2))

print("\nDataFrame summary using info():")
df.info()