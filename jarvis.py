import speech_recognition as sr
import webbrowser
import pyttsx3
import requests 
from textblob import TextBlob

#news 
def get_news():
    api_key = "621827580ed64e8cb32a9236d6c9f40f" 
    url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        articles = response.json()["articles"]
        speak("Here are the top news headlines:")
        for i, article in enumerate(articles[:5]):  # Reads top 5 headlines
            speak(f"{i+1}. {article['title']}")
    else:
        speak("Sorry, I couldn't fetch the news.")

#weather
def get_weather(city):
    api_key = "ae8d0e1cf40267b404623d84a190684b" 
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        speak(f"The weather in {city} is {weather} with {temp}°C.")
    else:
        speak("Sorry, I could not retrieve the weather information.")



try:
    import musicLibrary  # Ensure this module exists
except ImportError:
    musicLibrary = None  # Handle missing module


r = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    
    engine.say(text)
    engine.runAndWait()

def processCommand(command):
    """Process recognized commands"""
    command = command.lower()
    print(f"Command received: {command}")


    
    

    if "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://google.com")
    elif "open facebook" in command:
        speak("Opening Facebook")
        webbrowser.open("https://facebook.com")
    elif "open youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://youtube.com")
    elif "weather" in command:
        speak("Which city should I check the weather for?")
        city = take_command()
        get_weather(city)
    elif "news" in command:
        get_news()


    elif command.startswith("play") and musicLibrary:
        song = command.split(" ", 1)[1]  # Get song name after "play"
        if song in musicLibrary.music:
            speak(f"Playing {song}")
            webbrowser.open(musicLibrary.music[song])
        else:
            speak("Song not found in the library.")
    

    else:
        speak("Sorry, I didn't understand that command.")

if __name__ == "__main__":
    speak("Initializing Jarvis...")

    while True:
        print("Listening for 'Jarvis'...")
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=1)
            try:
                audio = r.listen(source, timeout=5, phrase_time_limit=3)
                word = r.recognize_google(audio).lower()
                
                if word == "jarvis":
                    speak("Yes?")
                    print("Jarvis Activated!")

                    # Listen for command
                    audio = r.listen(source, timeout=5, phrase_time_limit=3)
                    command = r.recognize_google(audio)
                    processCommand(command)

            except sr.UnknownValueError:
                print("Could not understand the audio.")
            except sr.RequestError:
                print("Error connecting to Google Speech Recognition.")
            except Exception as e:
                print(f"Error: {e}")
