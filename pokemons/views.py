import requests
from django.http import JsonResponse
from django.core.paginator import Paginator

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .models import Pokemon

#pide token
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])



def pokemon_list(request):
    url = 'https://pokeapi.co/api/v2/pokemon?limit=30'
    response = requests.get(url)
    
    if response.status_code != 200:
        return JsonResponse({'error': 'Error fetching data from PokeAPI'}, status=500)
    
    data = response.json()
    pokemon_names = [pokemon['name'] for pokemon in data['results']]
    
  
    paginator = Paginator(pokemon_names, 10)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return JsonResponse({'pokemons': list(page_obj)}, status=200)
# pide token
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])


def pokemon_detail(request, pokemon_id):
    # Validar que el ID este en un rango aceptable
    if pokemon_id < 1 or pokemon_id > 10:
        return JsonResponse({'error': 'El ID debe estar entre 1 y 10.'}, status=400)

    # Intentar recuperar el Pokemon desde la base de datos
    pokemon = Pokemon.objects.filter(id=pokemon_id).first()
    if pokemon:
        # Si existe devolver los datos desde la base de datos
        data = {
            'id': pokemon.id,
            'name': pokemon.name,
            'height': pokemon.height,
            'weight': pokemon.weight,
            'types': pokemon.types.split(','),  # Convertir a lista
            'sprite': pokemon.sprite
        }
    else:
        # Si no  consultar la API externa
        url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"
        response = requests.get(url)

        if response.status_code != 200:
            return JsonResponse({'error': 'No se pudo obtener el Pokémon.'}, status=response.status_code)

        # Parsear los datos de la API
        pokemon_data = response.json()
        data = {
            'id': pokemon_data['id'],
            'name': pokemon_data['name'],
            'height': pokemon_data['height'],
            'weight': pokemon_data['weight'],
            'types': [t['type']['name'] for t in pokemon_data['types']],
            'sprite': pokemon_data['sprites']['front_default']
        }

        # Guardar los datos en la base
        Pokemon.objects.create(
            id=data['id'],
            name=data['name'],
            height=data['height'],
            weight=data['weight'],
            types=','.join(data['types']),  # Guardar como texto
            sprite=data['sprite']
        )

    return JsonResponse(data)
    
    
def health_check(request):
    #estatus 
    return JsonResponse({'status': 'ok'}, status=200)