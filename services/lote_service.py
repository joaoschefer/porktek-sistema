from datetime import date, datetime
from database import conectar


def validar_data(data):
    try:
        datetime.strptime(data, "%d/%m/%Y")
        return True
    except ValueError:
        return False


def validar_numero_positivo(valor, nome):
    if valor <= 0:
        return False, f"{nome} deve ser maior que zero."
    return True, ""


def calcular_data_media_chegada(chegadas):
    quantidade_total = 0
    soma_datas = 0

    for chegada in chegadas:
        data_chegada, quantidade = chegada[0], chegada[1]
        data_convertida = datetime.strptime(data_chegada, "%d/%m/%Y").date()
        quantidade_total += quantidade
        soma_datas += data_convertida.toordinal() * quantidade

    if quantidade_total == 0:
        return None

    ordinal_medio = int((soma_datas + (quantidade_total / 2)) // quantidade_total)
    return date.fromordinal(ordinal_medio).strftime("%d/%m/%Y")


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


def buscar_lote_por_id(lote_id):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id, codigo, data_chegada, quantidade_inicial, quantidade_atual,
               peso_medio_atual, status, data_finalizacao
        FROM lotes
        WHERE id = ?
        LIMIT 1
    """, (lote_id,))

    lote = cursor.fetchone()
    conexao.close()

    return lote


def buscar_lote_dashboard():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT codigo, data_chegada, quantidade_inicial, quantidade_atual, peso_medio_atual
        FROM lotes
        WHERE status = 'ativo'
        LIMIT 1
    """)

    lote = cursor.fetchone()
    conexao.close()

    return lote


def buscar_lotes_finalizados():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id, codigo, data_chegada, data_finalizacao, quantidade_inicial, quantidade_atual, status
        FROM lotes
        WHERE status = 'finalizado'
        ORDER BY id DESC
    """)

    lotes = cursor.fetchall()
    conexao.close()

    return lotes


def buscar_mortalidade_lotes_finalizados():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT codigo, quantidade_inicial, mortalidade_total
        FROM lotes
        WHERE status = 'finalizado'
        ORDER BY id DESC
    """)

    registros = cursor.fetchall()
    conexao.close()

    mortalidades = []
    for codigo, quantidade_inicial, mortalidade_total in registros:
        percentual = 0
        if quantidade_inicial > 0:
            percentual = (mortalidade_total / quantidade_inicial) * 100

        mortalidades.append({
            "codigo": codigo,
            "quantidade_inicial": quantidade_inicial,
            "mortes": mortalidade_total,
            "percentual": round(percentual, 2)
        })

    return mortalidades


def criar_lote(nome_lote):
    conexao = conectar()
    cursor = conexao.cursor()

    try:
        lote_ativo = buscar_lote_ativo()

        if lote_ativo:
            return False, "Já existe um lote ativo. Finalize o lote atual antes de criar outro."

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
            None,
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


def buscar_quantidade_disponivel_saida(cursor, lote_id, saida_id=None):
    cursor.execute("""
        SELECT COALESCE(SUM(quantidade), 0)
        FROM chegadas
        WHERE lote_id = ?
    """, (lote_id,))
    total_chegadas = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM mortes
        WHERE lote_id = ?
    """, (lote_id,))
    total_mortes = cursor.fetchone()[0]

    if saida_id:
        cursor.execute("""
            SELECT COALESCE(SUM(quantidade), 0)
            FROM saidas
            WHERE lote_id = ? AND id <> ?
        """, (lote_id, saida_id))
    else:
        cursor.execute("""
            SELECT COALESCE(SUM(quantidade), 0)
            FROM saidas
            WHERE lote_id = ?
        """, (lote_id,))

    total_saidas = cursor.fetchone()[0]
    return total_chegadas - total_mortes - total_saidas


def buscar_animais_comprometidos(cursor, lote_id):
    cursor.execute("""
        SELECT COALESCE(SUM(quantidade), 0)
        FROM saidas
        WHERE lote_id = ?
    """, (lote_id,))
    total_saidas = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM mortes
        WHERE lote_id = ?
    """, (lote_id,))
    total_mortes = cursor.fetchone()[0]

    return total_saidas + total_mortes


def buscar_mossas_lote(lote_id):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT DISTINCT mossa
        FROM chegadas
        WHERE lote_id = ? AND mossa IS NOT NULL AND mossa > 0
        ORDER BY mossa
    """, (lote_id,))

    mossas = [mossa[0] for mossa in cursor.fetchall()]
    conexao.close()

    return mossas


def calcular_peso_medio(quantidade, peso_total):
    return round(peso_total / quantidade, 2)


def validar_chegada(data, mossa, quantidade, peso_total):
    if not validar_data(data):
        return False, "Informe a data no formato dd/mm/aaaa."

    valido, mensagem = validar_numero_positivo(mossa, "Mossa")
    if not valido:
        return False, mensagem

    valido, mensagem = validar_numero_positivo(quantidade, "Quantidade")
    if not valido:
        return False, mensagem

    valido, mensagem = validar_numero_positivo(peso_total, "Peso total")
    if not valido:
        return False, mensagem

    return True, ""


def cadastrar_chegada(lote_id, data, mossa, quantidade, peso_total, observacao):
    valido, mensagem = validar_chegada(data, mossa, quantidade, peso_total)
    if not valido:
        return False, mensagem

    peso_medio = calcular_peso_medio(quantidade, peso_total)

    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute("""
            INSERT INTO chegadas (lote_id, data, mossa, quantidade, peso_total, peso_medio, observacao)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (lote_id, data, mossa, quantidade, peso_total, peso_medio, observacao))

        conexao.commit()

    except Exception as erro:
        return False, f"Erro ao cadastrar chegada: {erro}"

    finally:
        conexao.close()

    recalcular_peso_medio_lote(lote_id)

    return True, "Chegada cadastrada com sucesso."


def atualizar_chegada(registro_id, lote_id, data, mossa, quantidade, peso_total, observacao):
    valido, mensagem = validar_chegada(data, mossa, quantidade, peso_total)
    if not valido:
        return False, mensagem

    peso_medio = calcular_peso_medio(quantidade, peso_total)

    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute("""
            SELECT COALESCE(SUM(quantidade), 0)
            FROM chegadas
            WHERE lote_id = ? AND id <> ?
        """, (lote_id, registro_id))
        outras_chegadas = cursor.fetchone()[0]
        animais_comprometidos = buscar_animais_comprometidos(cursor, lote_id)

        if outras_chegadas + quantidade < animais_comprometidos:
            return False, f"Quantidade menor que saídas e mortes já registradas ({animais_comprometidos})."

        cursor.execute("""
            UPDATE chegadas
            SET data = ?, mossa = ?, quantidade = ?, peso_total = ?, peso_medio = ?, observacao = ?
            WHERE id = ? AND lote_id = ?
        """, (data, mossa, quantidade, peso_total, peso_medio, observacao, registro_id, lote_id))

        if cursor.rowcount == 0:
            return False, "Chegada não encontrada."

        conexao.commit()

    except Exception as erro:
        return False, f"Erro ao atualizar chegada: {erro}"

    finally:
        conexao.close()

    recalcular_peso_medio_lote(lote_id)

    return True, "Chegada atualizada com sucesso."


def validar_morte(data, mossa):
    if not validar_data(data):
        return False, "Informe a data no formato dd/mm/aaaa."

    valido, mensagem = validar_numero_positivo(mossa, "Mossa")
    if not valido:
        return False, mensagem

    return True, ""


def cadastrar_morte(lote_id, data, mossa, causa, observacao):
    valido, mensagem = validar_morte(data, mossa)
    if not valido:
        return False, mensagem

    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute("""
            SELECT quantidade_atual
            FROM lotes
            WHERE id = ?
        """, (lote_id,))
        lote = cursor.fetchone()

        if not lote or lote[0] <= 0:
            return False, "Não há suínos disponíveis para registrar morte."

        cursor.execute("""
            INSERT INTO mortes (lote_id, data, mossa, causa, observacao)
            VALUES (?, ?, ?, ?, ?)
        """, (lote_id, data, mossa, causa, observacao))

        conexao.commit()

    except Exception as erro:
        return False, f"Erro ao registrar morte: {erro}"

    finally:
        conexao.close()

    recalcular_peso_medio_lote(lote_id)

    return True, "Morte registrada com sucesso."


def atualizar_morte(registro_id, lote_id, data, mossa, causa, observacao):
    valido, mensagem = validar_morte(data, mossa)
    if not valido:
        return False, mensagem

    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute("""
            UPDATE mortes
            SET data = ?, mossa = ?, causa = ?, observacao = ?
            WHERE id = ? AND lote_id = ?
        """, (data, mossa, causa, observacao, registro_id, lote_id))

        if cursor.rowcount == 0:
            return False, "Morte não encontrada."

        conexao.commit()

    except Exception as erro:
        return False, f"Erro ao atualizar morte: {erro}"

    finally:
        conexao.close()

    recalcular_peso_medio_lote(lote_id)

    return True, "Morte atualizada com sucesso."


def validar_racao(data, tipo, quantidade_kg):
    if not validar_data(data):
        return False, "Informe a data no formato dd/mm/aaaa."

    if tipo.strip() == "":
        return False, "Informe o tipo de ração."

    valido, mensagem = validar_numero_positivo(quantidade_kg, "Quantidade")
    if not valido:
        return False, mensagem

    return True, ""


def validar_data_opcional(data, nome):
    if data and not validar_data(data):
        return False, f"Informe {nome} no formato dd/mm/aaaa."

    return True, ""


def validar_observacao(data_inicio, data_termino):
    valido, mensagem = validar_data_opcional(data_inicio, "a data de início")
    if not valido:
        return False, mensagem

    valido, mensagem = validar_data_opcional(data_termino, "a data de término")
    if not valido:
        return False, mensagem

    return True, ""


def cadastrar_observacao(lote_id, observacao, data_inicio, data_termino):
    valido, mensagem = validar_observacao(data_inicio, data_termino)
    if not valido:
        return False, mensagem

    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute("""
            INSERT INTO observacoes (lote_id, observacao, data_inicio, data_termino)
            VALUES (?, ?, ?, ?)
        """, (lote_id, observacao, data_inicio, data_termino))

        conexao.commit()
        return True, "Observação registrada com sucesso."

    except Exception as erro:
        return False, f"Erro ao registrar observação: {erro}"

    finally:
        conexao.close()


def atualizar_observacao(registro_id, lote_id, observacao, data_inicio, data_termino):
    valido, mensagem = validar_observacao(data_inicio, data_termino)
    if not valido:
        return False, mensagem

    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute("""
            UPDATE observacoes
            SET observacao = ?, data_inicio = ?, data_termino = ?
            WHERE id = ? AND lote_id = ?
        """, (observacao, data_inicio, data_termino, registro_id, lote_id))

        if cursor.rowcount == 0:
            return False, "Observação não encontrada."

        conexao.commit()
        return True, "Observação atualizada com sucesso."

    except Exception as erro:
        return False, f"Erro ao atualizar observação: {erro}"

    finally:
        conexao.close()


def cadastrar_racao(lote_id, data, tipo, quantidade_kg, observacao):
    valido, mensagem = validar_racao(data, tipo, quantidade_kg)
    if not valido:
        return False, mensagem

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


def atualizar_racao(registro_id, lote_id, data, tipo, quantidade_kg, observacao):
    valido, mensagem = validar_racao(data, tipo, quantidade_kg)
    if not valido:
        return False, mensagem

    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute("""
            UPDATE racoes
            SET data = ?, tipo = ?, quantidade_kg = ?, observacao = ?
            WHERE id = ? AND lote_id = ?
        """, (data, tipo, quantidade_kg, observacao, registro_id, lote_id))

        if cursor.rowcount == 0:
            return False, "Ração não encontrada."

        conexao.commit()
        return True, "Ração atualizada com sucesso."

    except Exception as erro:
        return False, f"Erro ao atualizar ração: {erro}"

    finally:
        conexao.close()


def validar_saida(data, quantidade, peso_medio):
    if not validar_data(data):
        return False, "Informe a data no formato dd/mm/aaaa."

    valido, mensagem = validar_numero_positivo(quantidade, "Quantidade")
    if not valido:
        return False, mensagem

    valido, mensagem = validar_numero_positivo(peso_medio, "Peso médio")
    if not valido:
        return False, mensagem

    return True, ""


def cadastrar_saida(lote_id, data, quantidade, peso_medio, observacao):
    valido, mensagem = validar_saida(data, quantidade, peso_medio)
    if not valido:
        return False, mensagem

    conexao = conectar()
    cursor = conexao.cursor()

    try:
        quantidade_disponivel = buscar_quantidade_disponivel_saida(cursor, lote_id)

        if quantidade > quantidade_disponivel:
            return False, f"Quantidade de saída maior que disponível ({quantidade_disponivel})."

        cursor.execute("""
            INSERT INTO saidas (lote_id, data, quantidade, peso_medio, observacao)
            VALUES (?, ?, ?, ?, ?)
        """, (lote_id, data, quantidade, peso_medio, observacao))

        conexao.commit()

    except Exception as erro:
        return False, f"Erro ao cadastrar saída: {erro}"

    finally:
        conexao.close()

    recalcular_peso_medio_lote(lote_id)

    return True, "Saída cadastrada com sucesso."


def atualizar_saida(registro_id, lote_id, data, quantidade, peso_medio, observacao):
    valido, mensagem = validar_saida(data, quantidade, peso_medio)
    if not valido:
        return False, mensagem

    conexao = conectar()
    cursor = conexao.cursor()

    try:
        quantidade_disponivel = buscar_quantidade_disponivel_saida(cursor, lote_id, registro_id)

        if quantidade > quantidade_disponivel:
            return False, f"Quantidade de saída maior que disponível ({quantidade_disponivel})."

        cursor.execute("""
            UPDATE saidas
            SET data = ?, quantidade = ?, peso_medio = ?, observacao = ?
            WHERE id = ? AND lote_id = ?
        """, (data, quantidade, peso_medio, observacao, registro_id, lote_id))

        if cursor.rowcount == 0:
            return False, "Saída não encontrada."

        conexao.commit()

    except Exception as erro:
        return False, f"Erro ao atualizar saída: {erro}"

    finally:
        conexao.close()

    recalcular_peso_medio_lote(lote_id)

    return True, "Saída atualizada com sucesso."


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


def buscar_historico_lote(lote_id):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id, data, mossa, quantidade, peso_total, peso_medio, observacao
        FROM chegadas
        WHERE lote_id = ?
        ORDER BY id DESC
    """, (lote_id,))
    chegadas = cursor.fetchall()

    cursor.execute("""
        SELECT id, data, mossa, causa, observacao
        FROM mortes
        WHERE lote_id = ?
        ORDER BY id DESC
    """, (lote_id,))
    mortes = cursor.fetchall()

    cursor.execute("""
        SELECT id, data, tipo, quantidade_kg, observacao
        FROM racoes
        WHERE lote_id = ?
        ORDER BY id DESC
    """, (lote_id,))
    racoes = cursor.fetchall()

    cursor.execute("""
        SELECT id, data, quantidade, peso_medio, observacao
        FROM saidas
        WHERE lote_id = ?
        ORDER BY id DESC
    """, (lote_id,))
    saidas = cursor.fetchall()

    cursor.execute("""
        SELECT id, observacao, data_inicio, data_termino
        FROM observacoes
        WHERE lote_id = ?
        ORDER BY id DESC
    """, (lote_id,))
    observacoes = cursor.fetchall()

    conexao.close()

    return {
        "chegadas": chegadas,
        "mortes": mortes,
        "racoes": racoes,
        "saidas": saidas,
        "observacoes": observacoes
    }


def buscar_resumo_lote(lote_id):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT quantidade_inicial, quantidade_atual, mortalidade_total, peso_medio_atual
        FROM lotes
        WHERE id = ?
    """, (lote_id,))
    lote = cursor.fetchone()

    if not lote:
        conexao.close()
        return None

    cursor.execute("""
        SELECT COALESCE(SUM(quantidade_kg), 0)
        FROM racoes
        WHERE lote_id = ?
    """, (lote_id,))
    total_racao = cursor.fetchone()[0]

    cursor.execute("""
        SELECT
            COALESCE(SUM(quantidade), 0),
            COALESCE(SUM(quantidade * peso_medio), 0)
        FROM saidas
        WHERE lote_id = ?
    """, (lote_id,))
    total_saidas, peso_total_saidas = cursor.fetchone()

    conexao.close()

    quantidade_inicial, quantidade_atual, mortes, peso_medio_atual = lote
    mortalidade_percentual = 0
    racao_por_animal = 0

    if quantidade_inicial > 0:
        mortalidade_percentual = (mortes / quantidade_inicial) * 100
        racao_por_animal = total_racao / quantidade_inicial

    peso_medio_saida = 0
    if total_saidas > 0:
        peso_medio_saida = peso_total_saidas / total_saidas

    return {
        "quantidade_inicial": quantidade_inicial,
        "quantidade_atual": quantidade_atual,
        "mortes": mortes,
        "mortalidade_percentual": round(mortalidade_percentual, 2),
        "total_racao": round(total_racao, 2),
        "racao_por_animal": round(racao_por_animal, 2),
        "peso_medio_atual": peso_medio_atual,
        "total_saidas": total_saidas,
        "peso_medio_saida": round(peso_medio_saida, 2)
    }


def excluir_movimentacao(tipo, registro_id, lote_id):
    tabelas = {
        "chegadas": "chegadas",
        "mortes": "mortes",
        "racoes": "racoes",
        "saidas": "saidas",
        "observacoes": "observacoes"
    }

    tabela = tabelas.get(tipo)
    if not tabela:
        return False, "Tipo de movimentação inválido."

    conexao = conectar()
    cursor = conexao.cursor()

    try:
        if tipo == "chegadas":
            cursor.execute("""
                SELECT quantidade
                FROM chegadas
                WHERE id = ? AND lote_id = ?
            """, (registro_id, lote_id))
            chegada = cursor.fetchone()

            if not chegada:
                return False, "Registro não encontrado."

            cursor.execute("""
                SELECT COALESCE(SUM(quantidade), 0)
                FROM chegadas
                WHERE lote_id = ?
            """, (lote_id,))
            total_chegadas = cursor.fetchone()[0]
            animais_comprometidos = buscar_animais_comprometidos(cursor, lote_id)

            if total_chegadas - chegada[0] < animais_comprometidos:
                return False, "Não é possível excluir: existem saídas ou mortes usando essa quantidade."

        cursor.execute(f"""
            DELETE FROM {tabela}
            WHERE id = ? AND lote_id = ?
        """, (registro_id, lote_id))

        if cursor.rowcount == 0:
            return False, "Registro não encontrado."

        conexao.commit()

    except Exception as erro:
        return False, f"Erro ao excluir registro: {erro}"

    finally:
        conexao.close()

    if tipo not in ("racoes", "observacoes"):
        recalcular_peso_medio_lote(lote_id)

    return True, "Registro excluído com sucesso."


def recalcular_peso_medio_lote(lote_id):
    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute("""
            SELECT data, quantidade, peso_medio, peso_total
            FROM chegadas
            WHERE lote_id = ?
            ORDER BY id
        """, (lote_id,))
        chegadas = cursor.fetchall()

        cursor.execute("""
            SELECT quantidade
            FROM saidas
            WHERE lote_id = ?
        """, (lote_id,))
        saidas = cursor.fetchall()

        cursor.execute("""
            SELECT COUNT(*)
            FROM mortes
            WHERE lote_id = ?
        """, (lote_id,))
        total_mortes = cursor.fetchone()[0]

        peso_total_chegadas = 0
        quantidade_total_chegadas = 0

        for _, quantidade, peso_medio, peso_total in chegadas:
            peso_total_chegadas += peso_total if peso_total is not None else quantidade * peso_medio
            quantidade_total_chegadas += quantidade

        quantidade_total_saidas = 0

        for (quantidade,) in saidas:
            quantidade_total_saidas += quantidade

        quantidade_atual = quantidade_total_chegadas - quantidade_total_saidas - total_mortes

        if quantidade_total_chegadas > 0:
            peso_medio_atual = peso_total_chegadas / quantidade_total_chegadas
        else:
            peso_medio_atual = 0

        data_chegada = calcular_data_media_chegada(chegadas)

        cursor.execute("""
            UPDATE lotes
            SET
                data_chegada = ?,
                quantidade_inicial = ?,
                quantidade_atual = ?,
                mortalidade_total = ?,
                peso_medio_inicial = ?,
                peso_medio_atual = ?
            WHERE id = ?
        """, (
            data_chegada,
            quantidade_total_chegadas,
            quantidade_atual,
            total_mortes,
            round(peso_medio_atual, 2),
            round(peso_medio_atual, 2),
            lote_id
        ))

        conexao.commit()

    finally:
        conexao.close()
