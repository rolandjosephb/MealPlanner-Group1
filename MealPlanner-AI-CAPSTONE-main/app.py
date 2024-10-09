import os
from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
from dotenv import load_dotenv

# Load API key from environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Configure the model generation
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

app = Flask(__name__)

# Route to render the homepage
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate_meal_plan', methods=['POST'])
def generate_meal_plan():
    data = request.json
    fitness_goal = data.get("fitness_goal")
    food_preference = data.get("food_preference")
    allergies = data.get("allergies")
    weight = data.get("weight")
    height = data.get("height")
    daily_calories = data.get("daily_calories")

    # Automatically construct the specific meal plan query
    query = (
        f"My fitness goal is {fitness_goal}.\n"
        f"I prefer {food_preference} food.\n"
        f"I have allergies to {allergies}.\n"
        f"My weight is {weight} kg and my height is {height}.\n"
        f"My daily calorie requirement is {daily_calories} calories.\n"
        "Please create a 7-day meal plan with specific meals formatted like:\n"
        "Day 1:\n"
        "Breakfast (# calories):** Example meal description.\n"
        "Lunch (# calories):** Example meal description.\n"
        "Dinner (# calories):** Example meal description.\n"
        "Snacks (# calories):** Example snack description.\n"
        
        "**Important Tips:\n"
        "Portion control is key: Use measuring cups and spoons to ensure you're staying within your calorie goals.\n"
        "Choose lean protein: Include lean protein sources like chicken breast, tofu, fish, and lean beef.\n"
        "Prioritize vegetables: Load up on vegetables for fiber and nutrients.\n"
        "Choose whole grains: Opt for whole-wheat pasta, brown rice, and quinoa for sustained energy and fiber.\n"
        "Stay hydrated: Drink plenty of water throughout the day.\n"
        "Be mindful of cheese: Parmesan cheese can be high in calories. Use it in moderation.\n"
        "Use olive oil sparingly: Olive oil is a healthy fat, but it's still high in calories. Use it in moderation.\n"
        
        "Remember: This is just a starting point. You can adjust the meal plan to suit your preferences and needs. "
        "Don't hesitate to experiment with different recipes and flavors to make it enjoyable.\n"
        "Remember: A registered dietitian can provide more customized guidance, taking into account your individual needs and health status."
    )

    # Start chat session
    chat_session = model.start_chat(history=[])

    # Send the constructed query to the model
    response = chat_session.send_message(query)

    # Extract and format the model's response
    formatted_response = response.text.strip()
    
    return jsonify({"meal_plan": formatted_response})

if __name__ == '__main__':
    app.run(debug=True)
