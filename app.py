import streamlit as st
from datetime import date
from database import init_db, add_bill, get_bills, delete_bill, update_bill

init_db()
st.title("Bill Tracker")

with st.form("add_bill_form", clear_on_submit=True):
    col1, col2, col3 = st.columns(3)
    name = col1.text_input("Bill Name")
    balance = col2.number_input("Balance", step=10.0)
    due_date = col3.date_input("Due Date")
    recurring = st.checkbox("Recurring?")
    autopay = st.checkbox("Autopay?")
    paid = st.checkbox("Paid?")
    submitted = st.form_submit_button("Add Bill")

if submitted:
    add_bill(name, balance, due_date, recurring, autopay, paid)

st.subheader("Your Bills")
for bill in get_bills():
    bill_id = bill[0]
    bill_name = bill[1]
    bill_amount = bill[2]
    bill_due_date = date.fromisoformat(bill[3])
    bill_recurring = bill[4]
    bill_autopay = bill[5]
    bill_paid = bill[6]

    edit_key = f"editing_{bill_id}"
    if edit_key not in st.session_state:
        st.session_state[edit_key] = False

    if st.session_state[edit_key]:
        with st.form(f"edit_form_{bill_id}"):
            col1, col2, col3 = st.columns(3)
            new_name = col1.text_input("Name", value=bill_name)
            new_amount = col2.number_input("Amount", value=bill_amount)
            new_due_date = col3.date_input("Due Date", value=bill_due_date)
            new_recurring = st.checkbox("Recurring?", value=bool(bill_recurring))
            new_autopay = st.checkbox("Autopay?", value=bool(bill_autopay))
            new_paid = st.checkbox("Paid?", value=bool(bill_paid))
            saved = st.form_submit_button("Save")
        if saved:
            update_bill(bill_id, new_name, new_amount, new_due_date, new_recurring, new_autopay, new_paid)
            st.session_state[edit_key] = False
            st.rerun()

    else:
        today = date.today()
        # Name, Amount, Recurring, Autopay, Due, Edit, Delete, Paid
        col1, col2, col3, col4, col5, col6, col7, col8 = st.columns([2, 0.7, 0.3, 0.3, 1.5, .7, 1, 0.3])
        col1.write(f"{bill_name} ({bill_due_date})")
        col2.write(f"${bill_amount:,.2f}")

        if bill_paid:
            col8.write("✅")

        if bill_recurring:
            col3.write("🔄")

        if bill_autopay:
            col4.write("🔁")

        if today < bill_due_date:
            datediff = (bill_due_date - today).days
            col5.success(f"Upcoming ({datediff} days)")
        elif today > bill_due_date:
            datediff = (today - bill_due_date).days
            col5.error(f"Overdue ({datediff} days)")
        else:
            col5.warning("Due Today")

        if col6.button("Edit", key=f"edit_{bill_id}"):
            st.session_state[edit_key] = True
            st.rerun()

        if col7.button("Delete", key=f"delete_{bill_id}"):
            delete_bill(bill_id)
            st.rerun()
