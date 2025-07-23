import streamlit as st
import pandas as pd

# Page config
st.set_page_config(page_title="Grow a Garden Calculator", layout="wide")

# Mock data
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

# Initialize session state
if 'weight' not in st.session_state:
    st.session_state.weight = 8.0
if 'quantity' not in st.session_state:
    st.session_state.quantity = 1
if 'friend_boost' not in st.session_state:
    st.session_state.friend_boost = 0

# Custom CSS for appealing UI
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #f0f7f4 0%, #e0f0e9 100%);
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .stTitle {
        color: #2c3e50;
        font-family: 'Arial', sans-serif;
        text-align: center;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    .stSubheader {
        color: #34495e;
        font-weight: bold;
        margin-top: 15px;
    }
    .stSelectbox, .stMultiselect, .stNumberInput {
        background-color: #ffffff;
        border-radius: 8px;
        padding: 8px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
        margin-bottom: 10px;
    }
    .stMetric {
        background: linear-gradient(135deg, #f9e79f 0%, #f1c40f 100%);
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        color: #2c3e50;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .stButton {
        background-color: #3498db;
        color: white;
        border-radius: 8px;
        padding: 8px 16px;
        margin-top: 10px;
    }
    .stButton:hover {
        background-color: #2980b9;
    }
    </style>
""", unsafe_allow_html=True)

# Main app
st.markdown('<div class="main">', unsafe_allow_html=True)
st.title("🌱 Grow a Garden Calculator")
st.markdown("Calculate fruit prices with mutation effects and Friend Boosts to find your most valuable crops.")

# Input section
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("🎑 Select Crop")
    crop = st.selectbox(" ", list(crops.keys()), index=0)

    st.subheader("🧬 Select Mutations")
    admin_mut = st.multiselect("Admin", list(mutations["Admin"].keys()), default=[])
    weather_mut = st.multiselect("Weather", list(mutations["Weather"].keys()), default=[])
    growth_mut = st.multiselect("Growth", list(mutations["Growth"].keys()), default=["None"])

    st.subheader("⚖️ Enter Weight & Quantity")
    weight = st.number_input("Weight (kg)", min_value=0.1, value=st.session_state.weight, step=0.1, key="weight")
    quantity = st.number_input("Quantity", min_value=1, value=st.session_state.quantity, step=1, key="quantity")
    friend_boost = st.selectbox("Friend Boost (%)", friend_boosts, index=friend_boosts.index(st.session_state.friend_boost), key="friend_boost")

# Calculation
base_value = crops[crop]["base_value_per_kg"]
admin_multi = sum(mutations["Admin"][mut]["multiplier"] for mut in admin_mut) if admin_mut else 1.0
weather_multi = sum(mutations["Weather"][mut]["multiplier"] for mut in weather_mut) if weather_mut else 1.0
growth_multi = sum(mutations["Growth"][mut]["multiplier"] for mut in growth_mut) if growth_mut else 1.0
total_multiplier = admin_multi * weather_multi * growth_multi + (friend_boost / 100)
total_value = base_value * weight * total_multiplier * quantity

with col2:
    st.subheader("📊 Calculation Results")
    if st.button("Clear All"):
        st.session_state.weight = 8.0
        st.session_state.quantity = 1
        st.session_state.friend_boost = 0
        st.experimental_rerun()

    st.metric("Total Value", f"{total_value:,.0f} Sheckles")
    st.metric("Base Value", f"{base_value:,.0f} Sheckles")
    st.metric("Total Multiplier", f"{total_multiplier:.1f}x")

st.markdown('</div>', unsafe_allow_html=True)