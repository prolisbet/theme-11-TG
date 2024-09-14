from googletrans import Translator

translator = Translator()
try:
    result = translator.translate("Привет", dest='en', src='ru')
    print(result.text)
except Exception as e:
    print(f"Ошибка: {e}")
