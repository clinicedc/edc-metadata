Overview
========

.. automodule:: bhp_entry


Module :mod:`bhp_entry` manages the metadata for scheduled and additional data collection forms and requisitions.
The metadata is stored in models referred to as entry buckets; namely, models :class:`bhp_entry.models.ScheduledEntryMetaData` 
and  :class:`bhp_entry.models.AdditionalEntryBucket`. Requisitions are managed using the same base class as these "buckets"
and reside in :mod:`bhp_lab_entry`.

Entry bucket data tracks a models entry status and due date. Entry bucket data is generated according to the data collection
schedule in :mod:`bhp_visit` and the chronological position of a subject in that schedule.

Flow
++++
An example of the flow is as follows. 
 * Completed a consent
 * Navigate to the dashboard
 * Complete a registration / membership form
 * The membership form triggers the creation of appointments
 * Set an appointment to "in progress"
 * Complete the visit tracking form
 * Navigate to the forms for the current appointment / visit
 * See on the dashboard "links" to complete scheduled, additional, lab forms/models.

These  "links" are displayed using Entry Bucket data.
 
Connection to entry rules
+++++++++++++++++++++++++

Entry rules are a good way to manipulate Entry Bucket data after it has been generated using default
information. See module :mod:`bhp_entry_rules`.

Visit reason
++++++++++++

The visit tracking form (a subclass of :class:`bhp_visit_tracking.models.BaseVisitTracking`) has a field
'reason'. Reasons for a visit are ['scheduled', 'unscheduled', 'missed', 'lost', 'death', 'off study']. Module 
:mod:`bhp_entry` uses this field to determine if Entry Bucket data is required for a visit. That is, if a 
visit is a scheduled visit, the dashboard links to the data collection tools should be displayed. If the 
visit reason is 'missed', the dashboard links to the data collection tools should not be displayed.

Note that the visit reason value does not act as a filter. Entry bucket data is deleted if not needed. 
By default, data is generated for every visit when the visit tracking form is completed, but if the 
reason is, for example, 'missed', the entry bucket data will be deleted, if it exists, or never created 
in the first place. Of course, if the model instance that the dashboard link points to has been filled in,
the Entry Bucket data will not be deleted for the given model.

.. warning:: Visit reasons attached to the visit tracking model are verified by :class:`bhp_entry.classes.ScheduledEntry` and
             the choices tuple you use on your visit model must conform to have the required values. Currently the required values 
             are ['scheduled', 'unscheduled', 'missed', 'lost', 'death', 'off study'].
             These values trigger how the class handles Entry Bucket data.

.. seealso:: :class:`bhp_entry.classes.ScheduledEntry`, method :func:`bhp_entry.classes.ScheduledEntry.add_or_update_for_visit`
             and method :func:`bhp_entry.classes.ScheduledEntry.check_visit_model_reason_field` and 
             and model method :func:`bhp_visit_tracking.models.BaseVisitTracking._get_visit_reason_choices`.
 