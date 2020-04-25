
class Riddle:
    def __init__(self, raw: dict):
        self.answer = raw.get("answer")
        self.help = raw.get("help")
        self.letters = raw.get("letters")
        self.remove = raw.get("remove")
        self.reveals = raw.get("reveals")
        self.riddle = raw.get("riddle")

    def to_dict(self) -> dict:
        return {
            "answer": self.answer,
            "help": self.help,
            "remove": self.remove,
            "reveals": self.reveals,
            "letters": self.letters,
            "riddle": self.riddle
        }

