import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from xgboost import XGBClassifier, plot_importance
from sklearn.model_selection import train_test_split

df = pd.read_csv("clean_telco.csv")

X = df.drop("Churn", axis=1)
y = df["Churn"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

xgb = XGBClassifier(
    n_estimators=200,
    max_depth=5,
    learning_rate=0.1,
    subsample=0.8,
    colsample_bytree=0.8,

    random_state=42,
    scale_pos_weight=(y_train.value_counts()[0] / y_train.value_counts()[1])
)
xgb.fit(X_train, y_train)

importances = xgb.feature_importances_
features = X.columns
importance_df = pd.DataFrame({
    "Feature": features,
    "Importance": importances
}).sort_values(by="Importance", ascending=False)

importance_df["Importance"] = importance_df["Importance"] / importance_df["Importance"].sum()

importance_df.to_csv("feature_importance.csv", index=False)
print("✅ Feature importance saved to feature_importance.csv")

plt.figure(figsize=(10,6))
sns.barplot(
    x="Importance", 
    y="Feature", 
    hue="Feature",       
    data=importance_df.head(10),
    palette="viridis",
    legend=False      
)

for i, val in enumerate(importance_df["Importance"]):
    plt.text(val + 0.002, i, f"{val:.2%}", va="center")

plt.title("Top 10 Churn Drivers (XGBoost Feature Importance)", fontsize=14, weight="bold")
plt.xlabel("Relative Importance")
plt.ylabel("Feature")
plt.tight_layout()
plt.show()
