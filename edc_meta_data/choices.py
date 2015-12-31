from edc_constants.constants import (
    NOT_REQUIRED, KEYED, UNKEYED, MISSED_VISIT, SCHEDULED, UNSCHEDULED, LOST_VISIT, DEATH_VISIT)

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

TAG_TYPE = (
    ('REGISTRATION', 'Registration'),
    ('OTHER', 'Other'),
)


SUBJECT_TYPE = (
    ('ADULT', 'ADULT'),
    ('MOTHER', 'MOTHER'),
    ('INFANT', 'INFANT'),
    ('SUBJECT', 'SUBJECT'),
    ('INDEX', 'INDEX'),
    ('PARTNER', 'PARTNER'),
)

VISIT_INFO_SOURCE = (
    ('participant', '1. Clinic visit with participant'),
    ('other_contact', '2. Other contact with participant'),
    ('other_doctor', '3. Contact with external health care provider/medical doctor'),
    ('family', '4. Contact with family or designated person who can provide information'),
    ('chart', '5. Hospital chart or other medical record'),
    ('OTHER', '9. Other'),
)

VISIT_REASON = (
    (SCHEDULED, '1. Scheduled visit/contact'),
    (MISSED_VISIT, '2. Missed Scheduled visit'),
    (UNSCHEDULED, '3. Unscheduled visit at which lab samples or data are being submitted'),
    (LOST_VISIT, '4. Lost to follow-up'),
    (DEATH_VISIT, '5. Death'),
)
