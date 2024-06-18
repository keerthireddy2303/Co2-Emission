import streamlit as st
import requests

st.title("CO2 Emission Estimator")

location = st.text_input("Enter Location:")

if st.button("Predict CO2 Emissions"):
    if location:
        try:
            response = requests.post('http://localhost:5000/predict', json={'location': location})
            data = response.json()
            st.write(f"Location: {data['Area']}")
            st.write(f"Estimated CO2 Emissions: {data['co2_emissions']:.2f}")
        except requests.exceptions.RequestException as e:
            st.error(f"Failed to get predictions due to a request exception: {e}")
    else:
        st.write("Please enter a valid location.")