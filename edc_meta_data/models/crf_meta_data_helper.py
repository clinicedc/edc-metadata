from ..models import CrfMetaData, CrfEntry

from .base_meta_data_helper import BaseMetaDataHelper


class CrfMetaDataHelper(BaseMetaDataHelper):

    meta_data_model = CrfMetaData
    entry_model = CrfEntry
    entry_attr = 'crf_entry'
