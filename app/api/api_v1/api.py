from fastapi import APIRouter

from app.api.api_v1.endpoints import blocks, characters, codepoints, planes

router = APIRouter()
router.include_router(characters.router, prefix="/characters", tags=["Unicode Characters"])
router.include_router(codepoints.router, prefix="/codepoints", tags=["Unicode Codepoints"])
router.include_router(blocks.router, prefix="/blocks", tags=["Unicode Blocks"])
router.include_router(planes.router, prefix="/planes", tags=["Unicode Planes"])
