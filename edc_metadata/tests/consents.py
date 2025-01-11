from dateutil.relativedelta import relativedelta
from edc_consent.consent_definition import ConsentDefinition
from edc_constants.constants import FEMALE, MALE

from .constants import test_datetime

consent_v1 = ConsentDefinition(
    "edc_metadata.subjectconsentv1",
    version="1",
    start=test_datetime,
    end=test_datetime + relativedelta(years=3),
    age_min=18,
    age_is_adult=18,
    age_max=64,
    gender=[MALE, FEMALE],
)
