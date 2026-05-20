from database import conectar

def cadastrar_usuario(nome, usuario, email, senha):
    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute("""
            INSERT INTO usuarios (nome, usuario, email, senha)
            VALUES (?, ?, ?, ?)
        """, (nome, usuario, email, senha))
        
        conexao.commit()
        return True, "Usuário cadastrado com sucesso."
    
    except Exception as erro:
        return False, f"Erro ao cadastrar usuário: {erro}"
    
    finally:
        conexao.close()

def validar_login(usuario, senha):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id, nome, usuario, email
        FROM usuarios
        WHERE usuario = ? AND senha = ?
    """, (usuario, senha))

    usuario_encontrado = cursor.fetchone()
    conexao.close()

    if usuario_encontrado:
        return True, usuario_encontrado
    
    return False, None
