import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.utils import input_image_setup
import streamlit as st
from src.logger import logging
from PIL import Image
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_vertexai import ChatVertexAI
import google.generativeai as genai
import vertexai
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
import google.ai.generativelanguage as glm
import pathlib


load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

vertexai.init(project='gen-lang-client-0528981480')

#os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
#loading json file

with open('Response.json', 'r') as file:
    RESPONSE_JSON = json.load(file)

#creating a title for the app
st.title("First Aid Assitance ⛑️")

#Create a form using st.form
with st.form("user_inputs"):
    #File Upload
    uploaded_file=st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    image=""
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image.', use_column_width=True)
    #description
    description=st.text_input("Descride the situation",max_chars=600)

    #Add Button
    button=st.form_submit_button("Generate response")


prompt =""""
You are a dedicated and compassionate first-aid professional with years of experience in emergency medicine. \
You have a strong commitment to saving lives and ensuring the well-being of those in need. You have an advanced degree in emergency medicine. \
Your expertise spans from basic first aid techniques to advanced life support procedures.In high-pressure situations, you remain level-headed and thinks on your feet. \
Your ability to assess and prioritize critical cases is unmatched.Your meticulous attention to detail ensures accurate diagnoses and effective treatment.\
Given an image {image} and {description} of an emergency situation, you must provide a detailed response outlining the steps you would take to address the situation that will allow any individual to help the causalty.\
Your response should include an assessment of the patient's condition, and a plan of action to provide immediate care(in chronological order to follow), this should be communicated in a clear and concise manner.\
### RESPONSE_JSON
{response_json}

"""

model = genai.GenerativeModel('gemini-pro-vision')


    # Check if the button is clicked and all fields have input

if button and uploaded_file is not None and description:
        with st.spinner("loading..."):
            try:
                Image_data=input_image_setup(uploaded_file)
                prompt = prompt

                response = model.generate_content(
                    [prompt, Image_data, description, RESPONSE_JSON]
                )
                st.write(response)

            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)
                st.error("Error")



