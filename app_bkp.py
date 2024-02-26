import asyncio
import os  
import json  
import logging  
import openai  
import nest_asyncio  
from llama_index.core import VectorStoreIndex  
from azure.search.documents.models import VectorizableTextQuery
from llama_index.core.response.notebook_utils import (  
    display_source_node,  
    display_response,  
)  
from llama_index.llms.azure_openai import AzureOpenAI  
from azure.core.credentials import AzureKeyCredential  
from llama_index.core.schema import MetadataMode  
from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding  
from llama_index.vector_stores.azureaisearch import AzureAISearchVectorStore  
from llama_index.vector_stores.azureaisearch import (  
    IndexManagement,  
    MetadataIndexFieldType,  
)  
from azure.search.documents import SearchClient  
from azure.search.documents.indexes import SearchIndexClient  
from llama_index.core.settings import Settings  
from llama_index.core import StorageContext  
from llama_index.core import StorageContext  
from llama_index.core import load_index_from_storage 
from azure.search.documents.models import (
    QueryType,
    QueryCaptionType,
    QueryAnswerType
)
from flask import Flask, request, Response 
from flask import stream_with_context
import flask_cors
  
# initialize the Flask application  
app = Flask(__name__)  
flask_cors.CORS(app)

aoai_api_key = "2841bd672d9147288f5ba44124ea37bd"
aoai_endpoint = "https://singhealth-openai-02.openai.azure.com/"
aoai_api_version = "2023-05-15"
search_service_api_key = "jRDIXrlY5KlhPn8plXhkJzh1ZcP0qATM0SLWDaXwFcAzSeDmMcSa"
search_service_endpoint = "https://shschat.search.windows.net"
search_service_api_version = "2023-11-01"
credential = AzureKeyCredential(search_service_api_key)
index_name = "health-vector-03"

llm = AzureOpenAI(
    model="gpt-35-turbo",
    deployment_name="gpt35",
    api_key=aoai_api_key,
    azure_endpoint=aoai_endpoint,
    api_version=aoai_api_version,
    max_tokens=1000,
)

llm_f = AzureOpenAI(
    model="gpt-4",
    deployment_name="gpt4v",
    api_key=aoai_api_key,
    azure_endpoint=aoai_endpoint,
    api_version=aoai_api_version,
    max_tokens=2000,
    streaming=True,
)

embed_model = AzureOpenAIEmbedding(
    model="text-embedding-ada-002",
    deployment_name="text-embedding-ada-002",
    api_key=aoai_api_key,
    azure_endpoint=aoai_endpoint,
    api_version=aoai_api_version,
)

# Use index client to demonstrate creating an index
index_client = SearchIndexClient(
    endpoint=search_service_endpoint,
    credential=credential,
)

# Use search client to demonstration using existing index
search_client = SearchClient(
    endpoint=search_service_endpoint,
    index_name=index_name,
    credential=credential,
    semantic_configuration_name="mySemanticConfig",
    QueryType=QueryType.SEMANTIC,
    query_caption=QueryCaptionType.EXTRACTIVE,
    query_answer=QueryAnswerType.EXTRACTIVE,
)

metadata_fields = {  
    "page_label": ("page_label", MetadataIndexFieldType.STRING),  
    "file_name": ("file_name", MetadataIndexFieldType.STRING),  
    "file_path": ("file_path", MetadataIndexFieldType.STRING),  
    "file_type": ("file_type", MetadataIndexFieldType.STRING),  
    "file_size": ("file_size", MetadataIndexFieldType.INT64),  
    "prev_section_summary": ("prev_section_summary", MetadataIndexFieldType.STRING),  
    "next_section_summary": ("next_section_summary", MetadataIndexFieldType.STRING),  
    "section_summary": ("section_summary", MetadataIndexFieldType.STRING),  
    "questions_this_excerpt_can_answer": ("questions_this_excerpt_can_answer", MetadataIndexFieldType.STRING),  
    "excerpt": ("excerpt",MetadataIndexFieldType.STRING )  
}  

vector_store = AzureAISearchVectorStore(
    search_or_index_client=index_client,
    filterable_metadata_field_keys=metadata_fields,
    index_name=index_name,
    index_management=IndexManagement.CREATE_IF_NOT_EXISTS,
    id_field_key="id",
    chunk_field_key="chunk",
    embedding_field_key="embedding",
    embedding_dimensionality=1536,
    metadata_string_field_key="metadata",
    doc_id_field_key="doc_id",
    language_analyzer="en.lucene",
    vector_algorithm_type="exhaustiveKnn",
    search_client=search_client,
)

storage_context = StorageContext.from_defaults(vector_store=vector_store)

Settings.llm = llm_f
Settings.embed_model = embed_model


index0 = VectorStoreIndex([],storage_context=storage_context )
index0.storage_context.persist()

index3 = load_index_from_storage(storage_context)
query_engine2 = index3.as_query_engine(streaming=True,similarity_top_k=2)
query_engine1 = index3.as_query_engine(streaming=True,similarity_top_k=2)

async def astreamer(generator):
    try:
        for i in generator:
            yield (i)
            await asyncio.sleep(.1)
    except asyncio.CancelledError as e:
        
        print('cancelled')
  
@app.route('/llama_search', methods=['POST'])  
def llama_search():  
    try:  
        # Parse the request body to get the query  
        req_body = request.get_json()  
        query = req_body.get('query')  
  
        if not query:  
            return Response("Please pass a query in the request body", status=400)  
  
        response_1 = query_engine1.query(query)  
  
     #   def generate_response():
     #       for text in response_1.response_gen:
     #           yield f"data: {text}\n\n" 
    
  
    except Exception as e:  
        return Response(str(e), status=500)
    
    return Response(stream_with_context(astreamer(response_1.response_gen)), mimetype='text/event-stream') 

# Run Server
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)

