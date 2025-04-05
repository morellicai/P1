from fastapi import HTTPException, status
from model.model_prod import ProdutoModel
from typing import Optional

def validar_produto(nome: str, preco: float, estoque: int):
    """Valida os dados do produto"""
    errors = []
    
    if not nome or len(nome) < 3:
        errors.append("O nome deve ter no mínimo 3 caracteres")
    
    if preco is None or preco <= 0:
        errors.append("O preço deve ser um valor positivo")
    
    if estoque is None or estoque < 0 or not isinstance(estoque, int):
        errors.append("O estoque deve ser um número inteiro maior ou igual a zero")
    
    if errors:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=", ".join(errors)
        )

def criar_produto(nome: str, preco: float, estoque: int):
    try:
        # Valida os dados
        validar_produto(nome, preco, estoque)
        
        # Cria o produto
        produto_id = ProdutoModel.criar(nome, preco, estoque)
        return {"id": produto_id, "nome": nome, "preco": preco, "estoque": estoque}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar produto: {str(e)}"
        )

def listar_produtos():
    try:
        produtos = ProdutoModel.obter_todos()
        return produtos
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar produtos: {str(e)}"
        )

def obter_produto(id: int):
    try:
        produto = ProdutoModel.obter_por_id(id)
        return produto
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar produto: {str(e)}"
        )

def atualizar_produto(id: int, nome: Optional[str] = None, preco: Optional[float] = None, estoque: Optional[int] = None):
    try:
        # Valida os dados que serão atualizados
        if nome is not None and len(nome) < 3:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="O nome deve ter no mínimo 3 caracteres"
            )
        
        if preco is not None and preco <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="O preço deve ser um valor positivo"
            )
        
        if estoque is not None and (estoque < 0 or not isinstance(estoque, int)):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="O estoque deve ser um número inteiro maior ou igual a zero"
            )
        
        # Atualiza o produto
        atualizados = ProdutoModel.atualizar(id, nome, preco, estoque)
        if atualizados == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Produto não encontrado"
            )
        
        return ProdutoModel.obter_por_id(id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao atualizar produto: {str(e)}"
        )

def deletar_produto(id: int):
    try:
        deletados = ProdutoModel.deletar(id)
        if deletados == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Produto não encontrado"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao deletar produto: {str(e)}"
        )