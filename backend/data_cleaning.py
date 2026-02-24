import pandas as pd

# Load datasets
info = pd.read_csv("data/studentInfo.csv")
assess = pd.read_csv("data/studentAssessment.csv")
vle = pd.read_csv("data/studentVle.csv")

# Shape check
print("studentInfo shape:", info.shape)
print("studentAssessment shape:", assess.shape)
print("studentVle shape:", vle.shape)

# Check missing values
print("\nMissing values in studentInfo:")
print(info.isnull().sum())

# Drop rows with missing student id (safety)
info = info.dropna(subset=["id_student"])
assess = assess.dropna(subset=["id_student"])
vle = vle.dropna(subset=["id_student"])

print("\nData cleaning completed successfully!")
