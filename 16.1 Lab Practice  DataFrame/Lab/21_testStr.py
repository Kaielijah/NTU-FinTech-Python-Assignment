import pandas as pd

df = pd.DataFrame({
"Name": ["Braund, Mr. Owen Harris",
"Allen, Mr. William Henry",
"Bonnell, Miss. Elizabeth"],
"Age": [22, 35, 58],
"Sex": ["male", "male", "female"]})

# print(df)
# print(df["Sex"].str.upper())

daily = pd.read_csv('test.csv')

# print(daily.head(10))

selected = daily[daily['Security Name'].str.lower().str.contains("american")]
filter_A = daily[daily['Symbol'].str.upper().str.contains('A')]
# print(selected)
print(filter_A)
