from enum import Enum

class Race(Enum):
    (0, "Other")
    (1, "White")
    (2, "Black/African American")
    (3, "American Indian or Alaskan Native")
    (4, "Asian")
    (5, "Native Hawaiian or Pacific Islander")
    (6, "Hispanic/Latino")
    (7, "Middle Eastern")

class Verified(Enum):
    (0, "None")
    (1, "From Pop-up")
    (2, "Pending")
    (3, "Verified")


class Gender(Enum):
    (0, "Other")
    (1, "Male")
    (2, "Female")


class Party(Enum):
    (1, "Republican")
    (2, "Democrat")
    (3, "Independent")
    (4, "Other")


class Position(Enum):
    (0, "Other")
    (1, "Senator")
    (2, "Congressperson")
    (3, "President")
    (4, "Secretary")


class State(Enum):
    ('AL', "Alabama"),
    ('AK', "Alaska"),
    ('AS', "American Samoa"),
    ('AZ', "Arizona"),
    ('AR', "Arkansas"),
    ('CA', "California"),
    ('CO', "Colorado"),
    ('CT', "Connecticut"),
    ('DE', "Delaware"),
    ('DC', "District of Columbia"),
    ('FL', "Florida"),
    ('GA', "Georgia"), ('GU', "Guam"),
    ('HI', "Hawaii"),
    ('ID', "Idaho"),
    ('IL', "Illinois"),
    ('IN', "Indiana"),
    ('IA', "Iowa"),
    ('KS', "Kansas"),
    ('KY', "Kentucky"),
    ('LA', "Louisiana"),
    ('ME', "Maine"),
    ('MD', "Maryland"),
    ('MH', "Marshall Islands"),
    ('MA', "Massachusetts"),
    ('MI', "Michigan"),
    ('FM', "Micronesia"),
    ('MN', "Minnesota"),
    ('MS', "Mississippi"),
    ('MO', "Missouri"),
    ('MT', "Montana"),
    ('NE', "Nebraska"),
    ('NV', "Nevada"),
    ('NH', "New Hampshire"),
    ('NJ', "New Jersey"),
    ('NM', "New Mexico"),
    ('NY', "New York"),
    ('NC', "North Carolina"),
    ('ND', "North Dakota"),
    ('MP', "Northern Marianas"),
    ('OH', "Ohio"),
    ('OK', "Oklahoma"),
    ('OR', "Oregon"),
    ('PW', "Palau"),
    ('PA', "Pennsylvania"),
    ('PR', "Puerto Rico"),
    ('RI', "Rhode Island"),
    ('SC', "South Carolina"),
    ('SD', "South Dakota"),
    ('TN', "Tennessee"),
    ('TX', "Texas"),
    ('UT', "Utah"),
    ('VT', "Vermont"),
    ('VA', "Virginia"),
    ('VI', "Virgin Islands"),
    ('WA', "Washington"),
    ('WV', "West Virginia"),
    ('WI', "Wisconsin"),
    ('WY', "Wyoming"),


class Status(Enum):
    (0, "Inactive")
    (1, "Introduced")
    (2, "In Committee")
    (3, "House Schedule")
    (4, "Passed House")
    (5, "Passed Senate")
    (6, "Signed by President"),


class Title(Enum):
    (1, "Senator")
    (2, "Congressman")
    (3, "Congresswoman")
    (4, "President")
    (5, "Honerable")
    (6, "Mr.")
    (7, "Ms.")
