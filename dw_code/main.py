import os
import json
import gradio as gr
from groq import Groq

# Load API key from config file
working_dir = os.path.dirname(os.path.abspath(__file__))
config_data = json.load(open(f"{working_dir}/config.json"))
GROQ_API_KEY = config_data["GROQ_API_KEY"]

client = Groq(api_key=GROQ_API_KEY)

# Function to build prompt and get response
def get_recommendation(age, gender, goal, food_prefs, allergies):
    prompt = f"""You are a health and fitness assistant. Create a personalized **diet and workout plan** based on the following details:

- Age: {age}
- Gender: {gender}
- Fitness Goal: {goal}
- Food Preferences: {food_prefs}
- Allergies or Restrictions: {allergies}

Be specific and structured. Include meal suggestions and a weekly workout schedule.
"""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content

# Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("## 🥗 AI Diet & Workout Planner (LLaMA 3.3 via Groq)")

    with gr.Row():
        age = gr.Textbox(label="Age")
        gender = gr.Dropdown(choices=["Male", "Female", "Other"], label="Gender")
    
    goal = gr.Textbox(label="Fitness Goal (e.g., weight loss, muscle gain)")
    food_prefs = gr.Textbox(label="Food Preferences (e.g., vegetarian, keto, Indian)")
    allergies = gr.Textbox(label="Allergies / Restrictions")

    submit_btn = gr.Button("Get Recommendation")
    output = gr.Textbox(label="Your Personalized Plan", lines=15)

    submit_btn.click(
        fn=get_recommendation,
        inputs=[age, gender, goal, food_prefs, allergies],
        outputs=output
    )

demo.launch(share=True)