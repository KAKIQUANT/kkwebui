import streamlit as st
import os

# Helper function to read the contents of a file
def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# Function to list all files in a given directory
def list_files(directory):
    files = []
    for root, dirs, file_names in os.walk(directory):
        for file_name in file_names:
            files.append(os.path.join(root, file_name))
    return files

# Initialize Streamlit app
st.set_page_config(page_title="Forum", layout="wide")

# Sidebar for selecting files
st.sidebar.title("Knowledge Base")
folder_path = st.sidebar.text_input("Enter the folder path containing documents:")
if folder_path:
    files = list_files(folder_path)
    selected_file = st.sidebar.selectbox("Select a file to view its content", files)
    if selected_file:
        file_content = read_file(selected_file)
        st.sidebar.write(file_content)

# Main page for forum and chat
st.title("Forum Page")

# Section for leaving messages
st.subheader("Leave a Message")
message = st.text_area("Enter your message here:")
if st.button("Submit"):
    st.write("Message submitted:", message)

# Section for chat
st.subheader("Chat Room")
chat_message = st.text_input("Enter your chat message:")
if st.button("Send"):
    st.write("Chat message sent:", chat_message)

# Display file content if selected
if folder_path and selected_file:
    st.subheader("Document Content")
    st.write(file_content)

# Display 'About' and 'Contact Us' buttons at the bottom
st.markdown("""
    <style>
        .footer {
            position: fixed;
            bottom: 0;
            width: 100%;
            background-color: #f1f1f1;
            text-align: center;
            padding: 10px;
        }
    </style>
    <div class="footer">
        <a href="#about">About</a> | <a href="#contact">Contact Us</a>
    </div>
    """, unsafe_allow_html=True)

# About section
st.markdown("""
    <h2 id="about">About</h2>
    <p>This is a simple forum page with a chat room and a knowledge base.</p>
""")

# Contact Us section
st.markdown("""
    <h2 id="contact">Contact Us</h2>
    <p>For any inquiries, please contact us at forum@example.com.</p>
""")
