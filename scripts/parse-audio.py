import whisper

# Load the Whisper model
model = whisper.load_model("medium")

def transcribe_audio(audio_path):
    # Transcribe an audio file
    result = model.transcribe("data/annotation_1.wav") 

    # Output the transcription (going to save this in a file instead)
    print(result["text"])

def create_data(annotation, transcription, question, answer):
    return {'context': f'Annotated Session: {annotation} Explanation: {transcription}', 'question': question, 'answer': answer}