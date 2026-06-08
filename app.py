import streamlit as st
import pandas as pd
import json
import os
import plotly.express as px
from datetime import date

# 1. Page Configuration (Title and Icon in Browser)
st.set_page_config(
    page_title="Expense Tracker",
    page_icon="💸",
    layout="wide"
)

# 2. Files where data is stored (matching CLI main.py)
EXPENSE_FILE = "expense_tracker_d1.json"
BUDGET_FILE = "expense_budget.json"

# Helper: Load data from JSON files into Streamlit's session state
def load_data():
    if "expenses" not in st.session_state:
        if os.path.exists(EXPENSE_FILE):
            try:
                with open(EXPENSE_FILE, "r") as file:
                    st.session_state["expenses"] = json.load(file)
            except Exception:
                st.session_state["expenses"] = []
        else:
            st.session_state["expenses"] = []

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

# Helper: Save expenses to JSON file
def save_expenses():
    with open(EXPENSE_FILE, "w") as file:
        json.dump(st.session_state["expenses"], file, indent=4)

# Helper: Save budget to JSON file
def save_budget():
    with open(BUDGET_FILE, "w") as file:
        json.dump({"Budget": st.session_state["budget"]}, file, indent=4)

# Load data when app starts
load_data()

# ----------------- APP HEADER -----------------
st.title("💸 Personal Expense Tracker")
st.write("Manage your daily expenses, monitor your monthly budget, and view visual spending analytics.")
st.markdown("---")

# ----------------- SIDEBAR: ADD EXPENSES & BUDGET -----------------
with st.sidebar:
    st.header("⚙️ Settings & Inputs")
    
    # Section A: Set Monthly Budget
    st.subheader("🎯 Monthly Budget")
    new_budget = st.number_input(
        "Enter Monthly Budget (₹)",
        min_value=0.0,
        value=st.session_state["budget"],
        step=100.0
    )
    if new_budget != st.session_state["budget"]:
        st.session_state["budget"] = new_budget
        save_budget()
        st.success(f"Budget updated to ₹{new_budget:,.2f}!")
        st.rerun()
        
    st.markdown("---")
    
    # Section B: Form to Add New Expense
    st.subheader("➕ Add New Expense")
    with st.form("expense_form", clear_on_submit=True):
        name = st.text_input("Expense Name", placeholder="e.g. Pizza, Petrol, Rent").strip()
        amount = st.number_input("Amount (₹)", min_value=0.0, step=10.0)
        category = st.selectbox(
            "Category", 
            ["Food", "Shopping", "Transport", "Bills", "Entertainment", "Health", "Education", "Other"]
        )
        expense_date = st.date_input("Date", value=date.today())
        
        submit_button = st.form_submit_button("Add Expense")
        
        if submit_button:
            if not name:
                st.error("Please enter a name for the expense.")
            elif amount <= 0:
                st.error("Amount must be greater than 0.")
            else:
                # Append the new expense dictionary to the database list
                new_item = {
                    "Name": name.title(),
                    "Amount": float(amount),
                    "Category": category,
                    "Date": str(expense_date)
                }
                st.session_state["expenses"].append(new_item)
                save_expenses()
                st.success(f"Added '{name}' of ₹{amount:,.2f} successfully!")
                st.rerun()

# ----------------- MAIN INTERFACE -----------------

# Calculations for metrics
expenses_list = st.session_state["expenses"]
total_spent = sum(item["Amount"] for item in expenses_list)
budget = st.session_state["budget"]
remaining_budget = budget - total_spent
num_expenses = len(expenses_list)

# Budget limit alert banners
if budget > 0:
    if total_spent > budget:
        st.error(f"⚠️ **Budget Exceeded!** You are over budget by ₹{abs(remaining_budget):,.2f}.")
    elif total_spent >= budget * 0.85:
        st.warning(f"⚠️ **Warning:** You have used over 85% of your budget. Remaining: ₹{remaining_budget:,.2f}")
    else:
        st.success(f"✅ **Under Budget:** You have ₹{remaining_budget:,.2f} left for the month.")

# Top Metrics Row
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Spent", f"₹{total_spent:,.2f}")
with col2:
    st.metric("Monthly Budget", f"₹{budget:,.2f}")
with col3:
    st.metric("Remaining Budget", f"₹{remaining_budget:,.2f}")
with col4:
    st.metric("Number of Expenses", str(num_expenses))

st.markdown("---")

# If there is no data, prompt the user
if not expenses_list:
    st.info("No expenses added yet. Use the left sidebar to add your first expense!")
else:
    # Convert list of dicts to a pandas DataFrame for sorting, filtering, and charts
    df = pd.DataFrame(expenses_list)
    df["Date"] = pd.to_datetime(df["Date"])
    
    # Create two main tabs: 1. Dashboard & Reports, 2. Manage Database
    tab_dashboard, tab_manage = st.tabs(["📊 Dashboard & Analytics", "✏️ Edit & Delete Data"])
    
    # ----------------- TAB 1: DASHBOARD & ANALYTICS -----------------
    with tab_dashboard:
        # Row 1: Charts
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            st.subheader("🍕 Spending by Category")
            # Group by category and sum amounts
            category_data = df.groupby("Category")["Amount"].sum().reset_index()
            fig = px.pie(
                category_data, 
                values="Amount", 
                names="Category", 
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            # Make chart background transparent to fit the theme
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="#F8FAFC")
            st.plotly_chart(fig, use_container_width=True)
            
        with col_chart2:
            st.subheader("📅 Spending Over Time")
            # Group by date to show daily totals
            daily_data = df.groupby(df["Date"].dt.date)["Amount"].sum().reset_index()
            # Rename columns for simple streamlit line chart compatibility
            daily_data = daily_data.set_index("Date")
            st.line_chart(daily_data["Amount"])
            
        st.markdown("---")
        
        # Row 2: Search, Sort, and Extremes
        col_search, col_extremes = st.columns(2)
        
        with col_search:
            st.subheader("🔍 Search & Filter Expenses")
            
            # Simple Search Bar
            search_query = st.text_input("Search expense by name:", "").strip().lower()
            
            # Simple Sort selector
            sort_option = st.selectbox(
                "Sort by:", 
                ["Date (Newest First)", "Date (Oldest First)", "Amount (Highest First)", "Amount (Lowest First)"]
            )
            
            # Filter and sort the dataframe
            filtered_df = df.copy()
            if search_query:
                filtered_df = filtered_df[filtered_df["Name"].str.lower().str.contains(search_query)]
                
            if sort_option == "Date (Newest First)":
                filtered_df = filtered_df.sort_values("Date", ascending=False)
            elif sort_option == "Date (Oldest First)":
                filtered_df = filtered_df.sort_values("Date", ascending=True)
            elif sort_option == "Amount (Highest First)":
                filtered_df = filtered_df.sort_values("Amount", ascending=False)
            elif sort_option == "Amount (Lowest First)":
                filtered_df = filtered_df.sort_values("Amount", ascending=True)
            
            # Clean date format for display
            display_df = filtered_df.copy()
            display_df["Date"] = display_df["Date"].dt.strftime("%Y-%m-%d")
            st.dataframe(display_df[["Name", "Amount", "Category", "Date"]], use_container_width=True, hide_index=True)
            
        with col_extremes:
            st.subheader("💡 Financial Insights")
            
            # Find Highest and Lowest Expenses
            highest_exp = df.loc[df["Amount"].idxmax()]
            lowest_exp = df.loc[df["Amount"].idxmin()]
            
            st.info(
                f"🏆 **Highest Expense:**\n\n"
                f"*   **Name:** {highest_exp['Name']}\n"
                f"*   **Amount:** ₹{highest_exp['Amount']:,.2f}\n"
                f"*   **Category:** {highest_exp['Category']}\n"
                f"*   **Date:** {highest_exp['Date'].strftime('%Y-%m-%d')}"
            )
            
            st.info(
                f"📉 **Lowest Expense:**\n\n"
                f"*   **Name:** {lowest_exp['Name']}\n"
                f"*   **Amount:** ₹{lowest_exp['Amount']:,.2f}\n"
                f"*   **Category:** {lowest_exp['Category']}\n"
                f"*   **Date:** {lowest_exp['Date'].strftime('%Y-%m-%d')}"
            )
            
            # Export to CSV
            st.markdown(" ")
            csv_data = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 Export All to CSV",
                data=csv_data,
                file_name="expenses.csv",
                mime="text/csv",
                use_container_width=True
            )

    # ----------------- TAB 2: EDIT & DELETE DATABASE -----------------
    with tab_manage:
        st.subheader("📝 Edit or Delete Database Records")
        st.write("Double-click any cell to edit it. To delete row(s), select them and click the trash 🗑️ icon at the top right of the table.")
        
        # Prepare dates as simple strings for data editor compat
        df_editor = df.copy()
        df_editor["Date"] = df_editor["Date"].dt.date
        
        # Use data editor to allow user to add, edit, or delete rows
        edited_df = st.data_editor(
            df_editor,
            num_rows="dynamic",
            use_container_width=True,
            column_config={
                "Name": st.column_config.TextColumn("Name", required=True),
                "Amount": st.column_config.NumberColumn("Amount (₹)", min_value=0.0, format="₹%.2f", required=True),
                "Category": st.column_config.SelectboxColumn(
                    "Category", 
                    options=["Food", "Shopping", "Transport", "Bills", "Entertainment", "Health", "Education", "Other"],
                    required=True
                ),
                "Date": st.column_config.DateColumn("Date", required=True)
            }
        )
        
        # Check if the database has changed, and save the updates
        if not edited_df.equals(df_editor):
            # Remove any empty/null rows that were created accidentally
            cleaned_df = edited_df.dropna(subset=["Name", "Amount"])
            cleaned_df = cleaned_df[cleaned_df["Name"].str.strip() != ""]
            
            # Convert format back to dict format
            cleaned_df["Date"] = cleaned_df["Date"].astype(str)
            cleaned_df["Amount"] = cleaned_df["Amount"].astype(float)
            cleaned_df["Name"] = cleaned_df["Name"].str.title()
            
            # Save and update session state
            st.session_state["expenses"] = cleaned_df.to_dict(orient="records")
            save_expenses()
            st.toast("Database changes saved! 💾")
            st.rerun()
