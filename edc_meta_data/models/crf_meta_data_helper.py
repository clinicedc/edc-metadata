from .base_meta_data_helper import BaseMetaDataHelper
from .crf_entry import CrfEntry
from .crf_meta_data import CrfMetaData


class CrfMetaDataHelper(BaseMetaDataHelper):

    meta_data_model = CrfMetaData
    entry_model = CrfEntry
    entry_attr = 'crf_entry'
