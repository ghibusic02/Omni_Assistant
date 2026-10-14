import os
import base64
import google.genai as genai
from PIL import Image

# API Configuration
API_KEY = "AQ.Ab8RN6IlXjeyhQjzpb1VivxuKqskdyzxq60jEt9jpVEbMuUbag" 

# Initialize the modern Gemini Client
client = genai.Client(api_key=API_KEY)
MODEL_NAME = "gemini-3.8-flash"

def text_summarizer_module():
    print("\n--- MODULE: TEXT SUMMARIZER & ANALYZER ---")
    user_text = input("Paste or type the text you want me to analyze:\n> ")
    if not user_text.strip():
        print("Error: The provided text is empty.")
        return
    prompt = f"Analyze and summarize this text in 3-5 bullet points with sentiment analysis:\n{user_text}"
    try:
        interaction = client.interactions.create(model=MODEL_NAME, input=prompt)
        print("\n--- ANALYSIS RESULT ---")
        print(interaction.output_text)
    except Exception as e:
        print(f"An error occurred: {e}")

def interactive_chatbot_module():
    print("\n--- MODULE: INTERACTIVE CHATBOT --- (Type 'exit' to quit)")
    previous_id = None
    while True:
        user_message = input("\nYou: ")
        if user_message.lower() == 'exit': break
        try:
            interaction = client.interactions.create(
                model=MODEL_NAME, 
                input=user_message, 
                previous_interaction_id=previous_id
            )
            print(f"AI: {interaction.output_text}")
            previous_id = interaction.id
        except Exception as e:
            print(f"An error occurred: {e}")

def computer_vision_module():
    print("\n--- MODULE: COMPUTER VISION ---")
    image_path = input("Enter path to image:\n> ").strip("'\"")
    if not os.path.exists(image_path):
        print("Error: File not found.")
        return
    user_question = input("What do you want to know about this image?\n> ")
    try:
        with open(image_path, "rb") as f:
            image_b64 = base64.b64encode(f.read()).decode("utf-8")
        interaction = client.interactions.create(
            model=MODEL_NAME,
            input=[{"type": "text", "text": user_question}, 
                   {"type": "image", "data": image_b64, "mime_type": "image/jpeg"}]
        )
        print("\n--- VISUAL AI RESPONSE ---")
        print(interaction.output_text)
    except Exception as e:
        print(f"An error occurred: {e}")

def main_menu():
    while True:
        print("\n1. Text Summarizer\n2. ChatBot\n3. Computer Vision\n4. Exit")
        choice = input("Select an option (1-4): ")
        if choice == "1": text_summarizer_module()
        elif choice == "2": interactive_chatbot_module()
        elif choice == "3": computer_vision_module()
        elif choice == "4": break

if __name__ == "__main__":
    main_menu()
