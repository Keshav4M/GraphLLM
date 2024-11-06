import streamlit as st
import requests
from PIL import Image


# Streamlit UI Configuration
st.set_page_config(page_title="IBD Chatbot", page_icon="💬", layout="centered")

# Custom CSS for light background
st.markdown(
    """
    <style>
        /* Set background color for the app */
        .main {
            background-color: black;  
        }

        /* Set sidebar color */
        .stSidebar {
            background-color: #e6f7ff;  /* Slightly darker than main */
        }

        /* Set style for text input and button */
        input[type="text"] {
            border: 1px solid #d9d9d9;
            border-radius: 5px;
            padding: 10px;
            width: 100%;
        }

        /* Center align the title and add some spacing */
        .stApp {
            padding: 20px;
            background-color: #e0e0e0;
            color: black;  /* Set text color to black */
        }

        /* Set style for the button */
        .stButton > button {
            background-color: #4CAF50;
            color: white;
            font-size: 16px;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
        }

        /* Set text color in sidebar */
        .stSidebar .stTextInput, .stSidebar .stButton, .stSidebar h1, .stSidebar h2, .stSidebar h3, .stSidebar p {
            color: black;  /* Set sidebar text color to black */
        }

        /* Main title color */
        .stApp h1 {
            color: #007bff;  /* Change to your desired color */
        }

        /* Input prompt color */
        .stApp label {
            color: black;  /* Change label color for text input */
        }

        /* Query history title color */
        .stApp h3 {
            color: #007bff;  /* Change to your desired color for the Query History */
        }

        /* Logo styling */
        .logo {
            width: 150px;
            display: block;
            margin: auto;
            padding-bottom: 10px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Load logo image (you'll need a logo file like 'logo.png' in the same directory)
logo = Image.open("dept_PNG-12.png")



# Sidebar Logo and App Title
with st.sidebar:
    st.image(logo, use_column_width=True)
    st.title("IBD Chatbot")
    st.caption("Powered by Neo4j and RAG LLM Agent")

# Main Title
st.title("Chatbot for Inflammatory Bowel Disease")

# Session state for query history
if "history" not in st.session_state:
    st.session_state.history = []

# Input for user's query with Enter key functionality
user_prompt = st.text_input(
    "Enter your question here:", 
    placeholder="Type your question about IBD...",
    on_change=lambda: st.session_state.update({"get_answer": True})  # Correct syntax
)

# Press Enter to trigger 'Get Answer' button
if st.session_state.get("get_answer"):
    st.session_state.get_answer = True
    st.session_state.history.append({"query": user_prompt})

# Button for getting the answer
if st.button("Get Answer") or st.session_state.get("get_answer"):
    # Send request to Flask API
    try:
        response = requests.post("http://127.0.0.1:5000/query", json={"user_prompt": user_prompt})
        response_data = response.json()
        
        # Add the response to the history
        answer = response_data.get("Model Response", "No result")
        st.session_state.history[-1]["response"] = answer  # Update latest entry with response
        
        # Display response
        st.write("**Model Response:**", answer)

    except requests.exceptions.RequestException as e:
        st.error(f"API call failed: {e}")

# Display query history
st.write("### Query History")
for idx, entry in enumerate(st.session_state.history, start=1):
    with st.expander(f"Query: {entry['query']}"):
        st.write("**Response:**", entry.get("response", "No response yet"))
