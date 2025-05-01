import os
import json
import streamlit as st
from groq import Groq

# Load API key from config.json
working_dir = os.path.dirname(os.path.abspath(__file__))
config_data = json.load(open(f"{working_dir}/config.json"))
GROQ_API_KEY = config_data["GROQ_API_KEY"]

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

# Streamlit page setup
st.set_page_config(page_title="Stress Management AI", page_icon="🧘", layout="centered")

st.image("stress_relief.png", caption="🌿 The Journey of Your Peaceful Mind Starts Here 🌿", output_format='PNG', use_container_width=True)

st.title("🧘 Stress Management Assistant")

st.write("Describe your current stress level, feelings, and lifestyle, and get a personalized plan.")

# User input
with st.form("stress_form"):
    stress_level = st.slider("Rate your stress level", 0, 10, 5)
    feelings = st.text_area("How are you feeling lately?")
    lifestyle = st.text_area("Describe your daily routine/lifestyle")
    submit = st.form_submit_button("Get Recommendations")

# Chat logic
if submit:
    prompt = f"""You are a compassionate and intelligent assistant trained to help users manage stress.

User reported:
- Stress level: {stress_level}/10
- Feelings: {feelings}
- Lifestyle: {lifestyle}

Based on this, provide:
1. A brief analysis of the user's stress.
2. Breathing or relaxation techniques.
3. Lifestyle improvements.
4. Tips to reduce mental fatigue.
5. Encourage healthy habits.

Use a warm and supportive tone.
"""

    with st.spinner("Generating your personalized stress relief plan..."):
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # Groq's recommended versatile LLaMA 3.3 model
            messages=[{"role": "user", "content": prompt}]
        )

        result = response.choices[0].message.content
        st.success("Here's your personalized plan:")
        st.markdown(result)
