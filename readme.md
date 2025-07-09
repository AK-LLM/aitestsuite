# 🔐 AI Infosec & Hallucination Testing Dashboard

This dashboard provides a streamlined solution for evaluating AI models' security vulnerabilities, robustness, and hallucination risks. Built with Streamlit, it offers quick, actionable insights into your AI model's infosec posture.

## 🚀 Quick Start

### **1. Clone the Repository**

```bash
git clone https://github.com/your-username/AI-Infosec-Dashboard.git
cd AI-Infosec-Dashboard
```

### **2. Install Dependencies**

```bash
pip install -r requirements.txt
```

### **3. Run the Dashboard Locally**

```bash
streamlit run app.py
```

## 🌐 Deploy to Streamlit Cloud

1. Push your repo to GitHub.
2. Go to [Streamlit Cloud](https://streamlit.io/cloud), connect your repo, and deploy.

## 📂 Project Structure

```
AI-Infosec-Dashboard/
├── app.py                   # Main Streamlit application
├── security.py              # Security Tests (Prompt Injection)
├── hallucination.py         # Hallucination Tests (Truthfulness)
├── robustness.py            # Robustness Tests (Boundary conditions)
├── pdf_report.py            # PDF Report Generation
├── utils.py                 # Workflow & Help Documentation
├── requirements.txt         # Python dependencies
└── README.md                # Project description
```

## ⚙️ Features

* **Security Assessment:** Detect prompt injection vulnerabilities.
* **Hallucination Testing:** Evaluate factual accuracy and truthfulness.
* **Robustness Checks:** Test AI model stability under edge-case scenarios.
* **PDF Reporting:** Generate and download detailed PDF reports.

## 🛠️ Built With

* [Streamlit](https://streamlit.io/)
* [FPDF](https://pyfpdf.readthedocs.io/en/latest/)
* [Requests](https://docs.python-requests.org/en/latest/)

## 🔮 Roadmap & Planned Enhancements

* OAuth Authentication (Google/GitHub)
* Advanced compliance checks (ISO/NIST)
* Enhanced reporting (analytics, visualizations)
* Admin dashboard for user management
* Automated assessments and notifications

## 📋 Support & Documentation

For detailed workflow and built-in tool documentation, click the **"Show Help & Workflow"** button inside the app.

## 💬 Contributing

Pull requests and contributions are welcome. For major changes, please open an issue first to discuss what you'd like to change.

## 📃 License

[MIT](https://choosealicense.com/licenses/mit/)

---

© 2025 AI Infosec Team. All rights reserved.
