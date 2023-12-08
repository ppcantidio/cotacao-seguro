from fastapi import APIRouter


router = APIRouter(prefix="/cotacoes", tags=["cotacao"])


@router.post('')
async def cotar_seguro():
    pass


@router.get('/ofertas')
async def resgatar_ofertas():
    pass


@router.get('/realizadas')
async def resgatar_cotacoes_realizadas():
    pass
