from .constants import NOT_REQUIRED, KEYED, UNKEYED

ENTRY_CATEGORY = (
    ('CLINIC', 'Clinic'),
    ('LAB', 'Lab'),
    ('OTHER', 'Other'),
)

ENTRY_STATUS = (
    (UNKEYED, 'New'),
    (KEYED, 'Keyed'),
    ('MISSED', 'Missed'),
    (NOT_REQUIRED, 'Not required'),
)

ENTRY_WINDOW = (
    ('VISIT', 'Visit'),
    ('FORM', 'Form'),
)

VISIT_INTERVAL_UNITS = (
    ('H', 'Hour'),
    ('D', 'Day'),
    ('M', 'Month'),
    ('Y', 'Year'),
)

TAG_TYPE = (
    ('REGISTRATION', 'Registration'),
    ('OTHER', 'Other'),
)
