from django.db import models
#modelo del pokemon
class Pokemon(models.Model):
    id = models.IntegerField(primary_key=True)  # ID del Pokémon
    name = models.CharField(max_length=100)     # Nombre
    height = models.IntegerField()              # Altura
    weight = models.IntegerField()              # Peso
    types = models.CharField(max_length=200)    # Tipos en formato texto
    sprite = models.URLField()                  # URL de la imagen

    def __str__(self):
        return self.name
