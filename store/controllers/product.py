from typing import List
from datetime import datetime
from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query, status
from pydantic import UUID4
from store.core.exceptions import NotFoundException, InsertionException
from store.schemas.product import ProductIn, ProductOut, ProductUpdate, ProductUpdateOut
from store.usecases.product import ProductUsecase

# Cria um roteador para gerenciar as rotas relacionadas aos produtos
router = APIRouter(tags=["products"])

# Rota para criar um novo produto
@router.post(path="/", status_code=status.HTTP_201_CREATED)
async def post(
    body: ProductIn = Body(...), usecase: ProductUsecase = Depends()
) -> ProductOut:
    try:
        # Tenta criar um novo produto usando o caso de uso
        return await usecase.create(body=body)
    except InsertionException as exc:
        # Lança uma exceção HTTP se ocorrer um erro de inserção
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=exc.message)

# Rota para obter um produto pelo ID
@router.get(path="/{id}", status_code=status.HTTP_200_OK)
async def get(
    id: UUID4 = Path(alias="id"), usecase: ProductUsecase = Depends()
) -> ProductOut:
    try:
        # Tenta obter o produto pelo ID usando o caso de uso
        return await usecase.get(id=id)
    except NotFoundException as exc:
        # Lança uma exceção HTTP se o produto não for encontrado
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message)

# Rota para consultar produtos por intervalo de preço
@router.get(path="/", status_code=status.HTTP_200_OK)
async def query(
    price_min: float = Query(None, alias="price_min"),
    price_max: float = Query(None, alias="price_max"),
    usecase: ProductUsecase = Depends()
) -> List<ProductOut]:
    # Consulta produtos dentro de um intervalo de preço usando o caso de uso
    return await usecase.query(price_min=price_min, price_max=price_max)

# Rota para atualizar parcialmente um produto pelo ID
@router.patch(path="/{id}", status_code=status.HTTP_200_OK)
async def patch(
    id: UUID4 = Path(alias="id"),
    body: ProductUpdate = Body(...),
    usecase: ProductUsecase = Depends(),
) -> ProductUpdateOut:
    try:
        # Atualiza o campo updated_at com a data e hora atuais
        body.updated_at = datetime.utcnow()
        # Tenta atualizar o produto pelo ID usando o caso de uso
        return await usecase.update(id=id, body=body)
    except NotFoundException as exc:
        # Lança uma exceção HTTP se o produto não for encontrado
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message)

# Rota para deletar um produto pelo ID
@router.delete(path="/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(
    id: UUID4 = Path(alias="id"), usecase: ProductUsecase = Depends()
) -> None:
    try:
        # Tenta deletar o produto pelo ID usando o caso de uso
        await usecase.delete(id=id)
    except NotFoundException as exc:
        # Lança uma exceção HTTP se o produto não for encontrado
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message)
