import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib

# Load the Excel sheet
df = pd.read_excel(
    "C:\\Users\\vinayak.mathur_thero\\Desktop\\Coding\\Telco_customer_churn.xlsx",
    sheet_name='Telco_Churn',
    index_col='CustomerID'
)

# Select features and target
X = df[['Tenure Months', 'Monthly Charges', 'Total Charges']].copy()
y = df['Churn Label'].map({'Yes': 1, 'No': 0})

# Convert all X columns to numeric (force errors to NaN)
X = X.apply(pd.to_numeric, errors='coerce')

# Drop rows with missing values in either X or y
X = X.dropna()
y = y.loc[X.index]  # Ensure y matches cleaned X

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Train model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Save model
joblib.dump(model, 'churn_model.pkl')
print("Model trained and saved successfully!")
