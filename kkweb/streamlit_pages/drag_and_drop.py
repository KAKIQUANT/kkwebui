import streamlit as st
import streamlit.components.v1 as components
def drag_and_drop():
    # Define the drag and drop component
    _drag_and_drop_html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Drag and Drop</title>
        <style>
            #draggable-elements {
                display: flex;
                flex-direction: column;
                width: 200px;
            }
    
            .draggable {
                margin: 10px;
                padding: 10px;
                background-color: lightgrey;
                border: 1px solid #ccc;
                cursor: move;
            }
    
            #drop-zone {
                width: 100%;
                min-height: 200px;
                margin: 10px 0;
                padding: 10px;
                background-color: #f9f9f9;
                border: 2px dashed #ccc;
            }
        </style>
    </head>
    <body>
        <div id="draggable-elements">
            <div class="draggable" draggable="true" ondragstart="drag(event)" id="element1">Strategy Component 1</div>
            <div class="draggable" draggable="true" ondragstart="drag(event)" id="element2">Strategy Component 2</div>
            <div class="draggable" draggable="true" ondragstart="drag(event)" id="element3">Strategy Component 3</div>
        </div>
        <div id="drop-zone" ondrop="drop(event)" ondragover="allowDrop(event)">
            Drop components here to build your strategy
        </div>
        <script>
            function allowDrop(event) {
                event.preventDefault();
            }
    
            function drag(event) {
                event.dataTransfer.setData("text", event.target.id);
            }
    
            function drop(event) {
                event.preventDefault();
                var data = event.dataTransfer.getData("text");
                event.target.appendChild(document.getElementById(data));
                updateDropZone();
            }
    
            function updateDropZone() {
                const dropZone = document.getElementById('drop-zone');
                const components = Array.from(dropZone.children);
                const componentIds = components.map(c => c.id).join(',');
                window.parent.postMessage(componentIds, '*');
            }
        </script>
    </body>
    </html>
    """

    # Create the Streamlit app
    st.title('Drag and Drop Strategy Builder')

    # Embed the drag and drop HTML
    components.html(_drag_and_drop_html, height=400)

    # Listen for messages from the drag and drop component
    component_ids = st.experimental_get_query_params().get('component_ids', [])

    if component_ids:
        st.write('You have selected the following components:')
        st.write(component_ids)

    st.markdown("""
    <style>
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)
