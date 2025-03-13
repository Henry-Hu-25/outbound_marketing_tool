from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
import os
import logging

logger = logging.getLogger(__name__)

def generate_sales_email(company_description, client_info, sample_products, popular_styles, fabrics_descriptions, quiet=True):
    """Generate a sales email based on client and product information"""
    prompt_email = PromptTemplate.from_template(
        '''
        ### INSTRUCTION:
        You are a business development executive at Airry Garments., LTD. Your job is to write a cold email to a prospective client.

        ### DESCRIPTION ABOUT AIRRY GARMENTS:
        {company_description}

        ### INFORMATION ABOUT THE CLIENT:
        {client_info}

        ### SAMPLE CLIENT PRODUCTS:
        {sample_products}

        ### RELEVANT PRODUCTS MATCHING CLIENT'S NEEDS:
        {popular_styles}
        Here are addtional information about the fabrics (OPTIONAL MENTION): 
        {fabrics_descriptions}

        ### IMPORTANT RULES:
        1. BE CONCISE
        2. INCLUDE A CALL TO ACTION (PROPOSE TO SEND CATALOGS AND SAMPLES)
        3. CUSTOMIZE THE MESSAGE TO THE CLIENT

        ### EMAIL (NO PREAMBLE):
        '''
    )
    
    # Use the model specified in environment variables
    model_name = os.getenv("GROQ_MODEL_NAME_1")
    
    if not quiet:
        logger.info(f"Using model: {model_name}")
    
    llm_groq = ChatGroq(
        temperature=0,
        model_name=model_name
    )
    
    chain_email = prompt_email | llm_groq
    
    if not quiet:
        logger.info("Generating email...")
        
    response = chain_email.invoke({
        "company_description": company_description,
        "client_info": client_info,
        "sample_products": sample_products,
        "popular_styles": str(popular_styles),
        "fabrics_descriptions": str(fabrics_descriptions)
    })
    
    if not quiet and hasattr(response, 'response_metadata') and response.response_metadata:
        logger.info(f"Email generated using model: {response.response_metadata.get('model_name', model_name)}")
    
    return response.content 