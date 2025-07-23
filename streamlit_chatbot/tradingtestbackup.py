import streamlit as st
import pandas as pd
from datetime import datetime
import google.generativeai as genai
import json
import os

# Page config with blurred farm background
st.set_page_config(page_title="Grow a Garden App", layout="wide")
st.markdown(
    """
    <style>
    .main {
        background: url('https://images.unsplash.com/photo-1600585154340-be6161a56a0c?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80') no-repeat center center fixed;
        background-size: cover;
        backdrop-filter: blur(5px);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 6px 18px rgba(0,0,0,0.1);
        color: #2c3e50;
    }
    .stTitle {
        color: #ffffff;
        font-family: 'Arial', sans-serif;
        text-align: center;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .stSubheader {
        color: #ffffff;
        font-weight: bold;
        margin-top: 15px;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.2);
    }
    .stSelectbox, .stMultiselect, .stNumberInput, .stTextInput, .stTextArea {
        background-color: rgba(255, 255, 255, 0.9);
        border-radius: 10px;
        padding: 10px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
        margin-bottom: 12px;
        color: #2c3e50;
    }
    .results-card, .trade-card, .chat-card {
        background: linear-gradient(135deg, #f9e79f 0%, #f1c40f 50%, #e67e22 100%);
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.2);
        margin-top: 15px;
        animation: fadeIn 0.5s ease-in;
    }
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    .results-card h3, .trade-card h3, .chat-card h3 {
        color: #ffffff;
        font-size: 1.6em;
        font-weight: bold;
        text-align: center;
        margin-bottom: 15px;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.3);
    }
    .results-card p, .trade-card p, .chat-card p {
        color: #ffffff;
        font-size: 1.3em;
        font-weight: bold;
        margin: 12px 0;
        text-shadow: 1px 1px 4px rgba(0,0,0,0.3);
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 10px;
        padding: 10px 20px;
        font-weight: bold;
        border: none;
        width: 100%;
        margin-top: 12px;
        transition: background-color 0.3s;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .success-box {
        background-color: rgba(200, 230, 201, 0.9);
        padding: 10px;
        border-radius: 8px;
        color: #2e7d32;
        margin-top: 10px;
    }
    .error-box {
        background-color: rgba(255, 205, 210, 0.9);
        padding: 10px;
        border-radius: 8px;
        color: #c62828;
        margin-top: 10px;
    }
    .chat-message {
        background-color: rgba(255, 255, 255, 0.9);
        border-radius: 8px;
        padding: 10px;
        margin: 5px 0;
        color: #2c3e50;
    }
    .chat-message.user {
        background-color: rgba(200, 230, 201, 0.9);
        text-align: right;
    }
    .chat-message.other {
        background-color: rgba(187, 222, 251, 0.9);
        text-align: left;
    }
    </style>
    <script>
    function toggleSidebar() {
        const sidebar = document.querySelector('.sidebar');
        sidebar.classList.toggle('active');
    }
    </script>
    """,
    unsafe_allow_html=True
)

# Mock data for crops and mutations
crops = {
    "Carrot": {"base_value_per_kg": 22},
    "Strawberry": {"base_value_per_kg": 19},
    "Blueberry": {"base_value_per_kg": 21},
    "Orange Tulip": {"base_value_per_kg": 792},
    "Tomato": {"base_value_per_kg": 35},
    "Corn": {"base_value_per_kg": 44},
    "Daffodil": {"base_value_per_kg": 988},
    "Watermelon": {"base_value_per_kg": 2905},
    "Pumpkin": {"base_value_per_kg": 3854},
    "Apple": {"base_value_per_kg": 266},
    "Bamboo": {"base_value_per_kg": 3944},
    "Coconut": {"base_value_per_kg": 2670},
    "Cactus": {"base_value_per_kg": 3224},
    "Dragon Fruit": {"base_value_per_kg": 4566},
    "Mango": {"base_value_per_kg": 6308},
    "Grape": {"base_value_per_kg": 7554},
    "Mushroom": {"base_value_per_kg": 142443},
    "Pepper": {"base_value_per_kg": 7577},
    "Cacao": {"base_value_per_kg": 10456},
    "Beanstalk": {"base_value_per_kg": 18788},
    "Peach": {"base_value_per_kg": 283},
    "Pineapple": {"base_value_per_kg": 2554},
    "Banana": {"base_value_per_kg": 1778},
    "Avocado": {"base_value_per_kg": 354},
    "Green Apple": {"base_value_per_kg": 322},
    "Cauliflower": {"base_value_per_kg": 53},
    "Blood Banana": {"base_value_per_kg": 6100},
    "Moonglow": {"base_value_per_kg": 20300},
    "Moon Melon": {"base_value_per_kg": 17750},
    "Celestiberry": {"base_value_per_kg": 9100},
    "Moonflower": {"base_value_per_kg": 8900},
    "Starfruit": {"base_value_per_kg": 14100},
    "Mint": {"base_value_per_kg": 6800},
    "Nightshade": {"base_value_per_kg": 2300},
    "Raspberry": {"base_value_per_kg": 98},
    "Glowshroom": {"base_value_per_kg": 282},
    "Moon Mango": {"base_value_per_kg": 24340},
    "Moon Blossom": {"base_value_per_kg": 53512},
    "Soul Fruit": {"base_value_per_kg": 3328},
    "Cursed Fruit": {"base_value_per_kg": 15944},
    "Lotus": {"base_value_per_kg": 24598},
    "Candy Blossom": {"base_value_per_kg": 99436},
    "Cherry Blossom": {"base_value_per_kg": 566},
    "Venus Fly Trap": {"base_value_per_kg": 18854},
    "Cranberry": {"base_value_per_kg": 2054},
    "Durian": {"base_value_per_kg": 4911},
    "Easter Egg": {"base_value_per_kg": 4844},
    "Lemon": {"base_value_per_kg": 554},
    "Passionfruit": {"base_value_per_kg": 3299},
    "Eggplant": {"base_value_per_kg": 7089},
    "Papaya": {"base_value_per_kg": 1288},
    "Candy Sunflower": {"base_value_per_kg": 164440},
    "Red Lollipop": {"base_value_per_kg": 81297},
    "Chocolate Carrot": {"base_value_per_kg": 17258},
    "Nectarine": {"base_value_per_kg": 36100},
    "Sugar Apple": {"base_value_per_kg": 43320},
    "Dragon Pepper": {"base_value_per_kg": 80221},
    "Cocovine": {"base_value_per_kg": 60166},
    "Bendboo": {"base_value_per_kg": 139888},
    "Nectar Thorn": {"base_value_per_kg": 40111},
    "Suncoil": {"base_value_per_kg": 72200},
    "Violet Corn": {"base_value_per_kg": 45000},
    "Bee Balm": {"base_value_per_kg": 16245},
    "Succulent": {"base_value_per_kg": 19500},
    "Crocus": {"base_value_per_kg": 27075},
    "Feijoa": {"base_value_per_kg": 13977},
    "Loquat": {"base_value_per_kg": 8457},
    "Prickly Pear": {"base_value_per_kg": 58000},
    "Bell Pepper": {"base_value_per_kg": 5981},
    "Kiwi": {"base_value_per_kg": 4500},
    "Nectarshade": {"base_value_per_kg": 45125},
    "Wild Carrot": {"base_value_per_kg": 26544},
    "Parasol Flower": {"base_value_per_kg": 165300},
    "Rosy Delight": {"base_value_per_kg": 110522},
    "Elephant Ears": {"base_value_per_kg": 78053},
    "Horned Dinoshroom": {"base_value_per_kg": 50000},
    "Guanabana": {"base_value_per_kg": 28000},
    "Lily of the Valley": {"base_value_per_kg": 9000},
    "Aloe Vera": {"base_value_per_kg": 25000},
    "Peace Lily": {"base_value_per_kg": 18000},
    "Delphinium": {"base_value_per_kg": 5000}
}
mutations = {
    "Admin": {
        "None": {"multiplier": 1.0},
        "Plasma": {"multiplier": 5},
        "Heavenly": {"multiplier": 5},
        "Fried": {"multiplier": 8},
        "Molten": {"multiplier": 25},
        "Infected": {"multiplier": 75},
        "Sundried": {"multiplier": 85},
        "Aurora": {"multiplier": 90},
        "Alienlike": {"multiplier": 100},
        "Galactic": {"multiplier": 120},
        "Disco": {"multiplier": 125},
        "Meteoric": {"multiplier": 125},
        "Voidtouched": {"multiplier": 135},
        "Dawnbound": {"multiplier": 150}
    },
    "Weather": {
        "Wet": {"multiplier": 2},
        "Chilled": {"multiplier": 2},
        "Choc": {"multiplier": 2},
        "Moonlit": {"multiplier": 2},
        "Windstruck": {"multiplier": 2},
        "Pollinated": {"multiplier": 3},
        "Sandy": {"multiplier": 3},
        "Bloodlit": {"multiplier": 4},
        "Burnt": {"multiplier": 4},
        "Verdant": {"multiplier": 4},
        "Wiltproof": {"multiplier": 4},
        "Drenched": {"multiplier": 5},
        "HoneyGlazed": {"multiplier": 5},
        "Twisted": {"multiplier": 5},
        "Cloudtouched": {"multiplier": 5},
        "Clay": {"multiplier": 5},
        "Frozen": {"multiplier": 10},
        "Cooked": {"multiplier": 10},
        "Amber": {"multiplier": 10},
        "Tempestuous": {"multiplier": 14},
        "OldAmber": {"multiplier": 20},
        "Zombified": {"multiplier": 25},
        "Ceramic": {"multiplier": 30},
        "AncientAmber": {"multiplier": 50},
        "Friendbound": {"multiplier": 70},
        "Shocked": {"multiplier": 100},
        "Paradisal": {"multiplier": 100},
        "Celestial": {"multiplier": 120}
    },
    "Growth": {
        "None": {"multiplier": 1.0},
        "Golden": {"multiplier": 20},
        "Rainbow": {"multiplier": 50}
    }
}
friend_boosts = [0, 10, 20, 30, 40, 50]
trade_items = ["Sword", "Shield", "Potion", "Helmet", "Armor", "Ring", "Amulet", "Bow", "Arrow", "Staff"]

# Initialize session state
if 'harvest' not in st.session_state:
    st.session_state.harvest = {}
if 'fruit_count' not in st.session_state:
    st.session_state.fruit_count = 0
if 'default_weight' not in st.session_state:
    st.session_state.default_weight = 8.0
if 'quantity' not in st.session_state:
    st.session_state.quantity = 1
if 'friend_boost' not in st.session_state:
    st.session_state.friend_boost = 0
if 'trades' not in st.session_state:
    st.session_state.trades = {}
if 'notifications' not in st.session_state:
    st.session_state.notifications = {}
if 'trade_history' not in st.session_state:
    st.session_state.trade_history = {}
if 'trade_counter' not in st.session_state:
    st.session_state.trade_counter = 0
if 'offer_counter' not in st.session_state:
    st.session_state.offer_counter = 0
if 'active_chat' not in st.session_state:
    st.session_state.active_chat = None
if 'chat_messages' not in st.session_state:
    st.session_state.chat_messages = {}
if 'user_id' not in st.session_state:
    st.session_state.user_id = "User_" + str(hash(datetime.now()))[:8]
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Migration: convert old 'wanted_item' keys to 'wanted_items' list
for trade_id, trade in st.session_state.trades.items():
    if "wanted_item" in trade and "wanted_items" not in trade:
        trade["wanted_items"] = [trade.pop("wanted_item")]

# Configure Gemini API
GOOGLE_API_KEY = "AIzaSyAsut5nuxR7w-LrfqhMePB3Q26n3jmtixc"  # Replace with your API key
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

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
    save_trades()  # Save after adding trade
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
    save_trades()  # Save after adding offer
    st.rerun()  # Force re-run to update UI with notifications

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
    save_trades()  # Save after adding chat message

def end_chat(trade_id, offer_id, rejected=True):
    # Mark offer and trade as rejected or terminated
    st.session_state.trades[trade_id]["offers"][offer_id]["status"] = "rejected" if rejected else "terminated"
    poster = st.session_state.trades[trade_id]["poster"]
    if poster in st.session_state.notifications and offer_id in st.session_state.notifications[poster]:
        st.session_state.notifications[poster][offer_id]["status"] = "rejected" if rejected else "terminated"
    save_trades()  # Save after ending chat

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
    save_trades()  # Save after saving trade history

def clear_notification(poster, offer_id):
    if poster in st.session_state.notifications and offer_id in st.session_state.notifications[poster]:
        del st.session_state.notifications[poster][offer_id]
    save_trades()  # Save after clearing notification

def save_trades():
    with open("trades.txt", "w") as f:
        for trade_id, trade in st.session_state.trades.items():
            f.write(json.dumps({"trade_id": trade_id, **trade}) + "\n")

def load_trades():
    if os.path.exists("trades.txt"):
        with open("trades.txt", "r") as f:
            st.session_state.trades = {}
            for line in f:
                if line.strip():
                    try:
                        trade_data = json.loads(line.strip())
                        trade_id = trade_data.pop("trade_id")
                        st.session_state.trades[trade_id] = trade_data
                    except json.JSONDecodeError:
                        st.warning(f"Skipping malformed trade data in line: {line.strip()}")
            # Update counters based on loaded trades
            st.session_state.trade_counter = max(st.session_state.trades.keys(), default=-1) + 1
            # Safely compute offer_counter
            all_offer_ids = []
            for trade in st.session_state.trades.values():
                if "offers" in trade and trade["offers"]:
                    all_offer_ids.extend([int(k) for k in trade["offers"].keys() if k.isdigit()])
            st.session_state.offer_counter = max(all_offer_ids, default=-1) + 1

def clear_trades():
    st.session_state.trades.clear()
    st.session_state.trade_counter = 0
    st.session_state.offer_counter = 0
    save_trades()
    st.success("All trades have been cleared!")
    st.rerun()

# Load trades on startup
load_trades()

# Value Calculator Tab
def value_calculator_tab():
    st.markdown('<div class="main">', unsafe_allow_html=True)
    st.title("🌱 Grow a Garden Calculator")
    st.markdown("Calculate crop values with mutations and boosts. Switch modes below!")

    tab1, tab2 = st.columns([1, 1])
    with tab1:
        if st.button("Single Crop Mode", key="tab_single"):
            st.session_state.active_tab = "single"
        if st.button("Harvest Mode", key="tab_harvest"):
            st.session_state.active_tab = "harvest"
    active_tab = st.session_state.get("active_tab", "single")

    if active_tab == "single":
        st.markdown('<div class="tab-content active">', unsafe_allow_html=True)
        col1, col2 = st.columns([1, 1])

        with col1:
            st.subheader("🎑 Select Crop")
            crop = st.selectbox(" ", list(crops.keys()), index=0)

            st.subheader("🧬 Select Mutations")
            admin_mut = st.multiselect("Admin", list(mutations["Admin"].keys()), default=["None"])
            weather_mut = st.multiselect("Weather", list(mutations["Weather"].keys()), default=[])
            growth_mut = st.multiselect("Growth", list(mutations["Growth"].keys()), default=["None"])

            st.subheader("⚖️ Enter Weight & Quantity")
            weight = st.number_input("Weight (kg)", min_value=0.1, value=st.session_state.default_weight, step=0.1, key="weight_single")
            quantity = st.number_input("Quantity", min_value=1, value=st.session_state.quantity, step=1, key="quantity_single")
            friend_boost = st.selectbox("Friend Boost (%)", friend_boosts, index=friend_boosts.index(st.session_state.friend_boost), key="friend_boost_single")

        base_value = crops[crop]["base_value_per_kg"]
        growth_multi = next((mutations["Growth"][mut]["multiplier"] for mut in growth_mut if mut in mutations["Growth"]), 1.0)
        admin_weather_multi = sum(mutations["Admin"][mut]["multiplier"] for mut in admin_mut if mut in mutations["Admin"] and mut != "None") + \
                             sum(mutations["Weather"][mut]["multiplier"] for mut in weather_mut if mut in mutations["Weather"])
        total_value = ((base_value * weight * growth_multi) * (admin_weather_multi if admin_weather_multi > 0 else 1.0)) + friend_boost
        total_value *= quantity

        with col2:
            st.markdown('<div class="results-card">', unsafe_allow_html=True)
            st.subheader("📊 Calculation Results")
            st.metric("Total Value", f"{total_value:,.0f} Sheckles")
            st.metric("Base Value", f"{base_value:,.0f} Sheckles")
            st.metric("Total Multiplier", f"{(growth_multi * (admin_weather_multi if admin_weather_multi > 0 else 1.0)):.2f}x")
            if st.button("Reset", key="reset_single"):
                st.session_state.default_weight = 8.0
                st.session_state.quantity = 1
                st.session_state.friend_boost = 0
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    if active_tab == "harvest":
        st.markdown('<div class="tab-content active">', unsafe_allow_html=True)
        col1, col2 = st.columns([1, 1])

        with col1:
            st.subheader("🎑 Add Fruit to Harvest")
            with st.form(key="fruit_form"):
                fruit = st.selectbox("Select Fruit", options=list(crops.keys()), key=f"fruit_{st.session_state.fruit_count}")
                weight = st.number_input("Weight (kg)", min_value=0.1, value=st.session_state.default_weight, step=0.1, format="%.2f", key=f"weight_{st.session_state.fruit_count}")
                admin_mut = st.multiselect("Admin Mutations", list(mutations["Admin"].keys()), default=["None"], key=f"admin_{st.session_state.fruit_count}")
                weather_mut = st.multiselect("Weather Mutations", list(mutations["Weather"].keys()), default=[], key=f"weather_{st.session_state.fruit_count}")
                growth_mut = st.multiselect("Growth Mutations", list(mutations["Growth"].keys()), default=["None"], key=f"growth_{st.session_state.fruit_count}")
                friend_boost = st.selectbox("Friend Boost (%)", friend_boosts, index=friend_boosts.index(st.session_state.friend_boost), key=f"boost_{st.session_state.fruit_count}")
                submit = st.form_submit_button("Add Fruit")

                if submit:
                    if weight <= 0:
                        st.error("Weight must be greater than 0.")
                    elif fruit in st.session_state.harvest:
                        st.error("Fruit already added. Clear harvest to start over.")
                    else:
                        all_mutations = admin_mut + weather_mut + growth_mut
                        st.session_state.harvest[fruit] = {
                            "weight": weight,
                            "mutations": all_mutations if all_mutations else ["None"],
                            "friend_boost": friend_boost
                        }
                        st.session_state.fruit_count += 1
                        st.session_state.default_weight = 8.0
                        st.success(f"Added {fruit} to harvest!")

        if st.session_state.harvest:
            st.subheader("Current Harvest")
            for fruit, details in st.session_state.harvest.items():
                mutations_str = ", ".join(details["mutations"])
                st.write(f"{fruit}: {details['weight']:.2f} kg, Mutations: {mutations_str}, Friend Boost: {details['friend_boost']}%")

        def calculate_harvest_value(harvest, crops, mutations):
            result = []
            total_value = 0.0
            total_multiplier = 0.0
            result.append("### Harvest Value Calculation")
            result.append("---")
            
            for fruit, details in harvest.items():
                if fruit in crops:
                    base_value = crops[fruit]["base_value_per_kg"]
                    weight = details["weight"]
                    all_mutations = details["mutations"]
                    friend_boost = details["friend_boost"]
                    growth_multi = next((mutations["Growth"][mut]["multiplier"] for mut in all_mutations if mut in mutations["Growth"]), 1.0)
                    admin_weather_multi = sum(mutations["Admin"][mut]["multiplier"] for mut in all_mutations if mut in mutations["Admin"] and mut != "None") + \
                                         sum(mutations["Weather"][mut]["multiplier"] for mut in all_mutations if mut in mutations["Weather"])
                    value = ((base_value * weight * growth_multi) * (admin_weather_multi if admin_weather_multi > 0 else 1.0)) + friend_boost
                    total_value += value
                    total_multiplier += (growth_multi * (admin_weather_multi if admin_weather_multi > 0 else 1.0))
                    result.append(f"**{fruit}**")
                    result.append(f"{weight:.2f} kg x ({base_value:,} sheckles/kg * {growth_multi:.1f}x) * {(admin_weather_multi if admin_weather_multi > 0 else 1.0):.1f}x + {friend_boost} = {value:,.2f} sheckles")
                    if all_mutations != ["None"]:
                        result.append(f"(Mutations: {', '.join(all_mutations)})")
                    result.append("")
                else:
                    result.append(f"**{fruit}**: Invalid fruit")
            total_multiplier = total_multiplier / len(harvest) if harvest else 0.0
            result.append("---")
            result.append(f"**Total Value**: {total_value:,.2f} sheckles")
            result.append(f"**Average Total Multiplier**: {total_multiplier:.2f}x")
            return result, total_value, total_multiplier

        def save_harvest(harvest, total_value, total_multiplier):
            with open("garden_harvest_log.txt", "a") as file:
                file.write(f"\nHarvest Log - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                file.write("-" * 35 + "\n")
                for fruit, details in harvest.items():
                    file.write(f"{fruit}: {details['weight']:.2f} kg, Mutations: {', '.join(details['mutations'])}, Friend Boost: {details['friend_boost']}%\n")
                file.write(f"Total Value: {total_value:.2f} sheckles\n")
                file.write(f"Average Total Multiplier: {total_multiplier:.2f}x\n")
                file.write("-" * 35 + "\n")

        with col2:
            st.subheader("📊 Calculation Results")
            if st.button("Calculate Harvest Value"):
                if not st.session_state.harvest:
                    st.error("No fruits in harvest. Add at least one fruit.")
                else:
                    result, total_value, total_multiplier = calculate_harvest_value(st.session_state.harvest, crops, mutations)
                    st.markdown('<div class="results-card">', unsafe_allow_html=True)
                    st.markdown("\n".join(result))
                    st.markdown('</div>', unsafe_allow_html=True)
                    save_harvest(st.session_state.harvest, total_value, total_multiplier)
                    st.success("Harvest saved to garden_harvest_log.txt")

            if st.button("Clear Harvest"):
                st.session_state.harvest = {}
                st.session_state.fruit_count = 0
                st.success("Harvest cleared!")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# Trading Ads Tab
def trading_ads_tab():
    st.markdown('<div class="main">', unsafe_allow_html=True)
    st.title("🤝 Trading Ads")
    st.markdown("Post items you want to trade and find what you're looking for!")

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

        selected_trade_items = st.multiselect("Select item(s) you want to trade", trade_items, key="trade_items")
        trade_value = st.number_input("Value (number)", min_value=0.0, step=1.0, key="trade_value")
        trade_description = st.text_area("Description", key="trade_description")
        wanted_items = st.multiselect("Item(s) you want in exchange", trade_items, key="wanted_items")

        if st.button("Post Trade"):
            if not selected_trade_items:
                st.error("Please select at least one item to trade.")
            elif trade_value <= 0:
                st.error("Please enter a value greater than 0.")
            elif not wanted_items:
                st.error("Please select at least one item you want in exchange.")
            else:
                trade_id = add_trade(current_user, selected_trade_items, trade_value, trade_description, wanted_items)
                st.success(f"Trade posted successfully! Trade ID: {trade_id}")
                st.rerun()  # Force re-run to refresh UI

    # ----------- TRADES FEED TAB -----------
    with tabs[1]:
        st.header("Trades Feed")
        if st.button("Clear Trades", key="clear_trades"):
            clear_trades()

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
                        st.markdown(f"### Trading by **{poster}**", unsafe_allow_html=True)
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

                        # Show offer modal within a form
                        if st.session_state.get(f"offer_modal_{trade_id}", False):
                            with st.form(key=f"offer_form_{trade_id}"):
                                st.markdown(f"**Make an offer on trade {trade_id}**")
                                offer_username = st.text_input("Your username", value=current_user, key=f"offer_username_{trade_id}")
                                offer_message = st.text_area("Message", key=f"offer_message_{trade_id}")
                                col1, col2 = st.columns(2)
                                with col1:
                                    if st.form_submit_button("Send Offer"):
                                        if not offer_username.strip():
                                            st.error("Please enter your username.")
                                        elif not offer_message.strip():
                                            st.error("Please enter a message.")
                                        else:
                                            add_offer(trade_id, offer_username.strip(), offer_message.strip())
                                            st.success("Offer sent!")
                                            st.session_state[f"offer_modal_{trade_id}"] = False
                                with col2:
                                    if st.form_submit_button("Cancel"):
                                        st.session_state[f"offer_modal_{trade_id}"] = False
                                st.form_submit_button("Close")  # Additional close option

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
                                save_trades()  # Save after updating status
                        with col2:
                            if st.button(f"Reject Offer {offer_id}"):
                                notif["rejected"] = True
                                notif["status"] = "rejected"
                                # Mark offer rejected in trade data too
                                st.session_state.trades[trade_id]["offers"][offer_id]["status"] = "rejected"
                                to_remove.append(offer_id)
                                save_trades()  # Save after updating status
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
                                st.rerun()
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
                                    st.rerun()
                                else:
                                    st.info("Waiting for the other user to accept.")

                        with col_rej:
                            if st.button(f"Reject Trade (Offer {offer_id})"):
                                end_chat(trade_id, offer_id, rejected=True)
                                st.error("Trade rejected and chat terminated.")
                                to_remove.append(offer_id)
                                st.rerun()

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

    st.markdown('</div>', unsafe_allow_html=True)

# Help Tab with Gemini AI
def help_tab():
    st.markdown('<div class="main">', unsafe_allow_html=True)
    st.title("🧘 Help?!")
    st.markdown("A space to support your well-being with a Gemini AI chatbot.")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Chat input with mode selection
    mode = st.selectbox("Select Chat Mode", ["Game Help", "Mental Help", "AI Partner"])
    if prompt := st.chat_input("Chat with Gemini"):
        with st.chat_message("user"):
            st.write(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Get Gemini response based on mode
        try:
            if mode == "Game Help":
                response_prompt = f"Provide a gaming response with gameplay tutorials/tips and tricks for: {prompt}. Optionally include a link if relevant."
            elif mode == "Mental Help":
                response_prompt = f"Provide a positive, supportive response to help the user get back on track for: {prompt}."
            else:  # AI Partner
                response_prompt = f"Respond as a friendly girlfriend/boyfriend to: {prompt}."
            response = model.generate_content(response_prompt)
            with st.chat_message("assistant"):
                st.write(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            with st.chat_message("assistant"):
                st.error(f"Error integrating Gemini AI: {e}. Please try again later.")
            st.session_state.messages.append({"role": "assistant", "content": "Sorry, AI response unavailable. Please try again later."})

    st.markdown('</div>', unsafe_allow_html=True)

# Main app function
def main():
    tab1, tab2, tab3 = st.tabs(["Value Calculator", "Trading Ads", "Help?!"])
    
    with tab1:
        value_calculator_tab()
    with tab2:
        trading_ads_tab()
    with tab3:
        help_tab()

    st.markdown("""
        <div style='text-align: center; margin-top: 30px; padding: 12px;
        background: linear-gradient(to right, #ff9800, #f44336);
        color: white; border-radius: 12px; font-style: italic;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);'>
            ⚠️ Disclaimer: The calculated value is most likely inaccurate, so please take it with a grain of salt.
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()