import factory

from edc.core.bhp_content_type_map.tests.factories import ContentTypeMapFactory
from edc_visit_schedule.tests.factories import VisitDefinitionFactory

from ...models import Entry


class EntryFactory(factory.DjangoModelFactory):
    class Meta:
        model = Entry

    visit_definition = factory.SubFactory(VisitDefinitionFactory)
    content_type_map = factory.SubFactory(ContentTypeMapFactory)
    entry_order = factory.Sequence(lambda n: int(n) + 100)
