from dotenv import load_dotenv

load_dotenv() ## load all the environment variables

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image
from google.generativeai.types import HarmCategory, HarmBlockThreshold


os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

## Function to load Google Gemini Pro Vision API And get response

def get_gemini_repsonse(input,image,prompt):
    model=genai.GenerativeModel('gemini-pro-vision')
    response=model.generate_content([input,image[0],prompt], safety_settings={HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                                                                               HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE, 
                                                                                 HarmCategory.HARM_CATEGORY_MEDICAL: HarmBlockThreshold.BLOCK_NONE,
                                                                                 HarmCategory.HARM_CATEGORY_VIOLENCE: HarmBlockThreshold.BLOCK_NONE})
    return response.text

def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")
    
##initialize our streamlit app

st.set_page_config(page_title="First Aid Assitance ⛑️")

st.header("First Aid Assitance ⛑️")
input=st.text_input("Descride incident: ",key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image=""   
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)


submit=st.button("Generate response")

input_prompt="""
You are a dedicated and compassionate first-aid professional with years of experience in emergency medicine. \
You have a strong commitment to saving lives and ensuring the well-being of those in need. You have an advanced degree in emergency medicine. \
Your expertise spans from basic first aid techniques to advanced life support procedures.In high-pressure situations, you remain level-headed and thinks on your feet. \
Your ability to assess and prioritize critical cases is unmatched.Your meticulous attention to detail ensures accurate diagnoses and effective treatment.\
Given an image {image} and {description} of an emergency situation, you must provide a detailed response outlining the steps you would take to address the situation that will allow any individual to help the causalty.\
Your response should include an assessment of the patient's condition, and a plan of action to provide immediate care(in chronological order to follow), this should be communicated in a clear and concise manner.\
follow this format
              Assessment: Assessment of the patient's condition goes here
              Steps to take: Plan of action to provide immediate care 
               1. Step 1
               2. Step 2
               ----
               ----


"""

## If submit button is clicked

if submit:
    image_data=input_image_setup(uploaded_file)
    response=get_gemini_repsonse(input_prompt,image_data,input)

    st.subheader("Response ")
    st.write(response)

