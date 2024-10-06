from enum import Enum
class RowNames(Enum):
    DATE = "date"
    NAME = "name"
    TYPE = "type"
    AS = "as"
    RB = "rb"
    KB = "kb"
    GB = "gb"
    MOT = "mot"
    ASI = "asi"
    KADER = "kad"
    OFF = "off"
    SAT = "sat"
    MONTH = "month"
    FIXED = "fixed"
    ORDER = "order"
    TIME = "time"
    THEME = "theme"
    CALLED_UP = "called_up"
    RESPONSIBLE = "responsible"
    DETAILS = "details"

class HolidayRowNames(Enum):
    NAME = "name"
    START = "start"
    END = "end"
    ONLY_JF = "only_jf"

class Groups(Enum):
    JF = "jf"
    GB = "gb"
    KB = "kb"
    RB = "rb"
