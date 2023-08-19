from enum import Enum

class WeekdaySelect(str, Enum):
    monday = "monday"
    tuesday = "tuesday"
    wednessday = "wednessday"
    thursday = "thursday"
    friday = "friday"
    saturday = "saturday"
    sunday = "sunday"
    everyday = "everyday"


def encode_selected_weekdays(selection: list[WeekdaySelect]) -> int:
    encoding = 0
    if WeekdaySelect.everyday in selection:
        return 127
    if WeekdaySelect.monday in selection:
        encoding += 64
    if WeekdaySelect.tuesday in selection:
        encoding += 32
    if WeekdaySelect.wednessday in selection:
        encoding += 16
    if WeekdaySelect.thursday in selection:
        encoding += 8
    if WeekdaySelect.friday in selection:
        encoding += 4
    if WeekdaySelect.saturday in selection:
        encoding += 2
    if WeekdaySelect.sunday in selection:
        encoding += 1
    return encoding
