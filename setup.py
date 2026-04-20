"""
Run this once to set up the environment:
    python setup.py
"""
import os
import subprocess
import sys

def run(cmd):
    print(f"\n>>> {cmd}")
    subprocess.run(cmd, shell=True, check=True)

def main():
    # 1. Install dependencies
    run(f"{sys.executable} -m pip install -r requirements.txt")

    # 2. Download spaCy English model
    run(f"{sys.executable} -m spacy download en_core_web_sm")

    # 3. Download NLTK data
    import nltk
    for pkg in ["punkt", "stopwords", "averaged_perceptron_tagger", "maxent_ne_chunker", "words"]:
        nltk.download(pkg, quiet=True)
    print("\nNLTK data downloaded.")

    # 4. Create output folders
    for folder in ["outputs", "outputs/charts", "outputs/exports"]:
        os.makedirs(folder, exist_ok=True)
    print("\nOutput folders created.")

    print("\n✅  Setup complete. Run the app with:  streamlit run app.py")

if __name__ == "__main__":
    main()
