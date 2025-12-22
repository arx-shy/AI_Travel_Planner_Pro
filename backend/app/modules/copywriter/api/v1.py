"""
Copywriter Module API Routes (v1)
"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db.session import get_db
from app.core.security.deps import get_current_active_user
from app.modules.copywriter.schemas.content_schema import ContentCreate, ContentResponse, ContentRating
from app.modules.copywriter.services.content_service import ContentService

router = APIRouter()


@router.post("/generate", response_model=ContentResponse)
async def generate_content(
    content_data: ContentCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    service = ContentService(db)
    content = await service.generate_content(current_user.id, content_data)
    return ContentResponse.model_validate(content)


@router.get("/contents", response_model=list[ContentResponse])
async def get_my_contents(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_active_user),
    page: int = 1,
    size: int = 20
):
    service = ContentService(db)
    contents = await service.list_contents(current_user.id, page=page, size=size)
    return [ContentResponse.model_validate(item) for item in contents]


@router.post("/contents/{content_id}/rate", response_model=ContentResponse)
async def rate_content(
    content_id: int,
    payload: ContentRating,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    service = ContentService(db)
    content = await service.rate_content(current_user.id, content_id, payload.rating)
    if not content:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Content not found")
    return ContentResponse.model_validate(content)


@router.post("/upload-image")
async def upload_image(
    image: UploadFile = File(...),
    current_user = Depends(get_current_active_user)
):
    return {"image_url": f"https://example.com/uploads/{image.filename}", "image_id": 1}
