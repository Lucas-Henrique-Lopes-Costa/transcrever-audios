import speech_recognition as sr
from pydub import AudioSegment
import os

def extract_audio(file_path):
    """Extrai o áudio de um arquivo de vídeo e converte para FLAC com qualidade otimizada."""
    flac_path = file_path.replace(".mkv", ".flac")
    
    # Carregar o áudio do arquivo original
    audio = AudioSegment.from_file(file_path)
    
    # Converter para 16kHz e 16-bit PCM para reduzir tamanho
    audio = audio.set_frame_rate(16000).set_sample_width(2).set_channels(1)
    
    # Exportar como FLAC
    audio.export(flac_path, format="flac")
    
    print(f"Áudio convertido: {flac_path} ({round(os.path.getsize(flac_path) / (1024 * 1024), 2)} MB)")
    return flac_path

def transcribe_audio(file_path):
    """Transcreve o áudio usando a API do Google."""
    recognizer = sr.Recognizer()
    flac_path = extract_audio(file_path)
    
    with sr.AudioFile(flac_path) as source:
        audio = recognizer.record(source)  # Lê todo o arquivo
    
    try:
        text = recognizer.recognize_google(audio, language='pt-BR')
        return text
    except sr.UnknownValueError:
        return "Google Web Speech API não conseguiu entender o áudio"
    except sr.RequestError as e:
        return f"Erro na conexão com Google API: {e}"

# Lista de arquivos de vídeo/áudio para transcrição
audio_files = [
    "audio.mkv",  # Adicione mais arquivos se necessário
]

# Processar e transcrever os arquivos
transcriptions = {file: transcribe_audio(file) for file in audio_files}

# Exibir resultados
for file, transcription in transcriptions.items():
    print(f"{file}: {transcription}\n")
