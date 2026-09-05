import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_local_storage import LocalStorage

# ---------------------------------------------------------------------------
# Streamlit app for Budget Tracker
# On directory, must run following command to run this file: `cd python-testing`
# When running this file, use: `streamlit run py_interface.py`
# Alternatively run as `cd python-testing && streamlit run py_interface.py`
# ---------------------------------------------------------------------------


# Import BudgetTracker from main_terminal.py (must be in the same directory)
from main_terminal import BudgetTracker

# ---------------------------------------------------------------------------
# Session state init — builds a BudgetTracker from localStorage data on first
# load so the in-memory tracker always reflects what the browser has saved.
# On the very first render localStorage returns None (browser hasn't responded
# yet); the app initializes with empty state and repopulates on the next cycle.
# ---------------------------------------------------------------------------

def rebuild_tracker(transactions: list, user: str) -> BudgetTracker:
    tracker = BudgetTracker()
    tracker.user = user
    for tx in transactions:
        if tx["type"] == "income":
            tracker.income += tx["amount"]
            tracker.add_one_deposit()
            tracker.each_transaction.append(tx["amount"])
        else:
            tracker.expenses += tx["amount"]
            tracker.add_one_tx()
            tracker.each_transaction.append(-tx["amount"])
    return tracker

# ---------------------------------------------------------------------------
# Initialization of a session state. Upload transactions, if any; otherwise 
# create a new session with an empty tracker and no transactions. 
# ---------------------------------------------------------------------------
def init_session_state(ls: LocalStorage):
    if "tracker" not in st.session_state:
        data = ls.getItem("budget_data") or {"user": "", "transactions": []}
        tracker = rebuild_tracker(data.get("transactions", []), data.get("user", ""))
        st.session_state.tracker = tracker
        st.session_state.transactions = data.get("transactions", [])

# ---------------------------------------------------------------------------
# Main app - runs at execution
# ---------------------------------------------------------------------------
def main():
    st.set_page_config(page_title="Budget Tracker", page_icon="💰", layout="wide")
    ls = LocalStorage()
    init_session_state(ls)
    tracker: BudgetTracker = st.session_state.tracker

    st.title("💰 Personal Budget Tracker")
    
    st.subheader("Your income and expenses visualized. ")

    # -----------------------------------------------------------------------
    # Sidebar — user settings + live budget summary
    # Also allows a user to input their name in a textbox.
    # -----------------------------------------------------------------------
    with st.sidebar:
        st.header("⚙️ Settings")
        name_input = st.text_input("Your Name", value=tracker.user)
        if name_input != tracker.user:
            tracker.user = name_input
            ls.setItem("budget_data", {
                "user": name_input,
                "transactions": st.session_state.transactions,
            })

        if tracker.user:
            st.write(f"Welcome, **{tracker.user}**!")

        st.divider()
        st.header("📊 Budget Summary")

        balance = tracker.income - tracker.expenses

        st.metric("Current Balance", f"${balance:,.2f}")
        st.metric("Total Income",    f"${tracker.income:,.2f}")
        st.metric("Total Expenses",  f"${tracker.expenses:,.2f}")

        st.divider()
        st.caption(
            f"Deposits recorded: {tracker.get_deposit_count()}  |  "
            f"Expenses recorded: {tracker.get_tx_count()}"
        )

    # -----------------------------------------------------------------------
    # Main content — two-column layout
    # -----------------------------------------------------------------------
    left, right = st.columns([1, 2], gap="large")

    # --- Left column: forms ------------------------------------------------
    with left:

        # Add transaction
        st.subheader("➕ Add Transaction")
        
        with st.form("add_transaction", clear_on_submit=True):
            tx_type    = st.radio("Type", ["Income", "Expense"], horizontal=True)
            description = st.text_input("Description")
            amount     = st.number_input("Amount ($)", min_value=0.01,
                                         step=0.01, format="%.2f")
            category   = st.selectbox(
                "Category",
                ["Income", "Food", "Transport", "Bills",
                 "Entertainment", "Health", "Savings", "Other"],
            )
            submitted = st.form_submit_button("Add Transaction",
                                              use_container_width=True)

        if submitted:
            if amount > 0:
                tx = {
                    "type":        tx_type.lower(),
                    "description": description or "(no description)",
                    "amount":      amount,
                    "category":    category,
                }
                if tx_type == "Income":
                    tracker.add_income(amount)
                else:
                    tracker.add_expense(amount)

                st.session_state.transactions.append(tx)
                ls.setItem("budget_data", {
                    "user": tracker.user,
                    "transactions": st.session_state.transactions,
                })

                st.success(f"{'Deposit' if tx_type == 'Income' else 'Expense'} "
                           f"of **${amount:,.2f}** added!")
                st.rerun()
            else:
                st.error("Amount must be greater than $0.")

        st.divider()

        # Remove most-recent matching expense
        st.subheader("🗑️ Remove Expense")
        with st.form("remove_expense", clear_on_submit=True):
            remove_amount = st.number_input("Amount to Remove ($)", min_value=0.01,
                                            step=0.01, format="%.2f")
            remove_submitted = st.form_submit_button("Remove Expense",
                                                     use_container_width=True)

        if remove_submitted:
            if tracker.expenses > 0 and tracker.tx_count > 0:
                tracker.remove_expense(remove_amount)
                for i in range(len(st.session_state.transactions) - 1, -1, -1):
                    tx = st.session_state.transactions[i]
                    if tx["type"] == "expense" and tx["amount"] == remove_amount:
                        st.session_state.transactions.pop(i)
                        break
                ls.setItem("budget_data", {
                    "user": tracker.user,
                    "transactions": st.session_state.transactions,
                })
                st.success(f"Removed expense of **${remove_amount:,.2f}**.")
                st.rerun()
            else:
                st.error("No expenses to remove.")

    # --- Right column: charts ----------------------------------------------
    with right:
        st.subheader("📈 Budget Overview")

        if tracker.income > 0 or tracker.expenses > 0:
            fig_bar = go.Figure(data=[
                go.Bar(x=["Income"],   y=[tracker.income],   name="Income",
                       marker_color="mediumseagreen"),
                go.Bar(x=["Expenses"], y=[tracker.expenses], name="Expenses",
                       marker_color="tomato"),
            ])
            fig_bar.update_layout(
                title="Income vs Expenses",
                yaxis_title="Amount ($)",
                showlegend=False,
                height=320,
                margin=dict(t=40, b=20),
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("Add transactions to see your budget chart.")

        if st.session_state.transactions:
            df = pd.DataFrame(st.session_state.transactions)
            expenses_df = df[df["type"] == "expense"]
            if not expenses_df.empty:
                fig_pie = px.pie(
                    expenses_df,
                    values="amount",
                    names="category",
                    title="Expenses by Category",
                    height=320,
                )
                fig_pie.update_layout(margin=dict(t=40, b=20))
                st.plotly_chart(fig_pie, use_container_width=True)

    # -----------------------------------------------------------------------
    # Transaction history table — full width below the two columns
    # -----------------------------------------------------------------------
    st.divider()
    st.subheader("🧾 Transaction History")

    if st.session_state.transactions:
        df = pd.DataFrame(st.session_state.transactions)

        df["display_amount"] = df.apply(
            lambda row: f"+${row['amount']:,.2f}"
            if row["type"] == "income"
            else f"-${row['amount']:,.2f}",
            axis=1,
        )

        display_df = df[["type", "description", "category", "display_amount"]].copy()
        display_df.columns = ["Type", "Description", "Category", "Amount"]
        display_df["Type"] = display_df["Type"].str.capitalize()
        display_df.insert(0, "Delete", False)

        edited_df = st.data_editor(
            display_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Delete": st.column_config.CheckboxColumn("🗑️", default=False)
            },
            disabled=["Type", "Description", "Category", "Amount"],
        )

        btn_col1, btn_col2 = st.columns([1, 1])
        with btn_col1:
            if st.button("Delete Selected", use_container_width=True):
                rows_to_delete = edited_df[edited_df["Delete"]].index.tolist()
                if rows_to_delete:
                    for i in sorted(rows_to_delete, reverse=True):
                        st.session_state.transactions.pop(i)
                    st.session_state.tracker = rebuild_tracker(
                        st.session_state.transactions, tracker.user
                    )
                    ls.setItem("budget_data", {
                        "user": tracker.user,
                        "transactions": st.session_state.transactions,
                    })
                    st.success(f"Deleted {len(rows_to_delete)} transaction(s).")
                    st.rerun()
                else:
                    st.warning("No rows selected — check the 🗑️ box on any row first.")

        with btn_col2:
            if st.button("Clear All Transactions", type="primary", use_container_width=True):
                st.session_state.confirm_clear = True
                st.rerun()

        if st.session_state.get("confirm_clear"):
            st.warning("This will permanently delete all transactions. Are you sure?")
            yes_col, no_col, _ = st.columns([1, 1, 4])
            with yes_col:
                if st.button("Yes, clear all", type="primary", use_container_width=True):
                    st.session_state.transactions = []
                    st.session_state.tracker = rebuild_tracker([], tracker.user)
                    ls.setItem("budget_data", {
                        "user": tracker.user,
                        "transactions": [],
                    })
                    st.session_state.confirm_clear = False
                    st.success("All transactions cleared.")
                    st.rerun()
            with no_col:
                if st.button("Cancel", use_container_width=True):
                    st.session_state.confirm_clear = False
                    st.rerun()
    else:
        st.info("No transactions yet — add one above to get started!")


if __name__ == "__main__":
    main()
