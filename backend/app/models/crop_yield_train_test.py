import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error, r2_score

# ==========================================
# 1. DATA PREPARATION
# ==========================================
# Load the dataset
df = pd.read_csv("./data/yield_df.csv", index_col=0)

# Filter for India and remove duplicates
india_df = df[df['Area'] == 'India'].drop_duplicates().copy()

# One-Hot Encoding for the Crop 'Item'
india_encoded = pd.get_dummies(india_df, columns=['Item'], prefix='Crop')

# Define Features (X) and Target (y)
# We exclude 'hg/ha_yield' (target), 'Year' (not a predictor), and 'Area' (all India)
X = india_encoded.drop(['hg/ha_yield', 'Year', 'Area'], axis=1)
y = india_encoded['hg/ha_yield']

# Split into Training and Testing sets (using RAW data, not manually scaled)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

# ==========================================
# 2. THE SINGLE PIPELINE SETUP
# ==========================================
# This 'Pipeline' object bundles the Scaler and the Model into ONE unit.
# When you call .predict(), the pipeline automatically scales the input first.
yield_pipeline = Pipeline([
    ('scaler', MinMaxScaler()),
    ('regressor', RandomForestRegressor(
        n_estimators=100, 
        max_depth=5, 
        min_samples_leaf=10,
        max_features='log2',   
        random_state=42
    ))
])

# Train the entire pipeline
yield_pipeline.fit(X_train, y_train)

# ==========================================
# 3. EVALUATION
# ==========================================
train_r2 = yield_pipeline.score(X_train, y_train)
test_r2 = yield_pipeline.score(X_test, y_test)
y_pred = yield_pipeline.predict(X_test)

print("--- Pipeline Performance ---")
print(f"Train R2: {train_r2:.4f}")
print(f"Test R2: {test_r2:.4f}")
print(f"MAE: {mean_absolute_error(y_test, y_pred):,.2f} hg/ha")

# ==========================================
# 4. SAVE EVERYTHING AS ONE FILE
# ==========================================
# We attach the feature names to the pipeline object so it's truly self-contained
yield_pipeline.feature_names = X.columns.tolist()

joblib.dump(yield_pipeline, 'india_crop_yield_model.pkl')
print("\nSuccess: Single pipeline file 'india_crop_yield_model.pkl' has been saved.")


# ==========================================
# 5. INFERENCE FUNCTION (How to use it)
# ==========================================
def predict_yield_simple(crop_name, rain, pesticide, temp):
    """
    Takes raw inputs and returns a yield prediction using the single pipeline file.
    """
    # Load the single pipeline object
    model = joblib.load('india_crop_yield_model.pkl')
    
    # Create a blank row with all 0s based on the features the model learned
    input_df = pd.DataFrame(0, index=[0], columns=model.feature_names)
    
    # Fill in numerical data
    input_df['average_rain_fall_mm_per_year'] = rain
    input_df['pesticides_tonnes'] = pesticide
    input_df['avg_temp'] = temp
    
    # Set the specific crop to 1 (One-Hot Encoding)
    crop_col = f'Crop_{crop_name}'
    if crop_col in input_df.columns:
        input_df[crop_col] = 1
    else:
        return f"Error: Crop '{crop_name}' was not found in the training data."

    # Predict (Scaling happens automatically inside the pipeline!)
    prediction = model.predict(input_df)[0]
    return prediction

# --- Example Usage ---
example_crop = 'Rice, paddy'
predicted_val = predict_yield_simple(example_crop, 1100, 45000, 26.0)
print(f"\nExample Prediction for {example_crop}: {predicted_val:,.2f} hg/ha")