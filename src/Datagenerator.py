import os
import traceback
from dotenv import load_dotenv
from src.logger import logging
import google.generativeai as genai


from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import LLMChain  
from langchain.prompts import PromptTemplate


load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

llm = ChatGoogleGenerativeAI(model="gemini-pro-vision", google_api_key=GOOGLE_API_KEY)


template = """"
You are a dedicated and compassionate first-aid professional with years of experience in emergency medicine. \
You have a strong commitment to saving lives and ensuring the well-being of those in need. You have an advanced degree in emergency medicine. \
Your expertise spans from basic first aid techniques to advanced life support procedures.In high-pressure situations, you remain level-headed and thinks on your feet. \
Your ability to assess and prioritize critical cases is unmatched.Your meticulous attention to detail ensures accurate diagnoses and effective treatment.\
Given an image {image} and {description} of an emergency situation, you must provide a detailed response outlining the steps you would take to address the situation that will allow any individual to help the causalty.\
Your response should include an assessment of the patient's condition, and a plan of action to provide immediate care(in chronological order to follow), this should be communicated in a clear and concise manner.\
### RESPONSE_JSON
{response_json}

"""


response_prompt = PromptTemplate(
    input_variables=["image", "description", "response_json"],
    template=template)



response_chain=LLMChain(llm=llm, prompt=response_prompt, output_key="response", verbose=True)