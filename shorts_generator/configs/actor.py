from shorts_generator.configs.voice import Voice, to_voice


class Actor:
    def __init__(
        self,
        name: str,
        voice: Voice,
        traits: list[str],
        unique_phrases: list[str],
        text_font: str = "Arial",
        text_font_size: int = 120,
        text_color: str = "white",
        text_stroke_color: str = "black",
        text_stroke_width: int = 3,
    ):
        self.name = name
        self.voice = voice
        self.traits = traits
        self.unique_phrases = unique_phrases
        self.text_font = text_font
        self.text_font_size = text_font_size
        self.text_color = text_color
        self.text_stroke_color = text_stroke_color
        self.text_stroke_width = text_stroke_width

    @classmethod
    def from_dict(cls, actor_dict: dict):
        return cls(
            name=actor_dict["name"],
            voice=to_voice(actor_dict["voice"]),
            traits=actor_dict.get("traits", []),
            unique_phrases=actor_dict.get("unique_phrases", []),
            text_font=actor_dict.get("text_font", "Arial"),
            text_font_size=actor_dict.get("text_font_size", 120),
            text_color=actor_dict.get("text_color", "white"),
            text_stroke_color=actor_dict.get("text_stroke_color", "black"),
            text_stroke_width=actor_dict.get("text_stroke_width", 3),
        )
