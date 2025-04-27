from typing import Annotated, List
import operator
from typing import TypedDict
from .struct import Section, SearchResults


class ResearchState(TypedDict):
    section: Section
    knowledge: str
    search_results: Annotated[List[SearchResults], operator.add]
    accumulated_content: str