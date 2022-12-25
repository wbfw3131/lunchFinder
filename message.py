class Message:
    def __init__(self, content: str, hasFood: bool = True):
        self.content = content
        self.hasFood = hasFood

    def __repr__(self) -> str:
        return self.content
