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
        /* Background and container styling */
        .stApp {
            background-color: #f4f6f8;
            padding: 20px;
        }
        .stApp h1 {
            font-family: 'Arial', sans-serif;
            font-weight: bold;
            color: #1a73e8;
        }
        /* Sidebar background */
        .stSidebar {
            background-color: #e3f2fd;
            padding: 10px;
        }
        
        /* Input box styling */
        .stTextInput input {
            padding: 10px;
            border: 1px solid #d9d9d9;
            border-radius: 10px;
            width: 100%;
        }
        
        /* Button styling */
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
        
        /* Sidebar description */
        .sidebar-description {
            font-size: 14px;
            color: #333;
            margin-top: 10px;
            text-align: justify;
        }
        
        /* Query history title and individual items */
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

    # Display query history in sidebar
    st.markdown("<div class='query-history-title'>Query History</div>", unsafe_allow_html=True)
    for idx, entry in enumerate(st.session_state.history[::-1], start=1):
        with st.expander(f"Query at {entry['time']}"):
            st.write("**Question:**", entry['query'])
            st.write("**Response:**", entry['response'])

# Main Title
st.title("GutGuide")

# User input for query
user_prompt = st.text_input("Enter your question here:", placeholder="Type your question about IBD...")

# Button for getting the answer
if st.button("Get Answer"):
    if user_prompt.strip():
        # Add query to history
        query_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.history.append({"query": user_prompt, "time": query_time, "response": "Processing..."})
        
        # Send request to Flask API
        try:
            response = requests.post("http://127.0.0.1:5000/query", json={"user_prompt": user_prompt})
            response_data = response.json()
            
            # Retrieve response and add to history
            answer = response_data.get("Model Response", "No result")
            st.session_state.history[-1]["response"] = answer
            
            # Display the answer
            st.write("**Model Response:**", answer)
        
        except requests.exceptions.RequestException as e:
            st.error(f"API call failed: {e}")
            st.session_state.history[-1]["response"] = "API call failed"
