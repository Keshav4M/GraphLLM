# import streamlit as st
# import requests
# from PIL import Image
# from datetime import datetime

# # Streamlit UI Configuration
# st.set_page_config(page_title="GutGuide", page_icon="💬", layout="centered")

# # Load logo image (ensure logo file like 'dept_PNG-12.png' is in the directory)
# logo = Image.open("dept_PNG-12.png")

# # Custom CSS for styling
# st.markdown(
#     """
#     <style>
#         .stApp {
#             background-color: #f4f6f8;
#             padding: 20px;
#         }
#         .stApp h1 {
#             font-family: 'Arial', sans-serif;
#             font-weight: bold;
#             color: #1a73e8;
#         }
#         .stSidebar {
#             background-color: #e3f2fd;
#             padding: 10px;
#         }
#         .stTextInput input {
#             padding: 10px;
#             border: 1px solid #d9d9d9;
#             border-radius: 10px;
#             width: 100%;
#         }
#         .stButton > button {
#             background-color: #1a73e8;
#             color: white;
#             font-size: 16px;
#             padding: 10px 24px;
#             border-radius: 5px;
#             border: none;
#             font-family: 'Arial', sans-serif;
#             transition: all 0.3s;
#         }
#         .stButton > button:hover {
#             background-color: #155db3;
#             transform: scale(1.05);
#         }
#         .sidebar-description {
#             font-size: 14px;
#             color: #333;
#             margin-top: 10px;
#             text-align: justify;
#         }
#         .query-history-title {
#             color: #1a73e8;
#             font-weight: bold;
#             margin-top: 20px;
#         }
#         .query-item {
#             padding: 10px;
#             border-bottom: 1px solid #e0e0e0;
#             border-radius: 5px;
#             background-color: #ffffff;
#             margin-bottom: 10px;
#             box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1);
#             color: #000000;
#         }
#         .query-item p, .query-item div {
#             color: #000000;
#         }
#         .response-text {
#             color: #000000;
#         }
#     </style>
#     """,
#     unsafe_allow_html=True
# )

# # Sidebar with logo, title, description, and query history
# with st.sidebar:
#     st.image(logo, use_column_width=True)
#     st.title("GutGuide")
#     st.caption("Powered by Neo4j and RAG LLM Agent")
#     st.markdown(
#         "<div class='sidebar-description'>"
#         "GutGuide is an intelligent chatbot designed to support patients with Inflammatory Bowel Disease (IBD). Offering personalized insights, symptom tracking, and dietary guidance, GutGuide empowers users to better manage and understand their IBD journey, improving daily well-being."
#         "</div>",
#         unsafe_allow_html=True
#     )

#     # Initialize session state for query history
#     if "history" not in st.session_state:
#         st.session_state.history = []

#     # Display query history in sidebar with updated styling
#     st.markdown("<div class='query-history-title'>Query History</div>", unsafe_allow_html=True)
#     for idx, entry in enumerate(st.session_state.history[::-1], start=1):
#         with st.expander(f"Query at {entry['time']}"):
#             st.markdown(f"<div class='query-item'><strong>Question:</strong> {entry['query']}</div>", unsafe_allow_html=True)
#             st.markdown(f"<div class='query-item response-text'><strong>Response:</strong> {entry['response']}</div>", unsafe_allow_html=True)

# # Function to handle query submission
# def submit_query():
#     user_prompt = st.session_state.user_input  # Get the user input from session state
#     if user_prompt.strip():  # Only process non-empty input
#         query_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         st.session_state.history.append({"query": user_prompt, "time": query_time, "response": "Processing..."})
        
#         # Send request to Flask API
#         try:
#             response = requests.post("http://127.0.0.1:5000/query", json={"user_prompt": user_prompt})
#             response_data = response.json()
            
#             # Retrieve response and add to history
#             answer = response_data.get("Model Response", "No result")
#             st.session_state.history[-1]["response"] = answer  # Update the latest history item
            
#             # Display the answer in the main response area in black color
#             st.markdown(f"<div class='response-text'><strong>Model Response:</strong> {answer}</div>", unsafe_allow_html=True)
        
#         except requests.exceptions.RequestException as e:
#             error_message = f"API call failed: {e}"
#             st.error(error_message)
#             st.session_state.history[-1]["response"] = error_message  # Update the latest history item with error

# # Main Title
# st.title("GutGuide")

# # User input for query with Enter key submission
# st.text_input(
#     "Enter your question here:", 
#     placeholder="Type your question about IBD...",
#     key="user_input",  
#     on_change=submit_query  
# )

# # Button for getting the answer manually
# if st.button("Get Answer"):
#     submit_query()


import streamlit as st
import requests
from PIL import Image
from datetime import datetime

# Streamlit UI Configuration
st.set_page_config(page_title="GutGuide", page_icon="💬", layout="centered")

# Load logo image (ensure logo file like 'dept_PNG-12.png' is in the directory)
logo = Image.open("dept_PNG-12.png")

# Custom CSS for styling
st.markdown(
    """
    <style>
        .stApp {
            background-color: #f4f6f8;
            padding: 20px;
        }
        .stApp h1 {
            font-family: 'Arial', sans-serif;
            font-weight: bold;
            color: #1a73e8;
        }
        .stSidebar {
            background-color: #e3f2fd;
            padding: 10px;
        }
        .stTextInput input {
            padding: 10px;
            border: 1px solid #d9d9d9;
            border-radius: 10px;
            width: 100%;
        }
        .stButton > button {
            background-color: #1a73e8;
            color: white;
            font-size: 16px;
            padding: 10px 24px;
            border-radius: 5px;
            border: none;
            font-family: 'Arial', sans-serif;
            transition: all 0.3s;
        }
        .stButton > button:hover {
            background-color: #155db3;
            transform: scale(1.05);
        }
        .sidebar-description {
            font-size: 14px;
            color: #333;
            margin-top: 10px;
            text-align: justify;
        }
        .query-history-title {
            color: #1a73e8;
            font-weight: bold;
            margin-top: 20px;
        }
        .query-item {
            padding: 10px;
            border-bottom: 1px solid #e0e0e0;
            border-radius: 5px;
            background-color: #ffffff;
            margin-bottom: 10px;
            box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1);
            color: #000000;
        }
        .query-item p, .query-item div {
            color: #000000;
        }
        .response-text {
            color: #000000;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar with logo, title, description, and query history
with st.sidebar:
    st.image(logo, use_column_width=True)
    st.title("GutGuide")
    st.caption("Powered by Neo4j and RAG LLM Agent")
    st.markdown(
        "<div class='sidebar-description'>"
        "GutGuide is an intelligent chatbot designed to support patients with Inflammatory Bowel Disease (IBD). Offering personalized insights, symptom tracking, and dietary guidance, GutGuide empowers users to better manage and understand their IBD journey, improving daily well-being."
        "</div>",
        unsafe_allow_html=True
    )

    # Initialize session state for query history
    if "history" not in st.session_state:
        st.session_state.history = []

    # Display query history in sidebar with updated styling
    st.markdown("<div class='query-history-title'>Query History</div>", unsafe_allow_html=True)
    for idx, entry in enumerate(st.session_state.history[::-1], start=1):
        with st.expander(f"Query at {entry['time']}"):
            st.markdown(f"<div class='query-item'><strong>Question:</strong> {entry['query']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='query-item response-text'><strong>Response:</strong> {entry['response']}</div>", unsafe_allow_html=True)

# Function to handle query submission
def submit_query():
    user_prompt = st.session_state.user_input  # Get the user input from session state
    if user_prompt.strip():  # Only process non-empty input
        query_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.history.append({"query": user_prompt, "time": query_time, "response": "Processing..."})
        
        # Send request to Flask API
        try:
            response = requests.post("http://127.0.0.1:5000/query", json={"user_prompt": user_prompt})
            response_data = response.json()
            
            # Retrieve response and add to history
            answer = response_data.get("Model Response", "No result")
            st.session_state.history[-1]["response"] = answer  # Update the latest history item
            
            # Display the answer in the reserved placeholder area
            response_placeholder.markdown(f"<div class='response-text'><strong>Model Response:</strong> {answer}</div>", unsafe_allow_html=True)
            st.markdown(answer)
        
        except requests.exceptions.RequestException as e:
            error_message = f"API call failed: {e}"
            st.error(error_message)
            st.session_state.history[-1]["response"] = error_message  # Update the latest history item with error

# Main Title
st.title("GutGuide")

# Placeholder for response to ensure it appears below the title
response_placeholder = st.empty()

# User input for query with Enter key submission
st.text_input(
    "Enter your question here:", 
    placeholder="Type your question about IBD...",
    key="user_input",  
    on_change=submit_query  
)

# Button for getting the answer manually
if st.button("Get Answer"):
    submit_query()
