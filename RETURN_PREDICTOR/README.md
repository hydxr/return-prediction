# ⚡ RETURNAI // Intelligent Order Return Predictor

A machine learning system engineered to predict e-commerce product returns, detect sizing bracket purchasing behaviors, and mitigate reverse-logistics margin losses.

---

## 🚀 How to Run the Project

You have two instant options to run this project:

### Option 1: Instant Browser App (Zero Setup Required)
> **No installation or Python dependencies required.**
1. Open this folder in Windows File Explorer:
   `c:\Users\hp\OneDrive\Documents\RETURN_PREDICTOR`
2. Double-click **`index.html`** (or right-click -> *Open with* -> Google Chrome / Microsoft Edge).
3. The interactive web app will open immediately with live risk simulation, probability scoring, dynamic charts, and prevention recommendations.

---

### Option 2: Full Python + Streamlit Machine Learning Suite (Recommended)

#### 🔹 Method A: 1-Click Windows Launcher
1. In File Explorer, simply **double-click `run.bat`**.
2. The script will automatically:
   - Create a virtual environment (`venv`)
   - Install all required libraries from `requirements.txt`
   - Generate synthetic training data & train the Random Forest model (`return_model.joblib`)
   - Launch the Streamlit dashboard in your default browser at `http://localhost:8501`.

#### 🔹 Method B: Run Manually via Terminal (PowerShell / Command Prompt)
Open PowerShell or Command Prompt in this folder and execute:

```powershell
# 1. Create and activate a virtual environment
python -m venv venv
.\venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Train the model and generate data (first time only)
python train_model.py

# 4. Launch the Streamlit web dashboard
streamlit run app.py
```

---

## 🎨 Distinctive Interface Highlights

This application includes custom styling:
- **Cyber-Glassmorphism Theme**: Deep space dark canvas (`#030712`), frosted glass cards (`backdrop-filter`), and neon accents.
- **Radial Risk Gauge**: Real-time Plotly circular indicator and probability percentage.
- **Financial Exposure Calculator**: Live calculation of estimated reverse logistics shipping/restock costs and net margin at risk.
- **Interactive Sizing & Bracket Buyer Toggles**: Simulates customer purchase patterns (e.g. buying multiple sizes of the same apparel/shoe SKU to return the wrong fit).
- **Batch CSV Ingestion**: Upload custom order CSVs or evaluate simulated streams with instant sorting by highest return hazard.
- **Top Feature Drivers**: Horizontal bar charts displaying feature importance (past return frequency, discount rate, product category, payment method).
- **Automated Mitigation Playbooks**: Prescriptive operational interventions (anti-bracket sizing concierges, COD WhatsApp verification, 1-click size exchange incentives).

---

## 📂 Project Architecture

```
RETURN_PREDICTOR/
│
├── index.html            # Standalone, zero-setup interactive web dashboard
├── app.py                # Main Streamlit ML application with custom CSS
├── data_generator.py     # Realistic e-commerce dataset generator
├── train_model.py        # ML training pipeline (Random Forest + Scikit-Learn)
├── requirements.txt      # Python dependencies (Streamlit, Scikit-learn, Plotly, Pandas)
├── run.bat               # 1-Click Windows automated launcher
└── README.md             # Project documentation & run guide
```

