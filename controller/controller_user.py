from fastapi import HTTPException, status
from model.model_user import UsuarioModel
from typing import Optional
import mysql.connector

def validar_email_simples(email: str) -> bool:
    if not email or '@' not in email:
        return False
    
    partes = email.split('@')
    if len(partes) != 2:  # Deve ter exatamente uma @
        return False
    
    usuario, dominio = partes
    
    # Valida parte do usuário
    if not usuario or any(c in usuario for c in ' \t\n\r'):
        return False
    
    # Valida parte do domínio
    if '.' not in dominio or dominio.startswith('.') or dominio.endswith('.'):
        return False
    
    # Verifica se há pelo menos um ponto após o @
    dominio_partes = dominio.split('.')
    if len(dominio_partes) < 2:
        return False
    
    # Verifica a extensão (última parte após o ponto)
    extensao = dominio_partes[-1]
    if len(extensao) < 2:
        return False
    
    return True

def validar_usuario(nome: str, email: str, senha: str):
    errors = []
    
    if not nome or len(nome) < 3:
        errors.append("O nome deve ter no mínimo 3 caracteres")
    
    if not email or not validar_email_simples(email):
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
        validar_usuario(nome, email, senha)
        usuario_id = UsuarioModel.criar(nome, email, senha)
        return {"id": usuario_id, "nome": nome, "email": email}
    except HTTPException:
        raise
    except mysql.connector.Error as e:
        if e.errno == 1062:
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
        return UsuarioModel.obter_todos()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar usuários: {str(e)}"
        )

def obter_usuario(id: int):
    try:
        return UsuarioModel.obter_por_id(id)
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
        if e.errno == 1062:
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