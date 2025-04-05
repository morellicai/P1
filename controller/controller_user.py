from fastapi import HTTPException, status
from model.model_user import UsuarioModel
from typing import Optional
import re
import mysql.connector

def validar_email(email: str):
    """Valida o formato do email"""
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(regex, email) is not None

def validar_usuario(nome: str, email: str, senha: str):
    """Valida os dados do usuário"""
    errors = []
    
    if not nome or len(nome) < 3:
        errors.append("O nome deve ter no mínimo 3 caracteres")
    
    if not email or not validar_email(email):
        errors.append("Email inválido")
    
    if not senha or len(senha) < 6:
        errors.append("A senha deve ter no mínimo 6 caracteres")
    
    if errors:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=", ".join(errors)
        )

def criar_usuario(nome: str, email: str, senha: str):
    try:
        # Valida os dados
        validar_usuario(nome, email, senha)
        
        # Cria o usuário
        usuario_id = UsuarioModel.criar(nome, email, senha)
        return {"id": usuario_id, "nome": nome, "email": email}
    except HTTPException:
        raise
    except mysql.connector.Error as e:
        if e.errno == 1062:  # Duplicate entry
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email já cadastrado"
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar usuário: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar usuário: {str(e)}"
        )

def listar_usuarios():
    try:
        usuarios = UsuarioModel.obter_todos()
        return usuarios
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar usuários: {str(e)}"
        )

def obter_usuario(id: int):
    try:
        usuario = UsuarioModel.obter_por_id(id)
        return usuario
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar usuário: {str(e)}"
        )

def atualizar_usuario(id: int, nome: Optional[str] = None, email: Optional[str] = None, senha: Optional[str] = None):
    try:
        # Valida os dados que serão atualizados
        if nome is not None and len(nome) < 3:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="O nome deve ter no mínimo 3 caracteres"
            )
        
        if email is not None and not validar_email(email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email inválido"
            )
        
        if senha is not None and len(senha) < 6:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A senha deve ter no mínimo 6 caracteres"
            )
        
        # Atualiza o usuário
        atualizados = UsuarioModel.atualizar(id, nome, email, senha)
        if atualizados == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado"
            )
        
        return UsuarioModel.obter_por_id(id)
    except HTTPException:
        raise
    except mysql.connector.Error as e:
        if e.errno == 1062:  # Duplicate entry
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email já cadastrado"
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao atualizar usuário: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao atualizar usuário: {str(e)}"
        )

def deletar_usuario(id: int):
    try:
        deletados = UsuarioModel.deletar(id)
        if deletados == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao deletar usuário: {str(e)}"
        )