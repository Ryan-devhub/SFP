import streamlit as st
import pandas as pd
from datetime import datetime

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

# Custom CSS with vibrant garden-themed background
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #4CAF50 0%, #8BC34A 25%, #CDDC39 50%, #FFEB3B 75%, #FF9800 100%);
        background-size: cover;
        background-attachment: fixed;
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
    .stSelectbox, .stMultiselect, .stNumberInput {
        background-color: rgba(255, 255, 255, 0.9);
        border-radius: 10px;
        padding: 10px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
        margin-bottom: 12px;
        color: #2c3e50;
    }
    .results-card {
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
    .results-card h3 {
        color: #ffffff;
        font-size: 1.6em;
        font-weight: bold;
        text-align: center;
        margin-bottom: 15px;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.3);
    }
    .results-card p {
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
    .tab-content {
        display: none;
    }
    .tab-content.active {
        display: block;
    }
    .tab-button {
        background-color: rgba(255, 255, 255, 0.8);
        border: none;
        padding: 10px 20px;
        margin-right: 5px;
        border-radius: 5px;
        cursor: pointer;
        font-weight: bold;
        color: #2c3e50;
    }
    .tab-button:hover, .tab-button.active {
        background-color: #4CAF50;
        color: white;
    }
    .stMetric > div {
        background-color: rgba(255, 255, 255, 0.8);
        border-radius: 10px;
        padding: 10px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Main app function
def main():
    st.markdown('<div class="main">', unsafe_allow_html=True)
    st.title("🌱 Grow a Garden Calculator")
    st.markdown("Calculate crop values with mutations and boosts. Switch modes below!")

    # Tab selection
    tab1, tab2 = st.columns([1, 1])
    with tab1:
        if st.button("Single Crop Mode", key="tab_single"):
            st.session_state.active_tab = "single"
        if st.button("Harvest Mode", key="tab_harvest"):
            st.session_state.active_tab = "harvest"
    active_tab = st.session_state.get("active_tab", "single")

    # Tab content
    st.markdown('<div id="tab-content">', unsafe_allow_html=True)

    # Single Crop Mode
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

        # Calculation for single crop with corrected formula
        base_value = crops[crop]["base_value_per_kg"]
        growth_multi = next((mutations["Growth"][mut]["multiplier"] for mut in growth_mut if mut in mutations["Growth"]), 1.0)
        admin_weather_multi = sum(mutations["Admin"][mut]["multiplier"] for mut in admin_mut if mut in mutations["Admin"] and mut != "None") + \
                             sum(mutations["Weather"][mut]["multiplier"] for mut in weather_mut if mut in mutations["Weather"])
        total_value = ((base_value * weight * growth_multi) * (admin_weather_multi if admin_weather_multi > 0 else 1.0)) + friend_boost
        total_value *= quantity  # Apply quantity

        with col2:
            st.subheader("📊 Calculation Results")
            st.metric("Total Value", f"{total_value:,.0f} Sheckles")
            st.metric("Base Value", f"{base_value:,.0f} Sheckles")
            st.metric("Total Multiplier", f"{(growth_multi * (admin_weather_multi if admin_weather_multi > 0 else 1.0)):.2f}x")
            if st.button("Reset", key="reset_single"):
                st.session_state.default_weight = 8.0
                st.session_state.quantity = 1
                st.session_state.friend_boost = 0
                st.experimental_rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # Harvest Mode
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

        # Display current harvest
        if st.session_state.harvest:
            st.subheader("Current Harvest")
            for fruit, details in st.session_state.harvest.items():
                mutations_str = ", ".join(details["mutations"])
                st.write(f"{fruit}: {details['weight']:.2f} kg, Mutations: {mutations_str}, Friend Boost: {details['friend_boost']}%")

        # Calculate harvest value with corrected formula
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
                    # Extract growth multiplier
                    growth_multi = next((mutations["Growth"][mut]["multiplier"] for mut in all_mutations if mut in mutations["Growth"]), 1.0)
                    # Sum admin and weather multipliers
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
            total_multiplier = total_multiplier / len(harvest) if harvest else 0.0  # Average multiplier
            result.append("---")
            result.append(f"**Total Value**: {total_value:,.2f} sheckles")
            result.append(f"**Average Total Multiplier**: {total_multiplier:.2f}x")
            return result, total_value, total_multiplier

        # Save harvest to log file
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


  # Disclaimer box
    st.markdown("""
        <div style='text-align: center; margin-top: 30px; padding: 12px;
        background: linear-gradient(to right, #ff9800, #f44336);
        color: white; border-radius: 12px; font-style: italic;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);'>
            ⚠️ Disclaimer: The calculated value is most likely inaccurate, so please take it with a grain of salt.
        </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
        <script>
        document.querySelectorAll('.tab-button').forEach(button => {
            button.addEventListener('click', () => {
                document.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('active'));
                document.querySelectorAll('.tab-button').forEach(btn => btn.classList.remove('active'));
                button.classList.add('active');
                document.getElementById(button.getAttribute('data-tab')).classList.add('active');
            });
        });
        </script>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()