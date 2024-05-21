from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
import speech_recognition as sr
from googletrans import Translator
from django.shortcuts import redirect
from gtts import gTTS
from pydub import AudioSegment
from io import BytesIO
import base64
import io
from django.conf import settings

AudioSegment.converter = "C:\\Program Files\\ffmpeg\\bin\\ffmpeg.exe"

def home(request):
    return render(request, "home.html")

def get_code(lang_name):
    dic = {
        "afrikaans": "af",
        "albanian": "sq",
        "amharic": "am",
        "arabic": "ar",
        "armenian": "hy",
        "azerbaijani": "az",
        "basque": "eu",
        "belarusian": "be",
        "bengali": "bn",
        "bosnian": "bs",
        "bulgarian": "bg",
        "catalan": "ca",
        "cebuano": "ceb",
        "chichewa": "ny",
        "chinese (simplified)": "zh-cn",
        "chinese (traditional)": "zh-tw",
        "corsican": "co",
        "croatian": "hr",
        "czech": "cs",
        "danish": "da",
        "dutch": "nl",
        "english": "en",
        "esperanto": "eo",
        "estonian": "et",
        "filipino": "tl",
        "finnish": "fi",
        "french": "fr",
        "frisian": "fy",
        "galician": "gl",
        "georgian": "ka",
        "german": "de",
        "greek": "el",
        "gujarati": "gu",
        "haitian creole": "ht",
        "hausa": "ha",
        "hawaiian": "haw",
        "hebrew": "he",
        "hindi": "hi",
        "hmong": "hmn",
        "hungarian": "hu",
        "icelandic": "is",
        "igbo": "ig",
        "indonesian": "id",
        "irish": "ga",
        "italian": "it",
        "japanese": "ja",
        "javanese": "jw",
        "kannada": "kn",
        "kazakh": "kk",
        "khmer": "km",
        "korean": "ko",
        "kurdish (kurmanji)": "ku",
        "kyrgyz": "ky",
        "lao": "lo",
        "latin": "la",
        "latvian": "lv",
        "lithuanian": "lt",
        "luxembourgish": "lb",
        "macedonian": "mk",
        "malagasy": "mg",
        "malay": "ms",
        "malayalam": "ml",
        "maltese": "mt",
        "maori": "mi",
        "marathi": "mr",
        "mongolian": "mn",
        "myanmar (burmese)": "my",
        "nepali": "ne",
        "norwegian": "no",
        "odia": "or",
        "pashto": "ps",
        "persian": "fa",
        "polish": "pl",
        "portuguese": "pt",
        "punjabi": "pa",
        "romanian": "ro",
        "russian": "ru",
        "samoan": "sm",
        "scots gaelic": "gd",
        "serbian": "sr",
        "sesotho": "st",
        "shona": "sn",
        "sindhi": "sd",
        "sinhala": "si",
        "slovak": "sk",
        "slovenian": "sl",
        "somali": "so",
        "spanish": "es",
        "sundanese": "su",
        "swahili": "sw",
        "swedish": "sv",
        "tajik": "tg",
        "tamil": "ta",
        "telugu": "te",
        "thai": "th",
        "turkish": "tr",
        "ukrainian": "uk",
        "urdu": "ur",
        "uyghur": "ug",
        "uzbek": "uz",
        "vietnamese": "vi",
        "welsh": "cy",
        "xhosa": "xh",
        "yiddish": "yi",
        "yoruba": "yo",
        "zulu": "zu",
    }
    # Get the language code corresponding to the language name
    lang_code = dic.get(lang_name.lower())

    # If the language name is not in the dictionary, return a default value
    if lang_code is None:
        lang_code = "en"  # Default to English

    return lang_code

def translation_result(request, translated_text, translated_audio):
    return render(
        request,
        "translation_result.html",
        {
            "translated_text": translated_text,
            #"translated_audio": "data:audio/mp3;base64," + translated_audio,
            "translated_audio": translated_audio,
        },
    )


@csrf_exempt
def translate(request):
    if request.method == "POST":
        # Retrieve the audio data and the destination language from the request
        audio_data_url = request.POST.get("audio_data")
        to_lang = request.POST.get("to_lang")

        if audio_data_url is None:
            translated_text = "Audio data not found"
        else:
            audio_data = base64.b64decode(audio_data_url.split(",")[1])
            audio_file = io.BytesIO(audio_data)
            # Convert the audio data to WAV format
            wav_file = convert_to_wav(audio_file)
            query = recognize(wav_file)
            translated_text = translate_text(query, to_lang)
            
            #executes no problem
            translated_audio = generate_audio(translated_text, to_lang)
        # Redirect to the translation_result view with the translated text and audio
        return redirect(
            "translation_result",
            translated_text=translated_text,
            translated_audio=translated_audio,
        )
        

    # If request method is not POST, redirect to home page or handle it appropriately
    return redirect("home")

def convert_to_wav(audio_data):
    audio = AudioSegment.from_file(audio_data, format="webm")
    audio = audio.set_frame_rate(16000)  # Set frame rate suitable for speech recognition
    wav_data = io.BytesIO()
    audio.export(wav_data, format="wav")
    wav_data.seek(0)  # Move cursor to start of the file
    return wav_data

def recognize(audio_data):
    # Initialize recognizer class (for recognizing the speech)
    r = sr.Recognizer()

    # Reading Audio file as source
    # listening the audio file and store in audio_text variable
    with sr.AudioFile(audio_data) as source:
        
        audio_text = r.listen(source)
        
    # recoginize_() method will throw a request error if the API is unreachable, hence using exception handling
    try:
        
        # using google speech recognition
        print('Converting audio transcripts into text ...')
        text = r.recognize_google(audio_text)
        return text
     
    except:
         print('Sorry.. run again...')

def translate_text(text, to_lang):
    if text is None:
        return 'No text to translate'
    translator = Translator()
    translated = translator.translate(text, dest=to_lang)
    return translated.text


import os

def generate_audio(text, to_lang):
    speak = gTTS(text=text, lang=get_code(to_lang), slow=False)
    audio_file_path = os.path.join(settings.MEDIA_ROOT, "captured_voice.mp3")
    speak.save(audio_file_path)
    return os.path.join(settings.MEDIA_URL, "captured_voice.mp3")

def generate_audio1(text):
    speak = gTTS(text=text, lang="es", slow=False)
    speak.save("captured_voice.mp3")
    return "captured_voice.mp3"

