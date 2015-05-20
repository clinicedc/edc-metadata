from edc.constants import NEW, NOT_REQUIRED, KEYED

ENTRY_CATEGORY = (
    ('CLINIC', 'Clinic'),
    ('LAB', 'Lab'),
    ('OTHER', 'Other'),
    )

ENTRY_STATUS = (
    (NEW, 'New'),
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
    ('scheduled', '1. Scheduled visit/contact'),
    ('missed', '2. Missed Scheduled visit'),
    ('unscheduled', '3. Unscheduled visit at which lab samples or data are being submitted'),
    ('lost', '4. Lost to follow-up'),
    ('death', '5. Death'),
)
