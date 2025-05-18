from pydantic import BaseModel


class DataModel(BaseModel):
    """
    Base class for the collection the data.
    """

    string: str
