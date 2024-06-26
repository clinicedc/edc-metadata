from __future__ import annotations

from ..metadata import RequisitionMetadataGetter
from .metadata_wrappers import MetadataWrappers
from .requisition_metadata_wrapper import RequisitionMetadataWrapper


class RequisitionMetadataWrappers(MetadataWrappers):
    metadata_getter_cls: RequisitionMetadataGetter = RequisitionMetadataGetter
    metadata_wrapper_cls: RequisitionMetadataWrapper = RequisitionMetadataWrapper
