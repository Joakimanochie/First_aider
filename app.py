import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.utils import input_image_setup
import streamlit as st
from src.Datagenerator import response_chain
from src.logger import logging

#loading json file

with open('Response.json', 'r') as file:
    RESPONSE_JSON = json.load(file)

#creating a title for the app
st.title("First Aid Assitance ⛑️")

#Create a form using st.form
with st.form("user_inputs"):
    #File Upload
    uploaded_file=st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    
    #description
    description=st.text_input("Descride the situation",max_chars=600)

    #Add Button
    button=st.form_submit_button("Generate response")

    # Check if the button is clicked and all fields have input

    if button and uploaded_file is not None and description:
        with st.spinner("loading..."):
            try:
                Image_data=input_image_setup(uploaded_file)
                response=response_chain(
                        {
                        "image": uploaded_file,
                        "description": description,
                        "response_json": json.dumps(RESPONSE_JSON)
                            }
                    )
                st.write(response)

            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)
                st.error("Error")



