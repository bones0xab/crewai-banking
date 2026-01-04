import os
import pdfplumber
from crewai import Agent, Task, Crew, LLM
import requests
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import json

# ========= CONFIRM OLLAMA =========
print("🔄 Checking Ollama...")
try:
    resp = requests.get("http://localhost:11434/api/tags", timeout=5)
    if resp.status_code == 200:
        print("✅ Ollama is running")
except:
    print("❌ Ollama not reachable")
    exit(1)

# ========= LLM CONFIG =========
ollama_llm = LLM(
    model="ollama/llama3.2",
    base_url="http://localhost:11434",
    temperature=0.1
)

# ========= EXTRACT PDF =========
def read_pdf(pdf_path):
    """Read PDF with pdfplumber"""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            return text
    except Exception as e:
        return f"Error: {str(e)}"

# ========= READ THE PDF =========
pdf_path = "dummy_statement.pdf"
if not os.path.exists(pdf_path):
    print(f"❌ File not found: {pdf_path}")
    exit(1)

pdf_content = read_pdf(pdf_path)
print(f"📄 PDF content: {len(pdf_content)} characters")
print(f"Preview: {pdf_content[:300]}...\n")

# ========= AGENTS =========
extractor = Agent(
    role="PDF Transaction Extractor",
    goal="Extract all transactions from bank statement",
    backstory="Expert in parsing bank PDFs",
    llm=ollama_llm,
    verbose=True
)

categorizer = Agent(
    role="Expense Categorizer", 
    goal="Categorize transactions",
    backstory="Accountant specializing in categorization",
    llm=ollama_llm,
    verbose=True
)

analyst = Agent(
    role="Financial Analyst",
    goal="Generate financial report",
    backstory="Financial analyst expert",
    llm=ollama_llm,
    verbose=True
)

# ========= TASKS =========
task1 = Task(
    description=f"""Extract ALL transactions from this bank statement:

{pdf_content[:2000]}

Return as CSV with columns: date,amount,description
Example:
10/02,-4.23,POS PURCHASE
10/03,763.01,PREAUTHORIZEDCREDIT""",
    expected_output="CSV of transactions",
    agent=extractor
)

task2 = Task(
    description="""Categorize transactions:
- INCOME: PREAUTHORIZEDCREDIT, PAYROLL, INTEREST
- SHOPPING: POS PURCHASE  
- BILLS: CHECK
- CASH: ATM
- FEES: SERVICE CHARGE
Add 'category' column.""",
    expected_output="CSV with category column",
    agent=categorizer,
    context=[task1]
)

task3 = Task(
    description="""Analyze and create report:
1. Total income
2. Total expenses
3. Net balance
4. Top spending categories
5. 3 recommendations
Write in French.""",
    expected_output="Financial report in French",
    agent=analyst,
    context=[task2]
)

# ========= RUN =========
crew = Crew(
    agents=[extractor, categorizer, analyst],
    tasks=[task1, task2, task3],
    verbose=True
)

print("🚀 Starting analysis...")
result = crew.kickoff()

print("\n" + "="*60)
print("📊 FINANCIAL REPORT")
print("="*60)
print(result)



# ========= GENERATE PDF REPORT =========
def create_pdf_report(result, output_file="financial_report.pdf"):
    """Create a PDF from the analysis result"""
    doc = SimpleDocTemplate(output_file, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()
    
    # Title
    title = Paragraph("FINANCIAL ANALYSIS REPORT", styles['Title'])
    story.append(title)
    story.append(Spacer(1, 12))
    
    # Add the analysis result
    result_text = str(result)
    
    # Split into paragraphs
    paragraphs = result_text.split('\n')
    for para in paragraphs:
        if para.strip():
            p = Paragraph(para, styles['Normal'])
            story.append(p)
            story.append(Spacer(1, 6))
    
    # Build PDF
    doc.build(story)
    print(f"✅ PDF report generated: {output_file}")

# ========= AFTER CREW RUNS =========
print("🚀 Starting analysis...")
result = crew.kickoff()

print("\n" + "="*60)
print("📊 FINANCIAL REPORT")
print("="*60)
print(result)

# Generate PDF report
create_pdf_report(result)

# Also save text report
with open("financial_report.txt", "w", encoding="utf-8") as f:
    f.write(str(result))
print("✅ Text report saved: financial_report.txt")