import streamlit as st
from langchain_groq import ChatGroq
import json
import os

# 🔑 API KEY (DON'T PUT REAL KEY IN GITHUB)
GROQ_API_KEY = "    "

# LLM
llm = ChatGroq(
    temperature=0,
    model_name="llama-3.1-8b-instant",
    api_key=GROQ_API_KEY
)

# ---------- FILE NAME ----------
FILE = "parking_data.json"

# ---------- LOAD DATA ----------
def load_data():
    if os.path.exists(FILE):
        with open(FILE, "r") as f:
            return json.load(f)
    else:
        return {
            "mall": {"name": "Parking A", "slots": 5},
            "hospital": {"name": "Parking B", "slots": 2},
            "college": {"name": "Parking C", "slots": 10}
        }

# ---------- SAVE DATA ----------
def save_data(data):
    with open(FILE, "w") as f:
        json.dump(data, f)

# ---------- INITIALIZE ----------
if "parking_data" not in st.session_state:
    st.session_state.parking_data = load_data()

# TOOL
def parking_finder(location):
    data = st.session_state.parking_data
    if location.lower() in data:
        p = data[location.lower()]
        return f"{p['name']} - {p['slots']} slots available"
    else:
        return "No parking found"

# UI
st.set_page_config(page_title="Smart Parking AI", page_icon="🚗")

st.title("🚗 Smart Parking Assistant")
st.write("Persistent Parking System (Data saved even after refresh)")

location = st.text_input("Enter location (mall, hospital, college)")

if location.lower() in st.session_state.parking_data:
    current = st.session_state.parking_data[location.lower()]

    st.info(f"📍 {current['name']} | Slots: {current['slots']}")

    col1, col2 = st.columns(2)

    # 🚗 PARK
    if col1.button("🚗 Park Car"):
        if current["slots"] > 0:
            current["slots"] -= 1
            save_data(st.session_state.parking_data)  # SAVE
            st.success("Car parked ✅")
        else:
            st.error("No slots ❌")

    # 🚪 LEAVE
    if col2.button("🚪 Leave"):
        current["slots"] += 1
        save_data(st.session_state.parking_data)  # SAVE
        st.success("Slot freed ✅")

# AI RESPONSE
if st.button("Find Parking"):
    if location:
        tool_output = parking_finder(location)

        response = llm.invoke(f"Parking at {location}: {tool_output}")

        st.write(response.content)
    else:
        st.warning("Enter location")
