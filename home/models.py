from django.db import models
from neomodel import StructuredNode, StringProperty, RelationshipTo,RelationshipFrom

# Create your models here.
class yayın_tür(StructuredNode):
    tür = StringProperty()
    yer = StringProperty()

    yayın = RelationshipFrom('yayın','yayınlandı')

class yayın(StructuredNode):
    isim = StringProperty()
    yıl = StringProperty()

    yazdı = RelationshipTo(yayın_tür,'yayınlandı')
    arastırmacı = RelationshipFrom('arastırmacı','Yazdı')

class arastırmacı(StructuredNode):
    isim = StringProperty()

    ortak = RelationshipTo('arastırmacı','ortak')
    Yazdı = RelationshipTo(yayın,'Yazdı')

    def __str__(self):
        return self.isim
    