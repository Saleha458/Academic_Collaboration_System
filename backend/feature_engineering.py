import pandas as pd

# Load raw datasets
assess = pd.read_csv("data/studentAssessment.csv")
vle = pd.read_csv("data/studentVle.csv")

# ===============================
# PERFORMANCE FEATURES
# ===============================
assess_features = assess.groupby("id_student").agg(
    avg_score=("score", "mean"),
    assessment_count=("id_assessment", "count")
).reset_index()

# Save assessment features
assess_features.to_csv("backend/assess_features.csv", index=False)

print("Assessment features created")
print(assess_features.head())

# ===============================
# ENGAGEMENT FEATURES
# ===============================
vle_features = vle.groupby("id_student").agg(
    total_clicks=("sum_click", "sum"),
    active_days=("date", "nunique")
).reset_index()

vle_features["avg_clicks_per_day"] = (
    vle_features["total_clicks"] / vle_features["active_days"]
)

# Save VLE features
vle_features.to_csv("backend/vle_features.csv", index=False)

print("\nVLE features created")
print(vle_features.head())
