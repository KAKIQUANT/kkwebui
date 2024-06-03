import os
import runpy
import sys

def main() -> None:
    streamlit_script_path = os.path.join(os.path.dirname(__file__), "streamlit_main.py")
    sys.argv = ["streamlit", "run", streamlit_script_path]
    runpy.run_module("streamlit", run_name="__main__")


if __name__ == "__main__":
    main()