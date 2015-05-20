import factory

from edc.base.model.tests.factories import BaseUuidModelFactory
from edc.core.bhp_content_type_map.tests.factories import ContentTypeMapFactory
from edc.subject.visit_schedule.tests.factories import VisitDefinitionFactory

from ...models import Entry


class EntryFactory(BaseUuidModelFactory):
    FACTORY_FOR = Entry

    visit_definition = factory.SubFactory(VisitDefinitionFactory)
    content_type_map = factory.SubFactory(ContentTypeMapFactory)
    entry_order = factory.Sequence(lambda n: int(n) + 100)
