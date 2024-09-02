import streamlit as st
import anthropic
import os

# Initialize usage counter and built-in API key
usage_count = st.session_state.get('usage_count', 0)
built_in_api_key = os.getenv("CLAUDE_API_KEY")

# Function to create the Claude client based on the key
def create_claude_client(api_key):
    return anthropic.Anthropic(api_key=api_key)

# Prompt for user's own API key if usage exceeds limit
user_api_key = None
if usage_count >= 2:
    st.warning("You have reached the limit of using the built-in API key. Please enter your own API key to continue.It is for the testing purpose but if you want to use this generate your claude api for free from https://www.anthropic.com/api ")
    user_api_key = st.text_input("Enter your Claude API key:", type="password")

# Decide which API key to use
api_key_to_use = user_api_key if user_api_key else built_in_api_key

# Create the Claude client
client = create_claude_client(api_key_to_use)

# Functions to generate content using Claude API
def generate_game_environment(environment_description):
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=150,
        temperature=0,
        system="You are a creative game designer. Generate a detailed and immersive game environment description.",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"Describe the game environment based on the following details: {environment_description}"
                    }
                ]
            }
        ]
    )
    return message.content[0].text

def generate_protagonist(protagonist_description):
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=150,
        temperature=0,
        system="You are a creative game designer. Generate a detailed and compelling protagonist description.",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"Describe the protagonist based on the following traits: {protagonist_description}"
                    }
                ]
            }
        ]
    )
    return message.content[0].text

def generate_antagonist(antagonist_description):
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=150,
        temperature=0,
        system="You are a creative game designer. Generate a detailed and menacing antagonist description.",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"Describe the antagonist based on the following traits: {antagonist_description}"
                    }
                ]
            }
        ]
    )
    return message.content[0].text

def generate_game_story(environment_description, protagonist_description, antagonist_description):
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=150,
        temperature=0,
        system="You are a creative game designer. Generate an engaging game story.",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"Create a game story based on the following details:\nEnvironment: {environment_description}\nProtagonist: {protagonist_description}\nAntagonist: {antagonist_description}"
                    }
                ]
            }
        ]
    )
    return message.content[0].text

# Set up the title in the center
st.markdown("<h1 style='text-align: center;'>Game Design Document Generator</h1>", unsafe_allow_html=True)

# Description below the title
st.write("""
This tool helps game developers generate a comprehensive Game Design Document (GDD) by providing structured inputs for the game environment, protagonist, antagonist, and the overarching game story.
""")

# Sidebar inputs
st.sidebar.header("Game Environment")
environment = st.sidebar.text_area("Describe the game environment:")

st.sidebar.header("Protagonist")
protagonist = st.sidebar.text_area("Describe the protagonist:")

st.sidebar.header("Antagonist")
antagonist = st.sidebar.text_area("Describe the antagonist:")

# Generate Button
if st.sidebar.button("Generate Game Design Document"):
    if usage_count < 2 or user_api_key:
        # Generate content based on inputs
        environment_text = generate_game_environment(environment)
        protagonist_text = generate_protagonist(protagonist)
        antagonist_text = generate_antagonist(antagonist)
        game_story_text = generate_game_story(environment, protagonist, antagonist)

        # Display the generated content in the main area with centered headings
        st.markdown("<h2 style='text-align: center;'>Game Environment</h2>", unsafe_allow_html=True)
        st.write(environment_text)

        st.markdown("<h2 style='text-align: center;'>Protagonist</h2>", unsafe_allow_html=True)
        st.write(protagonist_text)

        st.markdown("<h2 style='text-align: center;'>Antagonist</h2>", unsafe_allow_html=True)
        st.write(antagonist_text)

        st.markdown("<h2 style='text-align: center;'>Game Story</h2>", unsafe_allow_html=True)
        st.write(game_story_text)

        # Increment the usage count
        st.session_state.usage_count = usage_count + 1
    else:
        st.error("You need to enter your own API key to generate more content.")
