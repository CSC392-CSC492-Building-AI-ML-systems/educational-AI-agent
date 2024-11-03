import whisper

# Load the Whisper model (medium, large, or small can be chosen depending on your speed/accuracy needs)
model = whisper.load_model("medium")  # You can replace "base" with "small", "medium", "large"

# Transcribe an audio file (MP3, WAV, etc.)
result = model.transcribe("your_audio_file.wav")

# Output the transcription
print(result["text"])
