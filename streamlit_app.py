import streamlit as st
import requests

# Title of the Streamlit app
st.title("CO2 Emission Estimator")

# Input: Get location from the user
location = st.text_input("Enter Location:")

if st.button("Predict CO2 Emissions") and location:
    try:
        # Send POST request to the Flask API (using 127.0.0.1 to ensure it's using localhost correctly)
        response = requests.post('http://127.0.0.1:5001/predict', json={'location': location})  # Use 127.0.0.1 instead of localhost
        
        

        # Check if the request was successful
        if response.status_code == 200:
            prediction_data = response.json()  # Parse the JSON response
            
            # Display the prediction results
            st.write(f"Location: {location}")
            st.write(f"Estimated CO2 Emissions: {prediction_data['co2_emission']} g")
            st.write(f"Temperature: {prediction_data['temperature']} °C")
            st.write(f"Humidity: {prediction_data['humidity']} %")
        else:
            st.error(f"Error: Unable to get predictions from the API. Status code: {response.status_code}")
    
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to get predictions due to a request exception: {e}")
        st.write("Detailed Exception: ", e)  # This will display the full exception for debugging
