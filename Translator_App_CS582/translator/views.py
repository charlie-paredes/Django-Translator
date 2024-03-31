from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from playsound import playsound
import speech_recognition as sr
from googletrans import Translator
from django.shortcuts import redirect
from gtts import gTTS
import os
import base64


def home(request):

    dic = (
        "afrikaans",
        "af",
        "albanian",
        "sq",
        "amharic",
        "am",
        "arabic",
        "ar",
        "armenian",
        "hy",
        "azerbaijani",
        "az",
        "basque",
        "eu",
        "belarusian",
        "be",
        "bengali",
        "bn",
        "bosnian",
        "bs",
        "bulgarian",
        "bg",
        "catalan",
        "ca",
        "cebuano",
        "ceb",
        "chichewa",
        "ny",
        "chinese (simplified)",
        "zh-cn",
        "chinese (traditional)",
        "zh-tw",
        "corsican",
        "co",
        "croatian",
        "hr",
        "czech",
        "cs",
        "danish",
        "da",
        "dutch",
        "nl",
        "english",
        "en",
        "esperanto",
        "eo",
        "estonian",
        "et",
        "filipino",
        "tl",
        "finnish",
        "fi",
        "french",
        "fr",
        "frisian",
        "fy",
        "galician",
        "gl",
        "georgian",
        "ka",
        "german",
        "de",
        "greek",
        "el",
        "gujarati",
        "gu",
        "haitian creole",
        "ht",
        "hausa",
        "ha",
        "hawaiian",
        "haw",
        "hebrew",
        "he",
        "hindi",
        "hi",
        "hmong",
        "hmn",
        "hungarian",
        "hu",
        "icelandic",
        "is",
        "igbo",
        "ig",
        "indonesian",
        "id",
        "irish",
        "ga",
        "italian",
        "it",
        "japanese",
        "ja",
        "javanese",
        "jw",
        "kannada",
        "kn",
        "kazakh",
        "kk",
        "khmer",
        "km",
        "korean",
        "ko",
        "kurdish (kurmanji)",
        "ku",
        "kyrgyz",
        "ky",
        "lao",
        "lo",
        "latin",
        "la",
        "latvian",
        "lv",
        "lithuanian",
        "lt",
        "luxembourgish",
        "lb",
        "macedonian",
        "mk",
        "malagasy",
        "mg",
        "malay",
        "ms",
        "malayalam",
        "ml",
        "maltese",
        "mt",
        "maori",
        "mi",
        "marathi",
        "mr",
        "mongolian",
        "mn",
        "myanmar (burmese)",
        "my",
        "nepali",
        "ne",
        "norwegian",
        "no",
        "odia",
        "or",
        "pashto",
        "ps",
        "persian",
        "fa",
        "polish",
        "pl",
        "portuguese",
        "pt",
        "punjabi",
        "pa",
        "romanian",
        "ro",
        "russian",
        "ru",
        "samoan",
        "sm",
        "scots gaelic",
        "gd",
        "serbian",
        "sr",
        "sesotho",
        "st",
        "shona",
        "sn",
        "sindhi",
        "sd",
        "sinhala",
        "si",
        "slovak",
        "sk",
        "slovenian",
        "sl",
        "somali",
        "so",
        "spanish",
        "es",
        "sundanese",
        "su",
        "swahili",
        "sw",
        "swedish",
        "sv",
        "tajik",
        "tg",
        "tamil",
        "ta",
        "telugu",
        "te",
        "thai",
        "th",
        "turkish",
        "tr",
        "ukrainian",
        "uk",
        "urdu",
        "ur",
        "uyghur",
        "ug",
        "uzbek",
        "uz",
        "vietnamese",
        "vi",
        "welsh",
        "cy",
        "xhosa",
        "xh",
        "yiddish",
        "yi",
        "yoruba",
        "yo",
        "zulu",
        "zu",
    )

    return render(request, "home.html")


def translation_result(request, translated_text, translated_audio):
    return render(
        request,
        "translation_result.html",
        {
            "translated_text": translated_text,
            "translated_audio": translated_audio,
        },
    )


@csrf_exempt
def translate(request):
    if request.method == "POST":
        # Retrieve the audio data and the destination language from the request
        audio_data_url = request.POST.get("audio_data")
        to_lang = request.POST.get("to_lang")

        # Decode the audio data from base64
        audio_data = base64.b64decode(audio_data_url.split(",")[1])

        # Perform the translation
        translated_text = translate_text(
            audio_data, to_lang
        )  # Call translate_text with two arguments
        translated_audio = "Translated audio"  # Replace with actual translated audio

        # Redirect to the translation_result view with the translated text and audio
        return redirect(
            "translation_result",
            translated_text=translated_text,
            translated_audio=translated_audio,
        )

    # If request method is not POST, redirect to home page or handle it appropriately
    return redirect("home")


def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening.....")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing audio.....")
        query = r.recognize_google(audio, language="en-in")
        print(f"The User said {query}\n")
        return query
    except Exception as e:
        print("say that again please.....")
        return None


def translate_text(query, to_lang):
    translator = Translator()
    translated = translator.translate(query, dest=to_lang)
    return translated.text


def generate_audio(text):
    speak = gTTS(text=text, lang="es", slow=False)
    speak.save("captured_voice.mp3")
    playsound("captured_voice.mp3")
    os.remove("captured_voice.mp3")
