
import pandas as pd
import numpy as np
import pickle
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from imblearn.pipeline import Pipeline as ImbPipeline
from imblearn.over_sampling import SMOTE
from sklearn.metrics import classification_report, accuracy_score

# 1. Load and Clean Data
df = pd.read_csv("./data/FertilizerPrediction.csv")
df.columns = df.columns.str.replace('Temparature', 'Temperature')

X = df.drop("Fertilizer Name", axis=1)
y = df["Fertilizer Name"]

# Store the feature names globally right now so the function can see them
GLOBAL_FEATURES = X.columns.tolist()

cat_cols = ["Soil Type", "Crop Type"]
num_cols = [col for col in X.columns if col not in cat_cols]

# 2. Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)

# 3. Preprocessing
preprocessor = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), num_cols),
        ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), cat_cols)
    ]
)

# 4. Build Pipeline
pipeline = ImbPipeline(steps=[
    ("preprocessor", preprocessor),
    ("smote", SMOTE(random_state=42, k_neighbors=3)),
    ("classifier", RandomForestClassifier(
        n_estimators=50,
        max_depth=5,
        min_samples_split=20,
        min_samples_leaf=4,
        max_features='log2',
        class_weight='balanced',
        random_state=42,
        n_jobs=-1
    ))
])

# 5. Train
pipeline.fit(X_train, y_train)


# pipeline.predict uses ONLY transform internally on test data
y_pred = pipeline.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))


# 6. Save the Bundle (Pipeline + Column Names)
model_bundle = {
    "pipeline": pipeline,
    "features": GLOBAL_FEATURES
}

with open("fertilizer_bundle.pkl", "wb") as f:
    pickle.dump(model_bundle, f)

print("Model trained and saved as 'fertilizer_bundle.pkl'")

# ---------------------------------------------------------
# 7. INFERENCE SECTION
# ---------------------------------------------------------

def predict_fertilizer(input_dict):
    # Load the bundle inside or use the already trained 'pipeline'
    # For a standalone script, we load it to ensure the file works
    with open("fertilizer_bundle.pkl", "rb") as f:
        loaded_bundle = pickle.load(f)
        model = loaded_bundle["pipeline"]
        features = loaded_bundle["features"]
    
    df_input = pd.DataFrame([input_dict])
    df_input.columns = df_input.columns.str.replace('Temparature', 'Temperature')
    
    # Ensure column order matches the training features
    df_input = df_input.reindex(columns=features)
    
    return model.predict(df_input)[0]

# Example Test
if __name__ == "__main__":
    sample_input = {
        'Temperature': 30.0,
        'Humidity': 60.0,
        'Moisture': 42.0,
        'Soil Type': 'Sandy',
        'Crop Type': 'Maize',
        'Nitrogen': 22,
        'Potassium': 0,
        'Phosphorous': 21
    }
    
    result = predict_fertilizer(sample_input)
    print(f"\nPredicted Fertilizer: {result}")