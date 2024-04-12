import moviepy.editor as mp
import speech_recognition as sr

# Function to transcribe audio using Google Speech Recognition
def transcribe_audio(audio):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data)
            return text
        except sr.UnknownValueError:
            return "[ERROR] Could not understand audio"
        except sr.RequestError as e:
            return f"[ERROR] Could not request results from Google Speech Recognition service; {e}"

# Function to split audio into segments based on speaker changes (dummy implementation)
def split_audio_by_speaker(audio):
    # Dummy implementation: just split into 10-second segments
    segment_duration = 10  # seconds
    num_segments = int(audio.duration / segment_duration)
    segments = []
    for i in range(num_segments):
        start_time = i * segment_duration
        end_time = min((i + 1) * segment_duration, audio.duration)
        segments.append(audio.subclip(start_time, end_time))
    return segments

# Load the video and extract audio
video_path = "project.mp4"
audio_path = "audio1.wav"
video = mp.VideoFileClip(video_path)
video.audio.write_audiofile(audio_path)

# Split audio into segments
audio = mp.AudioFileClip(audio_path)
audio_segments = split_audio_by_speaker(audio)

# Transcribe each segment
transcriptions = []
for i, segment in enumerate(audio_segments):
    segment_audio_path = f"segment_{i}.wav"
    segment.write_audiofile(segment_audio_path)
    transcription = transcribe_audio(segment_audio_path)
    transcriptions.append(transcription)

# Combine transcriptions into a single transcript
full_transcript = "\n".join(transcriptions)
print(full_transcript)
f = open("transcription3.txt", "a")
f.write(full_transcript)
f.write(" ")
f.close()

# Clean up temporary audio files
audio.close()
video.close()
