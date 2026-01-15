from faster_whisper import WhisperModel

class AudioProcessor:
    
    def __init__(self, model_size="small", compute_type="int8"):
        self.model = WhisperModel(model_size, device="cpu")

    def transcribe(self, audio_path):
        segment_raw, _ = self.model.transcribe(
            audio_path,
            task="transcribe",
            language="en",
            beam_size=5,
            best_of=5
        )

        return "".join([segment.text for segment in segment_raw])

