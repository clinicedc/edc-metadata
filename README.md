# edc_meta_data

`edc-meta-data` puts a meta data layer between your user and scheduled data collection models. The meta data can be used to display links to the data collection models on a dashboard (`edc_dashboard`) and be manipulated in ways that control how the meta data is displayed (`edc_rule_groups`). A data manager uses the meta data to correctly determine data completeness for a timepoint.

To install:

    pip install git+https://github.com/botswana-harvard/edc-meta-data@develop#egg=edc-meta-data
    

To configure:

`edc-meta-data` works together with `edc-visit-schedule`.


Meta data is collected in two models which have to be declared manually in your application:

    class CrfMetaData(CrfMetaDataModelMixin, BaseUuidModel):
    
        registered_subject = models.ForeignKey(RegisteredSubject)
    
        appointment = models.ForeignKey(Appointment, related_name='+')
    
        class Meta:
            app_label = 'my_app'
    
    
    class RequisitionMetaData(RequisitionMetaDataModelMixin, BaseUuidModel):
    
        registered_subject = models.ForeignKey(RegisteredSubject)
    
        appointment = models.ForeignKey(Appointment, related_name='+')
    
        class Meta:
            app_label = 'my_app'

The two models have to be declared in your application since they need keys to your `RegisteredSubject` model and 'Appointment` model.

The `AppConfig` then needs to know where these two models reside. In your `apps.py` do the following:

    from edc_meta_data.apps import EdcMetaDataAppConfig as EdcMetaDataAppConfigParent

    class EdcMetaDataAppConfig(EdcMetaDataAppConfigParent):
        model_attrs = [('my_app', 'crfmetadata'), ('my_app', 'requisitionmetadata')]

Your application collects data on a schedule. Before declaring the `visit_schedule` let's prepare the models that will be used in the scheduled data collection. These models are your visit models, crf models and requisition models.

Your application also has one or more `Visit` models. Each visit model should be declared with the `CrfMetaDataMixin`:

    class SubjectVisit(CrfMetaDataMixin, PreviousVisitMixin, VisitModelMixin, BaseUuidModel):
    
        appointment = models.OneToOneField(Appointment)
    
        class Meta:
            app_label = 'example'

Your Crf models must be declared with the `entry_meta_data_manager` and the `CrfModelMixin`:

    class CrfOne(CrfModelMixin, BaseUuidModel):
    
        subject_visit = models.ForeignKey(SubjectVisit)
    
        f1 = models.CharField(max_length=10, default='erik')
    
        entry_meta_data_manager = CrfMetaDataManager(SubjectVisit)
    
        class Meta:
            app_label = 'example'
    
Your requisition models are declared with the `entry_meta_data_manager` and the `RequisitionModelMixin`:

    class RequisitionOne(RequisitionModelMixin, BaseUuidModel):
    
        subject_visit = models.ForeignKey(SubjectVisit)
    
        f1 = models.CharField(max_length=10, default='erik')
    
        entry_meta_data_manager = CrfMetaDataManager(SubjectVisit)
    
        class Meta:
            app_label = 'example'

??????

Introduction
------------
Data collection follows a schedule where some collection tools or case report forms (CRFs) are required and others not. This module exposes a meta-data layer that can be used to manage and present CRFs scheduled for a visit or time point. 

See also edc-rule-groups.

### How meta-data is created
CRF and Requisition meta data are created by the `meta_data_on_post_save` post-save signal for any model that uses the `VisitModelMixin` mixin.

### How meta-data is updated
The same post-save signal updates existing meta data for other models that use either the `CrfMetaDataManager` or the `RequisitionMetaDatManager` from `edc_meta_data.manager`.