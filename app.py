from flask import Flask, request, jsonify
import pickle
import pandas as pd
import numpy as np

app = Flask(__name__)

# Load the trained model from the pickle file
with open('model.pkl', 'rb') as file:
    model = pickle.load(file)
    if not hasattr(model, 'predict'):
        raise ValueError("The loaded object is not a valid model, it doesn't have a 'predict' method.")

# Load the environmental data from CSV (replace with your actual CSV path)
data = pd.read_csv('Airquality.csv')  # Replace with the path to your CSV file

@app.route('/')
def home():
    return "Welcome to the CO2 Emission Predictor API! Use the /predict endpoint to get predictions."

@app.route('/predict', methods=['POST'])
def predict():
    # Get the location from the request
    location = request.json.get('location')

    # Filter the data for the requested location
    location_data = data[data['Area'] == location]

    if location_data.empty:
        return jsonify({"error": "Location not found"})

    # Extract the relevant features for the model (assuming these columns are in your CSV)
    features = location_data[[
        'AQI US', 'PM 2.5', 'PM 10', 'SO2', 'Ozone', 'CO', 'NO2', 'TEMPERATURE', 'HUMIDITY'
    ]].values  # Get the features as a NumPy array (no need for the extra [0] here)

    # Convert the NumPy array into a DataFrame to retain column names
    features_df = pd.DataFrame(features, columns=[
        'AQI US', 'PM 2.5', 'PM 10', 'SO2', 'Ozone', 'CO', 'NO2', 'TEMPERATURE', 'HUMIDITY'
    ])

    # Use the model to make predictions
    try:
        prediction = model.predict(features_df)  # This will return a single prediction

        # You can modify this if your model outputs more than one value
        co2_emission = prediction[0]  # Assuming the first value is CO2 emission

        # Ensure that the result is serializable by converting any numpy types to regular Python types
        co2_emission = int(co2_emission)  # Convert from numpy.int64 to native Python int

        # Return the prediction results as JSON
        return jsonify({
            'co2_emission': co2_emission,
            'temperature': int(features_df['TEMPERATURE'].iloc[0]),  # Convert from numpy.int64 to int
            'humidity': int(features_df['HUMIDITY'].iloc[0])         # Convert from numpy.int64 to int
        })
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True, use_reloader=False)
