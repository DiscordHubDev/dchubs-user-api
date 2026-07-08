# schema/__init__.py
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class BaseResponseModel(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        alias_generator=to_camel,
        populate_by_name=True,
        extra="ignore",
        str_strip_whitespace=True,
        validate_assignment=True,
        arbitrary_types_allowed=True,
    )
