from flask import Flask, request, Response  
import json  
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
import flask_cors  
  
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
    stream=True,  
)  
  
embed_model = AzureOpenAIEmbedding(  
    model="text-embedding-ada-002",  
    deployment_name="text-embedding-ada-002",  
    api_key=aoai_api_key,  
    azure_endpoint=aoai_endpoint,  
    api_version=aoai_api_version,  
)  
  
index_client = SearchIndexClient(  
    endpoint=search_service_endpoint,  
    credential=credential,  
)  
  
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
    "excerpt": ("excerpt", MetadataIndexFieldType.STRING)  
}  
  
vector_store = AzureAISearchVectorStore(  
    search_or_index_client=index_client,  
    filterable_metadata_field_keys=metadata_fields,  
    index_name="health-vector-03",  
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
  
index0 = VectorStoreIndex([], storage_context=storage_context)  
#index0.storage_context.persist()  
  
index3 = load_index_from_storage(storage_context)  
#query_engine2 = index3.as_query_engine(streaming=True, similarity_top_k=2)  
query_engine1 = index3.as_query_engine(streaming=True, similarity_top_k=2)  


#Defining vector store and index for Digital book
vector_store_01 = AzureAISearchVectorStore(  
    search_or_index_client=index_client,  
    filterable_metadata_field_keys=metadata_fields,  
    index_name="book-vector-01",  
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
  
storage_context_01 = StorageContext.from_defaults(vector_store=vector_store_01)  
  
Settings.llm = llm_f  
Settings.embed_model = embed_model  
  
index_01 = VectorStoreIndex([], storage_context=storage_context_01)  
#index0.storage_context.persist()  
  
index_03 = load_index_from_storage(storage_context_01)  
#query_engine2 = index3.as_query_engine(streaming=True, similarity_top_k=2)  
query_engine2 = index_03.as_query_engine(streaming=True, similarity_top_k=2) 
  
  
@app.route('/llama_search', methods=['POST'])  
def llama_search():  
    try: 
         
        req_body = request.json  
        query = req_body.get('query')  
  
        if not query:  
            return {"message": "Please pass a query in the request body"}, 400  
  
        response_1 = query_engine1.query(query)  
        metadata_1 = response_1.source_nodes[1].metadata  
        metadata_2 = response_1.source_nodes[0].metadata  
        page_label_1 = metadata_1.get("page_label")  
        page_label_2 = metadata_2.get("page_label")  
        file_name_1 = metadata_1.get("file_name")  
        file_name_2 = metadata_2.get("file_name")  
        content_text_1 = response_1.source_nodes[1].text 
        content_text_2 = response_1.source_nodes[0].text  
  
        def responseStream():  
            for i in response_1.response_gen:  
                # yield str(i).encode('utf-8') 
                yield str(i).encode('utf-8')      
            # Add metadata values to the response stream  
            yield f"\npage_label_1: {page_label_1}".encode('utf-8')  
            yield f"\npage_label_2: {page_label_2}".encode('utf-8')  
            yield f"\nfile_name_1: {file_name_1}".encode('utf-8')  
            yield f"\nfile_name_2: {file_name_2}".encode('utf-8')  
            yield f"\ncontent_text_1: {content_text_1}".encode('utf-8')  
            yield f"\ncontent_text_2: {content_text_2}".encode('utf-8')  
  
        return Response(responseStream() , mimetype="text/event-stream")  
  
    except ValueError as e:  
        return {"message": str(e)}, 400  
    except Exception as e:  
        return {"message": "An error occurred: " + str(e)}, 500  
    
@app.route('/llama_search_01', methods=['POST'])  
def llama_search_01():  
    try: 
         
        req_body = request.json  
        query = req_body.get('query')  
  
        if not query:  
            return {"message": "Please pass a query in the request body"}, 400  
  
        response_1 = query_engine2.query(query)  
        metadata_1 = response_1.source_nodes[1].metadata  
        metadata_2 = response_1.source_nodes[0].metadata  
        page_label_1 = metadata_1.get("page_label")  
        page_label_2 = metadata_2.get("page_label")  
        file_name_1 = metadata_1.get("file_name")  
        file_name_2 = metadata_2.get("file_name")  
        content_text_1 = response_1.source_nodes[1].text 
        content_text_2 = response_1.source_nodes[0].text  
  
        def responseStream():  
            for i in response_1.response_gen:  
                # yield str(i).encode('utf-8') 
                yield str(i).encode('utf-8')      
            # Add metadata values to the response stream  
            yield f"\npage_label_1: {page_label_1}".encode('utf-8')  
            yield f"\npage_label_2: {page_label_2}".encode('utf-8')  
            yield f"\nfile_name_1: {file_name_1}".encode('utf-8')  
            yield f"\nfile_name_2: {file_name_2}".encode('utf-8')  
            yield f"\ncontent_text_1: {content_text_1}".encode('utf-8')  
            yield f"\ncontent_text_2: {content_text_2}".encode('utf-8')  
  
        return Response(responseStream() , mimetype="text/event-stream")  
  
    except ValueError as e:  
        return {"message": str(e)}, 400  
    except Exception as e:  
        return {"message": "An error occurred: " + str(e)}, 500      
  
  
if __name__ == '__main__':  
    app.run(host="0.0.0.0", port=8000)  
