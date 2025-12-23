import pandas as pd

df = pd.DataFrame({
    'customer_id': ['001', '002', '003', '004'],
    'age': ['25', '30', '--', 'forty'],
    'income': ['50,000', '60,000', 'N/A', '70000'],
    'gender': ['Male', 'female', 'F', 'm'],
    'is_member': ['Yes', 'no', '1', '0'],
    'signup_date': ['2023/01/15', '15-02-2023', 'March 3, 2023', 'unknown'],
    'notes': ['Great customer', '<b>VIP</b>', 'Late payment', 'Regular <i>buyer</i>']
})

df["age"] = pd.to_numeric(df["age"], errors="coerce")
df["income"].str.replace(",", "").replace("N/A", pd.NA)
df["income"] = pd.to_numeric(df["income"], errors="coerce")
df["gender"] = df["gender"].str.lower().replace({"m": "Male", "f": "Female"})
df["gender"] = df["gender"].str.title().astype("category")
df["is_member"] = df["is_member"].str.lower().map({"yes": "True", "no": "False", "1": "True", "0": "False"})
df["signup_date"] = pd.to_datetime(df["signup_date"], errors="coerce")
df["notes"] = df["notes"].str.replace(r"<.*?>", "", regex=True)
df["notes"] = df["notes"].str.strip().str.title()
df["signup_date"] = pd.to_datetime(df["signup_date"], format="%D-%M-%Y")
df["income_grouped"] = df["income"].apply(lambda x: "Low" if x < 55000 else("Average" if x<65000 else("High")))

print(df.head())
print(df.info())