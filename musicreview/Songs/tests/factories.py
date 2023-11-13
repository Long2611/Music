from django.template.defaultfilters import slugify
import factory
import factory.fuzzy
from ..models import Song


class SongFactory(factory.django.DjangoModelFactory):
    name = factory.fuzzy.FuzzyText()
    slug = factory.LazyAttribute(
        lambda obj: slugify(obj.name))
    description = factory.Faker(
        'paragraph', nb_sentences=3,
    variable_nb_sentences=True
    )
    firmness = factory.fuzzy.FuzzyChoice(
        [x[0] for x in Song.Firmness.choices]
    )
    country_of_origin = factory.Faker('country_code')

    class Meta:
        model = Song