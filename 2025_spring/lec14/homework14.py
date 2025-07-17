import datetime
import random
from gtts import gTTS
import speech_recognition as sr

def what_time_is_it(lang, filename):
    now = datetime.datetime.now()
    if lang.startswith('en'):
        text = f"The time is {now.strftime('%I:%M %p')}."
    elif lang.startswith('ja'):
        text = f"現在の時刻は {now.strftime('%H時%M分')} です。"
    else:
        text = f"The current time is {now.strftime('%H:%M')}."

    tts = gTTS(text=text, lang=lang)
    tts.save(filename)

def tell_me_a_joke(lang, audiofile):
    jokes = {
        'en': [
            "Why don't scientists trust atoms? Because they make up everything!",
            "What did the ocean say to the beach? Nothing, it just waved."
        ],
        'ja': [
            "コンピューターが疲れた理由は？ウィンドウズが多すぎたから。",
            "お寿司屋さんが嫌いな数学の授業は？さしすせそ。"
        ]
    }
    selected_joke = random.choice(jokes.get(lang[:2], ["I don't know any jokes in that language."]))
    tts = gTTS(text=selected_joke, lang=lang)
    tts.save(audiofile)

def what_day_is_it(lang, audiofile):
    today = datetime.datetime.today()
    if lang.startswith('en'):
        text = f"Today is {today.strftime('%A, %B %d, %Y')}."
    elif lang.startswith('ja'):
        weekdays = ['月曜日', '火曜日', '水曜日', '木曜日', '金曜日', '土曜日', '日曜日']
        day_text = weekdays[today.weekday()]
        text = f"今日は {today.year}年{today.month}月{today.day}日、{day_text}です。"
    else:
        text = today.strftime('%Y-%m-%d')

    tts = gTTS(text=text, lang=lang)
    tts.save(audiofile)

    # Return a URL for a calendar view
    return f"https://www.timeanddate.com/calendar/?year={today.year}&month={today.month}"

def personal_assistant(lang, filename):
    r = sr.Recognizer()
    mic = sr.Microphone()
    print("Please speak a command...")

    with mic as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    try:
        command = r.recognize_google(audio, language=lang)
        command = command.lower()
        print("You said:", command)

        if "time" in command or ("時刻" in command):
            what_time_is_it(lang, filename)
        elif "day" in command or ("日" in command):
            what_day_is_it(lang, filename)
        elif "joke" in command or ("ジョーク" in command):
            tell_me_a_joke(lang, filename)
        else:
            tts = gTTS(text="Sorry, I did not understand that.", lang=lang)
            tts.save(filename)

    except Exception as e:
        print("Error:", e)
        tts = gTTS(text="I couldn't understand. Please try again.", lang=lang)
        tts.save(filename)