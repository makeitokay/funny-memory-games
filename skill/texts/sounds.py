class Sound:
    def __init__(self, name):
        self.name = name

    @property
    def tts(self):
        return f"<speaker audio='{self.name}'>"
