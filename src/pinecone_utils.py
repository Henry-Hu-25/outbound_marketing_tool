import os
from pinecone import Pinecone, ServerlessSpec

def setup_pinecone_index():
    """Set up Pinecone index"""
    pc = Pinecone()
    index_name = os.getenv("INDEX_NAME")
    index_list = {index.name for index in pc.list_indexes()}

    if index_name not in index_list:
        pc.create_index(
            name=index_name,
            dimension=512,  # Replace with your model dimensions
            metric="dotproduct",  # Replace with your model metric
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            )
        )
    else:
        index = pc.Index(index_name)
        dimension = index.describe_index_stats()["dimension"]
        if dimension != 512:
            pc.delete_index(index_name)
            pc.create_index(
                name=index_name,
                dimension=512,  # Replace with your model dimensions
                metric="dotproduct",  # Replace with your model metric
                spec=ServerlessSpec(
                    cloud="aws",
                    region="us-east-1"
                )
            )
    
    return pc.Index(index_name)

def upsert_inventory_to_pinecone(index, inventory_df, clip_model, bm25_model):
    """Upsert inventory data to Pinecone index"""
    for _, row in inventory_df.iterrows():
        # Extracting Elements
        image_id = row["style"]
        image_path = row["Image"]
        image_description = row["Description"]

        # Image Embedding
        dense_embeds = clip_model.get_image_embedding(image_path).squeeze(0).tolist()

        # Text Embedding
        sparse_embeds = bm25_model.encode_documents(image_description)
        
        # Get metadata
        metadata = row.to_dict()
        if index.fetch([image_id])['vectors']:
            print(f"ID {image_id} already exists in the database. Skipping upsert.")
            continue
        else:
            index.upsert([{
                'id': image_id,
                'sparse_values': sparse_embeds,
                'values': dense_embeds,
                'metadata': metadata
            }]) 