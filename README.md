# 🧠 Personal AI Data Analyst

**A local, privacy-first AI data analyst that generates code instead of hallucinating answers.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

---

## 🎯 The Problem

Traditional "Chat with your Data" tools ask LLMs to **directly compute answers** from your data. This leads to:
- ❌ Mathematical hallucinations
- ❌ Unreliable results you can't verify
- ❌ Privacy concerns (sending data to cloud APIs)
- ❌ Black-box reasoning with no transparency

## 💡 The Solution

**Don't ask AI to do math. Ask AI to write code that does math.**

This project uses a **hybrid deterministic + LLM architecture** where:
1. **Deterministic patterns** handle common queries (statistics, correlations, visualizations)
2. **Local LLM** (via Ollama) generates Python code for complex requests
3. **Sandboxed execution** runs the code and returns verifiable results
4. **You** own your data—it never leaves your machine

```
User Question → Code Generation → Safe Execution → Real Results
```

---

## ✨ Key Features

- 📂 **Multi-format support**: CSV, Excel, JSON
- 🧠 **Intelligent profiling**: Automatic column type detection (numeric, categorical, datetime)
- 💬 **Natural language interface**: Ask questions like "Show correlation heatmap" or "Find outliers"
- 🔐 **Privacy-first**: Runs 100% locally, no cloud dependencies
- 🤖 **Optional LLM**: Use Ollama for advanced queries, or run purely deterministic
- 📊 **Safe visualizations**: Matplotlib-only charts with sandboxed execution
- 🎯 **Transparent**: See the exact Python code generated before execution

---

## 🏗️ Architecture

```
┌─────────────────┐
│  User Prompt    │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────┐
│  Deterministic Translator       │  ◄── Trusted patterns (stats, plots, etc.)
│  (Pattern matching)             │
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│  LLM Code Generator (Optional)  │  ◄── Ollama (llama3.1, qwen, etc.)
│  Fallback for complex queries   │
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│  Sandboxed Python Execution     │  ◄── Restricted namespace
│  (pandas, numpy, matplotlib)    │
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│  Tables / Charts / Text Results │
└─────────────────────────────────┘
```

### Core Design Principle

> **LLMs should NOT compute. LLMs should WRITE code that computes.**

This eliminates hallucinations while maintaining the natural language interface users expect.

---

## 📁 Project Structure

```
ai-data-analyst/
│
├── analyst/
│   ├── loader.py       # Robust file ingestion (CSV/Excel/JSON)
│   ├── profiler.py     # Column type detection & metadata
│   ├── translator.py   # Prompt → trusted Python code
│   ├── executor.py     # Sandboxed execution engine
│   └── llm.py          # Ollama HTTP client (optional)
│
├── app.py              # Streamlit web interface
├── requirements.txt    # Python dependencies
├── .gitignore
└── README.md
```

---

## 🚀 Quick Start

### Prerequisites
- **Python 3.10+**
- **Linux / macOS / WSL2** (recommended)
- **(Optional)** [Ollama](https://ollama.com) for LLM-powered queries

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/shrish842/ai-data-analyst.git
   cd ai-data-analyst
   ```

2. **Create and activate virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **(Optional) Set up Ollama**
   ```bash
   # Install Ollama
   curl -fsSL https://ollama.com/install.sh | sh
   
   # Pull a model
   ollama pull llama3.1
   
   # Start Ollama server
   ollama serve
   ```

### Running the Application

```bash
streamlit run app.py
```

The application will open at `http://localhost:8501`

*(WSL users: You may see `gio` warnings—these are harmless and can be ignored)*

---

## 🧪 Example Queries

### Basic Statistics
```
"Show summary statistics for all columns"
"What's the mean and median of price?"
"Show the distribution of categories"
```

### Visualizations
```
"Create a histogram of mileage"
"Show correlation heatmap"
"Plot sales over time"
"Create a scatter plot of price vs. mileage"
```

### Data Quality
```
"Find missing values"
"Detect outliers using z-score > 3"
"Show duplicate rows"
```

### Advanced Analysis
```
"Calculate rolling 7-day average"
"Group by category and show mean price"
"Show top 10 most common values"
```

---

## 🔐 Safety & Privacy Guarantees

✅ **No cloud dependencies**: All processing happens locally  
✅ **No automatic package installation**: Only pre-approved libraries  
✅ **Sandboxed execution**: Code runs in restricted namespace  
✅ **Transparent code generation**: Review Python code before execution  
✅ **No data leakage**: Your data never leaves your machine  
✅ **Minimal attack surface**: No `eval()` or `exec()` of raw strings  

---

## 📊 Supported Data Formats

| Format | Extension | Notes |
|--------|-----------|-------|
| CSV | `.csv` | Automatic delimiter detection |
| Excel | `.xlsx`, `.xls` | All sheets supported |
| JSON | `.json` | Records and table formats |

---

## 🛣️ Roadmap

- [ ] **AST-based validation** of LLM-generated code
- [ ] **Interactive profiling panel** (null counts, distributions, data quality)
- [ ] **Additional formats**: Parquet, DuckDB, SQLite
- [ ] **CLI mode** for scripting and automation
- [ ] **Exportable reports** (PDF, HTML)
- [ ] **Query history** and saved analysis templates
- [ ] **Multi-file analysis** (joins, merges)
- [ ] **Custom visualization themes**

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgements

Inspired by real-world data engineering practices and the fundamental limitation of LLMs in numerical reasoning. This project demonstrates that the best AI tools don't replace traditional computation—they make it more accessible.

**Built with:**
- [Streamlit](https://streamlit.io/) - Web interface
- [Pandas](https://pandas.pydata.org/) - Data manipulation
- [Ollama](https://ollama.com/) - Local LLM inference
- [Matplotlib](https://matplotlib.org/) - Visualizations

---

## 👤 Author

**Shrish Agrawal**

- GitHub: [@shrish842](https://github.com/shrish842)

---

## 🌟 Star History

If you find this project useful, please consider giving it a star! ⭐

---

<div align="center">
  
**Made with ❤️ for data analysts who value transparency and privacy**

</div>
