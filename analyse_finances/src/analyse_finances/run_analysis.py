# run_analysis.py
import os

# First, save your PDF as 'dummy_statement.pdf'
if not os.path.exists("dummy_statement.pdf"):
    print("❌ Please save your PDF as 'dummy_statement.pdf'")
    print("The file should be in the same folder as this script")
else:
    print("✅ Found dummy_statement.pdf")
    print("Starting analysis with Ollama...")
    
    # Run the main analysis
    from main import analyze_bank_statement
    analyze_bank_statement("dummy_statement.pdf")