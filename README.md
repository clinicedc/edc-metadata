# edc_meta_data

Adds models and other functionality to support a meta-data layer above models/CRFs.

Introduction
------------
Data collection follows a schedule where some collection tools or case report forms (CRFs) are required and others not. This module exposes a meta-data layer that can be used to manage and present CRFs scheduled for a visit or time point. 

See also edc-rule-groups.

### How meta-data is created
CRF and Requisition meta data are created by the `meta_data_on_post_save` post-save signal for any model that uses the `VisitModelMixin` mixin.

### How meta-data is updated
The same post-save signal updates existing meta data for other models that use either the `CrfMetaDataManager` or the `RequisitionMetaDatManager` from `edc_meta_data.manager`.