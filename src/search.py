def hybrid_scale(sparse, dense, style_similarity=1):
    """
    Hybrid vector scaling with alpha * dense + (1 - alpha) * sparse

    Args:
      - dense: array of floats
      - sparse: a dict of indices and values
      - alpha: 0 = sparse only, 1 = dense only
    """
    if style_similarity < 0 or style_similarity > 1:
        raise ValueError("Alpha must be between 0 and 1")

    scaled_sparse = {
        "indices": sparse["indices"],
        "values": [
            value * (1 - style_similarity) for value in sparse["values"]
        ]
    }
    scaled_dense = [style_similarity * value for value in dense]
    return scaled_sparse, scaled_dense

def collect_search_results(search_result):
    """
    Collect search results for search visualizations

    Args:
      - search_result: a pinecone query response
    
    Return:
      - a list of style names
      - a list of image paths
      - a list of composition descriptions
    """
    style_names = []
    image_paths = []
    composition_desc = []

    for match in search_result.matches:
        style_names.append(match["id"])
        image_paths.append(match["metadata"]["Image"])
        composition_desc.append(match['metadata']['Description'])
    
    return style_names, image_paths, composition_desc

def search_by_fabric(index, sparse, dense, top_k=3):
    """Search by fabric composition"""
    scaled_sparse, scaled_dense = hybrid_scale(sparse, dense, 0)
    
    result = index.query(
        top_k=top_k,
        vector=scaled_dense,
        sparse_vector=scaled_sparse,
        include_metadata=True
    )
    
    return result

def search_by_likeliness(index, sparse, dense, top_k=3):
    """Search by overall likeliness"""
    scaled_sparse, scaled_dense = hybrid_scale(sparse, dense)
    
    result = index.query(
        top_k=top_k,
        vector=scaled_dense,
        sparse_vector=scaled_sparse,
        include_metadata=True
    )
    
    return result 