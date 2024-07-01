import streamlit as st
from streamlit_ace import st_ace
import matplotlib.pyplot as plt
import subprocess
import sys
import os
import io
import contextlib

def python_online():
    # Function to scan a folder and get all file names
    def scan_folder(folder_path):
        files = []
        for file_name in os.listdir(folder_path):
            if file_name.endswith('.txt'):
                files.append(file_name)
        return files

    # Function to read the content of a file
    def read_file(file_path):
        with open(file_path, 'r') as file:
            return file.read()

    # Function to save the content to a file
    def save_file(file_path, content):
        with open(file_path, 'w') as file:
            file.write(content)

    # Function to install a package
    def install_package(package):
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])


    st.title("Online Python Editor")

    # Sidebar for file selection
    folder_path = "D:\\kkwebui\\strategies\\a"
    st.sidebar.title("File Browser")
    file_list = scan_folder(folder_path)
    selected_file = st.sidebar.selectbox("Select a file", file_list)

    # Sidebar for code snippet selection
    code_snippets = {
        "Hello World": "print('Hello, World!')",
        "Plot Example": """
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 5))
plt.plot([1, 2, 3, 4], [10, 20, 25, 30])
plt.title('Simple Plot')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.show()
    """,
        "Package Install Example": """
# To install a package, uncomment the line below
# !pip install numpy

import numpy as np
print(np.arange(15).reshape(3, 5))
    """
    }

    st.sidebar.title("Code Snippets")
    selected_snippet = st.sidebar.selectbox("Select a code snippet", list(code_snippets.keys()))

    # Initialize the ACE editor with the selected code snippet or file content
    if selected_file:
        code = read_file(os.path.join(folder_path, selected_file))
    else:
        code = code_snippets[selected_snippet]

    # This is necessary to keep track of file selection and update the editor content accordingly
    if 'last_selected_file' not in st.session_state:
        st.session_state.last_selected_file = selected_file

    if st.session_state.last_selected_file != selected_file:
        code = read_file(os.path.join(folder_path, selected_file))
        st.session_state.last_selected_file = selected_file

    code = st_ace(
        value=code,
        placeholder="Type your Python code here",
        language="python",
        theme="monokai",
        key="editor",
        height=400,
    )

    # Package installation input
    package_name = st.text_input("Package to install (leave blank if not needed)")

    # Run the code when the 'Run' button is clicked
    if st.button("Run"):
        if code:
            if package_name:
                with st.spinner(f"Installing {package_name}..."):
                    try:
                        install_package(package_name)
                        st.success(f"Successfully installed {package_name}")
                    except Exception as e:
                        st.error(f"Error installing package: {e}")

            # Capture the standard output and errors
            output = io.StringIO()
            with contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
                try:
                    exec_globals = {}
                    exec_locals = {}
                    exec(code, exec_globals, exec_locals)
                    st.success("Code executed successfully")
                except Exception as e:
                    output.write(f"Error: {e}\n")

            # Get the output
            result = output.getvalue()
            st.subheader("Execution Output")
            st.text(result)

            # Check if there are plots and display them
            if plt.get_fignums():
                st.subheader("Plots")
                st.pyplot(plt)

    # Save the code
    save_path = st.text_input("Save file as", value="script.py")
    if st.button("Save Code"):
        save_file(save_path, code)
        st.success(f"Code saved as {save_path}")

if __name__ == "__main__":
    python_online()
