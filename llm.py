# from langchain.chains import RetrievalQA
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from dotenv import load_dotenv
# import os 
# from langchain_community.vectorstores import Neo4jVector
# from langchain_google_genai import GoogleGenerativeAI
# from langchain_google_genai import GoogleGenerativeAIEmbeddings

# # Load environment variables
# load_dotenv(r"C:\Users\shiva\Downloads\BTP_env_variables.env")

# # Get API key and folder paths
# NEO4J_URI = os.getenv('NEO4J_URI')
# NEO4J_USERNAME = os.getenv('NEO4J_USERNAME')
# NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD')
# google_api_key_1 = os.getenv('GOOGLE_API_KEY')

# # User prompt input (you can adjust this to take dynamic input in your app)
# user_prompt = input("Please enter your query: ")

# # Model prompt can be customized based on what context or instruction you want to provide to the model
# model_prompt = (
#     "Answer the following question based on the information provided:\n"
#     "Question: {user_query}\n"
#     "use the relevant information from the retrieved documents."
#     "Do not reply : I cannot answer to this question as it does not contain any information of the Question; Instead try to answer summarize content from the retrieved documents."
# )


# # Initialize Google Generative AI embeddings
# embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

# # Initialize Neo4j vector store from your existing Neo4j graph data
# vector_index = Neo4jVector.from_existing_graph(
#     embeddings,
#     url=NEO4J_URI,
#     username=NEO4J_USERNAME,
#     password=NEO4J_PASSWORD,
#     index_name='retriev_index',  # Replace this with your index name
#     node_label="Section",  # Assuming your nodes are labeled "Section"
#     text_node_properties=['content'],  # Assuming your documents' content is stored in a property called "content"
#     embedding_node_property='embedding',  # The property that stores the embedding vectors
# )

# # Perform a similarity search for the user's query
# retrieved_docs_with_scores = vector_index.similarity_search_with_score(user_prompt, k=1500)

# # Print the retrieved documents for debugging
# # print("Retrieved documents with scores and full content:")
# # for doc, score in retrieved_docs_with_scores:
# #     print(f"Score: {score}, Content: {doc.page_content[:100]}")

# # Split long documents if necessary
# text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)

# retrieved_docs = []
# for doc, score in retrieved_docs_with_scores:
#     chunks = text_splitter.split_text(doc.page_content)  # Split each document into smaller chunks
#     retrieved_docs.extend(chunks)

# # Initialize the Google Generative AI LLM
# llm = GoogleGenerativeAI(model="gemini-pro", google_api_key=google_api_key_1)

# # Set up the RAG pipeline with the user and model prompts
# vector_qa = RetrievalQA.from_chain_type(
#     llm=llm,
#     chain_type="stuff",  # "stuff" means combining the retrieved documents into a single response
#     retriever=vector_index.as_retriever(),
# )

# # Print the chunks to check if they are properly split
# # print("Chunks of the retrieved documents:")
# # for i, chunk in enumerate(retrieved_docs):
# #     print(f"Chunk {i+1}: {chunk[:100]}...")  # Display the first 100 characters of each chunk

# # Prepare the input data and print it for debugging
# input_data = {
#     "query": f"{model_prompt.format(user_query=user_prompt)}",
#     "retrieved_docs": retrieved_docs  # Pass the retrieved document chunks to the model
# }
# # print("Input to the model:", input_data)

# # Run the query through the model
# response = vector_qa.invoke(input_data)


# # Print the final response for debugging
# print("Model response:", response['result'])



# app.py

from flask import Flask, request, jsonify
from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
import os
from langchain_community.vectorstores import Neo4jVector
from langchain_google_genai import GoogleGenerativeAI, GoogleGenerativeAIEmbeddings

# Initialize Flask app
app = Flask(__name__)

# Load environment variables
load_dotenv(r"C:\Users\shiva\Downloads\BTP_env_variables.env")

# Get API key and folder paths
NEO4J_URI = os.getenv('NEO4J_URI')
NEO4J_USERNAME = os.getenv('NEO4J_USERNAME')
NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD')
google_api_key_1 = os.getenv('GOOGLE_API_KEY')

# Initialize embeddings and vector store
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
vector_index = Neo4jVector.from_existing_graph(
    embeddings,
    url=NEO4J_URI,
    username=NEO4J_USERNAME,
    password=NEO4J_PASSWORD,
    index_name='retriev_index',
    node_label="Section",
    text_node_properties=['content'],
    embedding_node_property='embedding',
)

# Route to handle the query
@app.route('/query', methods=['POST'])
def query():
    user_prompt = request.json.get("user_prompt", "")
    
    # Similarity search
    retrieved_docs_with_scores = vector_index.similarity_search_with_score(user_prompt, k= 50000)

    # Split long documents if necessary
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
    retrieved_docs = []
    for doc, score in retrieved_docs_with_scores:
        chunks = text_splitter.split_text(doc.page_content)
        retrieved_docs.extend(chunks)

    # Initialize the Google Generative AI LLM
    llm = GoogleGenerativeAI(model="gemini-pro", google_api_key=google_api_key_1)
    
    # Set up the RetrievalQA pipeline
    vector_qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="map_reduce",
        retriever=vector_index.as_retriever(),
    )

    # Run the query through the model
    model_prompt = (
        "Answer the following question based on the information provided:\n"
        "Question: {user_query}\n"
        "use the relevant information from the retrieved documents."
        "Do not reply : I cannot answer to this question as it does not contain any information of the Question; Instead try to answer summarize content from the retrieved documents."
    )
    input_data = {
        "query": model_prompt.format(user_query=user_prompt),
        "retrieved_docs": retrieved_docs
    }
    response = vector_qa.invoke(input_data)

    # Return the response
    return jsonify({"Model Response": response['result']})

if __name__ == '__main__':
    app.run(debug=True)
