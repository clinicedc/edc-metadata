from edc_metadata.constants import CRF

from .visit_schedule_rule import VisitScheduleRule


class CrfRule(VisitScheduleRule):

    def __init__(self, target_models, **kwargs):
        super().__init__(**kwargs)
        self.metadata_category = CRF
        self.target_models = target_models