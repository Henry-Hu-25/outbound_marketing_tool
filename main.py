import os
import argparse
import logging
from src.config import load_environment, print_environment_variables
from src.web_scraping import load_web_content, extract_product_info, extract_client_info
from src.data_processing import load_inventory_data, process_inventory_data
from src.models.clip_model import CLIPModelWrapper
from src.models.bm25_model import BM25ModelWrapper
from src.pinecone_utils import setup_pinecone_index, upsert_inventory_to_pinecone
from src.search import search_by_fabric, search_by_likeliness, collect_search_results
from src.visualization import show_matched_images
from src.email_generator import generate_sales_email
from src.evaluation import setup_evaluation_dataset, evaluate_email
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq

# Set up logging
logger = logging.getLogger(__name__)

def main(product_url=None, client_url=None, quiet=True):
    """
    Main function to generate sales email based on product and client URLs
    
    Args:
        product_url: URL for the product page
        client_url: URL for the client's page
        quiet: If True, suppresses most print output for API usage
    
    Returns:
        The generated email content
    """
    # Load environment variables
    load_environment()
    if not quiet:
        print_environment_variables()
    
    # Configure the model
    model_name = os.getenv("GROQ_MODEL_NAME_1")
    if not quiet:
        print(f"Using model: {model_name}")
    
    # Test LLM connections (only in verbose mode)
    if not quiet:
        print("Testing OpenAI connection...")
        llm_openai = ChatOpenAI()
        response_openai = llm_openai.invoke("Hello, world!")
        print(response_openai)
        
        print("Testing Groq connection...")
        llm_groq = ChatGroq(
            temperature=0,
            model_name=model_name
        )
        response_groq = llm_groq.invoke("Hello, world!")
        print(response_groq)
    
    # Web scraping
    if not quiet:
        print("Scraping product data...")
    if not product_url:
        product_url = "https://www.dudalina.com.br/blazer-de-veludo-com-bolsos-dudalina-masculino-cinza-medio-21-13-0108/p?skuId=16968"
    page_data_product = load_web_content(product_url)
    json_res_product = extract_product_info(page_data_product)
    if not quiet:
        print(json_res_product)
    
    if not quiet:
        print("Scraping client data...")
    if not client_url:
        client_url = "https://www.dudalina.com.br/quem-somos"
    page_data_client = load_web_content(client_url)
    json_res_client = extract_client_info(page_data_client)
    if not quiet:
        print(json_res_client)
    
    # Data processing
    print("Processing inventory data...")
    inventory_df = load_inventory_data("./images/test_image.csv")
    inventory_df = process_inventory_data(inventory_df)
    print(inventory_df.head())
    
    # Initialize models
    print("Initializing models...")
    clip_model = CLIPModelWrapper()
    bm25_model = BM25ModelWrapper()
    bm25_model.fit(inventory_df['Description'])
    
    # Setup Pinecone
    print("Setting up Pinecone...")
    index = setup_pinecone_index()
    print(index.describe_index_stats())
    
    # Upsert inventory to Pinecone
    print("Upserting inventory to Pinecone...")
    upsert_inventory_to_pinecone(index, inventory_df, clip_model, bm25_model)
    
    # Search
    print("Performing search...")
    query = f"Fabric: {json_res_product['fabric composition']}; Description: {json_res_product['garment description']}"
    print(f"Search query: {query}")
    
    sparse = bm25_model.encode_queries(query)
    dense = clip_model.get_text_embedding(query).squeeze(0).tolist()
    
    # Search by fabric
    print("Searching by fabric...")
    fabric_search_result = search_by_fabric(index, sparse, dense)
    style_names_fabric, image_paths_fabric, composition_desc_fabric = collect_search_results(fabric_search_result)
    print(style_names_fabric)
    
    # Search by likeliness
    print("Searching by likeliness...")
    likeliness_search_result = search_by_likeliness(index, sparse, dense)
    style_names_likeliness, image_paths_likeliness, composition_desc_likeliness = collect_search_results(likeliness_search_result)
    print(style_names_likeliness)
    
    # Visualization
    # print("Visualizing search results...")
    # show_matched_images(style_names_fabric, image_paths_fabric, composition_desc_fabric)
    # show_matched_images(style_names_likeliness, image_paths_likeliness, composition_desc_likeliness)
    
    # Email generation
    print("Generating sales email...")
    company_description = '''
    ### About Us:

    AIRRY GARMENTS CO., LTD. is a seasoned garment manufacturer. The company specializes in producing high-quality men's and ladies' suits, blazers, trousers, jackets, coats, and overcoats.

    Most of AIRRY's production is destined for European department stores and boutiques, but for the past ten years, AIRRY has supplied designer garments for North and South American clients, replacing their European suppliers with compelling price points and state-of-the-art production and supply chain management capabilities.

    AIRRY has one owned factory and two contracted factories with over 1,000 total staff, offering economy of scale and flexibility in production quantity.

    ### Our Differentiations:

    AIRRY is an experienced client-centric garment supplier whose passion for fashion aesthetics runs deep.

    We develop trendy new samples every season. Our innovative fabric, colorway and design often provide inspiration to our clients. Our team members possess a sense of style and can offer our clients design support and industry insights when needed.

    Unlike most clothing suppliers with a strict minimum order quantity, AIRRY offers quantity flexibility and welcomes special detail or craftsmanship requests. Our manufacturing and supply chain management capabilities can make your design a reality.

    ## Key Competitive Advantages:

    1. 120+ Years of Experience We have specialized in garment production for over two decades and have partnered with clients worldwide.

    2. Best Value via Supply Chain Advantage We can get the best prices from fabric and accessory suppliers offering the highest quality goods to deliver maximum value to clients.

    3. Comprehensive R&D Capabilities We develop new styles to add to our huge showroom collection every season and show them to our clients. Also, we can quickly fulfill clients' patterns, materials, and sample creation requests.

    4. Unmatched Flexibility We accept order quantities from 100 to 10,000+ pieces per style and welcome requests for special garment details.

    5. Piece-by-Piece Inspection Before shipments, our dedicated and well-trained Quality Control team inspects every piece of the finished goods.
    '''
    
    email_content = generate_sales_email(
        company_description,
        json_res_client,
        json_res_product,
        style_names_likeliness,
        composition_desc_likeliness
    )
    print(email_content)
    
    # Evaluation
    print("Setting up evaluation...")
    dataset_name = setup_evaluation_dataset(email_content)
    
    print("Evaluating email...")
    evaluation_results = evaluate_email(dataset_name)
    print(evaluation_results)
    
    print("Process completed successfully!")
    
    # Return the generated email for the API
    return email_content

if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Generate a sales email based on product and client information.')
    parser.add_argument('--product_url', type=str, help='URL of the product page')
    parser.add_argument('--client_url', type=str, help='URL of the client about us page')
    
    args = parser.parse_args()
    
    email = main(product_url=args.product_url, client_url=args.client_url)
    
    # Print only the email content for the API to capture
    print("\n--- GENERATED EMAIL ---\n")
    print(email) 