import pandas as pd
import os
import joblib
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier

# Path setting: Jahan ye script hai, wahi files dhundo
BASE_PATH = os.path.dirname(os.path.abspath(__file__))

print(f"Working in: {BASE_PATH}")

try:
    # Files directly current folder (backend) se uthayi jayengi
    info = pd.read_csv(os.path.join(BASE_PATH, "studentInfo.csv"))
    assess_feats = pd.read_csv(os.path.join(BASE_PATH, "assess_features.csv"))
    vle_feats = pd.read_csv(os.path.join(BASE_PATH, "vle_features.csv"))
    print("✅ Files load ho gayin!")
except Exception as e:
    print(f"❌ Error: Files nahi milin. Error detail: {e}")
    exit()

# Model Training Logic
le_edu = LabelEncoder()
df = info.merge(assess_feats, on="id_student", how="left").merge(vle_feats, on="id_student", how="left")
df.fillna(0, inplace=True)
df['edu_encoded'] = le_edu.fit_transform(df['highest_education'])
df['target'] = df['final_result'].apply(lambda x: 1 if x in ['Pass', 'Distinction'] else 0)

X = df[['studied_credits', 'num_of_prev_attempts', 'avg_score', 'total_clicks', 'edu_encoded']]
y = df['target']

rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X, y)

# Save in the same backend folder
joblib.dump(rf_model, os.path.join(BASE_PATH, 'success_model.pkl'))
df.to_csv(os.path.join(BASE_PATH, "final_dataset.csv"), index=False)

print("✅ Model Trained & Saved Successfully!")