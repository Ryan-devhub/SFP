import streamlit as st
from datetime import datetime

st.set_page_config(layout="wide", page_title="Trading Platform")

# --- Predefined item list ---
ITEMS = [
    "Sword", "Shield", "Potion", "Helmet", "Armor", "Ring", "Amulet", "Bow", "Arrow", "Staff"
]

# --- Initialize session state variables ---
if "trades" not in st.session_state:
    st.session_state.trades = {}

# Migration: convert old 'wanted_item' keys to 'wanted_items' list
for trade_id, trade in st.session_state.trades.items():
    if "wanted_item" in trade and "wanted_items" not in trade:
        trade["wanted_items"] = [trade.pop("wanted_item")]

if "notifications" not in st.session_state:
    # notifications: username -> list of offers {trade_id, from_user, message, accepted (bool), rejected (bool), chat_started (bool), chat_log}
    st.session_state.notifications = {}

if "trade_history" not in st.session_state:
    # trade_history: username -> list of completed trades {trade_id, chat_log, users_involved}
    st.session_state.trade_history = {}

if "trade_counter" not in st.session_state:
    st.session_state.trade_counter = 0

if "offer_counter" not in st.session_state:
    st.session_state.offer_counter = 0

# Helper functions
def add_trade(poster, items, value, description, wanted_items):
    trade_id = st.session_state.trade_counter
    st.session_state.trade_counter += 1
    st.session_state.trades[trade_id] = {
        "poster": poster,
        "items": items,
        "value": value,
        "description": description,
        "wanted_items": wanted_items,
        "offers": {},  # offer_id -> offer dict
        "status": "open",  # open, accepted, declined
    }
    return trade_id


def add_offer(trade_id, from_user, message):
    offer_id = st.session_state.offer_counter
    st.session_state.offer_counter += 1
    offer = {
        "offer_id": offer_id,
        "from_user": from_user,
        "message": message,
        "accepted": False,
        "rejected": False,
        "chat_started": False,
        "chat_log": [],  # {sender, message, timestamp}
        "accept_confirmed": {from_user: False, "poster": False},  # to track chat accept buttons
        "status": "pending",  # pending, accepted, rejected, terminated
    }
    st.session_state.trades[trade_id]["offers"][offer_id] = offer

    # Add notification for the poster
    poster = st.session_state.trades[trade_id]["poster"]
    if poster not in st.session_state.notifications:
        st.session_state.notifications[poster] = {}
    st.session_state.notifications[poster][offer_id] = {
        "trade_id": trade_id,
        "from_user": from_user,
        "message": message,
        "offer_id": offer_id,
        "accepted": False,
        "rejected": False,
        "chat_started": False,
        "chat_log": [],
        "accept_confirmed": {from_user: False, poster: False},
        "status": "pending",
    }

def add_chat_message(trade_id, offer_id, sender, message):
    chat_entry = {
        "sender": sender,
        "message": message,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    # Update in trades
    st.session_state.trades[trade_id]["offers"][offer_id]["chat_log"].append(chat_entry)
    # Update in notifications (if exists)
    poster = st.session_state.trades[trade_id]["poster"]
    if poster in st.session_state.notifications and offer_id in st.session_state.notifications[poster]:
        st.session_state.notifications[poster][offer_id]["chat_log"].append(chat_entry)

def end_chat(trade_id, offer_id, rejected=True):
    # Mark offer and trade as rejected or terminated
    st.session_state.trades[trade_id]["offers"][offer_id]["status"] = "rejected" if rejected else "terminated"
    poster = st.session_state.trades[trade_id]["poster"]
    if poster in st.session_state.notifications and offer_id in st.session_state.notifications[poster]:
        st.session_state.notifications[poster][offer_id]["status"] = "rejected" if rejected else "terminated"

def save_trade_history(trade_id, offer_id):
    trade = st.session_state.trades[trade_id]
    offer = trade["offers"][offer_id]
    users = [trade["poster"], offer["from_user"]]
    history_entry = {
        "trade_id": trade_id,
        "chat_log": offer["chat_log"],
        "users": users,
        "items": trade["items"],
        "value": trade["value"],
        "description": trade["description"],
        "wanted_items": trade["wanted_items"],
    }
    for user in users:
        if user not in st.session_state.trade_history:
            st.session_state.trade_history[user] = []
        st.session_state.trade_history[user].append(history_entry)
    # Mark trade and offer as accepted
    trade["status"] = "accepted"
    offer["status"] = "accepted"
    # Remove notification
    poster = trade["poster"]
    if poster in st.session_state.notifications and offer_id in st.session_state.notifications[poster]:
        del st.session_state.notifications[poster][offer_id]

def clear_notification(poster, offer_id):
    if poster in st.session_state.notifications and offer_id in st.session_state.notifications[poster]:
        del st.session_state.notifications[poster][offer_id]

# --- UI ---

st.title("Trading Platform")

# Current User input for simulation
current_user = st.text_input("Enter your username (simulate login)", key="current_user").strip()

if not current_user:
    st.warning("Please enter a username to continue.")
    st.stop()

# Tabs for Post Trade, Trades Feed, Notifications, Trade History
tabs = st.tabs(["Post Trade", "Trades Feed", "Trade Notifications", "Trade History"])

# ----------- POST TRADE TAB -----------
with tabs[0]:
    st.header("Post a Trade")

    trade_items = st.multiselect("Select item(s) you want to trade", ITEMS, key="trade_items")
    trade_value = st.number_input("Value (number)", min_value=0.0, step=1.0, key="trade_value")
    trade_description = st.text_area("Description", key="trade_description")
    wanted_items = st.multiselect("Item(s) you want in exchange", ITEMS, key="wanted_items")

if st.button("Post Trade"):
    if not trade_items:
        st.error("Please select at least one item to trade.")
    elif trade_value <= 0:
        st.error("Please enter a value greater than 0.")
    elif not wanted_items:
        st.error("Please select at least one item you want in exchange.")
    else:
        trade_id = add_trade(current_user, trade_items, trade_value, trade_description, wanted_items)
        st.success(f"Trade posted successfully! Trade ID: {trade_id}")

        # Clear inputs by rerunning:
        import streamlit.runtime.scriptrunner as scriptrunner
        raise scriptrunner.RerunException(scriptrunner.RerunData())


# ----------- TRADES FEED TAB -----------
with tabs[1]:
    st.header("Trades Feed")

    trades = st.session_state.trades

    if not trades:
        st.info("No trades posted yet.")
    else:
        # Display all trades except those posted by current user with "Make an offer" button
        for trade_id, trade in trades.items():
            poster = trade["poster"]
            items = trade["items"]
            value = trade["value"]
            description = trade["description"]
            wanted_items = trade["wanted_items"]
            status = trade["status"]

            # Container for each trade post
            with st.container():
                cols = st.columns([1, 1])
                with cols[0]:
                    st.markdown(f"### Trading by **{poster}**")
                    st.markdown(f"**Items:** {', '.join(items)}")
                    st.markdown(f"**Value:** {value}")
                    st.markdown(f"**Description:** {description}")
                with cols[1]:
                    st.markdown(f"### Wants")
                    st.markdown(f"**Items:** {', '.join(wanted_items)}")


                if poster != current_user and status == "open":
                    # Make an offer button
                    offer_key = f"make_offer_{trade_id}"
                    if st.button("Make an Offer", key=offer_key):
                        st.session_state[f"offer_modal_{trade_id}"] = True

                    # Show offer modal
                    if st.session_state.get(f"offer_modal_{trade_id}", False):
                        st.markdown("---")
                        st.markdown(f"**Make an offer on trade {trade_id}**")
                        offer_username = st.text_input("Your username", value=current_user, key=f"offer_username_{trade_id}")
                        offer_message = st.text_area("Message", key=f"offer_message_{trade_id}")
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button("Send Offer", key=f"send_offer_{trade_id}"):
                                if not offer_username.strip():
                                    st.error("Please enter your username.")
                                elif not offer_message.strip():
                                    st.error("Please enter a message.")
                                else:
                                    add_offer(trade_id, offer_username.strip(), offer_message.strip())
                                    st.success("Offer sent!")
                                    st.session_state[f"offer_modal_{trade_id}"] = False
                                    # Clear inputs
                                    st.session_state[f"offer_username_{trade_id}"] = ""
                                    st.session_state[f"offer_message_{trade_id}"] = ""
                        with col2:
                            if st.button("Cancel", key=f"cancel_offer_{trade_id}"):
                                st.session_state[f"offer_modal_{trade_id}"] = False
                                st.session_state[f"offer_username_{trade_id}"] = ""
                                st.session_state[f"offer_message_{trade_id}"] = ""

                elif poster == current_user:
                    if status == "open":
                        st.info("Your trade post. Waiting for offers...")
                    elif status == "accepted":
                        st.success("Trade completed.")
                    elif status == "declined":
                        st.error("Trade declined.")

                st.markdown("---")

# ----------- TRADE NOTIFICATIONS TAB -----------
with tabs[2]:
    st.header("Trade Notifications")

    notifications = st.session_state.notifications.get(current_user, {})

    if not notifications:
        st.info("No trade requests.")

    else:
        # Sidebar style closable trade notification box simulation
        # We'll list notifications with accept button to start chat
        to_remove = []
        for offer_id, notif in notifications.items():
            trade_id = notif["trade_id"]
            from_user = notif["from_user"]
            message = notif["message"]
            status = notif["status"]

            if status == "pending":
                with st.expander(f"Trade request from {from_user} (Offer ID: {offer_id})"):
                    st.markdown(f"**Message:** {message}")
                    col1, col2, col3 = st.columns([1,1,1])
                    with col1:
                        if st.button(f"Accept Offer {offer_id}"):
                            notif["accepted"] = True
                            notif["chat_started"] = True
                            # Update trade offer status
                            st.session_state.trades[trade_id]["offers"][offer_id]["accepted"] = True
                            st.session_state.trades[trade_id]["offers"][offer_id]["chat_started"] = True
                            notif["status"] = "accepted"
                    with col2:
                        if st.button(f"Reject Offer {offer_id}"):
                            notif["rejected"] = True
                            notif["status"] = "rejected"
                            # Mark offer rejected in trade data too
                            st.session_state.trades[trade_id]["offers"][offer_id]["status"] = "rejected"
                            to_remove.append(offer_id)
                    with col3:
                        if st.button(f"Close Notification {offer_id}"):
                            to_remove.append(offer_id)

            elif status == "accepted":
                st.success(f"Offer {offer_id} accepted. Chat started.")

                # Show chat box between poster and from_user
                chat_log = notif["chat_log"]
                chat_container = st.container()

                with chat_container:
                    for entry in chat_log:
                        sender = entry["sender"]
                        msg = entry["message"]
                        timestamp = entry["timestamp"]
                        st.markdown(f"**{sender}** ({timestamp}): {msg}")

                    # Message input
                    new_msg = st.text_input(f"Send message in chat with {from_user} (Offer {offer_id})", key=f"chat_input_{offer_id}")

                    if st.button(f"Send Message (Offer {offer_id})"):
                        if new_msg.strip():
                            add_chat_message(trade_id, offer_id, current_user, new_msg.strip())
                            st.experimental_rerun()
                        else:
                            st.warning("Enter a message to send.")

                    # Accept and Reject buttons for finalizing trade
                    col_acc, col_rej = st.columns(2)
                    with col_acc:
                        if st.button(f"Accept Trade (Offer {offer_id})"):
                            notif["accept_confirmed"][current_user] = True
                            offer = st.session_state.trades[trade_id]["offers"][offer_id]
                            # Check if both accepted
                            if all(notif["accept_confirmed"].values()):
                                save_trade_history(trade_id, offer_id)
                                st.success("Trade completed and saved to trade history.")
                                to_remove.append(offer_id)
                                st.experimental_rerun()
                            else:
                                st.info("Waiting for the other user to accept.")

                    with col_rej:
                        if st.button(f"Reject Trade (Offer {offer_id})"):
                            end_chat(trade_id, offer_id, rejected=True)
                            st.error("Trade rejected and chat terminated.")
                            to_remove.append(offer_id)
                            st.experimental_rerun()

            elif status == "rejected":
                st.error(f"Offer {offer_id} was rejected or trade terminated.")
                to_remove.append(offer_id)

        # Remove closed notifications
        for offer_id in to_remove:
            clear_notification(current_user, offer_id)

# ----------- TRADE HISTORY TAB -----------
with tabs[3]:
    st.header("Trade History")

    history = st.session_state.trade_history.get(current_user, [])

    if not history:
        st.info("No completed trades yet.")
    else:
        for entry in history:
            trade_id = entry["trade_id"]
            users = entry["users"]
            items = entry["items"]
            value = entry["value"]
            description = entry["description"]
            wanted_items = entry["wanted_items"]
            chat_log = entry["chat_log"]

            st.markdown(f"### Trade ID: {trade_id}")
            st.markdown(f"**Users involved:** {', '.join(users)}")
            st.markdown(f"**Items traded:** {', '.join(items)}")
            st.markdown(f"**Value:** {value}")
            st.markdown(f"**Description:** {description}")
            st.markdown(f"**Wanted Item:** {wanted_items}")
            st.markdown("**Chat log:**")
            for entry in chat_log:
                st.markdown(f"- **{entry['sender']}** ({entry['timestamp']}): {entry['message']}")
            st.markdown("---")
