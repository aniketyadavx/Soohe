import speech_recognition as sr
import pyttsx3
import os
import pyautogui
import time
import subprocess
import webbrowser
import datetime
import random
import winsound  # For playing sound files on Windows
import wikipedia

# Initialize text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # 1 for female voice, 0 for male

# Initialize recognizer
recognizer = sr.Recognizer()

# Music playlist (add your own music file paths)
music_playlist = {
    "pop": "E:/Music/Naina_Diljit_Dosanjh.mp3",
    "rock": "C:/Music/rock_song.mp3",
    "jazz": "C:/Music/jazz_song.mp3"
}

def speak(text):
    """Convert text to speech"""
    engine.say(text)
    engine.runAndWait()

def listen():
    """Listen for voice commands"""
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)
        
        try:
            command = recognizer.recognize_google(audio).lower()
            print(f"You said: {command}")
            return command
        except sr.UnknownValueError:
            speak("Sorry,I AM WORKING ON IT.")
            return ""
        except sr.RequestError:
            speak("Sorry, there was an error with the speech recognition service.")
            return ""

def open_application(app_name):
    """Open specified application"""
    try:
        apps = {
            "notepad": "notepad.exe",
            "calculator": "calc.exe",
            "browser": "https://www.google.com",
            "word": "winword.exe",
            "excel": "excel.exe",
            "powerpoint": "powerpnt.exe",
            "outlook": "outlook.exe",
            "vs code": "C:/Program Files/Microsoft VS Code/Code.exe",
            "spotify": "https://open.spotify.com",
            "zoom": "zoom.us"
            
            
            
        }
        
        for key, value in apps.items():
            if key in app_name:
                if "browser" in key:
                    webbrowser.open(value)
                else:
                    os.startfile(value)
                speak(f"Opening {key}")
                return
        speak(f"Sorry, I don't know how to open {app_name}")
    except Exception as e:
        speak(f"Error opening application: {str(e)}")

def music_control(command):
    """Control music playback"""
    try:
        if "play music" in command:
            genre = command.replace("play music", "").strip()
            if not genre:
                genre = random.choice(list(music_playlist.keys()))
            if genre in music_playlist:
                winsound.PlaySound(music_playlist[genre], winsound.SND_ASYNC)
                speak(f"Playing {genre} music")
            else:
                speak("Sorry, I don't have that genre")
        
        elif "stop music" in command:
            winsound.PlaySound(None, winsound.SND_ASYNC)
            speak("Music stopped")
        
        elif "pause music" in command:
            # Note: winsound doesn't support pause, using stop instead
            winsound.PlaySound(None, winsound.SND_ASYNC)
            speak("Music paused")
    except Exception as e:
        speak(f"Music control error: {str(e)}")

def get_time_date():
    """Tell current time and date"""
    current_time = datetime.datetime.now().strftime("%I:%M %p")
    current_date = datetime.datetime.now().strftime("%B %d, %Y")
    speak(f"It's currently {current_time} on {current_date}")

def set_reminder():
    """Set a simple reminder"""
    speak("What time would you like the reminder? Say it like 'in 5 minutes'")
    time_command = listen()
    try:
        if "in" in time_command and "minute" in time_command:
            minutes = int(time_command.split()[1])
            speak(f"Setting reminder for {minutes} minutes from now")
            time.sleep(minutes * 60)
            speak("Reminder! Time's up!")
    except:
        speak("Sorry, I couldn't understand the reminder time")
   

def process_command(command):
    """Process voice commands"""
    if not command:
        return
    
    if "hello" in command:
        speak("Hello! How can I assist you today?")
        
    elif "open geeksforgeeks" in query:
        speak("Opening GeeksforGeeks ")
        webbrowser.open("www.geeksforgeeks.org")
    
    elif "open" in command:
        app_name = command.replace("open", "").strip()
        open_application(app_name)
    
    elif "volume" in command:
        if "up" in command:
            pyautogui.press("volumeup")
            speak("Volume increased")
        elif "down" in command:
            pyautogui.press("volumedown")
            speak("Volume decreased")
        elif "mute" in command:
            pyautogui.press("volumemute")
            speak("Volume muted")
    
    elif "screenshot" in command:
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        screenshot = pyautogui.screenshot()
        screenshot.save(f"screenshot_{timestamp}.png")
        speak("Screenshot taken")
     
    elif "from wikipedia" in query:
        speak("Checking the wikipedia ")
        query = query.replace("wikipedia", "")
        result = wikipedia.summary(query, sentences=2)
        speak("According to wikipedia")
        speak(result)
    elif "music" in command:
        music_control(command)
    
    elif "time" in command or "date" in command:
        get_time_date()
    
    elif "reminder" in command:
        set_reminder()
    
    elif "weather" in command:
        speak("For weather updates, please tell me the city name")
        city = listen()
        if city:
            webbrowser.open(f"https://www.google.com/search?q=weather+{city}")
            speak(f"Opening weather for {city}")
    
    elif "shutdown" in command:
        speak("Shutting down the computer in 10 seconds")
        time.sleep(10)
        os.system("shutdown /s /t 1")
    
    elif "exit" in command or "bye" in command:
        speak("Goodbye")
        exit()
    
    else:
        speak("I'm not sure how to help with that.")

def main():
    """Main function to run the assistant"""
    speak("NAINA is here to help you?")
    
    while True:
        command = listen()
        process_command(command)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        speak("Shutting down the assistant")
    except Exception as e:
        speak(f"An error occurred: {str(e)}")
          
   
     
   