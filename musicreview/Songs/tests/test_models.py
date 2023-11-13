import pytest
from ..models import Song
from .factories import SongFactory

pytestmark = pytest.mark.django_db

def test__str__():
    Song = SongFactory()
    assert Song.__str__() == Song.name
    assert str(Song) == Song.name
