"""
banco_oracle.py
───────────────
Simula a integração com um banco de dados Oracle.
Gera os comandos SQL (INSERT) que seriam usados
para enviar os dados do sistema para o banco.

Em um ambiente real, usaríamos a biblioteca cx_Oracle
para conectar ao banco. Aqui, os comandos são
exibidos na tela e salvos em arquivo .sql para consulta.
"""

import os
from datetime import datetime


PASTA_DADOS = os.path.join(os.path.dirname(os.path.dirname(__file__)), "dados_do_sistema")


def simular_oracle(dados):
    """
    Gera e exibe os comandos SQL de INSERT para o Oracle
    com base nos dados cadastrados no sistema.
    """
    print("""
  ┌────────────────────────────────────────────┐
  │        SIMULAÇÃO ORACLE (Banco)            │
  └────────────────────────────────────────────┘

  O Oracle é um dos bancos de dados mais usados em
  empresas agrícolas e do agronegócio. Aqui simulamos
  como os dados do sistema seriam inseridos nele.

  Os comandos SQL abaixo seriam executados em uma
  conexão real com o banco usando a biblioteca cx_Oracle.
    """)

    areas = dados.get("areas", [])
    if not areas:
        print("  ⚠️  Nenhuma área cadastrada para gerar os comandos SQL.")
        return

    comandos = []
    agora = datetime.now().strftime("%d/%m/%Y %H:%M")

    # ── Criação das tabelas (DDL) ──
    ddl = """
-- ============================================
-- CanaGuard AI — Simulação Oracle
-- Gerado em: {data}
-- ============================================

-- TABELA: areas
CREATE TABLE areas (
    codigo        VARCHAR2(20)  PRIMARY KEY,
    produtor      VARCHAR2(100),
    fazenda       VARCHAR2(100),
    talhao        VARCHAR2(50),
    hectares      NUMBER(10,2),
    variedade     VARCHAR2(50),
    fase          VARCHAR2(30),
    data_cadastro DATE
);

-- TABELA: solo
CREATE TABLE solo (
    id            NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    area_codigo   VARCHAR2(20) REFERENCES areas(codigo),
    umidade       NUMBER(5,2),
    temperatura   NUMBER(5,2),
    nutrientes    VARCHAR2(20),
    observacoes   VARCHAR2(500),
    data_registro DATE
);

-- TABELA: insumos
CREATE TABLE insumos (
    id            NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    area_codigo   VARCHAR2(20) REFERENCES areas(codigo),
    nome          VARCHAR2(100),
    tipo          VARCHAR2(50),
    quantidade    NUMBER(10,2),
    unidade       VARCHAR2(20),
    custo         NUMBER(12,2),
    data_registro DATE
);

-- TABELA: producao
CREATE TABLE producao (
    id                  NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    area_codigo         VARCHAR2(20) REFERENCES areas(codigo),
    toneladas           NUMBER(12,2),
    produtividade_por_ha NUMBER(8,2),
    preco_por_tonelada  NUMBER(10,2),
    receita_total       NUMBER(15,2),
    data_registro       DATE
);
""".format(data=agora)

    comandos.append(ddl)
    print("  📋 Comandos SQL gerados:\n")

    # ── INSERT para cada área ──
    for area in areas:
        sql_area = (
            f"INSERT INTO areas (codigo, produtor, fazenda, talhao, hectares, variedade, fase, data_cadastro)\n"
            f"VALUES ('{area['codigo']}', '{area['produtor']}', '{area['fazenda']}',\n"
            f"        '{area['talhao']}', {area['hectares']}, '{area['variedade']}',\n"
            f"        '{area['fase']}', TO_DATE('{area.get('data_cadastro', '')}', 'YYYY-MM-DD'));\n"
        )
        comandos.append(sql_area)
        print(f"  ── Área: {area['codigo']} ──")
        print(f"  {sql_area.strip()}\n")

        # INSERT solo
        solo = area.get("solo")
        if solo:
            obs = solo["observacoes"].replace("'", "''")  # Escapa aspas simples
            sql_solo = (
                f"INSERT INTO solo (area_codigo, umidade, temperatura, nutrientes, observacoes, data_registro)\n"
                f"VALUES ('{area['codigo']}', {solo['umidade']}, {solo['temperatura']},\n"
                f"        '{solo['nutrientes']}', '{obs}',\n"
                f"        TO_DATE('{solo.get('data_registro', '')}', 'YYYY-MM-DD'));\n"
            )
            comandos.append(sql_solo)
            print(f"  {sql_solo.strip()}\n")

        # INSERT insumos
        for ins in area.get("insumos", []):
            sql_ins = (
                f"INSERT INTO insumos (area_codigo, nome, tipo, quantidade, unidade, custo, data_registro)\n"
                f"VALUES ('{area['codigo']}', '{ins['nome']}', '{ins['tipo']}',\n"
                f"        {ins['quantidade']}, '{ins['unidade']}', {ins['custo']},\n"
                f"        TO_DATE('{ins.get('data_registro', '')}', 'YYYY-MM-DD'));\n"
            )
            comandos.append(sql_ins)
            print(f"  {sql_ins.strip()}\n")

        # INSERT produção
        producao = area.get("producao")
        if producao:
            sql_prod = (
                f"INSERT INTO producao (area_codigo, toneladas, produtividade_por_ha, "
                f"preco_por_tonelada, receita_total, data_registro)\n"
                f"VALUES ('{area['codigo']}', {producao['toneladas']}, "
                f"{producao['produtividade_por_ha']},\n"
                f"        {producao['preco_por_tonelada']}, {producao['receita_total']},\n"
                f"        TO_DATE('{producao.get('data_registro', '')}', 'YYYY-MM-DD'));\n"
            )
            comandos.append(sql_prod)
            print(f"  {sql_prod.strip()}\n")

    # Salva os comandos em arquivo .sql
    os.makedirs(PASTA_DADOS, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    caminho_sql = os.path.join(PASTA_DADOS, f"oracle_inserts_{timestamp}.sql")

    try:
        with open(caminho_sql, "w", encoding="utf-8") as f:
            f.writelines(comandos)

        print(f"""
  ✅ Simulação Oracle concluída!
  ─────────────────────────────
  Comandos salvos em: dados_do_sistema/oracle_inserts_{timestamp}.sql

  💡 Explicação para uso real com cx_Oracle:
     import cx_Oracle
     conn = cx_Oracle.connect("usuario/senha@host:1521/sid")
     cursor = conn.cursor()
     cursor.execute(comando_sql)
     conn.commit()
        """)

    except Exception as e:
        print(f"  ❌ Erro ao salvar arquivo SQL: {e}")
