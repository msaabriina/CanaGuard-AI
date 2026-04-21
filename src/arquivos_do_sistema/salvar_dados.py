"""
salvar_dados.py
───────────────
Funções para carregar e salvar os dados do sistema
em arquivo JSON. O arquivo serve como banco de dados
local para persistência entre sessões.
"""

import json
import os

# Caminho do arquivo de dados
PASTA_DADOS = os.path.join(os.path.dirname(os.path.dirname(__file__)), "dados_do_sistema")
ARQUIVO_DADOS = os.path.join(PASTA_DADOS, "dados_canaguard.json")


def carregar_dados():
    """
    Carrega os dados do arquivo JSON.
    Se o arquivo não existir, retorna uma estrutura vazia.

    Retorna:
        dict: dicionário com os dados do sistema
    """
    # Garante que a pasta existe
    os.makedirs(PASTA_DADOS, exist_ok=True)

    if not os.path.exists(ARQUIVO_DADOS):
        print("  ℹ️  Iniciando com banco de dados vazio (primeiro acesso).")
        return {"areas": []}

    try:
        with open(ARQUIVO_DADOS, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
            total = len(dados.get("areas", []))
            if total > 0:
                print(f"  ✅ Dados carregados! {total} área(s) encontrada(s).")
            return dados
    except json.JSONDecodeError:
        print("  ⚠️  Arquivo de dados corrompido. Iniciando com dados vazios.")
        return {"areas": []}
    except Exception as e:
        print(f"  ❌ Erro ao carregar dados: {e}")
        return {"areas": []}


def salvar_dados(dados):
    """
    Salva os dados no arquivo JSON de forma legível (indentado).

    Parâmetros:
        dados (dict): dicionário com todos os dados do sistema
    """
    os.makedirs(PASTA_DADOS, exist_ok=True)

    try:
        with open(ARQUIVO_DADOS, "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, ensure_ascii=False, indent=4)
        print("  💾 Dados salvos com sucesso!")
    except Exception as e:
        print(f"  ❌ Erro ao salvar dados: {e}")
        print("  ⚠️  Seus dados podem não ter sido salvos. Tente novamente.")
