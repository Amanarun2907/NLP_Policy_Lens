"""
Execute NLP notebook and save all outputs including graphs
"""
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import sys

print("="*70)
print("🚀 EXECUTING NLP.ipynb WITH ALL VISUALIZATIONS")
print("="*70)

# Read the notebook
with open('NLP.ipynb', 'r', encoding='utf-8') as f:
    nb = nbformat.read(f, as_version=4)

# Execute the notebook
ep = ExecutePreprocessor(timeout=600, kernel_name='python3')

print("\n⏳ Running all cells and generating graphs...")
print("This will take 2-3 minutes...\n")

try:
    ep.preprocess(nb, {'metadata': {'path': '.'}})
    
    # Save the executed notebook with outputs
    with open('NLP.ipynb', 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)
    
    print("\n" + "="*70)
    print("✅ SUCCESS! NLP.ipynb executed with all outputs saved!")
    print("="*70)
    print("\n📊 All graphs and visualizations are now in the notebook")
    print("📍 File: NLP.ipynb")
    print("\n🎯 Next: Open NLP.ipynb to see all results with graphs!")
    print("="*70)
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\n💡 Opening Jupyter manually...")
    import subprocess
    subprocess.Popen(['jupyter', 'notebook', 'NLP.ipynb'])
