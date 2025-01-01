import requests
import json
from dotenv import load_dotenv
from puter import add_message, synthesize

def chat():
    print("You'll be talking to Chatbot (type 'exit' to quit)\nChatbot: Hello! How can I assist you today?")
    while True:
        user_input = input("You: ")
        if user_input.lower().strip() == "exit":
            print("Chatbot: Goodbye!")
            break
        bot_response = add_message(user_input)
        print(f"Chatbot: {bot_response}")

def main():
    print("Welcome! Please choose an option (or any other value to exit):")
    print("1. Chat")
    print("2. Generate Text to Speech (TTS)")
    choice = input("Enter the number of your choice: ")
    if choice == "1":
        chat()
    elif choice == "2":
        user_text = input("Enter the text you want to synthesize: ")
        responseContent = synthesize(user_text)
        if responseContent != None:
            with open('output_file.mp3', 'wb') as file:
                file.write(responseContent)
            print("MP3 file has been saved as 'output_file.mp3'.")
        else:
            print(f"Failed to retrieve the file.")
    else:
        print("Invalid choice so you want to quit.")

main()