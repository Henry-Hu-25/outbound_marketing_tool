from pinecone_text.sparse import BM25Encoder

class BM25ModelWrapper:
    def __init__(self):
        """Initialize BM25 encoder"""
        self.bm25 = BM25Encoder()
    
    def fit(self, descriptions):
        """Fit BM25 encoder on text descriptions"""
        self.bm25.fit(descriptions)
    
    def encode_documents(self, description):
        """Get sparse embeddings for text descriptions"""
        return self.bm25.encode_documents(description)
    
    def encode_queries(self, query):
        """Get sparse embeddings for queries"""
        return self.bm25.encode_queries(query) 