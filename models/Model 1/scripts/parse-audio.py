import os
import whisper
import json

# Load the Whisper model
model = whisper.load_model("medium")

def transcribe_audio(audio_path, destination_dir, filename):
    # Transcribe the audio file
    result = model.transcribe(audio_path) 

    # save transcription in a file
    transcription_filename = f'{filename}.txt'
    data_piece_path = os.path.join(destination_dir, transcription_filename)

    with open(data_piece_path, "w") as f:
        f.write(result["text"])

def create_data(annotation_file, transcription_file, question, answer):
    # get the contents of the annotation and transcription file
    with open(annotation_file, "r") as f:
        annotation = f.read()
    
    with open(transcription_file, "r") as f:
        transcription = f.read()

    return json.dumps({
        'context': f'Annotated Session: "{annotation}" Explanation: "{transcription}"',
        'question': question,
        'answer': answer
    }, indent=4)

if __name__ == "__main__":
    transcribe_audio("data/annotation_1.wav", "data", "annotation_1")