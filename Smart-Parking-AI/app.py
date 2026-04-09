import streamlit as st
from langchain_groq import ChatGroq

# 🔑 API KEY
GROQ_API_KEY = ""

# LLM
llm = ChatGroq(
    temperature=0,
    model_name="llama-3.1-8b-instant",
    api_key=GROQ_API_KEY
)

# ---------------- PARKING DATA (STATE) ---------------- #
if "parking_data" not in st.session_state:
    st.session_state.parking_data = {
        "mall": {"name": "Parking A", "slots": 5},
        "hospital": {"name": "Parking B", "slots": 2},
        "college": {"name": "Parking C", "slots": 10}
    }

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
st.write("Dynamic Parking System with Slot Management")

location = st.text_input("Enter location (mall, hospital, college)")

if location.lower() in st.session_state.parking_data:
    current = st.session_state.parking_data[location.lower()]

    st.info(f"📍 {current['name']} | Available Slots: {current['slots']}")

    col1, col2 = st.columns(2)

    # 🚗 PARK CAR
    if col1.button("🚗 Park Car"):
        if current["slots"] > 0:
            current["slots"] -= 1
            st.success("Car parked successfully ✅")
        else:
            st.error("No slots available ❌")

    # 🚪 LEAVE PARKING
    if col2.button("🚪 Leave Parking"):
        current["slots"] += 1
        st.success("Slot freed successfully ✅")

# FIND PARKING (AI RESPONSE)
if st.button("Find Parking"):

    if location:
        tool_output = parking_finder(location)

        prompt = f"""
User asked: Find parking near {location}

Parking Data: {tool_output}

Give helpful response.
"""

        response = llm.invoke(prompt)

        if "0 slots" in tool_output:
            st.error(response.content)
        elif "No parking" in tool_output:
            st.warning(response.content)
        else:
            st.success(response.content)

    else:
        st.warning("Enter location")