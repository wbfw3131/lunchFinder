class Message:
    def __init__(self, content: str, hasLunch: bool = True):
        self.content = content
        self.hasLunch = hasLunch

    def __repr__(self) -> str:
        return self.content
