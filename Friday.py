import pyttsx3
import speech_recognition as sr
import datetime
import time
import os
import pyautogui
import sys
import itertools
import threading
from colorama import init, Fore, Back, Style
import random

# Initialize colorama
init(autoreset=True)

def Engine_Init():
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 175)
    volume = engine.getProperty('volume')
    engine.setProperty('volume', min(volume+0.25, 1.0))
    return engine

def Speak(Text):
    engine = Engine_Init()
    print(Fore.CYAN + Text)
    engine.say(Text)
    engine.runAndWait()

# Animation control
animation_running = False
animation_event = threading.Event()

def animate_listening():
    global animation_running
    animation_running = True
    colors = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN]
    symbols = ["🔊", "🎙️", "👂", "🗣️"]
    i = 0
    while animation_running:
        color = colors[i % len(colors)]
        symbol = symbols[i % len(symbols)]
        sys.stdout.write(f'\r{color}Listening {symbol} ' + Style.RESET_ALL)
        sys.stdout.flush()
        i += 1
        time.sleep(0.3)

def animate_recognizing():
    global animation_running
    animation_running = True
    phases = ["⡿", "⣟", "⣯", "⣷", "⣾", "⣽", "⣻", "⢿"]
    colors = [Fore.YELLOW, Fore.LIGHTYELLOW_EX, Fore.LIGHTRED_EX, Fore.LIGHTMAGENTA_EX]
    i = 0
    while animation_running:
        color = colors[i % len(colors)]
        phase = phases[i % len(phases)]
        sys.stdout.write(f'\r{color}Processing {phase} ' + Style.RESET_ALL)
        sys.stdout.flush()
        i += 1
        time.sleep(0.1)

def animate_sleeping():
    global animation_running
    animation_running = True
    sleep_emojis = ["💤", "😴", "🌙", "✨", "⭐"]
    colors = [Fore.BLUE, Fore.LIGHTBLUE_EX, Fore.WHITE, Fore.LIGHTWHITE_EX]
    while animation_running:
        for i in range(5):
            for emoji in sleep_emojis:
                color = random.choice(colors)
                sys.stdout.write(f'\r{color}Sleeping {emoji} (Say "wake up") {emoji} ' + Style.RESET_ALL)
                sys.stdout.flush()
                time.sleep(0.2)
                if not animation_running:
                    return

def stop_animation():
    global animation_running
    animation_running = False
    sys.stdout.write('\r' + ' ' * 50 + '\r')
    sys.stdout.flush()

def print_banner():
    banner = r"""
    ╔════════════════════════════════════════════╗
    ║                                            ║
    ║     🎙️  JARVIS Voice Assistant  🎙️        ║
    ║                                            ║
    ╚════════════════════════════════════════════╝
    """
    print(Fore.LIGHTMAGENTA_EX + banner + Style.RESET_ALL)

def Take_Command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1.5)
        r.pause_threshold = 1.0
        r.phrase_threshold=0.3
        r.energy_threshold = 3000
        
        animation_thread = threading.Thread(target=animate_listening)
        animation_thread.start()
        
        audio = r.listen(source)
        stop_animation()
    
    try:
        animation_thread = threading.Thread(target=animate_recognizing)
        animation_thread.start()
        
        query = r.recognize_google(audio, language = 'en-in')
        stop_animation()
        
        print(Fore.LIGHTGREEN_EX + f'\rBoss said: {query}' + Style.RESET_ALL)
    except Exception as e:
        stop_animation()
        print(Fore.RED + "Please Say that again Boss." + Style.RESET_ALL)
        return 'None'
    return query.lower()

def CAL_DAY():
    day = datetime.datetime.today().weekday() +1
    day_dict = {
        1:"Monday",
        2:"Tuesday",
        3:"Wednesday",
        4:"Thursday",
        5:"Friday",
        6:"Saturday",
        7:"Sunday"
    }
    if day in day_dict.keys():
        day_of_week = day_dict[day]
        return day_of_week
    
def WishMe():
    hour = int(datetime.datetime.now().hour)
    t = time.strftime('%I:%M %p')
    day = CAL_DAY()

    if (hour>=0) and (hour<12) and ('AM' in t):
        Speak(f'Good Morning Boss. Its {day} and the time is {t}')
    elif (hour>=12) and (hour<16) and ('PM' in t):
        Speak(f'Good Afternoon Boss. The time is {t}')
    elif (hour>=16) and (hour<18) and ('PM' in t):
        Speak(f'Good Evening Boss. The time is now {t}')
    else:
        Speak(f'Good Night Boss. The time is now {t}')

if __name__ == '__main__':
    print_banner()
    WishMe()
    Speak("How can I help you Boss?")
    
    sleep_mode = False

    while True:
        if not sleep_mode:
            query = Take_Command()
        else:
            with sr.Microphone() as source:
                r = sr.Recognizer()
                r.adjust_for_ambient_noise(source)

                animation_thread = threading.Thread(target=animate_sleeping)
                animation_thread.start()
                
                audio = r.listen(source)
                stop_animation()
                
                try:
                    wake_query = r.recognize_google(audio, language='en-in').lower()
                    if "wake up" in wake_query:
                        sleep_mode = False
                        Speak("I'm awake now Boss! How can I help you?")
                        continue
                except:
                    continue

        if query == 'none' or not query:
            continue

        if "go to sleep" in query:
            sleep_mode = True
            Speak("Going to sleep mode. Say 'wake up' when you need me.")
            continue

        if sleep_mode:
            continue

        if "open game" in query:
            Speak("Which game do you want to open? Warband or Minecraft? Input 1 or 2.")
            inj = input("Enter Number: ")
            if "1" in inj:
                Speak("Oening Mount and blade warbend")
                os.startfile("C:\\GOG Games\\Mount and Blade - Warband\\mb_warband.exe")
                Speak("It is on your Display")
            elif "2" in inj:
                Speak("Oening Tlancher..")
                os.startfile('C:\\Users\\Hemal\\AppData\\Roaming\\.minecraft\\TLauncher.exe')
                Speak("It is on your Display")

        elif "open msi" in query:
            try:
                os.startfile("C:\\Program Files\\BlueStacks_msi5\\HD-Player.exe")
                Speak("MSI AppPlayer is now running")
            except Exception as e:
                Speak("Sorry Boss, I couldn't open MSI AppPlayer")
        
        elif "open cheat engine" in query:
            Speak("Opening Cheat Engine")
            os.startfile("C:\\Program Files\\Cheat Engine\\Cheat Engine.exe")
            Speak("Opened Cheat Engine")


        #Pyautogui Keypress
        elif "press enter" in query:
            Speak("Pressing Enter Key")
            pyautogui.keyDown('enter')
            pyautogui.keyUp('enter')
            Speak("Enter Key pressed")

        elif "type something" in query:
            Speak("Tell Me What Do You Want To Type")
            tk = Take_Command()
            pyautogui.typewrite(tk)
            Speak(f"You Have Ask Me To type {tk}. Can i asume it correctly.")

        elif "switch tab" in query:
            Speak("Switching tab")
            pyautogui.keyDown("alt")
            pyautogui.press("tab")
            pyautogui.keyUp("alt")
            Speak("Tab is switched")

        elif "play music" in query:
            path_music = "E:\\Music"
            song = os.listdir(path_music)
            Speak("Which song you went to play. Input Any number of this.")
            print(
                "DIA DELÍCIA = 0" 
                "FUNK SIGILO = 1" 
                "Itachi theam = 2" 
                "JUJALARIM ponk = 3" 
                "Kakashi Rap = 4" 
                "Matushka Ultrafunk = 5" 
                "Mean Mera = 6" 
                "NCTS = 7" 
                "ODNOGO FUNK = 8" 
                "ODNOGO ULTRAFUNK = 9" 
                "Ogryzek - AURA = 10" 
                "Ogryzek - EMPIRE = 11"
            )
            kit = int(input("Input Your Number: "))
            os.startfile(os.path.join(path_music,song[kit]))

        elif "puase music" in query:
            Speak("Pauseing Music")
            pyautogui.press("playpause")
            Speak("Music Paused")

        elif "quit" in query or "exit" in query or "stop" in query:
            Speak("Goodbye Boss! Have a great day!")
            for i in range(3, 0, -1):
                sys.stdout.write(f'\r{Fore.RED}Shutting down in {i}...' + Style.RESET_ALL)
                sys.stdout.flush()
                time.sleep(1)
            print("\n")
            break    

        if not sleep_mode:
            Speak("What else can I do for you Boss?")