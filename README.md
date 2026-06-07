# 💸 ExpenseTracker Pro

A modern, high-end, interactive web dashboard built with Python and **Streamlit** to manage your personal finances. This application elevates the original command-line tracker into a visually stunning, premium analytics tool with real-time charts, inline spreadsheet editing, and detailed financial reports.

---

## ✨ Features

### 📊 Real-Time Financial Analytics
*   **KPI Metrics Cards:** Instant view of Total Spending, Custom Monthly Budget, Remaining Budget (with color-coded alerts), and Transaction Counts.
*   **Interactive Charts (Plotly):**
    *   *Category Breakdown:* High-end Donut Chart visualizing expense distribution.
    *   *Budget Utilization Gauge:* Real-time dial chart indicating how close you are to your spending limit.
    *   *Spending Trends:* Area chart showcasing daily/monthly expenses.

### 📋 Full CRUD Database Editor
*   **Inline Editing (`st.data_editor`):** Edit expense names, amounts, dates, or categories directly inside a spreadsheet-like grid.
*   **Dynamic Deletion:** Select entries in the table and delete them with a single click.
*   **Real-time Synchronization:** Edits are auto-saved back to the `expense_tracker_d1.json` database.

### 📅 Advanced Reports & Filtering
*   **Monthly Report Generator:** Select any past month to view summarized expenses, transaction counts, and category reports.
*   **Search & Sort Console:** Live search by name/category and instant sorting (Highest-to-Lowest, Lowest-to-Highest, and chronological order).
*   **Extremes Highlight:** Highlights the single highest and lowest expense records in dedicated dashboard cards.

### 📥 Data Management
*   **Persistent Storage:** Data is stored locally in clean JSON formats (`expense_tracker_d1.json`, `expense_budget.json`).
*   **CSV Exporter:** Download your current filtered data as a CSV file with one click.

---

## 🛠️ Tech Stack

*   **Frontend/Dashboard:** [Streamlit](https://streamlit.io/)
*   **Data Processing:** [Pandas](https://pandas.pydata.org/)
*   **Visualizations:** [Plotly](https://plotly.com/)
*   **Styling:** Custom CSS with a premium Dark Emerald theme.

---

## 📁 Directory Structure

```text
Expense_Tracker_P1/
├── app.py                     # Streamlit Web Application (Main Entrypoint)
├── main.py                    # Original CLI application (preserved)
├── requirements.txt           # Python dependencies
├── expense_tracker_d1.json    # JSON storage for expenses
├── expense_budget.json        # JSON storage for monthly budget
├── expenses.csv               # Exported CSV
├── .streamlit/
│   └── config.toml            # Premium Dark Emerald styling config
└── README.md                  # This file
```

---

## ▶️ Running Locally

Follow these steps to run the application on your computer:

### 1. Set Up and Activate Virtual Environment
```bash
# In the project root directory
python3 -m venv venv

# Activate on macOS/Linux:
source venv/bin/activate

# Activate on Windows:
# venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Launch the Application
```bash
streamlit run app.py
```
This command will launch a local server and automatically open the application in your default web browser (usually at `http://localhost:8501`).

---

## 🌐 Deploying to Streamlit Community Cloud

You can host this application online for free using **Streamlit Community Cloud** by following these steps:

### Step 1: Push Project to GitHub
1. Create a new repository on your GitHub account (e.g., `Expense-Tracker-Pro`).
2. Push this local directory to your new GitHub repository:
   ```bash
   git init
   git add .
   git commit -m "Convert project to Streamlit dashboard"
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
   git branch -M main
   git push -u origin main
   ```

### Step 2: Sign Up & Connect to Streamlit
1. Go to [share.streamlit.io](https://share.streamlit.io/).
2. Log in using your GitHub account.

### Step 3: Deploy the App
1. Click the **"New app"** button.
2. Select your repository (`YOUR_USERNAME/YOUR_REPOSITORY`), the branch (`main`), and set the main file path to `app.py`.
3. Click **"Deploy!"**

Streamlit will automatically detect your `requirements.txt` file, install the necessary Python packages, apply the theme settings from `.streamlit/config.toml`, and run your app. Within 1–2 minutes, your dashboard will be live at a public URL (e.g., `https://your-app-name.streamlit.app`)!

---

⭐ If you find this project helpful, give it a star on GitHub!