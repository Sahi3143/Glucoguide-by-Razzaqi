import streamlit as st
import anthropic

api_key = st.secrets["claude_api_key"]

# Function to call Claude AI API and get a personalized meal plan
def get_meal_plan(api_key, age, sex, fasting_sugar, post_meal_sugar):
    # Initialize the Claude AI client with the provided API key
    client = anthropic.Anthropic(api_key=api_key)
    
    # Define the prompt to send to Claude AI
    prompt = (
        f"My age is {age} mg/dL, "
        f"my sex is {sex} mg/dL, "
        f"and my post-meal sugar level is {post_meal_sugar} mg/dL. "
        f"My fasting sugar is {fasting_sugar}. "
        "Please provide a personalized meal plan that can help me manage my blood sugar levels effectively. Take into account all the factors like age and sex. Suggest from variety of food"
    )
    
    # Call Claude AI API
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=500,
        temperature=-1,
        system="You are a world-class nutritionist who specializes in diabetes management.",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    
    raw_context = message.content
    itinerary = raw_context[0].text
    return itinerary

# Streamlit app
st.title("GlucoGuide by Razzaqi")

st.write("""
**GlucoGuide** is a personalized meal planning tool designed specifically for diabetic patients. 
By entering your sugar levels and dietary preferences, GlucoGuide generates meal plans that are 
tailored to help you manage your blood sugar levels effectively.
""")

# Sidebar inputs for sugar levels and dietary preferences
st.sidebar.header("Enter Your Details")

age = st.sidebar.number_input("Age (Years)", min_value=0, max_value=500, step=1)
fasting_sugar = st.sidebar.number_input("Fasting Sugar Levels (mg/dL)", min_value=0, max_value=500, step=1)
post_meal_sugar = st.sidebar.number_input("Post-Meal Sugar Levels (mg/dL)", min_value=0, max_value=500, step=1)
sex = st.sidebar.text_input("Sex (Male, Female)")

# Generate meal plan button
if st.sidebar.button("Generate Meal Plan"):
    meal_plan = get_meal_plan(api_key, age, sex, fasting_sugar, post_meal_sugar)
    st.write("Based on your sugar levels and dietary preferences, here is a personalized meal plan:")
    st.markdown(meal_plan)
        
