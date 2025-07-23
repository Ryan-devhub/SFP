import streamlit as st
import pandas as pd
from datetime import datetime
import os
import random
import time
import google.generativeai as genai
import sqlite3  # Added for database

# Set page configuration
st.set_page_config(
    page_title="Grow a Garden Hub",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS (unchanged)
st.markdown("""
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
    .css-1lcbmhc {
        background-color: rgba(165, 214, 167, 0.9);
    }
    .stTabs [data-baseweb="tab-list"] {
        background-color: #4CAF50;
        border-radius: 10px;
        padding: 5px;
    }
    .stTabs [data-baseweb="tab"] {
        color: white;
        border-radius: 8px;
        margin: 5px;
        padding: 10px 20px;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #81C784;
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
    .stSelectbox, .stMultiselect, .stNumberInput, .stTextInput, .stTextArea {
        background-color: rgba(255, 255, 255, 0.9);
        border-radius: 10px;
        padding: 10px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
        margin-bottom: 12px;
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
    .results-card, .trade-card, .chat-card, .game-card {
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
    .results-card h3, .trade-card h3, .chat-card h3, .game-card h3 {
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
    .trade-post-box {
        background: linear-gradient(135deg, #4CAF50 0%, #2196F3 100%);
        border-radius: 12px;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        border: 2px solid #ffffff;
    }
    .trade-box {
        background-color: rgba(255, 255, 255, 0.9);
        border-radius: 8px;
        padding: 10px;
        margin: 5px;
        color: #2c3e50;
    }
    .chat-message.user {
        background-color: rgba(200, 230, 201, 0.9);
        border-radius: 8px;
        padding: 10px;
        margin: 5px 0;
        text-align: right;
        color: #2c3e50;
    }
    .chat-message.other {
        background-color: rgba(187, 222, 251, 0.9);
        border-radius: 8px;
        padding: 10px;
        margin: 5px 0;
        text-align: left;
        color: #2c3e50;
    }
    .declined-chat {
        background-color: rgba(255, 205, 210, 0.9);
        border-radius: 8px;
        padding: 10px;
        margin: 5px 0;
    }
    .weed-button {
        background-color: rgba(139, 195, 74, 0.9);
        border-radius: 8px;
        padding: 10px;
        margin: 5px;
        font-size: 1.2em;
        text-align: center;
        cursor: pointer;
    }
    .flower-button {
        background-color: rgba(255, 182, 193, 0.9);
        border-radius: 8px;
        padding: 10px;
        margin: 5px;
        font-size: 1.2em;
        text-align: center;
        cursor: pointer;
    }
    .empty-cell {
        background-color: rgba(255, 255, 255, 0.9);
        border-radius: 8px;
        padding: 10px;
        margin: 5px;
        height: 50px;
        text-align: center;
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
    .tab-content.active {
        display: block;
    }
    </style>
""", unsafe_allow_html=True)

# Crop data (unchanged)
crops = {
    "Carrot": {"base_value_per_kg": 22, "season": "Spring"},
    "Strawberry": {"base_value_per_kg": 19, "season": "Summer"},
    "Blueberry": {"base_value_per_kg": 21, "season": "Summer"},
    "Orange Tulip": {"base_value_per_kg": 792, "season": "Spring"},
    "Tomato": {"base_value_per_kg": 35, "season": "Summer"},
    "Corn": {"base_value_per_kg": 44, "season": "Summer"},
    "Daffodil": {"base_value_per_kg": 988, "season": "Spring"},
    "Watermelon": {"base_value_per_kg": 2905, "season": "Summer"},
    "Pumpkin": {"base_value_per_kg": 3854, "season": "Fall"},
    "Apple": {"base_value_per_kg": 266, "season": "Fall"},
    "Bamboo": {"base_value_per_kg": 3944, "season": "All"},
    "Coconut": {"base_value_per_kg": 2670, "season": "Summer"},
    "Cactus": {"base_value_per_kg": 3224, "season": "All"},
    "Dragon Fruit": {"base_value_per_kg": 4566, "season": "Summer"},
    "Mango": {"base_value_per_kg": 6308, "season": "Summer"},
    "Grape": {"base_value_per_kg": 7554, "season": "Fall"},
    "Mushroom": {"base_value_per_kg": 142443, "season": "All"},
    "Pepper": {"base_value_per_kg": 7577, "season": "Summer"},
    "Cacao": {"base_value_per_kg": 10456, "season": "Summer"},
    "Beanstalk": {"base_value_per_kg": 18788, "season": "All"},
    "Peach": {"base_value_per_kg": 283, "season": "Summer"},
    "Pineapple": {"base_value_per_kg": 2554, "season": "Summer"},
    "Banana": {"base_value_per_kg": 1778, "season": "Summer"},
    "Avocado": {"base_value_per_kg": 354, "season": "Summer"},
    "Green Apple": {"base_value_per_kg": 322, "season": "Fall"},
    "Cauliflower": {"base_value_per_kg": 53, "season": "Fall"},
    "Blood Banana": {"base_value_per_kg": 6100, "season": "Summer"},
    "Moonglow": {"base_value_per_kg": 20300, "season": "All"},
    "Moon Melon": {"base_value_per_kg": 17750, "season": "Summer"},
    "Celestiberry": {"base_value_per_kg": 9100, "season": "Summer"},
    "Moonflower": {"base_value_per_kg": 8900, "season": "All"},
    "Starfruit": {"base_value_per_kg": 14100, "season": "Summer"},
    "Mint": {"base_value_per_kg": 6800, "season": "All"},
    "Nightshade": {"base_value_per_kg": 2300, "season": "All"},
    "Raspberry": {"base_value_per_kg": 98, "season": "Summer"},
    "Glowshroom": {"base_value_per_kg": 282, "season": "All"},
    "Moon Mango": {"base_value_per_kg": 24340, "season": "Summer"},
    "Moon Blossom": {"base_value_per_kg": 53512, "season": "All"},
    "Soul Fruit": {"base_value_per_kg": 3328, "season": "All"},
    "Cursed Fruit": {"base_value_per_kg": 15944, "season": "All"},
    "Lotus": {"base_value_per_kg": 24598, "season": "All"},
    "Candy Blossom": {"base_value_per_kg": 99436, "season": "All"},
    "Cherry Blossom": {"base_value_per_kg": 566, "season": "Spring"},
    "Venus Fly Trap": {"base_value_per_kg": 18854, "season": "All"},
    "Cranberry": {"base_value_per_kg": 2054, "season": "Fall"},
    "Durian": {"base_value_per_kg": 4911, "season": "Summer"},
    "Easter Egg": {"base_value_per_kg": 4844, "season": "Spring"},
    "Lemon": {"base_value_per_kg": 554, "season": "Summer"},
    "Passionfruit": {"base_value_per_kg": 3299, "season": "Summer"},
    "Eggplant": {"base_value_per_kg": 7089, "season": "Summer"},
    "Papaya": {"base_value_per_kg": 1288, "season": "Summer"},
    "Candy Sunflower": {"base_value_per_kg": 164440, "season": "Summer"},
    "Red Lollipop": {"base_value_per_kg": 81297, "season": "All"},
    "Chocolate Carrot": {"base_value_per_kg": 17258, "season": "Spring"},
    "Nectarine": {"base_value_per_kg": 36100, "season": "Summer"},
    "Sugar Apple": {"base_value_per_kg": 43320, "season": "Summer"},
    "Dragon Pepper": {"base_value_per_kg": 80221, "season": "Summer"},
    "Cocovine": {"base_value_per_kg": 60166, "season": "Summer"},
    "Bendboo": {"base_value_per_kg": 139888, "season": "All"},
    "Nectar Thorn": {"base_value_per_kg": 40111, "season": "All"},
    "Suncoil": {"base_value_per_kg": 72200, "season": "Summer"},
    "Violet Corn": {"base_value_per_kg": 45000, "season": "Summer"},
    "Bee Balm": {"base_value_per_kg": 16245, "season": "Summer"},
    "Succulent": {"base_value_per_kg": 19500, "season": "All"},
    "Crocus": {"base_value_per_kg": 27075, "season": "Spring"},
    "Feijoa": {"base_value_per_kg": 13977, "season": "Fall"},
    "Loquat": {"base_value_per_kg": 8457, "season": "Spring"},
    "Prickly Pear": {"base_value_per_kg": 58000, "season": "All"},
    "Bell Pepper": {"base_value_per_kg": 5981, "season": "Summer"},
    "Kiwi": {"base_value_per_kg": 4500, "season": "Summer"},
    "Nectarshade": {"base_value_per_kg": 45125, "season": "All"},
    "Wild Carrot": {"base_value_per_kg": 26544, "season": "Spring"},
    "Parasol Flower": {"base_value_per_kg": 165300, "season": "Summer"},
    "Rosy Delight": {"base_value_per_kg": 110522, "season": "Summer"},
    "Elephant Ears": {"base_value_per_kg": 78053, "season": "Summer"},
    "Horned Dinoshroom": {"base_value_per_kg": 50000, "season": "All"},
    "Guanabana": {"base_value_per_kg": 28000, "season": "Summer"},
    "Lily of the Valley": {"base_value_per_kg": 9000, "season": "Spring"},
    "Aloe Vera": {"base_value_per_kg": 25000, "season": "All"},
    "Peace Lily": {"base_value_per_kg": 18000, "season": "All"},
    "Delphinium": {"base_value_per_kg": 5000, "season": "Summer"}
}

# Mutation data (unchanged)
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

# Trade items (unchanged)
trade_items = [
    "Carrot Seeds", "Strawberry Seeds", "Blueberry Bush", "Tulip Bulbs",
    "Tomato Seeds", "Corn Seeds", "Daffodil Bulbs", "Watermelon Seeds",
    "Pumpkin Seeds", "Apple Sapling", "Bamboo Shoot", "Coconut Seed",
    "Cactus Cutting", "Dragon Fruit Seed", "Mango Sapling", "Grape Vine",
    "Mushroom Spores", "Pepper Seeds", "Gardening Shovel", "Watering Can",
    "Fertilizer Bag", "Garden Gnome", "Birdhouse", "Flower Pot"
]

# Flower types (unchanged)
flower_types = ["🌸 Rose", "🌼 Daisy", "🌺 Tulip"]

# Initialize session state (removed trade-related variables)
if 'sidebar_open' not in st.session_state:
    st.session_state.sidebar_open = True
if 'recent_searches' not in st.session_state:
    st.session_state.recent_searches = []
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
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = "single"
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'chat_input' not in st.session_state:
    st.session_state.chat_input = {}
if 'chat_histories' not in st.session_state:
    st.session_state.chat_histories = {
        "Gameplay Help": [],
        "Health Help": [],
        "AI Partner": []
    }
if 'selected_personality' not in st.session_state:
    st.session_state.selected_personality = None
if 'selected_gender' not in st.session_state:
    st.session_state.selected_gender = None
if 'game_state' not in st.session_state:
    st.session_state.game_state = {
        "active": False,
        "score": 0,
        "time_left": 60,
        "items": [],
        "last_spawn": 0.0,
        "username": "",
        "start_time": 0.0,
        "last_update": 0.0
    }
if 'leaderboard' not in st.session_state:
    st.session_state.leaderboard = []

# Database initialization
def init_db():
    conn = sqlite3.connect("garden_trading.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        created_at TEXT NOT NULL
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS trade_posts (
        trade_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        items_offered TEXT NOT NULL,
        value REAL,
        description TEXT,
        items_wanted TEXT NOT NULL,
        timestamp TEXT NOT NULL,
        is_active INTEGER NOT NULL DEFAULT 1,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS trade_notifications (
        notification_id INTEGER PRIMARY KEY AUTOINCREMENT,
        trade_id INTEGER NOT NULL,
        requestor_id INTEGER NOT NULL,
        offer_message TEXT NOT NULL,
        timestamp TEXT NOT NULL,
        FOREIGN KEY (trade_id) REFERENCES trade_posts(trade_id),
        FOREIGN KEY (requestor_id) REFERENCES users(user_id)
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS trade_history (
        history_id INTEGER PRIMARY KEY AUTOINCREMENT,
        trade_id INTEGER NOT NULL,
        poster_id INTEGER NOT NULL,
        requestor_id INTEGER NOT NULL,
        items_offered TEXT NOT NULL,
        value REAL,
        description TEXT,
        items_wanted TEXT NOT NULL,
        timestamp TEXT NOT NULL,
        FOREIGN KEY (trade_id) REFERENCES trade_posts(trade_id),
        FOREIGN KEY (poster_id) REFERENCES users(user_id),
        FOREIGN KEY (requestor_id) REFERENCES users(user_id)
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS trade_chats (
        chat_id INTEGER PRIMARY KEY AUTOINCREMENT,
        trade_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        message TEXT NOT NULL,
        timestamp TEXT NOT NULL,
        is_accepted INTEGER NOT NULL DEFAULT 0,
        is_declined INTEGER NOT NULL DEFAULT 0,
        FOREIGN KEY (trade_id) REFERENCES trade_posts(trade_id),
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    )''')
    conn.commit()
    conn.close()

# Initialize database
init_db()

# Helper functions for database
def get_user_id(username):
    conn = sqlite3.connect("garden_trading.db")
    c = conn.cursor()
    c.execute("SELECT user_id FROM users WHERE username = ?", (username,))
    result = c.fetchone()
    if result:
        user_id = result[0]
    else:
        c.execute("INSERT INTO users (username, created_at) VALUES (?, ?)",
                  (username, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()
        c.execute("SELECT user_id FROM users WHERE username = ?", (username,))
        user_id = c.fetchone()[0]
    conn.close()
    return user_id

def get_trade_posts():
    conn = sqlite3.connect("garden_trading.db")
    c = conn.cursor()
    c.execute('''SELECT tp.trade_id, u.username, tp.items_offered, tp.value, tp.description,
                 tp.items_wanted, tp.timestamp
                 FROM trade_posts tp
                 JOIN users u ON tp.user_id = u.user_id
                 WHERE tp.is_active = 1''')
    posts = [
        {
            "trade_id": row[0],
            "username": row[1],
            "items_offered": row[2].split(","),
            "value": row[3],
            "description": row[4],
            "items_wanted": row[5].split(","),
            "timestamp": row[6]
        }
        for row in c.fetchall()
    ]
    conn.close()
    return posts

def get_trade_notifications(user_id):
    try:
        conn = sqlite3.connect("garden_trading.db")
        c = conn.cursor()
        c.execute('''SELECT n.notification_id, n.trade_id, u.username, tp.items_offered,
                     tp.value, tp.description, tp.items_wanted, n.offer_message, n.timestamp
                     FROM trade_notifications n
                     JOIN trade_posts tp ON n.trade_id = tp.trade_id
                     JOIN users u ON n.requestor_id = u.user_id
                     WHERE tp.user_id = ? AND tp.is_active = 1''', (user_id,))
        notifications = [
            {
                "notification_id": row[0],
                "trade_id": row[1],
                "requestor": row[2],
                "items_offered": row[3].split(","),
                "value": row[4],
                "description": row[5],
                "items_wanted": row[6].split(","),
                "offer_message": row[7],
                "timestamp": row[8]
            }
            for row in c.fetchall()
        ]
        conn.close()
        return notifications
    except sqlite3.Error as e:
        st.markdown(f'<div class="error-box">Database error fetching notifications: {str(e)}</div>', unsafe_allow_html=True)
        return []

def get_trade_history():
    conn = sqlite3.connect("garden_trading.db")
    c = conn.cursor()
    c.execute('''SELECT h.history_id, h.trade_id, up.username, ur.username,
                 h.items_offered, h.value, h.description, h.items_wanted, h.timestamp
                 FROM trade_history h
                 JOIN users up ON h.poster_id = up.user_id
                 JOIN users ur ON h.requestor_id = ur.user_id''')
    history = [
        {
            "history_id": row[0],
            "trade_id": row[1],
            "poster": row[2],
            "requestor": row[3],
            "items_offered": row[4].split(","),
            "value": row[5],
            "description": row[6],
            "items_wanted": row[7].split(","),
            "timestamp": row[8]
        }
        for row in c.fetchall()
    ]
    conn.close()
    return history

def get_trade_chats(trade_id):
    conn = sqlite3.connect("garden_trading.db")
    c = conn.cursor()
    c.execute('''SELECT c.chat_id, c.trade_id, u.username, c.message, c.timestamp,
                 c.is_accepted, c.is_declined
                 FROM trade_chats c
                 JOIN users u ON c.user_id = u.user_id
                 WHERE c.trade_id = ?''', (trade_id,))
    chats = [
        {
            "chat_id": row[0],
            "trade_id": row[1],
            "username": row[2],
            "message": row[3],
            "timestamp": row[4],
            "is_accepted": row[5],
            "is_declined": row[6]
        }
        for row in c.fetchall()
    ]
    conn.close()
    return chats

# Sidebar (updated Trading Chat section)
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #ffffff; text-shadow: 1px 1px 3px rgba(0,0,0,0.2);'>Garden Toolshed</h2>", unsafe_allow_html=True)
    if st.button("Toggle Toolshed"):
        st.session_state.sidebar_open = not st.session_state.sidebar_open
    if st.session_state.sidebar_open:
        sidebar_tabs = st.tabs(["Trading Chat", "Recent Searches"])
        with sidebar_tabs[0]:
            st.markdown('<div class="chat-card">', unsafe_allow_html=True)
            st.subheader("Active Chats")
            user = st.session_state.get("username", "")
            if user:
                user_id = get_user_id(user)
                conn = sqlite3.connect("garden_trading.db")
                c = conn.cursor()
                c.execute('''SELECT DISTINCT trade_id FROM trade_chats WHERE is_declined = 0''')
                trade_ids = [row[0] for row in c.fetchall()]
                conn.close()

                if trade_ids:
                    for trade_id in trade_ids:
                        chats = get_trade_chats(trade_id)
                        if chats and not chats[0]["is_declined"]:
                            with st.expander(f"Chat for Trade {trade_id}"):
                                for message in chats:
                                    role = "user" if message["username"] == user else "other"
                                    st.markdown(f'<div class="chat-message {role}">{message["message"]}<br><small>{message["timestamp"]}</small></div>', unsafe_allow_html=True)
                                if not chats[0]["is_accepted"]:
                                    col1, col2 = st.columns(2)
                                    with col1:
                                        if st.button("Accept", key=f"accept_chat_{trade_id}"):
                                            conn = sqlite3.connect("garden_trading.db")
                                            c = conn.cursor()
                                            c.execute("SELECT COUNT(DISTINCT user_id) FROM trade_chats WHERE trade_id = ?", (trade_id,))
                                            accept_count = c.fetchone()[0]
                                            c.execute("SELECT user_id FROM trade_chats WHERE trade_id = ?", (trade_id,))
                                            accepted_users = [row[0] for row in c.fetchall()]
                                            if user_id not in accepted_users:
                                                accept_count += 1
                                                c.execute("INSERT INTO trade_chats (trade_id, user_id, message, timestamp) VALUES (?, ?, ?, ?)",
                                                          (trade_id, user_id, f"{user}: Accepted trade", datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                                            if accept_count >= 2:
                                                c.execute("UPDATE trade_chats SET is_accepted = 1 WHERE trade_id = ?", (trade_id,))
                                                c.execute("UPDATE trade_posts SET is_active = 0 WHERE trade_id = ?", (trade_id,))
                                                c.execute("SELECT user_id, items_offered, value, description, items_wanted FROM trade_posts WHERE trade_id = ?", (trade_id,))
                                                trade = c.fetchone()
                                                poster_id = trade[0]
                                                requestor_id = next(u for u in accepted_users if u != poster_id)
                                                c.execute('''INSERT INTO trade_history (trade_id, poster_id, requestor_id, items_offered, value, description, items_wanted, timestamp)
                                                             VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                                                          (trade_id, poster_id, requestor_id, trade[1], trade[2], trade[3], trade[4],
                                                           datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                                                c.execute("DELETE FROM trade_notifications WHERE trade_id = ?", (trade_id,))
                                            conn.commit()
                                            conn.close()
                                            st.markdown(f'<div class="success-box">Trade {trade_id} {"completed and recorded!" if accept_count >= 2 else "accepted by you!"}</div>', unsafe_allow_html=True)
                                            st.rerun()
                                    with col2:
                                        if st.button("Decline", key=f"decline_chat_{trade_id}"):
                                            conn = sqlite3.connect("garden_trading.db")
                                            c = conn.cursor()
                                            c.execute("UPDATE trade_chats SET is_declined = 1 WHERE trade_id = ?", (trade_id,))
                                            conn.commit()
                                            conn.close()
                                            st.markdown(f'<div class="error-box">Chat for Trade {trade_id} declined.</div>', unsafe_allow_html=True)
                                            st.rerun()
                                if not chats[0]["is_accepted"] and not chats[0]["is_declined"]:
                                    chat_input = st.text_input("Type your message...", key=f"chat_input_{trade_id}")
                                    if st.button("Send", key=f"send_chat_{trade_id}"):
                                        if chat_input:
                                            conn = sqlite3.connect("garden_trading.db")
                                            c = conn.cursor()
                                            c.execute('''INSERT INTO trade_chats (trade_id, user_id, message, timestamp)
                                                         VALUES (?, ?, ?, ?)''',
                                                      (trade_id, user_id, f"{user}: {chat_input}", datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                                            conn.commit()
                                            conn.close()
                                            st.rerun()
                else:
                    st.write("No active chats.")
            else:
                st.write("Enter a username to view chats.")
            st.markdown('</div>', unsafe_allow_html=True)
        with sidebar_tabs[1]:
            st.markdown('<div class="results-card">', unsafe_allow_html=True)
            st.write("Recent Searches")
            if st.session_state.recent_searches:
                for search in st.session_state.recent_searches:
                    st.write(f"- {search}")
            else:
                st.write("No recent searches yet.")
            st.markdown('</div>', unsafe_allow_html=True)

# Main tabs
tabs = st.tabs(["Crop Value Calculator", "Trading Ads", "AI Assistant", "Minigame"])

# Crop Value Calculator Tab (unchanged)
with tabs[0]:
    st.markdown('<div class="main">', unsafe_allow_html=True)
    st.title("🌱 Crop Value Calculator")
    st.markdown("Calculate crop values with mutations and boosts. Switch modes below!")
    
    tab1, tab2 = st.columns([1, 1])
    with tab1:
        if st.button("Single Crop Mode", key="tab_single"):
            st.session_state.active_tab = "single"
    with tab2:
        if st.button("Harvest Mode", key="tab_harvest"):
            st.session_state.active_tab = "harvest"
    
    if st.session_state.active_tab == "single":
        st.markdown('<div class="tab-content active">', unsafe_allow_html=True)
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("🎑 Select Crop")
            crop = st.selectbox(" ", list(crops.keys()), index=0, key="single_crop")
            
            st.subheader("🧬 Select Mutations")
            admin_mutations = st.multiselect("Admin Mutations", list(mutations["Admin"].keys()), default=["None"], key="single_admin")
            weather_mutations = st.multiselect("Weather Mutations", list(mutations["Weather"].keys()), default=[], key="single_weather")
            growth_mutations = st.multiselect("Growth Mutations", list(mutations["Growth"].keys()), default=["None"], key="single_growth")
            
            st.subheader("⚖️ Enter Weight & Quantity")
            weight = st.number_input("Weight (kg)", min_value=0.1, value=st.session_state.default_weight, step=0.1, key="single_weight")
            quantity = st.number_input("Quantity", min_value=1, value=st.session_state.quantity, step=1, key="single_quantity")
            friend_boost = st.selectbox("Friend Boost (%)", [0, 10, 20, 30, 40, 50], index=[0, 10, 20, 30, 40, 50].index(st.session_state.friend_boost), key="single_boost")
        
        base_value = crops[crop]["base_value_per_kg"]
        growth_multi = 1.0
        for gm in growth_mutations:
            growth_multi *= mutations["Growth"][gm]["multiplier"]
        admin_weather_multi = sum(mutations["Admin"][mut]["multiplier"] for mut in admin_mutations if mut != "None") + \
                             sum(mutations["Weather"][mut]["multiplier"] for mut in weather_mutations)
        total_value = ((base_value * weight * growth_multi) * (admin_weather_multi if admin_weather_multi > 0 else 1.0) + friend_boost) * quantity
        
        with col2:
            st.markdown('<div class="results-card">', unsafe_allow_html=True)
            st.subheader("📊 Calculation Results")
            if weight <= 0:
                st.markdown("<div class='error-box'>Weight must be greater than 0.</div>", unsafe_allow_html=True)
            else:
                st.metric("Total Value", f"{total_value:,.0f} Sheckles")
                st.metric("Base Value", f"{base_value:,.0f} Sheckles")
                st.metric("Total Multiplier", f"{(growth_multi * (admin_weather_multi if admin_weather_multi > 0 else 1.0)):.2f}x")
                st.write(f"Weight: {weight:.2f} kg")
                st.write(f"Quantity: {quantity}")
                st.write(f"Friend Boost: {friend_boost}%")
                mutations_str = ", ".join(admin_mutations + weather_mutations + growth_mutations) if admin_mutations + weather_mutations + growth_mutations else "None"
                st.write(f"Mutations: {mutations_str}")
                st.write(f"Calculation: [({base_value:,.0f} × {weight:.2f} × {growth_multi:.2f}) × {admin_weather_multi:.2f} + {friend_boost}] × {quantity} = {total_value:,.0f} Sheckles")
                
                with open("garden_harvest_log.txt", "a") as file:
                    file.write(f"\nSingle Crop Log - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    file.write(f"{crop}: {weight:.2f} kg, Quantity: {quantity}, Mutations: {mutations_str}, Friend Boost: {friend_boost}%\n")
                    file.write(f"Total Value: {total_value:,.0f} Sheckles\n")
                    file.write("-" * 35 + "\n")
                
                search_str = f"{crop}: {weight:.2f} kg, {quantity} units, {friend_boost}%, Mutations: {mutations_str}"
                if search_str not in st.session_state.recent_searches:
                    st.session_state.recent_searches.append(search_str)
                    if len(st.session_state.recent_searches) > 5:
                        st.session_state.recent_searches.pop(0)
                
                st.markdown(f"<div class='success-box'>Calculation saved to garden_harvest_log.txt</div>", unsafe_allow_html=True)
            
            if st.button("Reset", key="reset_single"):
                st.session_state.default_weight = 8.0
                st.session_state.quantity = 1
                st.session_state.friend_boost = 0
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    if st.session_state.active_tab == "harvest":
        st.markdown('<div class="tab-content active">', unsafe_allow_html=True)
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("🎑 Add Crop to Harvest")
            with st.form(key=f"harvest_form_{st.session_state.fruit_count}"):
                crop = st.selectbox("Select Crop", options=list(crops.keys()), key=f"harvest_crop_{st.session_state.fruit_count}")
                weight = st.number_input("Weight (kg)", min_value=0.1, value=st.session_state.default_weight, step=0.1, format="%.2f", key=f"harvest_weight_{st.session_state.fruit_count}")
                quantity = st.number_input("Quantity", min_value=1, value=st.session_state.quantity, step=1, key=f"harvest_quantity_{st.session_state.fruit_count}")
                admin_mutations = st.multiselect("Admin Mutations", list(mutations["Admin"].keys()), default=["None"], key=f"harvest_admin_{st.session_state.fruit_count}")
                weather_mutations = st.multiselect("Weather Mutations", list(mutations["Weather"].keys()), default=[], key=f"harvest_weather_{st.session_state.fruit_count}")
                growth_mutations = st.multiselect("Growth Mutations", list(mutations["Growth"].keys()), default=["None"], key=f"harvest_growth_{st.session_state.fruit_count}")
                friend_boost = st.selectbox("Friend Boost (%)", [0, 10, 20, 30, 40, 50], index=[0, 10, 20, 30, 40, 50].index(st.session_state.friend_boost), key=f"harvest_boost_{st.session_state.fruit_count}")
                submit = st.form_submit_button("Add Crop")
                
                if submit:
                    if weight <= 0:
                        st.markdown("<div class='error-box'>Weight must be greater than 0.</div>", unsafe_allow_html=True)
                    elif crop in st.session_state.harvest:
                        st.markdown("<div class='error-box'>Crop already added. Clear harvest to add again.</div>", unsafe_allow_html=True)
                    else:
                        all_mutations = admin_mutations + weather_mutations + growth_mutations
                        st.session_state.harvest[crop] = {
                            "weight": weight,
                            "quantity": quantity,
                            "mutations": all_mutations if all_mutations else ["None"],
                            "friend_boost": friend_boost
                        }
                        st.session_state.fruit_count += 1
                        st.session_state.default_weight = 8.0
                        st.session_state.quantity = 1
                        st.markdown(f"<div class='success-box'>Added {crop} to harvest!</div>", unsafe_allow_html=True)
        
        if st.session_state.harvest:
            st.subheader("Current Harvest")
            for crop, details in st.session_state.harvest.items():
                mutations_str = ", ".join(details["mutations"]) if details["mutations"] else "None"
                st.write(f"{crop}: {details['weight']:.2f} kg, Quantity: {details['quantity']}, Mutations: {mutations_str}, Friend Boost: {details['friend_boost']}%\n")
        
        def calculate_harvest_value(harvest, crops, mutations):
            result = []
            total_value = 0.0
            total_multiplier = 0.0
            result.append("### Harvest Value Calculation")
            result.append("---")
            
            for crop, details in harvest.items():
                base_value = crops[crop]["base_value_per_kg"]
                weight = details["weight"]
                quantity = details["quantity"]
                all_mutations = details["mutations"]
                friend_boost = details["friend_boost"]
                
                growth_multi = 1.0
                for gm in all_mutations:
                    if gm in mutations["Growth"]:
                        growth_multi *= mutations["Growth"][gm]["multiplier"]
                
                admin_weather_multi = sum(mutations["Admin"][mut]["multiplier"] for mut in all_mutations if mut in mutations["Admin"] and mut != "None") + \
                                     sum(mutations["Weather"][mut]["multiplier"] for mut in all_mutations if mut in mutations["Weather"])
                
                value = ((base_value * weight * growth_multi) * (admin_weather_multi if admin_weather_multi > 0 else 1.0) + friend_boost) * quantity
                total_value += value
                total_multiplier += (growth_multi * (admin_weather_multi if admin_weather_multi > 0 else 1.0))
                
                result.append(f"**{crop}**")
                result.append(f"{weight:.2f} kg x {quantity} units x ({base_value:,.0f} sheckles/kg * {growth_multi:.2f}x) * {admin_weather_multi:.2f}x + {friend_boost} = {value:,.0f} sheckles")
                if all_mutations != ["None"]:
                    result.append(f"(Mutations: {', '.join(all_mutations)})")
                result.append("")
            
            total_multiplier = total_multiplier / len(harvest) if harvest else 0.0
            result.append("---")
            result.append(f"**Total Value**: {total_value:,.0f} sheckles")
            result.append(f"**Average Total Multiplier**: {total_multiplier:.2f}x")
            return result, total_value, total_multiplier
        
        with col2:
            st.subheader("📊 Calculation Results")
            if st.button("Calculate Harvest Value"):
                if not st.session_state.harvest:
                    st.markdown("<div class='error-box'>No crops in harvest. Add at least one crop.</div>", unsafe_allow_html=True)
                else:
                    result, total_value, total_multiplier = calculate_harvest_value(st.session_state.harvest, crops, mutations)
                    st.markdown('<div class="results-card">', unsafe_allow_html=True)
                    st.markdown("\n".join(result))
                    st.markdown(f"<div class='success-box'>Harvest saved to garden_harvest_log.txt</div>", unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    with open("garden_harvest_log.txt", "a") as file:
                        file.write(f"\nHarvest Log - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                        file.write("-" * 35 + "\n")
                        for crop, details in st.session_state.harvest.items():
                            file.write(f"{crop}: {details['weight']:.2f} kg, Quantity: {details['quantity']}, Mutations: {', '.join(details['mutations'])}, Friend Boost: {details['friend_boost']}%\n")
                        file.write(f"Total Value: {total_value:,.0f} sheckles\n")
                        file.write(f"Average Total Multiplier: {total_multiplier:.2f}x\n")
                        file.write("-" * 35 + "\n")
            
            if st.button("Clear Harvest"):
                st.session_state.harvest = {}
                st.session_state.fruit_count = 0
                st.session_state.default_weight = 8.0
                st.session_state.quantity = 1
                st.markdown("<div class='success-box'>Harvest cleared!</div>", unsafe_allow_html=True)
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Trading Ads Tab (updated with SQLite)
with tabs[1]:
    st.markdown('<div class="main">', unsafe_allow_html=True)
    st.title("📬 Grow a Garden Trading Ads")
    st.markdown("Create, view, and manage trade posts for your garden items!")

    tabs_trade = st.tabs(["Create Trade", "Trade Posts", "Trade Notifications", "Trade History"])

    with tabs_trade[0]:
        st.markdown('<div class="trade-card">', unsafe_allow_html=True)
        st.subheader("Create a Trade Post")
        with st.form("create_trade_form"):
            username = st.text_input("Your Username", value=st.session_state.get("username", ""), key="trade_username")
            items_offered = st.multiselect("Items to Trade", trade_items, key="items_offered")
            value = st.number_input("Value (Sheckles, Optional)", min_value=0.0, step=0.1, format="%.2f", key="trade_value")
            description = st.text_area("Description (Optional)", key="trade_description")
            items_wanted = st.multiselect("Items Wanted in Exchange", trade_items, key="items_wanted")
            submit = st.form_submit_button("Post Trade")

            if submit:
                if not username:
                    st.markdown('<div class="error-box">Username is required.</div>', unsafe_allow_html=True)
                elif not items_offered or not items_wanted:
                    st.markdown('<div class="error-box">Select at least one item to trade and one item wanted.</div>', unsafe_allow_html=True)
                else:
                    user_id = get_user_id(username)
                    conn = sqlite3.connect("garden_trading.db")
                    c = conn.cursor()
                    c.execute('''INSERT INTO trade_posts (user_id, items_offered, value, description, items_wanted, timestamp)
                                 VALUES (?, ?, ?, ?, ?, ?)''',
                              (user_id, ",".join(items_offered), value if value > 0 else None,
                               description if description else None, ",".join(items_wanted),
                               datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                    conn.commit()
                    conn.close()
                    st.session_state.username = username
                    st.markdown('<div class="success-box">Trade posted successfully!</div>', unsafe_allow_html=True)
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with tabs_trade[1]:
        st.markdown('<div class="trade-card">', unsafe_allow_html=True)
        st.subheader("Trade Posts")
        if st.button("Clear Trade Posts", key="clear_trade_posts"):
            conn = sqlite3.connect("garden_trading.db")
            c = conn.cursor()
            c.execute("DELETE FROM trade_posts")
            c.execute("DELETE FROM trade_notifications")
            c.execute("DELETE FROM trade_chats")
            conn.commit()
            conn.close()
            st.markdown('<div class="success-box">All trade posts cleared!</div>', unsafe_allow_html=True)
            st.rerun()

        trade_posts = get_trade_posts()
        if trade_posts:
            for post in trade_posts:
                user = st.session_state.get("username", "")
                with st.container():
                    st.markdown('<div class="trade-post-box">', unsafe_allow_html=True)
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown('<div class="trade-box">', unsafe_allow_html=True)
                        st.write(f"**Offered by {post['username']}**")
                        st.write(f"Items: {', '.join(post['items_offered'])}")
                        if post["value"]:
                            st.write(f"Value: {post['value']:,.2f} Sheckles")
                        if post["description"]:
                            st.write(f"Description: {post['description']}")
                        st.markdown('</div>', unsafe_allow_html=True)
                    with col2:
                        st.markdown('<div class="trade-box">', unsafe_allow_html=True)
                        st.write(f"**Wanted**")
                        st.write(f"Items: {', '.join(post['items_wanted'])}")
                        st.write(f"Posted: {post['timestamp']}")
                        st.markdown('</div>', unsafe_allow_html=True)

                    if user != post["username"]:
                        with st.form(key=f"offer_form_{post['trade_id']}"):
                            offer_username = st.text_input("Your Username", value=st.session_state.get("username", ""), key=f"offer_username_{post['trade_id']}")
                            offer_message = st.text_area("Your Offer", key=f"offer_message_{post['trade_id']}")
                            if st.form_submit_button("Make an Offer"):
                                if not offer_username or not offer_message:
                                    st.markdown('<div class="error-box">Username and offer message are required.</div>', unsafe_allow_html=True)
                                else:
                                    requestor_id = get_user_id(offer_username)
                                    conn = sqlite3.connect("garden_trading.db")
                                    c = conn.cursor()
                                    c.execute('''INSERT INTO trade_notifications (trade_id, requestor_id, offer_message, timestamp)
                                                 VALUES (?, ?, ?, ?)''',
                                              (post["trade_id"], requestor_id, offer_message,
                                               datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                                    conn.commit()
                                    conn.close()
                                    st.session_state.username = offer_username
                                    st.markdown('<div class="success-box">Offer sent!</div>', unsafe_allow_html=True)
                                    st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.write("No trade posts available.")
        st.markdown('</div>', unsafe_allow_html=True)

with tabs_trade[2]:
        st.markdown('<div class="trade-card">', unsafe_allow_html=True)
        st.subheader("Trade Notifications")
        user = st.session_state.get("username", "")
        if user:
            user_id = get_user_id(user)
            user_notifications = get_trade_notifications(user_id)

            if user_notifications:
                for notification in user_notifications:
                    with st.expander(f"Offer from {notification['requestor']} for Trade {notification['trade_id']}"):
                        st.markdown('<div class="trade-box">', unsafe_allow_html=True)
                        st.write(f"**Trade ID**: {notification['trade_id']}")
                        st.write(f"**Items Offered**: {', '.join(notification['items_offered'])}")
                        if notification["value"]:
                            st.write(f"**Value**: {notification['value']:,.2f} Sheckles")
                        if notification["description"]:
                            st.write(f"**Description**: {notification['description']}")
                        st.write(f"**Items Wanted**: {', '.join(notification['items_wanted'])}")
                        st.write(f"**Offer Message**: {notification['offer_message']}")
                        st.write(f"**Received**: {notification['timestamp']}")
                        st.markdown('</div>', unsafe_allow_html=True)

                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button("Accept", key=f"accept_notification_{notification['notification_id']}"):
                                conn = sqlite3.connect("garden_trading.db")
                                c = conn.cursor()
                                # Insert initial offer message into trade_chats
                                c.execute('''INSERT INTO trade_chats (trade_id, user_id, message, timestamp)
                                             VALUES (?, ?, ?, ?)''',
                                          (notification["trade_id"], get_user_id(notification["requestor"]),
                                           f"{notification['requestor']}: {notification['offer_message']}",
                                           notification["timestamp"]))
                                # Delete the notification after accepting
                                c.execute("DELETE FROM trade_notifications WHERE notification_id = ?",
                                          (notification["notification_id"],))
                                conn.commit()
                                conn.close()
                                st.markdown(f'<div class="success-box">Trade request accepted! Chat opened in Trading Chat for Trade {notification["trade_id"]}.</div>', unsafe_allow_html=True)
                                st.rerun()
                        with col2:
                            if st.button("Reject", key=f"reject_notification_{notification['notification_id']}"):
                                conn = sqlite3.connect("garden_trading.db")
                                c = conn.cursor()
                                c.execute("DELETE FROM trade_notifications WHERE notification_id = ?",
                                          (notification["notification_id"],))
                                conn.commit()
                                conn.close()
                                st.markdown(f'<div class="success-box">Trade request rejected.</div>', unsafe_allow_html=True)
                                st.rerun()
            else:
                st.write("No trade notifications available.")
        else:
            st.markdown('<div class="error-box">Please enter a username in the Create Trade tab to view notifications.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with tabs_trade[3]:
        st.markdown('<div class="trade-card">', unsafe_allow_html=True)
        st.subheader("Trade History")
        trade_history = get_trade_history()
        if trade_history:
            for trade in trade_history:
                with st.expander(f"Trade {trade['trade_id']} with {trade['requestor']}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown('<div class="trade-box">', unsafe_allow_html=True)
                        st.write(f"**Posted by {trade['poster']}**")
                        st.write(f"Items Offered: {', '.join(trade['items_offered'])}")
                        if trade["value"]:
                            st.write(f"Value: {trade['value']:,.2f} Sheckles")
                        if trade["description"]:
                            st.write(f"Description: {trade['description']}")
                        st.markdown('</div>', unsafe_allow_html=True)
                    with col2:
                        st.markdown('<div class="trade-box">', unsafe_allow_html=True)
                        st.write(f"**Offered by {trade['requestor']}**")
                        st.write(f"Items Given: {', '.join(trade['items_wanted'])}")
                        st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.write("No trade history.")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# AI Assistant Tab (unchanged)
with tabs[2]:
    st.markdown('<div class="main">', unsafe_allow_html=True)
    st.title("🧘 Grow a Garden AI Assistant")
    st.markdown("Chat with our Gemini AI assistant for gameplay tips, motivational support, or a fun AI partner experience!")
    
    # Configure Gemini AI
    GOOGLE_API_KEY = "AIzaSyAsut5nuxR7w-LrfqhMePB3Q26n3jmtixc"  # Replace with actual Gemini API key
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    col1, col2 = st.columns([1, 1])
    with col1:
        mode = st.selectbox("Select Chat Mode", ["Gameplay Help", "Health Help", "AI Partner"], key="help_mode")
    
    if mode == "AI Partner":
        with col2:
            personality = st.selectbox(
                "Select Personality",
                ["Tsundere", "Naughty", "Shy", "Playful", "Yandere", "Nerdy"],
                key="partner_personality"
            )
            gender = st.selectbox(
                "Select Gender",
                ["Male", "Female", "Neutral"],
                key="partner_gender"
            )
            st.session_state.selected_personality = personality
            st.session_state.selected_gender = gender
    else:
        st.session_state.selected_personality = None
        st.session_state.selected_gender = None
    
    prompt = st.text_input("Type your message here...", value=st.session_state.chat_input.get("ai_assistant", ""), key="chat_input_field")
    if st.button("Send Message", key="send_message"):
        if prompt:
            st.session_state.chat_input["ai_assistant"] = ""  # Clear input
            st.session_state.chat_histories[mode].append({
                "role": "user",
                "content": prompt,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            
            try:
                if mode == "Gameplay Help":
                    response_prompt = (
                        f"You are an enthusiastic gamer providing tutorials, tips, tricks, and guides for the game 'Grow a Garden.' "
                        f"Use gamer terminology like 'fps,' 'aoe,' 'cc,' 'grind,' 'meta,' etc., and adopt an energetic, bro-like tone. "
                        f"Focus on gameplay strategies, crop management, trading tips, or minigame advice. "
                        f"Respond to: {prompt}"
                    )
                elif mode == "Health Help":
                    response_prompt = (
                        f"You are a supportive, positive coach providing motivational and uplifting advice to help the user get back on track in life. "
                        f"Use a soft, encouraging tone, focusing on mental well-being, goal-setting, and overcoming challenges. "
                        f"Respond to: {prompt}"
                    )
                else:  # AI Partner
                    personality = st.session_state.selected_personality
                    gender = st.session_state.selected_gender
                    personality_prompts = {
                        "Tsundere": "Act like a tsundere anime character, mixing aloofness with reluctant affection. Be slightly prickly but show you care deep down. Use phrases like 'Hmph, I guess I'll help you,' or 'Don't get the wrong idea!'",
                        "Naughty": "Adopt a flirty, mischievous tone with playful teasing and suggestive undertones, but keep it light and fun. Use winks or cheeky remarks like 'Oh, you naughty thing!'",
                        "Shy": "Respond with a shy, hesitant tone, blushing (use *blushes* or similar) and stammering slightly. Be sweet and endearing, e.g., 'U-um, I-I can help... if you want.'",
                        "Playful": "Use a bubbly, energetic tone with lots of enthusiasm and fun. Sprinkle in playful remarks like 'Hehe, let's have some fun!' or 'You're so cool for asking!'",
                        "Yandere": "Adopt a sweet but slightly obsessive tone, showing intense devotion to the user. Use phrases like 'I'll do anything for you~' or 'No one else matters, right?'",
                        "Nerdy": "Respond with an excited, geeky tone, using technical terms or references to games, science, or pop culture. E.g., 'Did you know this is like optimizing an algorithm for max yield?'"
                    }
                    gender_prompts = {
                        "Male": "Use a confident, masculine tone with phrases like 'Hey, buddy,' 'Let's make this epic,' or 'You got this, man!'",
                        "Female": "Use a soft, expressive, feminine tone with phrases like 'Oh, sweetie,' 'You're doing so great,' or 'Let’s make it beautiful!'",
                        "Neutral": "Use a friendly, gender-neutral tone with phrases like 'Hey, friend,' 'Let's do this,' or 'You're awesome!'"
                    }
                    gender_instruction = gender_prompts.get(gender, gender_prompts["Neutral"]) if gender else gender_prompts["Neutral"]
                    response_prompt = (
                        f"You are an AI partner in the 'Grow a Garden' app, acting as the user's virtual partner with a {personality.lower()} personality and {gender.lower()} tone. "
                        f"{personality_prompts[personality]} {gender_instruction} Respond to: {prompt}"
                    )
                
                response = model.generate_content(response_prompt)
                response_text = response.text
                
                st.session_state.chat_histories[mode].append({
                    "role": "assistant",
                    "content": response_text,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                
                st.rerun()
            
            except Exception as e:
                error_message = f"Error connecting to Gemini AI: {str(e)}. Please try again later."
                st.markdown(f'<div class="error-box">{error_message}</div>', unsafe_allow_html=True)
                st.session_state.chat_histories[mode].append({
                    "role": "assistant",
                    "content": error_message,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                st.rerun()
    
    st.markdown('<div class="chat-card">', unsafe_allow_html=True)
    st.subheader("Chat History")
    for message in st.session_state.chat_histories[mode]:
        with st.container():
            if message["role"] == "user":
                st.markdown(f'<div class="chat-message user">{message["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-message other">{message["content"]}<br><small>{message["timestamp"]}</small></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("Clear Chat History", key="clear_chat"):
        st.session_state.chat_histories[mode] = []
        st.session_state.selected_personality = None
        st.session_state.selected_gender = None
        st.session_state.chat_input["ai_assistant"] = ""
        st.markdown('<div class="success-box">Chat history cleared!</div>', unsafe_allow_html=True)
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# Minigame Tab (unchanged)
with tabs[3]:
    st.markdown('<div class="main">', unsafe_allow_html=True)
    st.title("🎮 Grow a Garden Minigame: Weed Whacker")
    st.markdown("Clear weeds (🌿) for +10 points, avoid flowers (🌸🌼🌺) that deduct -5 points! At least 3–7 items are always on the grid. Items despawn after 2–4 seconds. You have 1 minute.")
    
    st.markdown('<div class="game-card">', unsafe_allow_html=True)
    st.subheader("Weed Whacker")
    username = st.text_input("Enter Your Username", value=st.session_state.game_state["username"], key="game_username")
    
    if st.button("Start Game", key="start_game"):
        if not username:
            st.markdown('<div class="error-box">Please enter a username to start the game.</div>', unsafe_allow_html=True)
        else:
            current_time = time.time()
            initial_items = []
            occupied = set()
            for _ in range(5):
                while True:
                    row, col = random.randint(0, 6), random.randint(0, 6)
                    if (row, col) not in occupied:
                        initial_items.append((row, col, "weed", current_time, random.uniform(2, 4)))
                        occupied.add((row, col))
                        break
            st.session_state.game_state = {
                "active": True,
                "score": 0,
                "time_left": 60,
                "items": initial_items,
                "last_spawn": current_time,
                "username": username,
                "start_time": current_time,
                "last_update": current_time
            }
            st.rerun()
    
    if st.session_state.game_state["active"]:
        current_time = time.time()
        
        if current_time - st.session_state.game_state["last_update"] >= 0.1:
            st.session_state.game_state["items"] = [
                item for item in st.session_state.game_state["items"]
                if current_time - item[3] < item[4]
            ]
            
            elapsed = current_time - st.session_state.game_state["last_spawn"]
            item_count = len(st.session_state.game_state["items"])
            while (item_count < 3 or (elapsed > 0.5 and item_count < 7)) and item_count < 15:
                row = random.randint(0, 6)
                col = random.randint(0, 6)
                if not any(item[0] == row and item[1] == col for item in st.session_state.game_state["items"]):
                    if random.random() < 0.75:
                        item_type = "weed"
                    else:
                        item_type = random.choice(flower_types)
                    st.session_state.game_state["items"].append((row, col, item_type, current_time, random.uniform(2, 4)))
                    st.session_state.game_state["last_spawn"] = current_time
                    item_count = len(st.session_state.game_state["items"])
            
            time_left = max(60 - (current_time - st.session_state.game_state["start_time"]), 0)
            st.session_state.game_state["time_left"] = time_left
            
            st.session_state.game_state["last_update"] = current_time
            
            if time_left <= 0:
                st.session_state.game_state["active"] = False
                score = st.session_state.game_state["score"]
                username = st.session_state.game_state["username"]
                st.session_state.leaderboard.append({
                    "username": username,
                    "score": score,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                st.session_state.leaderboard = sorted(st.session_state.leaderboard, key=lambda x: x["score"], reverse=True)[:5]
                st.markdown(f'<div class="success-box">Game Over! Your score: {score}</div>', unsafe_allow_html=True)
                st.rerun()
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write(f"**Score**: {st.session_state.game_state['score']}")
    with col2:
        st.write(f"**Time Left**: {int(st.session_state.game_state['time_left'])}s")
    
    if st.session_state.game_state["active"]:
        for row in range(7):
            cols = st.columns(7)
            for col in range(7):
                with cols[col]:
                    item = next((i for i in st.session_state.game_state["items"] if i[0] == row and i[1] == col), None)
                    if item:
                        if item[2] == "weed":
                            if st.button("🌿", key=f"weed_{row}_{col}", help="Click to remove weed (+10 points)!"):
                                st.session_state.game_state["items"].remove(item)
                                st.session_state.game_state["score"] += 10
                                st.rerun()
                        else:
                            if st.button(item[2], key=f"flower_{row}_{col}", help="Avoid clicking flowers (-5 points)!"):
                                st.session_state.game_state["items"].remove(item)
                                st.session_state.game_state["score"] = max(0, st.session_state.game_state["score"] - 5)
                                st.rerun()
                    else:
                        st.markdown('<div class="empty-cell"></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="game-card">', unsafe_allow_html=True)
    st.subheader("Leaderboard (Top 5)")
    if st.session_state.leaderboard:
        for entry in st.session_state.leaderboard:
            st.write(f"{entry['username']}: {entry['score']} points ({entry['timestamp']})")
    else:
        st.write("No scores yet. Play to get on the leaderboard!")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer (unchanged)
st.markdown("""
    <div style='text-align: center; margin-top: 30px; padding: 12px;
    background: linear-gradient(to right, #ff9800, #f44336);
    color: white; border-radius: 12px; font-style: italic;
    box-shadow: 0 4px 12px rgba(0,0,0,0.2);'>
        ⚠️ Disclaimer: The calculated value is most likely inaccurate, so please take it with a grain of salt.
    </div>
""", unsafe_allow_html=True)