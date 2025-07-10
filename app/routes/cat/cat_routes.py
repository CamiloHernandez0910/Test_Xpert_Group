from fastapi import APIRouter, HTTPException, Query
from app.services.cat.cat_service import CatService

router = APIRouter(prefix="/cats", tags=["Cats"])

@router.get("/breeds", summary="Listar razas de gatos", description="Obtiene todas las razas disponibles desde TheCatAPI.")
async def list_breeds():
    breeds = await CatService.get_all_breeds()
    return breeds

@router.get("/breeds/search", summary="Buscar información asociado a la raza", description="Busca información de la raza de los gatos por campo usando TheCatAPI.")
async def search_breed(q: str = Query(..., description="Breed search query")):
    results = await CatService.search_breeds(q)
    return results

@router.get("/breeds/by_id/{breed_id}", summary="Consultar raza por ID", description="Devuelve información detallada de una raza de gato específica, consultando por su `breed_id` desde TheCatAPI.")
async def get_breed(breed_id: str):
    breed = await CatService.get_breed_by_id(breed_id)
    if not breed:
        raise HTTPException(status_code=404, detail=f"Breed with ID '{breed_id}' not found.")
    return breed


