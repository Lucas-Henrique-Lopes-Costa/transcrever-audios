import speech_recognition as sr
from pydub import AudioSegment

# Converter arquivos .ogg para .wav
def convert_to_wav(file_path):
    audio = AudioSegment.from_ogg(file_path)
    wav_path = file_path.replace(".ogg", ".wav")
    audio.export(wav_path, format="wav")
    return wav_path

# Inicializar o reconhecedor
recognizer = sr.Recognizer()

# Função para transcrever o arquivo de áudio
def transcribe_audio(file_path):
    wav_path = convert_to_wav(file_path)
    with sr.AudioFile(wav_path) as source:
        audio = recognizer.record(source)
    try:
        # Utilizando a API de reconhecimento de fala do Google
        text = recognizer.recognize_google(audio, language='pt-BR')
        return text
    except sr.UnknownValueError:
        return "Google Web Speech API não conseguiu entender o áudio"
    except sr.RequestError as e:
        return f"Não foi possível solicitar resultados da Google Web Speech API; {e}"

# Lista de arquivos de áudio
audio_files = [
    "Como são feitos os ajustes.ogg",
    "De quanto em quanto tempo eu preciso ir fazer quiropraxia?.ogg",
    "É normal sentir desconforto depois da sessão de quiro?.ogg",
    "Endereço.ogg",
    "Meios de Pagamento.ogg",
    "O que é a terapia ILIB? Tem contra indicação?.ogg",
    "Pessoa que tem hipercifose, escoliose ou lordose.ogg",
    "Primeira sessão.ogg",
    "Roupas e exames.ogg"
]

# Transcrevendo cada arquivo de áudio
transcriptions = {file: transcribe_audio(file) for file in audio_files}

# Exibindo as transcrições
for file, transcription in transcriptions.items():
    print(f"{file}: {transcription}\n")
