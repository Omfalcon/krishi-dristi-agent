
# import pandas as pd
# import pickle
# from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import OneHotEncoder, StandardScaler
# from sklearn.compose import ColumnTransformer
# from sklearn.pipeline import Pipeline
# from sklearn.ensemble import RandomForestClassifier
# from imblearn.pipeline import Pipeline as ImbPipeline
# from imblearn.over_sampling import SMOTE
# from sklearn.metrics import classification_report, accuracy_score

# # -----------------------------
# # 1. Load Data
# # -----------------------------
# df = pd.read_csv("./data/FertilizerPrediction.csv")

# # Features and target
# X = df.drop("Fertilizer Name", axis=1)
# y = df["Fertilizer Name"]

# # Identify categorical and numeric columns
# cat_cols = ["Soil Type", "Crop Type"]
# num_cols = [col for col in X.columns if col not in cat_cols]

# # -----------------------------
# # 2. Train/Test Split
# # -----------------------------
# X_train, X_test, y_train, y_test = train_test_split(
#     X, y, test_size=0.1, random_state=42
# )

# # -----------------------------
# # 3. Preprocessing
# # -----------------------------
# preprocessor = ColumnTransformer(
#     transformers=[
#         ("num", StandardScaler(), num_cols),
#         ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols)
#     ]
# )

# # -----------------------------
# # 4. Build Pipeline with SMOTE + Classifier
# # -----------------------------
# pipeline = ImbPipeline(steps=[
#     ("preprocessor", preprocessor),
#     ("smote", SMOTE(random_state=42, k_neighbors=3)),
#     ("classifier", RandomForestClassifier(n_estimators=100, random_state=42))
# ])


# # -----------------------------
# # 5. Train Pipeline
# # -----------------------------
# pipeline.fit(X_train, y_train)

# # -----------------------------
# # 6. Evaluate
# # -----------------------------
# y_pred = pipeline.predict(X_test)
# print("Accuracy:", accuracy_score(y_test, y_pred))
# print(classification_report(y_test, y_pred))

# # -----------------------------
# # 7. Save Pipeline
# # -----------------------------
# with open("fertilizer_pipeline.pkl", "wb") as f:
#     pickle.dump(pipeline, f)

# # -----------------------------
# # 8. Inference Example
# # -----------------------------
# def predict_fertilizer(input_dict):
#     """
#     input_dict example:
#     {
#         'Temperature': 26.0,
#         'Humidity': 52.0,
#         'Moisture': 38.0,
#         'Soil Type': 'Sandy',
#         'Crop Type': 'Maize',
#         'Nitrogen': 37,
#         'Potassium': 0,
#         'Phosphorous': 0
#     }
#     """
#     df_input = pd.DataFrame([input_dict])
#     pipeline = pickle.load(open("fertilizer_pipeline.pkl", "rb"))
#     pred = pipeline.predict(df_input)[0]
#     return pred

# # Example
# if __name__ == "__main__":
#     sample_input = {
#         'Temparature': 30.0,
#         'Humidity': 60.0,
#         'Moisture': 42.0,
#         'Soil Type': 'Sandy',
#         'Crop Type': 'Maize',
#         'Nitrogen': 22,
#         'Potassium': 0,
#         'Phosphorous': 21
#     }
#     print("Predicted Fertilizer:", predict_fertilizer(sample_input))



import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from imblearn.pipeline import Pipeline as ImbPipeline
from imblearn.over_sampling import SMOTE
from sklearn.metrics import classification_report, accuracy_score

# -----------------------------
# 1. Load Data
# -----------------------------
df = pd.read_csv("./data/FertilizerPrediction.csv")

# Clean column names if necessary (handles the common 'Temparature' typo in some datasets)
df.columns = df.columns.str.replace('Temparature', 'Temperature')

X = df.drop("Fertilizer Name", axis=1)
y = df["Fertilizer Name"]

cat_cols = ["Soil Type", "Crop Type"]
num_cols = [col for col in X.columns if col not in cat_cols]

# -----------------------------
# 2. Train/Test Split
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42,stratify=y           # This ensures every class is in both sets
)

# -----------------------------
# 3. Preprocessing & Scaling
# -----------------------------
# We encode categorical data first, then scale EVERYTHING in the next step of the pipeline
num_scaler = StandardScaler()
preprocessor = ColumnTransformer(
    transformers=[
        ("num", num_scaler, num_cols), # Scale only numbers
        ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), cat_cols)
    ],
    remainder="passthrough" # Keeps numeric columns as they are
)

# -----------------------------
# 4. Build Pipeline (Preprocessing -> Scaling -> SMOTE -> RF)
# -----------------------------
pipeline = ImbPipeline(steps=[
    ("preprocessor", preprocessor),
    ("smote", SMOTE(random_state=42, k_neighbors=3)),
    ("classifier", RandomForestClassifier(
        n_estimators=50,       # Keep it at 100 since 200 overfits
        max_depth=5,           # Stop trees from memorizing noise
        min_samples_split=20,
        min_samples_leaf=4,     # Ensure predictions are based on groups, not individuals
        max_features='log2',    # Increase variety between trees
        class_weight='balanced',   # Helps the rare 17-17-17 class
        oob_score=True,            # Gives you an extra health-check score
        random_state=42,
        n_jobs=-1               # Faster training
    ))
])

# -----------------------------
# 5. Train & Evaluate
# -----------------------------
# pipeline.fit uses fit_transform internally on training data
pipeline.fit(X_train, y_train)

# pipeline.predict uses ONLY transform internally on test data
y_pred = pipeline.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print("OOB Score:", pipeline.named_steps['classifier'].oob_score_)
print(classification_report(y_test, y_pred))


# -----------------------------
# 6. Save Pipeline
# -----------------------------
import os 
if os.path.exists("fertilizer_bundle.pkl"):
    with open("fertilizer_bundle.pkl", "rb") as f:
        bundle = pickle.load(f)
        LOADED_PIPELINE = bundle["pipeline"]
        TRAIN_FEATURES = bundle["feature_names"]

### inference
def predict_fertilizer(input_dict):
    """
    Takes a raw dictionary, formats it, and returns a prediction.
    """
    # Create DataFrame
    df_input = pd.DataFrame([input_dict])
    
    # Standardize column names (fix typos)
    df_input.columns = df_input.columns.str.replace('Temparature', 'Temperature')
    
    # MANDATORY: Force the input to have the exact same column order as training
    # This prevents the model from getting data in the wrong slots
    df_input = df_input.reindex(columns=TRAIN_FEATURES)
    
    # Predict using the globally loaded pipeline
    return LOADED_PIPELINE.predict(df_input)[0]


if __name__ == "__main__":
    sample_input = {
        'Temperature': 30.0, # Fixed spelling typo here
        'Humidity': 60.0,
        'Moisture': 42.0,
        'Soil Type': 'Sandy',
        'Crop Type': 'Maize',
        'Nitrogen': 22,
        'Potassium': 0,
        'Phosphorous': 21
    }
    print("Predicted Fertilizer:", predict_fertilizer(sample_input))