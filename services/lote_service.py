from datetime import date
from database import conectar


def buscar_lote_ativo():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id, codigo, data_chegada, quantidade_inicial, quantidade_atual, peso_medio_atual, status
        FROM lotes
        WHERE status = 'ativo'
        LIMIT 1
    """)

    lote = cursor.fetchone()
    conexao.close()

    return lote


def criar_lote(nome_lote):
    conexao = conectar()
    cursor = conexao.cursor()

    try:
        lote_ativo = buscar_lote_ativo()

        if lote_ativo:
            return False, "Já existe um lote ativo. Finalize o lote atual antes de criar outro."

        data_atual = date.today().strftime("%d/%m/%Y")

        cursor.execute("""
            INSERT INTO lotes (
                codigo,
                data_chegada,
                quantidade_inicial,
                quantidade_atual,
                peso_medio_inicial,
                peso_medio_atual,
                mortalidade_total,
                status,
                observacao
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            nome_lote,
            data_atual,
            0,
            0,
            0,
            0,
            0,
            "ativo",
            ""
        ))

        conexao.commit()
        return True, "Lote criado com sucesso."

    except Exception as erro:
        return False, f"Erro ao criar lote: {erro}"

    finally:
        conexao.close()

def cadastrar_chegada(lote_id, data, quantidade, peso_medio, observacao):
    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute("""
            INSERT INTO chegadas (lote_id, data, quantidade, peso_medio, observacao)
            VALUES (?, ?, ?, ?, ?)
        """, (lote_id, data, quantidade, peso_medio, observacao))

        cursor.execute("""
            UPDATE lotes
            SET
                quantidade_inicial = quantidade_inicial + ?,
                quantidade_atual = quantidade_atual + ?,
                peso_medio_inicial = ?,
                peso_medio_atual = ?
            WHERE id = ?
        """, (quantidade, quantidade, peso_medio, peso_medio, lote_id))

        conexao.commit()
        return True, "Chegada cadastrada com sucesso."
    
    except Exception as erro:
        return False, f"Erro ao cadastrar chegada: {erro}"
    
    finally:
        conexao.close()


def cadastrar_morte(lote_id, data, quantidade, causa, observacao):
    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute("""
            INSERT INTO mortes (lote_id, data, quantidade, causa, observacao)
            VALUES (?, ?, ?, ?, ?)
        """, (lote_id, data, quantidade, causa, observacao))

        cursor.execute("""
            UPDATE lotes
            SET
                mortalidade_total = mortalidade_total + ?,
                quantidade_atual = quantidade_atual - ?
            WHERE id = ?
        """, (quantidade, quantidade, lote_id))

        conexao.commit()
        return True, "Morte registrada com sucesso."
    
    except Exception as erro:
        return False, f"Erro ao registrar morte: {erro}"
    
    finally:
        conexao.close()

    
def cadastrar_racao(lote_id, data, tipo, quantidade_kg, observacao):
    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute("""
            INSERT INTO racoes (lote_id, data, tipo, quantidade_kg, observacao)
            VALUES (?, ?, ?, ?, ?)
        """, (lote_id, data, tipo, quantidade_kg, observacao))

        conexao.commit()
        return True, "Ração registrada com sucesso."
    
    except Exception as erro:
        return False, f"Erro ao registrar ração: {erro}"
    
    finally:
        conexao.close()


def cadastrar_saida(lote_id, data, quantidade, peso_medio, observacao):
    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute("""
            INSERT INTO saidas (lote_id, data, quantidade, peso_medio, observacao)
            VALUES (?, ?, ?, ?, ?)
        """, (lote_id, data, quantidade, peso_medio, observacao))

        cursor.execute("""
            UPDATE lotes
            SET
                quantidade_atual = quantidade_atual - ?,
                peso_medio_atual = ?,
            WHERE id = ?
        """, (quantidade, peso_medio, lote_id))

        conexao.commit()
        return True, "Saída cadastrada com sucesso."
    
    except Exception as erro:
        return False, f"Erro ao cadastrar saida: {erro}"
    
    finally:
        conexao.close()


def finalizar_lote(lote_id, data_finalizacao):
    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute("""
            UPDATE lotes
            SET
                status = 'finalizado',
                data_finalizacao = ?
            WHERE id = ?
        """, (data_finalizacao, lote_id))

        conexao.commit()
        return True, "Lote finalizado com sucesso."
    
    except Exception as erro:
        return False, f"Erro ao finalizar lote: {erro}"
    
    finally:
        conexao.close()
