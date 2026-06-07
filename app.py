import streamlit as st
import pandas as pd
import json
import os
import plotly.express as px
import plotly.graph_objects as go
from datetime import date, datetime

# Page configuration
st.set_page_config(
    page_title="ExpenseTracker Pro",
    page_icon="💸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling the dashboard
st.markdown("""
<style>
    /* Gradient headers */
    .main-header {
        font-family: 'Outfit', 'Inter', sans-serif;
        background: linear-gradient(135deg, #10B981 0%, #3B82F6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 2.8rem;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-family: 'Inter', sans-serif;
        color: #94A3B8;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    /* Styled Metric Cards */
    div[data-testid="stMetric"] {
        background: #1E293B;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 15px 20px;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
        transition: transform 0.2s, border-color 0.2s;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        border-color: #10B981;
    }
    
    /* Sidebar styling tweaks */
    section[data-testid="stSidebar"] {
        background-color: #0F172A;
        border-right: 1px solid #1E293B;
    }
    
    /* Alert details */
    .status-warning {
        padding: 10px;
        background-color: rgba(245, 158, 11, 0.1);
        border-left: 4px solid #F59E0B;
        color: #F59E0B;
        border-radius: 4px;
        margin-bottom: 1rem;
    }
    .status-danger {
        padding: 10px;
        background-color: rgba(239, 68, 68, 0.1);
        border-left: 4px solid #EF4444;
        color: #EF4444;
        border-radius: 4px;
        margin-bottom: 1rem;
    }
    .status-ok {
        padding: 10px;
        background-color: rgba(16, 185, 129, 0.1);
        border-left: 4px solid #10B981;
        color: #10B981;
        border-radius: 4px;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Data Persistence Functions
EXPENSE_FILE = "expense_tracker_d1.json"
BUDGET_FILE = "expense_budget.json"

def load_data():
    # Load Expenses
    if "expenses" not in st.session_state:
        if os.path.exists(EXPENSE_FILE):
            try:
                with open(EXPENSE_FILE, "r") as file:
                    st.session_state["expenses"] = json.load(file)
            except Exception:
                st.session_state["expenses"] = []
        else:
            st.session_state["expenses"] = []
            
    # Load Budget
    if "budget" not in st.session_state:
        if os.path.exists(BUDGET_FILE):
            try:
                with open(BUDGET_FILE, "r") as file:
                    budget_data = json.load(file)
                    st.session_state["budget"] = float(budget_data.get("Budget", 0.0))
            except Exception:
                st.session_state["budget"] = 0.0
        else:
            st.session_state["budget"] = 0.0

def save_expenses():
    try:
        with open(EXPENSE_FILE, "w") as file:
            json.dump(st.session_state["expenses"], file, indent=4)
    except Exception as e:
        st.error(f"Error saving expenses: {e}")

def save_budget():
    try:
        with open(BUDGET_FILE, "w") as file:
            json.dump({"Budget": st.session_state["budget"]}, file, indent=4)
    except Exception as e:
        st.error(f"Error saving budget: {e}")

# Initialize Data
load_data()

# ----------------- SIDEBAR -----------------
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/wallet.png", width=80)
    st.markdown("### **Expense Tracker Controls**")
    
    # Budget Section
    st.subheader("🎯 Monthly Budget Settings")
    new_budget = st.number_input(
        "Set Monthly Budget (₹)",
        min_value=0.0,
        value=st.session_state["budget"],
        step=500.0,
        format="%.2f"
    )
    
    if new_budget != st.session_state["budget"]:
        st.session_state["budget"] = new_budget
        save_budget()
        st.toast(f"Budget updated to ₹{new_budget:,.2f}! 🔒")
        st.rerun()

    st.markdown("---")
    
    # Add Expense Form
    st.subheader("➕ Add New Expense")
    with st.form("add_expense_form", clear_on_submit=True):
        exp_name = st.text_input("Expense Name", placeholder="Zomato Order, Rent, etc.").strip()
        exp_amount = st.number_input("Amount (₹)", min_value=0.0, step=10.0, format="%.2f")
        
        categories = ["Food", "Shopping", "Bills", "Transport", "Entertainment", "Health", "Education", "Travel", "Custom"]
        exp_category = st.selectbox("Category", categories)
        
        custom_cat = ""
        if exp_category == "Custom":
            custom_cat = st.text_input("Enter Custom Category").strip()
            
        exp_date = st.date_input("Date", value=date.today())
        
        submit_btn = st.form_submit_button("Add Expense ✅")
        
        if submit_btn:
            if not exp_name:
                st.error("Expense Name is required!")
            elif exp_amount <= 0:
                st.error("Amount must be greater than 0!")
            elif exp_category == "Custom" and not custom_cat:
                st.error("Please specify custom category!")
            else:
                final_cat = custom_cat.title() if exp_category == "Custom" else exp_category.title()
                new_expense = {
                    "Name": exp_name.title(),
                    "Amount": float(exp_amount),
                    "Category": final_cat,
                    "Date": str(exp_date)
                }
                st.session_state["expenses"].append(new_expense)
                save_expenses()
                st.toast(f"Added {exp_name} (₹{exp_amount:,.2f})! 💸")
                st.rerun()

# ----------------- MAIN LAYOUT -----------------
st.markdown('<div class="main-header">ExpenseTracker Pro</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Premium Financial Analytics & Real-Time Spending Insights</div>', unsafe_allow_html=True)

# Calculate metrics
expenses_list = st.session_state["expenses"]
total_spent = sum(item["Amount"] for item in expenses_list)
budget = st.session_state["budget"]
remaining_budget = budget - total_spent
num_expenses = len(expenses_list)

# Alerting Banner
if budget > 0:
    pct_used = (total_spent / budget) * 100
    if pct_used >= 100:
        st.markdown(f'<div class="status-danger">⚠️ <strong>Budget Exceeded!</strong> You have overspent by ₹{abs(remaining_budget):,.2f} ({pct_used:.1f}% used).</div>', unsafe_allow_html=True)
    elif pct_used >= 85:
        st.markdown(f'<div class="status-warning">⚠️ <strong>Approaching Budget Limit!</strong> You have used {pct_used:.1f}% of your budget. Remaining: ₹{remaining_budget:,.2f}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="status-ok">✅ <strong>Under Budget:</strong> You have used {pct_used:.1f}% of your budget. Remaining: ₹{remaining_budget:,.2f}</div>', unsafe_allow_html=True)

# Key KPI Cards
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="💸 Total Spending", value=f"₹{total_spent:,.2f}")
with col2:
    st.metric(label="🎯 Monthly Budget", value=f"₹{budget:,.2f}")
with col3:
    delta_color = "normal" if remaining_budget >= 0 else "inverse"
    st.metric(
        label="💰 Remaining Budget", 
        value=f"₹{remaining_budget:,.2f}", 
        delta=f"{'Over' if remaining_budget < 0 else 'Under'} Budget",
        delta_color=delta_color
    )
with col4:
    st.metric(label="🗓️ Total Transactions", value=str(num_expenses))

# Setup Tab views
tab1, tab2, tab3 = st.tabs(["📊 Analytics Overview", "⚙️ Manage Expenses", "📅 Reports & Insights"])

# ----------------- TAB 1: OVERVIEW -----------------
with tab1:
    if not expenses_list:
        st.info("💡 No expenses found. Use the sidebar to add your first expense!")
    else:
        # Visual row 1
        vcol1, vcol2 = st.columns([1, 1])
        df = pd.DataFrame(expenses_list)
        df["Date"] = pd.to_datetime(df["Date"])
        
        with vcol1:
            st.subheader("🍕 Category Breakdown")
            category_df = df.groupby("Category")["Amount"].sum().reset_index()
            fig_pie = px.pie(
                category_df, 
                values="Amount", 
                names="Category", 
                hole=0.45,
                color_discrete_sequence=px.colors.qualitative.Bold
            )
            fig_pie.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_color="#F8FAFC",
                margin=dict(l=10, r=10, t=10, b=10),
                legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
            )
            st.plotly_chart(fig_pie, use_container_width=True)
            
        with vcol2:
            st.subheader("📈 Budget Utilization Gauge")
            if budget > 0:
                fig_gauge = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = total_spent,
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    gauge = {
                        'axis': {'range': [None, max(budget, total_spent)], 'tickcolor': "#F8FAFC"},
                        'bar': {'color': "#10B981" if total_spent <= budget else "#EF4444"},
                        'bgcolor': "#1E293B",
                        'borderwidth': 1,
                        'bordercolor': "#334155",
                        'steps': [
                            {'range': [0, budget], 'color': 'rgba(16, 185, 129, 0.1)'},
                            {'range': [budget, max(budget, total_spent)], 'color': 'rgba(239, 68, 68, 0.25)'}
                        ],
                        'threshold': {
                            'line': {'color': "#EF4444", 'width': 4},
                            'thickness': 0.75,
                            'value': budget
                        }
                    }
                ))
                fig_gauge.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    font={'color': "#F8FAFC", 'family': "sans-serif"},
                    height=280,
                    margin=dict(l=20, r=20, t=40, b=20)
                )
                st.plotly_chart(fig_gauge, use_container_width=True)
            else:
                st.warning("Please set a monthly budget in the sidebar to view utilization metrics.")
        
        # Visual row 2 (Spending Trends)
        st.markdown("---")
        st.subheader("📅 Spending Trends Over Time")
        
        # Check date density
        date_df = df.groupby(df["Date"].dt.date)["Amount"].sum().reset_index()
        date_df = date_df.sort_values("Date")
        
        fig_trend = px.area(
            date_df,
            x="Date",
            y="Amount",
            labels={"Amount": "Daily Spent (₹)", "Date": "Date"},
            color_discrete_sequence=["#10B981"]
        )
        fig_trend.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color="#F8FAFC",
            xaxis=dict(showgrid=False, color="#94A3B8"),
            yaxis=dict(showgrid=True, gridcolor="#334155", color="#94A3B8"),
            margin=dict(l=10, r=10, t=10, b=10)
        )
        st.plotly_chart(fig_trend, use_container_width=True)

# ----------------- TAB 2: MANAGE EXPENSES -----------------
with tab2:
    st.subheader("📋 Expense Database")
    st.markdown("Double-click any cell to **edit** details, select a row and click 🗑️ (trash icon) to **delete**, or use the bottom blank row to **add** an expense.")
    
    if not expenses_list:
        df_empty = pd.DataFrame(columns=["Name", "Amount", "Category", "Date"])
        edited_df = st.data_editor(
            df_empty,
            num_rows="dynamic",
            use_container_width=True
        )
    else:
        df_manage = pd.DataFrame(expenses_list)
        df_manage["Date"] = pd.to_datetime(df_manage["Date"]).dt.date
        
        # Build Data Editor
        edited_df = st.data_editor(
            df_manage,
            num_rows="dynamic",
            use_container_width=True,
            column_config={
                "Name": st.column_config.TextColumn("Expense Name", required=True),
                "Amount": st.column_config.NumberColumn("Amount (₹)", min_value=0.0, format="₹%.2f", required=True),
                "Category": st.column_config.SelectboxColumn("Category", options=["Food", "Shopping", "Bills", "Transport", "Entertainment", "Health", "Education", "Travel", "Other"], required=True),
                "Date": st.column_config.DateColumn("Date", required=True)
            },
            key="db_editor"
        )
        
        # Check changes and save back
        if not edited_df.equals(df_manage):
            # Clean dataframe: drop rows with NaNs/None in Name or Amount
            cleaned_df = edited_df.dropna(subset=["Name", "Amount"])
            cleaned_df = cleaned_df[cleaned_df["Name"].str.strip() != ""]
            
            # Format and convert to dict records
            cleaned_df["Date"] = cleaned_df["Date"].astype(str)
            cleaned_df["Amount"] = cleaned_df["Amount"].astype(float)
            cleaned_df["Name"] = cleaned_df["Name"].str.title()
            cleaned_df["Category"] = cleaned_df["Category"].str.title()
            
            st.session_state["expenses"] = cleaned_df.to_dict(orient="records")
            save_expenses()
            st.toast("Expense database updated successfully! 💾")
            st.rerun()

    # CSV Exporter
    if expenses_list:
        st.markdown("---")
        df_export = pd.DataFrame(expenses_list)
        csv_data = df_export.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Export Expenses to CSV",
            data=csv_data,
            file_name="expenses.csv",
            mime="text/csv",
            key="csv_download"
        )

# ----------------- TAB 3: REPORTS & INSIGHTS -----------------
with tab3:
    if not expenses_list:
        st.info("💡 No data available to compile reports.")
    else:
        df_rep = pd.DataFrame(expenses_list)
        df_rep["DateObj"] = pd.to_datetime(df_rep["Date"])
        df_rep["YearMonth"] = df_rep["DateObj"].dt.strftime("%Y-%m")
        
        rcol1, rcol2 = st.columns([1, 1])
        
        with rcol1:
            st.subheader("🗓️ Monthly Expense Report")
            # Select month
            available_months = sorted(list(df_rep["YearMonth"].unique()), reverse=True)
            selected_month = st.selectbox("Select Month", available_months)
            
            # Filtered monthly data
            monthly_data = df_rep[df_rep["YearMonth"] == selected_month]
            
            # Show summary
            m_total = monthly_data["Amount"].sum()
            m_count = len(monthly_data)
            
            col_m1, col_m2 = st.columns(2)
            col_m1.metric("Spent in Month", f"₹{m_total:,.2f}")
            col_m2.metric("Total Transactions", str(m_count))
            
            # Display Table
            st.markdown(f"**Expenses in {selected_month}:**")
            st.dataframe(
                monthly_data[["Name", "Amount", "Category", "Date"]], 
                use_container_width=True,
                hide_index=True
            )
            
        with rcol2:
            st.subheader("🔍 Search & Sorting")
            
            # Search
            search_query = st.text_input("🔎 Search by Expense Name", "").strip().lower()
            
            # Sort Options
            sort_by = st.selectbox("Sort By", ["Date (Newest First)", "Date (Oldest First)", "Amount (Highest First)", "Amount (Lowest First)"])
            
            # Filter/Sort Logic
            filtered_df = df_rep.copy()
            if search_query:
                filtered_df = filtered_df[filtered_df["Name"].str.lower().str.contains(search_query)]
            
            if sort_by == "Date (Newest First)":
                filtered_df = filtered_df.sort_values("DateObj", ascending=False)
            elif sort_by == "Date (Oldest First)":
                filtered_df = filtered_df.sort_values("DateObj", ascending=True)
            elif sort_by == "Amount (Highest First)":
                filtered_df = filtered_df.sort_values("Amount", ascending=False)
            elif sort_by == "Amount (Lowest First)":
                filtered_df = filtered_df.sort_values("Amount", ascending=True)
                
            st.dataframe(
                filtered_df[["Name", "Amount", "Category", "Date"]],
                use_container_width=True,
                hide_index=True
            )
            
        st.markdown("---")
        st.subheader("📈 Spending Extremes & Analytics")
        
        ext_col1, ext_col2 = st.columns(2)
        
        # Highest
        highest_idx = df_rep["Amount"].idxmax()
        highest_exp = df_rep.loc[highest_idx]
        with ext_col1:
            st.markdown(
                f"""
                <div style="background: rgba(239, 68, 68, 0.05); border: 1px solid rgba(239, 68, 68, 0.3); border-radius: 12px; padding: 20px;">
                    <h4 style="color:#EF4444; margin-top:0;">🏆 Highest Expense Record</h4>
                    <p style="font-size: 1.5rem; font-weight: 700; margin: 5px 0;">₹{highest_exp['Amount']:,.2f}</p>
                    <p style="margin: 0; color: #94A3B8;"><strong>Name:</strong> {highest_exp['Name']}</p>
                    <p style="margin: 0; color: #94A3B8;"><strong>Category:</strong> {highest_exp['Category']}</p>
                    <p style="margin: 0; color: #94A3B8;"><strong>Date:</strong> {highest_exp['Date']}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            
        # Lowest
        lowest_idx = df_rep["Amount"].idxmin()
        lowest_exp = df_rep.loc[lowest_idx]
        with ext_col2:
            st.markdown(
                f"""
                <div style="background: rgba(16, 185, 129, 0.05); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 12px; padding: 20px;">
                    <h4 style="color:#10B981; margin-top:0;">📉 Lowest Expense Record</h4>
                    <p style="font-size: 1.5rem; font-weight: 700; margin: 5px 0;">₹{lowest_exp['Amount']:,.2f}</p>
                    <p style="margin: 0; color: #94A3B8;"><strong>Name:</strong> {lowest_exp['Name']}</p>
                    <p style="margin: 0; color: #94A3B8;"><strong>Category:</strong> {lowest_exp['Category']}</p>
                    <p style="margin: 0; color: #94A3B8;"><strong>Date:</strong> {lowest_exp['Date']}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
