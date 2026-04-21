"""
╔══════════════════════════════════════════════════════════╗
║              CanaGuard AI - Sistema Principal            ║
║     Plataforma de apoio à decisão para cana-de-açúcar    ║
╚══════════════════════════════════════════════════════════╝

Desenvolvido por:
  - Felipe de Sa Gomes Bruno
  - Karina Gaeta Szewczuk (Designer do Projeto)
  - Maria Sabrina Feitosa da Silva
  - Nicolas Lima Apolinário
  - Roger Gabriel de Souza de Jesus Costa

FIAP - Faculdade de Informática e Administração Paulista
Tutor: Sabrina Otoni | Coordenador: Andre Godoi
"""

import os
import sys

# Adiciona a pasta de arquivos do sistema ao caminho de importação
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from arquivos_do_sistema.cadastro import cadastrar_area, registrar_solo, registrar_insumo
from arquivos_do_sistema.cadastro import registrar_clima, registrar_incendio, registrar_producao
from arquivos_do_sistema.funcoes_menu import (
    calcular_financeiro, analisar_risco, gerar_recomendacoes,
    exibir_resumo_area, listar_areas
)
from arquivos_do_sistema.salvar_dados import carregar_dados, salvar_dados
from arquivos_do_sistema.relatorio import gerar_relatorio
from arquivos_do_sistema.banco_oracle import simular_oracle


# ──────────────────────────────────────────────
#  UTILITÁRIOS DE INTERFACE
# ──────────────────────────────────────────────

def limpar_tela():
    """Limpa o terminal para melhor visualização."""
    os.system("cls" if os.name == "nt" else "clear")


def pausar():
    """Aguarda o usuário pressionar Enter para continuar."""
    input("\n  Pressione ENTER para continuar...")


def separador(titulo="", largura=58):
    """Exibe uma linha separadora estilizada."""
    if titulo:
        espaco = largura - len(titulo) - 4
        esq = espaco // 2
        dir_ = espaco - esq
        print(f"\n  {'─' * esq}  {titulo}  {'─' * dir_}")
    else:
        print(f"\n  {'─' * largura}")


def cabecalho():
    """Exibe o cabeçalho principal do sistema."""
    limpar_tela()
    print("""
  ╔══════════════════════════════════════════════════════╗
  ║                 C A N A G U A R D                    ║
  ║     Plataforma Inteligente para Cana-de-Açúcar       ║
  ╚══════════════════════════════════════════════════════╝
    """)


def mensagem_boas_vindas():
    """Exibe mensagem de boas-vindas na primeira execução."""
    cabecalho()
    print("""
  Bem-vindo ao CanaGuard AI! 👋

  Este sistema foi criado para ajudar produtores de
  cana-de-açúcar a:

    ✅ Monitorar suas áreas e condições de solo
    ✅ Controlar custos e uso de insumos
    ✅ Avaliar riscos climáticos e de incêndio
    ✅ Calcular resultado financeiro da safra
    ✅ Receber recomendações de manejo

  💡 Dica: Cadastre pelo menos uma área antes de usar
     as outras funcionalidades do sistema.
    """)
    pausar()


# ──────────────────────────────────────────────
#  MENUS
# ──────────────────────────────────────────────

def exibir_menu_principal():
    """Exibe o menu principal do sistema."""
    cabecalho()
    print("  Selecione uma opção abaixo:\n")
    print("  ┌─────────────────────────────────────────┐")
    print("  │  📋  1. Gerenciar Áreas                 │")
    print("  │  🌱  2. Monitoramento do Solo           │")
    print("  │  🧪  3. Controle de Insumos             │")
    print("  │  🌤️   4. Condições Climáticas           │")
    print("  │  🔥  5. Risco de Incêndio               │")
    print("  │  🌾  6. Registro de Produção            │")
    print("  │  💰  7. Análise Financeira              │")
    print("  │  ⚠️   8. Análise de Risco               │")
    print("  │  📊  9. Relatório Completo              │")
    print("  │  🗄️  10. Simulação Oracle (banco)       │")
    print("  │  🚪  0. Sair do sistema                 │")
    print("  └───────────────────────────────────────-─┘")
    print()


def menu_areas(dados):
    """Submenu para gerenciamento de áreas."""
    while True:
        cabecalho()
        separador("📋 GERENCIAR ÁREAS")
        print("""
  1. Cadastrar nova área
  2. Ver resumo de uma área
  3. Listar todas as áreas
  0. Voltar ao menu principal
        """)
        opcao = input("  Digite a opção desejada: ").strip()

        if opcao == "1":
            cadastrar_area(dados)
            salvar_dados(dados)
        elif opcao == "2":
            exibir_resumo_area(dados)
        elif opcao == "3":
            listar_areas(dados)
            pausar()
        elif opcao == "0":
            break
        else:
            print("\n  ❌ Opção inválida. Tente novamente.")
            pausar()


# ──────────────────────────────────────────────
#  LOOP PRINCIPAL
# ──────────────────────────────────────────────

def main():
    """Função principal que controla o fluxo do sistema."""
    dados = carregar_dados()

    # Mostra boas-vindas se não houver áreas cadastradas
    if not dados.get("areas"):
        mensagem_boas_vindas()

    while True:
        exibir_menu_principal()
        opcao = input("  Digite a opção desejada: ").strip()

        if opcao == "1":
            menu_areas(dados)

        elif opcao == "2":
            separador("🌱 MONITORAMENTO DO SOLO")
            registrar_solo(dados)
            salvar_dados(dados)
            pausar()

        elif opcao == "3":
            separador("🧪 CONTROLE DE INSUMOS")
            registrar_insumo(dados)
            salvar_dados(dados)
            pausar()

        elif opcao == "4":
            separador("🌤️ CONDIÇÕES CLIMÁTICAS")
            registrar_clima(dados)
            salvar_dados(dados)
            pausar()

        elif opcao == "5":
            separador("🔥 RISCO DE INCÊNDIO")
            registrar_incendio(dados)
            salvar_dados(dados)
            pausar()

        elif opcao == "6":
            separador("🌾 REGISTRO DE PRODUÇÃO")
            registrar_producao(dados)
            salvar_dados(dados)
            pausar()

        elif opcao == "7":
            separador("💰 ANÁLISE FINANCEIRA")
            calcular_financeiro(dados)
            pausar()

        elif opcao == "8":
            separador("⚠️ ANÁLISE DE RISCO")
            analisar_risco(dados)
            gerar_recomendacoes(dados)
            pausar()

        elif opcao == "9":
            separador("📊 RELATÓRIO COMPLETO")
            gerar_relatorio(dados)
            pausar()

        elif opcao == "10":
            separador("🗄️ SIMULAÇÃO ORACLE")
            simular_oracle(dados)
            pausar()

        elif opcao == "0":
            cabecalho()
            print("\n  Obrigado por usar o CanaGuard AI! 🌿")
            print("  Até a próxima safra! 👋\n")
            salvar_dados(dados)
            break

        else:
            print("\n  ❌ Opção inválida. Digite um número de 0 a 10.")
            pausar()


# ──────────────────────────────────────────────
#  PONTO DE ENTRADA
# ──────────────────────────────────────────────

if __name__ == "__main__":
    main()
