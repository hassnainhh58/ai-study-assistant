from pydantic import BaseModel


class StudyResponse(BaseModel):
    answer: str
    topic: str
    difficulty: str
    used_calculator: bool
    used_weather: bool
    used_web_search: bool