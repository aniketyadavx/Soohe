import speech_recognition as sr
import webbrowser
import pyttsx3
import os
from openai import OpenAI

# Initialize recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Function to make the assistant speak
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to process commands using OpenAI
def ai_process(command):
    try:
        client = OpenAI(api_key=os.getenv("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"))  # Use environment variable for API key
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Use a valid model name
            messages=[
                {"role": "system", "content": "You are a virtual assistant named Soohee skilled in general tasks like Alexa and Google Assistant."},
                {"role": "user", "content": command}
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"Error in AI processing: {e}")
        return "Sorry, I encountered an error while processing your request."

# Function to process user commands
def process_command(command):
    command = command.lower()
    if "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")
    elif "open youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")
    elif "play" in command:
        song = command.split("play")[1].strip()
        # Assuming musicLibrary is a dictionary with song names as keys and URLs as values
        if "musicLibrary" in globals() and song in musicLibrary.music:
            webbrowser.open(musicLibrary.music[song])
        else:
            speak("Sorry, I couldn't find that song.")
    elif "exit" in command or "stop" in command:
        speak("Goodbye!")
        exit()
    else:
        output = ai_process(command)
        speak(output)

# Main program loop
if __name__ == "__main__":
    speak("Initializing Soohee....")
    while True:
        try:
            with sr.Microphone() as source:
                print("Listening....")
                recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)  # Increased timeout and phrase limit
                command = recognizer.recognize_google(audio)
                print(f"Command received: {command}")

                if "soohee" in command.lower():
                    speak("Yes, how can I help you?")
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)  # Wait for the next command
                    command = recognizer.recognize_google(audio)
                    process_command(command)
        except sr.UnknownValueError:
            print("Sorry, I didn't catch that. Please try again.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
        except Exception as e:
            print(f"Error: {e}")