from langchain_groq import ChatGroq
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
import os

def load_web_content(url):
    """Load content from a web page"""
    loader = WebBaseLoader(url)
    page_data = (loader.load().pop().page_content).strip()
    return page_data

def extract_product_info(page_data):
    """Extract product information from web page content"""
    prompt_extract_product = PromptTemplate.from_template(
        '''
        ### SCRAPED TEXT FROM WEBSITE:
        {page_data_product}


        ### INSTRUCTION:
        The scraped text is from a retailer's online store.

        1. You will first translate the web content into English.
        2. You will then extract the key product information and 
        return them in JSON format containing the following keys: 
        'brand', 'fabric composition', 'garment description'.
        Only return the valid JSON.


        ### VALID JSON (NO PREAMBLE): Do not include anything else in the response—no extra text, no explanations. If you need to provide explanations, put them as JSON fields within the JSON object.
        '''
    )
    
    llm_groq = ChatGroq(
        temperature=0,
        model_name=os.getenv("GROQ_MODEL_NAME_1")
    )
    
    chain_product = prompt_extract_product | llm_groq
    res_product = chain_product.invoke(input={'page_data_product': page_data})
    
    json_parser = JsonOutputParser()
    json_res_product = json_parser.parse(res_product.content)
    
    return json_res_product

def extract_client_info(page_data):
    """Extract client information from web page content"""
    prompt_extract_client = PromptTemplate.from_template(
        '''
        ### SCRAPED TEXT FROM WEBSITE:
        {page_data_client}

        ### INSTRUCTION:
        The scraped text the about section of a company's website.
        The company is a potential client. 

        1. You will first translate the web content into English.

        ### VALID JSON (NO PREAMBLE): Do not include anything else in the response—no extra text, no explanations. If you need to provide explanations, put them as JSON fields within the JSON object.
        '''
    )
    
    llm_groq = ChatGroq(
        temperature=0,
        model_name=os.getenv("GROQ_MODEL_NAME_1")
    )
    
    chain_client = prompt_extract_client | llm_groq
    res_client = chain_client.invoke(input={'page_data_client': page_data})
    
    json_parser = JsonOutputParser()
    json_res_client = json_parser.parse(res_client.content)
    
    return json_res_client 