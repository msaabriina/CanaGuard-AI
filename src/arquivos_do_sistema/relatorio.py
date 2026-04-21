"""
relatorio.py
────────────
Gera relatório completo em arquivo .txt com todos
os dados registrados no CanaGuard AI.
"""

import os
from datetime import datetime


# Pasta onde os relatórios serão salvos
PASTA_RELATORIOS = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "relatorios_gerados"
)


def gerar_relatorio(dados):
    """
    Gera um arquivo .txt com o relatório completo
    de todas as áreas cadastradas no sistema.
    """
    print("""
  ┌────────────────────────────────────────────┐
  │         📊 GERAÇÃO DE RELATÓRIO            │
  └────────────────────────────────────────────┘
    """)

    areas = dados.get("areas", [])
    if not areas:
        print("  ⚠️  Nenhuma área cadastrada para gerar relatório.")
        print("  💡 Cadastre pelo menos uma área antes de gerar o relatório.")
        return

    # Garante que a pasta existe
    os.makedirs(PASTA_RELATORIOS, exist_ok=True)

    # Nome do arquivo com data/hora para não sobrescrever
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_arquivo = f"relatorio_canaguard_{timestamp}.txt"
    caminho = os.path.join(PASTA_RELATORIOS, nome_arquivo)

    agora = datetime.now().strftime("%d/%m/%Y às %H:%M")

    linhas = []

    def linha(texto=""):
        linhas.append(texto + "\n")

    def separador(titulo="", char="─", largura=60):
        if titulo:
            esp = (largura - len(titulo) - 2) // 2
            linhas.append(f"{'─' * esp} {titulo} {'─' * esp}\n")
        else:
            linhas.append(f"{'─' * largura}\n")

    # ── Cabeçalho ──
    linha("=" * 60)
    linha("       RELATÓRIO COMPLETO — CanaGuard AI")
    linha("       Plataforma de Apoio à Decisão Agrícola")
    linha("=" * 60)
    linha()
    linha(f"  Data de geração : {agora}")
    linha(f"  Total de áreas  : {len(areas)}")
    linha()

    # ── Dados de cada área ──
    for idx, area in enumerate(areas, 1):
        separador(f"ÁREA {idx} — {area['codigo']}")
        linha()
        linha(f"  Produtor   : {area['produtor']}")
        linha(f"  Fazenda    : {area['fazenda']}")
        linha(f"  Talhão     : {area['talhao']}")
        linha(f"  Hectares   : {area['hectares']} ha")
        linha(f"  Variedade  : {area['variedade']}")
        linha(f"  Fase       : {area['fase']}")
        linha(f"  Cadastro   : {area.get('data_cadastro', 'N/A')}")
        linha()

        # Solo
        separador("DADOS DO SOLO", char="·", largura=50)
        solo = area.get("solo")
        if solo:
            linha(f"  Umidade      : {solo['umidade']}%")
            linha(f"  Temperatura  : {solo['temperatura']}°C")
            linha(f"  Nutrientes   : {solo['nutrientes']}")
            linha(f"  Observações  : {solo['observacoes']}")
            linha(f"  Registrado em: {solo.get('data_registro', 'N/A')}")
        else:
            linha("  Solo não registrado.")
        linha()

        # Clima
        separador("CONDIÇÕES CLIMÁTICAS", char="·", largura=50)
        clima = area.get("clima")
        if clima:
            linha(f"  Previsão     : {clima['previsao']}")
            linha(f"  Temperatura  : {clima['temperatura_prevista']}°C")
            linha(f"  Chuva prev.  : {clima['chuva_prevista_mm']} mm")
            linha(f"  Registrado em: {clima.get('data_registro', 'N/A')}")
        else:
            linha("  Clima não registrado.")
        linha()

        # Incêndio
        separador("RISCO DE INCÊNDIO", char="·", largura=50)
        incendio = area.get("incendio")
        if incendio:
            linha(f"  Nível de risco: {incendio['nivel_risco']}")
            linha(f"  Foco próximo  : {'Sim' if incendio['foco_proximo'] else 'Não'}")
            linha(f"  Registrado em : {incendio.get('data_registro', 'N/A')}")
        else:
            linha("  Risco de incêndio não registrado.")
        linha()

        # Insumos
        separador("INSUMOS UTILIZADOS", char="·", largura=50)
        insumos = area.get("insumos", [])
        if insumos:
            custo_total_insumos = 0
            for ins in insumos:
                linha(f"  • {ins['nome']} ({ins['tipo']})")
                linha(f"    Quantidade: {ins['quantidade']} {ins['unidade']}")
                linha(f"    Custo     : R$ {ins['custo']:.2f}")
                custo_total_insumos += ins['custo']
            linha()
            linha(f"  Total em insumos: R$ {custo_total_insumos:,.2f}")
        else:
            linha("  Nenhum insumo registrado.")
        linha()

        # Produção
        separador("PRODUÇÃO E RESULTADO", char="·", largura=50)
        producao = area.get("producao")
        if producao:
            linha(f"  Toneladas colhidas  : {producao['toneladas']} t")
            linha(f"  Produtividade       : {producao['produtividade_por_ha']} t/ha")
            linha(f"  Preço por tonelada  : R$ {producao['preco_por_tonelada']:.2f}")
            linha(f"  Receita total       : R$ {producao['receita_total']:,.2f}")

            # Calcula resultado financeiro
            custo_total = sum(i["custo"] for i in insumos)
            lucro = producao["receita_total"] - custo_total
            margem = (lucro / producao["receita_total"] * 100) if producao["receita_total"] > 0 else 0

            linha()
            linha(f"  Custo total insumos : R$ {custo_total:,.2f}")
            linha(f"  Custo por hectare   : R$ {custo_total / area['hectares']:,.2f}" if area["hectares"] > 0 else "  Custo por hectare: N/A")
            linha(f"  {'LUCRO' if lucro >= 0 else 'PREJUÍZO'}               : R$ {abs(lucro):,.2f}")
            linha(f"  Margem              : {margem:.1f}%")
        else:
            linha("  Produção não registrada.")
        linha()

        # Análise de risco
        analise = area.get("ultima_analise_risco")
        if analise:
            separador("ANÁLISE DE RISCO", char="·", largura=50)
            linha(f"  Nível geral: {analise['nivel_geral']}")
            linha(f"  Data       : {analise.get('data', 'N/A')}")
            alertas = analise.get("alertas", [])
            if alertas:
                linha("  Alertas:")
                for alerta in alertas:
                    linha(f"    • {alerta}")
            linha()

        linha()

    # ── Rodapé ──
    linha("=" * 60)
    linha("  CanaGuard AI — FIAP")
    linha("  Grupo: Felipe, Karina, Sabrina, Nicolas, Roger")
    linha("  Tutor: Sabrina Otoni | Coord.: Andre Godoi")
    linha("=" * 60)

    # Escreve o arquivo
    try:
        with open(caminho, "w", encoding="utf-8") as f:
            f.writelines(linhas)

        print(f"  ✅ Relatório gerado com sucesso!")
        print(f"  📄 Arquivo: {nome_arquivo}")
        print(f"  📁 Pasta  : relatorios_gerados/")
        print(f"\n  💡 Abra o arquivo .txt em qualquer editor de texto.")

    except Exception as e:
        print(f"  ❌ Erro ao gerar relatório: {e}")
