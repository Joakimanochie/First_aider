import os
import traceback
from dotenv import load_dotenv
from src.utils import get_data
from src.utils import logging


from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import LLMChain  
from langchain.chains import SequentialChain


load_dotenv()

key=os.getenv("Mykey")

llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=key)


template = """"


"""