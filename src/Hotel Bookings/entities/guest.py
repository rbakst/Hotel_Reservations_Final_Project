from enum import Enum
class Guest:
    def __init__(self, reservation_row):
        self.count_adults = reservation_row["adults"]
        self.count_children = reservation_row["children"]
        self.count_babies = reservation_row["babies"]
        self.origin_country = reservation_row["country"]