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
    .chat-card.accepted {
        background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
    }
    .sidebar {
        position: fixed;
        top: 0;
        left: 0;
        width: 250px;
        height: 100%;
        background-color: rgba(255, 255, 255, 0.9);
        padding: 20px;
        box-shadow: 2px 0 5px rgba(0,0,0,0.1);
        overflow-y: auto;
    }
    .sidebar h3 {
        color: #2c3e50;
        font-size: 1.5em;
        margin-bottom: 15px;
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
trade_items = ["Fox", "Dog", "Cat", "Chicken"]

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
if 'trade_posts' not in st.session_state:
    st.session_state.trade_posts = []
if 'active_chat' not in st.session_state:
    st.session_state.active_chat = None
if 'chat_messages' not in st.session_state:
    st.session_state.chat_messages = {}
if 'user_id' not in st.session_state:
    st.session_state.user_id = "User_" + str(hash(datetime.now()))[:8]
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'trade_notifications' not in st.session_state:
    st.session_state.trade_notifications = {}

# Configure Gemini API
GOOGLE_API_KEY = "AIzaSyAsut5nuxR7w-LrfqhMePB3Q26n3jmtixc"  # Replace with your API key
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

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

# Trading Ads Tab with username and persistent storage
def trading_ads_tab():
    st.markdown('<div class="main">', unsafe_allow_html=True)
    st.title("🤝 Trading Ads")
    st.markdown("Post items you want to trade and find what you're looking for!")

    # Load existing trade posts from file
    trade_posts_file = "trade_posts.json"
    if os.path.exists(trade_posts_file):
        with open(trade_posts_file, "r") as f:
            st.session_state.trade_posts = json.load(f)
    else:
        st.session_state.trade_posts = []

    # Form to post a trade
    st.subheader("📝 Create a Trade Post")
    with st.form(key="trade_form"):
        username = st.text_input("Your Username", key="trade_username")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Items to Trade**")
            trade_items_selected = st.multiselect("Item Names", options=trade_items, key="trade_items")
            trade_value = st.number_input("Total Value (Sheckles, optional)", min_value=0.0, step=1.0, format="%.2f", value=0.0, key="trade_value")
        with col2:
            st.markdown("**Items Desired**")
            want_items_selected = st.multiselect("Item Names", options=trade_items, key="want_items")
            want_value = st.number_input("Total Value (Sheckles, optional)", min_value=0.0, step=1.0, format="%.2f", value=0.0, key="want_value")
        description = st.text_area("Trade Description (optional)", key="trade_description")
        submit_trade = st.form_submit_button("Post Trade")

        if submit_trade:
            if not username or not trade_items_selected or not want_items_selected:
                st.error("Please enter a username and select at least one item to trade and one item desired.")
            else:
                trade_id = len(st.session_state.trade_posts)
                new_post = {
                    "trade_id": trade_id,
                    "user_id": st.session_state.user_id,
                    "username": username,
                    "trade_items": trade_items_selected,
                    "trade_value": trade_value if trade_value > 0 else None,
                    "want_items": want_items_selected,
                    "want_value": want_value if want_value > 0 else None,
                    "description": description if description else None,
                    "status": "open"
                }
                st.session_state.trade_posts.append(new_post)
                with open(trade_posts_file, "w") as f:
                    json.dump(st.session_state.trade_posts, f)
                st.success("Trade posted successfully!")

    # Display all trade posts
    st.subheader("📬 Available Trades")
    for post in st.session_state.trade_posts:
        if post["status"] == "open":
            st.markdown('<div class="trade-card">', unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**{post['username']} Offering**: {', '.join(post['trade_items'])}")
                if post["trade_value"]:
                    st.markdown(f"**Value**: {post['trade_value']:,.2f} Sheckles")
            with col2:
                st.markdown(f"**{post['username']} Looking For**: {', '.join(post['want_items'])}")
                if post["want_value"]:
                    st.markdown(f"**Value**: {post['want_value']:,.2f} Sheckles")
            if post["description"]:
                st.markdown(f"**Description**: {post['description']}")
            if st.session_state.user_id != post["user_id"]:  # Prevent self-offer
                if st.button("Make an Offer", key=f"offer_{post['trade_id']}"):
                    offerer_username = st.text_input("Your Username for this Offer", key=f"offerer_username_{post['trade_id']}")
                    if offerer_username:
                        # Store notification for the trade poster
                        if post["user_id"] not in st.session_state.trade_notifications:
                            st.session_state.trade_notifications[post["user_id"]] = {}
                        st.session_state.trade_notifications[post["user_id"]][post["trade_id"]] = offerer_username
                        st.session_state.active_chat = None  # Reset active chat to show sidebar
                        with open(trade_posts_file, "w") as f:
                            json.dump(st.session_state.trade_posts, f)
                        st.success(f"Trade request sent to {post['username']}!")
            else:
                st.write("You cannot make an offer on your own trade.")
            st.markdown('</div>', unsafe_allow_html=True)

    # Sidebar for trade notifications
    st.markdown('<div class="sidebar">', unsafe_allow_html=True)
    st.markdown('<h3>Trade Notifications</h3>', unsafe_allow_html=True)
    user_notifications = st.session_state.trade_notifications.get(st.session_state.user_id, {})
    for trade_id, offerer_username in user_notifications.items():
        post = next((p for p in st.session_state.trade_posts if p["trade_id"] == trade_id), None)
        if post and post["status"] == "open":
            if st.button(f"Start a Chat with {offerer_username} (Trade ID: {trade_id})", key=f"chat_{trade_id}"):
                st.session_state.active_chat = trade_id
                if trade_id not in st.session_state.chat_messages:
                    st.session_state.chat_messages[trade_id] = []
                # Remove notification after starting chat
                if st.session_state.user_id in st.session_state.trade_notifications and trade_id in st.session_state.trade_notifications[st.session_state.user_id]:
                    del st.session_state.trade_notifications[st.session_state.user_id][trade_id]
                    with open(trade_posts_file, "w") as f:
                        json.dump(st.session_state.trade_posts, f)
    st.markdown('</div>', unsafe_allow_html=True)

    # Chat interface for negotiation
    if st.session_state.active_chat is not None:
        trade_id = st.session_state.active_chat
        post = next((p for p in st.session_state.trade_posts if p["trade_id"] == trade_id), None)
        if post and post["status"] == "open":
            chat_class = "chat-card accepted" if st.session_state.chat_messages.get(trade_id, [{}])[0].get("accepted", False) else "chat-card"
            st.markdown(f'<div class="{chat_class}">', unsafe_allow_html=True)
            offerer_username = st.session_state.chat_messages.get(trade_id, [{}])[0].get("offerer_username")
            st.subheader(f"Negotiating Trade: {post['username']} - {', '.join(post['trade_items'])} for {', '.join(post['want_items'])}")
            if offerer_username and st.session_state.user_id == post["user_id"]:
                st.write(f"Offer from: {offerer_username}")
            for msg in st.session_state.chat_messages.get(trade_id, []):
                sender = "You" if msg["user_id"] == st.session_state.user_id else (msg.get("offerer_username") or post["username"])
                st.markdown(f'<div class="chat-message {'user' if msg['user_id'] == st.session_state.user_id else 'other'}">{sender}: {msg["message"]}</div>', unsafe_allow_html=True)
            with st.form(key=f"chat_form_{trade_id}"):
                message = st.text_area("Your Message", key=f"message_{trade_id}")
                col1, col2, col3 = st.columns([2, 1, 1])
                with col1:
                    if st.form_submit_button("Send Message"):
                        if message:
                            offerer_username = st.session_state.chat_messages.get(trade_id, [{}])[0].get("offerer_username") if st.session_state.chat_messages.get(trade_id) else st.session_state.get(f"offerer_username_{trade_id}")
                            st.session_state.chat_messages[trade_id].append({
                                "user_id": st.session_state.user_id,
                                "offerer_username": offerer_username,
                                "message": message,
                                "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            })
                            with open(trade_posts_file, "w") as f:
                                json.dump(st.session_state.trade_posts, f)
                            st.rerun()
                with col2:
                    if st.form_submit_button("Accept Offer"):
                        if trade_id in st.session_state.chat_messages:
                            st.session_state.chat_messages[trade_id][0]["accepted"] = st.session_state.chat_messages[trade_id][0].get("accepted", False) or {}
                            st.session_state.chat_messages[trade_id][0]["accepted"][st.session_state.user_id] = True
                            if all(st.session_state.chat_messages[trade_id][0]["accepted"].get(uid, False) for uid in [post["user_id"], next((msg["user_id"] for msg in st.session_state.chat_messages[trade_id] if msg.get("offerer_username")), None)]):
                                post["status"] = "accepted"
                                with open(trade_posts_file, "w") as f:
                                    json.dump(st.session_state.trade_posts, f)
                                st.success("Trade accepted and saved!")
                            st.rerun()
                with col3:
                    if st.form_submit_button("Decline Offer"):
                        if trade_id in st.session_state.chat_messages:
                            del st.session_state.chat_messages[trade_id]
                            post["status"] = "rejected"
                            with open(trade_posts_file, "w") as f:
                                json.dump(st.session_state.trade_posts, f)
                            st.session_state.active_chat = None
                            st.error("Trade declined and chat terminated.")
                            st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    # Save trade posts to file on session end or change
    with open(trade_posts_file, "w") as f:
        json.dump(st.session_state.trade_posts, f)

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