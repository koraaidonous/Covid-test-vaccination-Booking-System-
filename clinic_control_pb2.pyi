from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class appointmentFile(_message.Message):
    __slots__ = ["appointment"]
    APPOINTMENT_FIELD_NUMBER: _ClassVar[int]
    appointment: str
    def __init__(self, appointment: _Optional[str] = ...) -> None: ...

class appointmentRequest(_message.Message):
    __slots__ = ["hs_num", "name"]
    HS_NUM_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    hs_num: int
    name: str
    def __init__(self, name: _Optional[str] = ..., hs_num: _Optional[int] = ...) -> None: ...

class resultsFile(_message.Message):
    __slots__ = ["results"]
    RESULTS_FIELD_NUMBER: _ClassVar[int]
    results: int
    def __init__(self, results: _Optional[int] = ...) -> None: ...

class resultsRequest(_message.Message):
    __slots__ = ["hs_num", "name"]
    HS_NUM_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    hs_num: int
    name: str
    def __init__(self, name: _Optional[str] = ..., hs_num: _Optional[int] = ...) -> None: ...

class vacFile(_message.Message):
    __slots__ = ["vaccines"]
    VACCINES_FIELD_NUMBER: _ClassVar[int]
    vaccines: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, vaccines: _Optional[_Iterable[str]] = ...) -> None: ...

class vacRequest(_message.Message):
    __slots__ = ["hs_num", "name"]
    HS_NUM_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    hs_num: int
    name: str
    def __init__(self, name: _Optional[str] = ..., hs_num: _Optional[int] = ...) -> None: ...
