import streamlit as st
import pandas as pd
import joblib
import base64
import os
import streamlit.components.v1 as components

# Set Streamlit page config
st.set_page_config(
    page_title="Delhi House Price Predictor",
    page_icon="🏡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Load trained model
model = joblib.load("best_model.pkl")

# Background image embedding function
def set_background(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
            st.markdown(
                f"""
                <style>
                .stApp {{
                    background-image: url("data:image/jpg;base64,{encoded_string}");
                    background-size: cover;
                    background-attachment: fixed;
                }}
                </style>
                """,
                unsafe_allow_html=True
            )

# Set background
set_background("bg.jpg")

# Logo and Title Container
st.markdown("""
<div style="background-color: white; border-radius: 10px; padding: 10px 20px; margin-top: -15px;
            display: flex; align-items: center; justify-content: center;
            box-shadow: 0 3px 10px rgba(0,0,0,0.1);">
    <img src="data:image/png;base64,{}" width="100" style="margin-right: 15px;">
    <h3 style="color: #222; margin: 0;">Delhi House Price Predictor</h3>
</div>
""".format(
    base64.b64encode(open("logo.png", "rb").read()).decode()
), unsafe_allow_html=True)

st.markdown("<hr style='border-top: 1px #eeeeee;'>", unsafe_allow_html=True)

# Input Form with two columns
with st.container():
    with st.form("prediction_form"):

        col1, col2 = st.columns(2)

        with col1:
            area = st.number_input("Area (sqft)", min_value=300, max_value=10000, value=1200)
            locality = st.selectbox("Locality", [
                "Rohini", "Lajpat Nagar", "Chhattarpur", "Karol Bagh", "Okhla", "Hauz Khas",
                "Dilshad Garden", "Safdarjung Enclave", "Malviya Nagar", "Others"
            ])
            bhk = st.selectbox("BHK", [1, 2, 3, 4, 5])
            bathroom = st.selectbox("Bathrooms", [1, 2, 3, 4, 5])

        with col2:
            furnishing = st.selectbox("Furnishing", ["Unfurnished", "Semi Furnished", "Furnished"])
            parking = st.selectbox("Parking Spaces", [0, 1, 2, 3, 4])
            property_type = st.selectbox("Type", ["Builder Floor", "Apartment"])
            status = st.selectbox("Status", ["Ready To Move", "Almost Ready"])

        submitted = st.form_submit_button("🎯 Estimate Price")

# Predict & Show result
if submitted:
    input_df = pd.DataFrame([{
        'Area': area,
        'Locality': locality,
        'BHK': bhk,
        'Bathroom': bathroom,
        'Furnishing': furnishing,
        'Parking': parking,
        'Type': property_type,
        'Status': status
    }])

    price = model.predict(input_df)[0]
    price = max(0, price)

    # Format price to Indian units
    if price >= 1e7:
        formatted_price = f"₹{price / 1e7:.2f} Cr"
    elif price >= 1e5:
        formatted_price = f"₹{price / 1e5:.2f} Lakh"
    elif price >= 1e3:
        formatted_price = f"₹{price / 1e3:.2f} K"
    else:
        formatted_price = f"₹{price:.2f}"

    # Show success message and result in the same area
    with st.container():
        st.success("✅ Prediction complete. You can update values and re-estimate.")

        st.markdown(f"""
        <div style='background-color: #d8ecff; padding: 30px; border-radius: 12px;
                    text-align: center; box-shadow: 0 4px 12px rgba(0,0,0,0.15); margin-top: 20px;'>
            <h3 style="color:#000;">🏷️ Estimated Property Price</h3>
            <h1 style="color:#007bff;">{formatted_price}</h1>
        </div>
        """, unsafe_allow_html=True)

        # Auto-scroll to result
        components.html("""
            <script>
                const el = window.parent.document.querySelector('section.main');
                el.scrollTo({top: el.scrollHeight, behavior: 'smooth'});
            </script>
        """, height=0)

# Footer
st.markdown("<br><hr><p style='text-align: center; color: white;'>🔵 Built with ❤️ using Streamlit</p>", unsafe_allow_html=True)
