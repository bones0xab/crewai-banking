# Financial PDF Analysis System with CrewAI

## Overview
A multi-agent AI system that analyzes bank statement PDFs, categorizes transactions, and generates detailed financial reports. The system uses local LLMs via Ollama for privacy and cost-free operation.

## Features
- **PDF Transaction Extraction**: Automatically extracts transactions from bank statement PDFs
- **Smart Categorization**: Classifies transactions into income/expense categories
- **Financial Analysis**: Generates comprehensive reports with insights and recommendations
- **PDF Report Generation**: Creates professional PDF reports from analysis results
- **Local AI Processing**: Uses Ollama with llama3.2 model (100% local, no API costs)

## Project Structure
```
analyse_finances/
├── src/analyse_finances/
│   ├── main.py              # Main application with CrewAI agents
│   ├── dummy_statement.pdf  # Sample bank statement (add your own)
│   ├── financial_report.pdf # Generated PDF report
│   └── financial_report.txt # Generated text report
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Prerequisites
- Python 3.8+
- Ollama (local LLM runner)
- Git (optional)

## Installation

### 1. Install Ollama
Download and install Ollama from [ollama.com](https://ollama.com)

### 2. Pull the LLM Model
```bash
ollama pull llama3.2
```

### 3. Install Python Dependencies
```bash
pip install crewai pdfplumber reportlab requests
```

### 4. Start Ollama Server
```bash
ollama serve
```
*Keep this terminal running*

## Usage

### 1. Prepare Your PDF
Place your bank statement PDF in the project directory and rename it to `dummy_statement.pdf`

### 2. Run the Analysis
```bash
python main.py
```

### 3. Output Files
The system generates:
- **financial_report.pdf**: Professional PDF report
- **financial_report.txt**: Text version of the report
- **Console output**: Real-time analysis progress

## How It Works

### Agent Architecture
1. **PDF Transaction Extractor Agent**
   - Role: Extracts all transactions from bank statement PDFs
   - Goal: Parse PDF text and identify transaction data
   - Output: CSV-formatted transaction list

2. **Expense Categorizer Agent**
   - Role: Categorizes transactions into financial categories
   - Goal: Apply smart categorization based on transaction descriptions
   - Output: Categorized transaction list

3. **Financial Analyst Agent**
   - Role: Analyzes financial data and generates insights
   - Goal: Produce comprehensive financial reports
   - Output: Detailed financial analysis in French

### Workflow
```
PDF Input → Text Extraction → Transaction Parsing → 
Categorization → Analysis → Report Generation
```

### Transaction Categories
- **INCOME**: PREAUTHORIZEDCREDIT, PAYROLL, INTEREST CREDIT
- **SHOPPING**: POS PURCHASE, TERMINAL transactions
- **BILLS**: CHECK payments
- **CASH**: ATM WITHDRAWAL
- **FEES**: SERVICE CHARGE, bank fees
- **OTHER**: Unclassified transactions

## Report Contents
Each generated report includes:
- Total Income Calculation
- Total Expenses Analysis
- Net Balance
- Top Spending Categories
- Monthly Trends
- 3 Personalized Financial Recommendations
- Risk Assessment
- Budget Optimization Tips

## Troubleshooting

### Common Issues

1. **Ollama Connection Error**
   ```
   ❌ Ollama not reachable
   ```
   **Solution**: Ensure Ollama is running: `ollama serve`

2. **PDF Not Found**
   ```
   ❌ File not found: dummy_statement.pdf
   ```
   **Solution**: Place your PDF in the same directory as main.py

3. **PDF Extraction Issues**
   ```
   PDF content: 0 characters
   ```
   **Solution**: Ensure your PDF is text-based (not scanned/image PDF)

4. **Module Import Errors**
   ```
   ModuleNotFoundError: No module named 'crewai'
   ```
   **Solution**: Install missing dependencies: `pip install -r requirements.txt`

### Debug Mode
For detailed debugging, modify `main.py`:
```python
# Change verbose levels
extractor = Agent(verbose=True)  # Set to True for detailed output
crew = Crew(verbose=True)        # Set to True for workflow details
```

## Customization

### Modify Categories
Edit the `task2` description in `main.py` to change categorization rules:

```python
task2 = Task(
    description="""Categorize transactions:
- INCOME: SALARY, DEPOSIT, INTEREST
- GROCERIES: SUPERMARKET, FOOD
- ENTERTAINMENT: RESTAURANT, MOVIES
# Add your custom rules here""",
    ...
)
```

### Change Report Language
Modify the `task3` description:
```python
task3 = Task(
    description="""Analyze and create report:
# Change 'Write in French' to your preferred language
Write in English.""",
    ...
)
```

### Use Different LLM Model
Edit the LLM configuration:
```python
ollama_llm = LLM(
    model="ollama/mistral",  # Change to preferred model
    base_url="http://localhost:11434",
    temperature=0.1
)
```

## Sample PDF Format
The system works best with bank statements containing:
- Clear transaction tables with Date, Description, Amount columns
- Text-based PDFs (not scanned documents)
- Standard date formats (MM/DD or DD/MM)
- Currency symbols ($, €, etc.)

## Performance Notes
- Processing time depends on PDF size and Ollama model
- Typical analysis: 30-90 seconds for 20-50 transactions
- Larger PDFs may require more memory
- For best results, use recent bank statements with clear formatting

## Future Enhancements
Planned features:
- Support for multiple PDF formats
- Database integration for historical analysis
- Web interface with Streamlit
- Email report delivery
- Multi-currency support
- Budget tracking and alerts

## Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License
MIT License - See LICENSE file for details

## Support
For issues and questions:
1. Check the Troubleshooting section
2. Ensure all prerequisites are installed
3. Verify PDF format compatibility
4. Test with the sample PDF first

## Acknowledgments
- [CrewAI](https://www.crewai.com/) for the multi-agent framework
- [Ollama](https://ollama.com/) for local LLM hosting
- [pdfplumber](https://github.com/jsvine/pdfplumber) for PDF text extraction
- [ReportLab](https://www.reportlab.com/) for PDF generation
