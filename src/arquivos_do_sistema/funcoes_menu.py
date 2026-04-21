"""
funcoes_menu.py
───────────────
Funções de análise, cálculo financeiro, risco agrícola
e geração de recomendações de manejo do CanaGuard AI.
"""


# ──────────────────────────────────────────────
#  UTILITÁRIOS
# ──────────────────────────────────────────────

def _selecionar_area_menu(dados):
    """Exibe as áreas e pede que o usuário escolha uma."""
    areas = dados.get("areas", [])
    if not areas:
        print("\n  ⚠️  Nenhuma área cadastrada ainda.")
        print("  💡 Cadastre uma área primeiro no menu '1. Gerenciar Áreas'.")
        return None

    print("\n  Áreas disponíveis:")
    for i, area in enumerate(areas, 1):
        print(f"  {i}. [{area['codigo']}] {area['fazenda']} — Talhão: {area['talhao']} ({area['hectares']} ha)")

    print()
    while True:
        try:
            escolha = int(input(f"  Selecione a área (1 a {len(areas)}): "))
            if 1 <= escolha <= len(areas):
                return areas[escolha - 1]
            print("  ❌ Número fora do intervalo. Tente novamente.")
        except ValueError:
            print("  ❌ Digite apenas o número da área.")


# ──────────────────────────────────────────────
#  7. ANÁLISE FINANCEIRA
# ──────────────────────────────────────────────

def calcular_financeiro(dados):
    """
    Calcula e exibe o resultado financeiro de uma área:
    custo total, receita, lucro e margem.
    """
    print("""
  ┌────────────────────────────────────────────┐
  │          💰 ANÁLISE FINANCEIRA             │
  └────────────────────────────────────────────┘
    """)

    area = _selecionar_area_menu(dados)
    if not area:
        return

    print(f"\n  Calculando resultado financeiro para:")
    print(f"  {area['fazenda']} — Talhão: {area['talhao']} ({area['hectares']} ha)\n")

    # ── Cálculo dos custos ──
    insumos = area.get("insumos", [])
    custo_insumos = sum(i["custo"] for i in insumos)
    custo_por_ha = custo_insumos / area["hectares"] if area["hectares"] > 0 else 0

    # ── Receita ──
    producao = area.get("producao")
    if not producao:
        print("  ⚠️  Produção ainda não registrada para essa área.")
        print("  💡 Registre a produção no menu '6. Registro de Produção' primeiro.")
        return

    receita = producao["receita_total"]
    lucro = receita - custo_insumos
    margem = (lucro / receita * 100) if receita > 0 else 0

    # ── Exibição do resultado ──
    print("  ┌──────────────────────────────────────────┐")
    print("  │           RESULTADO FINANCEIRO           │")
    print("  ├──────────────────────────────────────────┤")
    print(f"  │  Área total       : {area['hectares']:.1f} ha".ljust(45) + "│")
    print(f"  │  Toneladas colhidas: {producao['toneladas']:.1f} t".ljust(45) + "│")
    print("  ├──────────────────────────────────────────┤")

    print(f"  │  💵 Receita total  : R$ {receita:>12,.2f}          │")
    print(f"  │  💸 Custo insumos  : R$ {custo_insumos:>12,.2f}          │")
    print(f"  │  📦 Custo por ha   : R$ {custo_por_ha:>12,.2f}          │")
    print("  ├──────────────────────────────────────────┤")

    if lucro >= 0:
        print(f"  │  ✅ LUCRO          : R$ {lucro:>12,.2f}          │")
    else:
        print(f"  │  ❌ PREJUÍZO       : R$ {abs(lucro):>12,.2f}          │")

    print(f"  │  📈 Margem         :    {margem:>11.1f}%          │")
    print("  └──────────────────────────────────────────┘")

    # ── Interpretação da margem ──
    print("\n  📊 Interpretação dos resultados:")
    if margem >= 30:
        print("  🟢 Excelente! Margem acima de 30% — operação muito rentável.")
    elif margem >= 15:
        print("  🟡 Bom! Margem entre 15% e 30% — operação saudável.")
    elif margem >= 0:
        print("  🟠 Atenção: Margem baixa (abaixo de 15%).")
        print("     Verifique possibilidades de redução de custos.")
    else:
        print("  🔴 Prejuízo! Custos superaram a receita.")
        print("     Avalie aumento de produtividade ou redução de gastos.")

    # Detalhamento dos insumos
    if insumos:
        print(f"\n  💡 Detalhamento dos custos ({len(insumos)} insumo(s) registrado(s)):")
        for ins in insumos:
            print(f"     • {ins['nome']} ({ins['tipo']}): R$ {ins['custo']:.2f}")


# ──────────────────────────────────────────────
#  8. ANÁLISE DE RISCO
# ──────────────────────────────────────────────

def analisar_risco(dados):
    """
    Analisa múltiplos fatores de risco da área selecionada
    e gera um nível geral de risco (Baixo, Médio, Alto, Crítico).
    """
    print("""
  ┌────────────────────────────────────────────┐
  │           ⚠️  ANÁLISE DE RISCO             │
  └────────────────────────────────────────────┘

  O sistema vai avaliar todos os fatores de risco
  registrados para a área selecionada.
    """)

    area = _selecionar_area_menu(dados)
    if not area:
        return

    print(f"\n  Analisando riscos para: {area['fazenda']} — {area['talhao']}\n")

    pontos = 0          # Acumula pontos de risco (mais = pior)
    alertas = []        # Lista de alertas detectados
    positivos = []      # Lista de pontos positivos

    # ── Análise do Solo ──
    solo = area.get("solo")
    if solo:
        print("  🌱 Solo........................", end=" ")
        if solo["umidade"] < 30:
            pontos += 2
            alertas.append(f"Solo com umidade muito baixa ({solo['umidade']}%) — risco de estresse hídrico")
            print("⚠️  ALERTA")
        elif solo["umidade"] > 80:
            pontos += 1
            alertas.append(f"Solo com umidade muito alta ({solo['umidade']}%) — risco de encharcamento")
            print("⚠️  ALERTA")
        else:
            positivos.append(f"Umidade do solo adequada ({solo['umidade']}%)")
            print("✅ OK")

        if solo["temperatura"] > 38:
            pontos += 1
            alertas.append(f"Temperatura do solo elevada ({solo['temperatura']}°C)")
        if solo["nutrientes"] == "Ruim":
            pontos += 2
            alertas.append("Condição nutricional do solo ruim — adubação necessária")
        elif solo["nutrientes"] == "Regular":
            pontos += 1
            alertas.append("Condição nutricional do solo regular — atenção à adubação")
    else:
        print("  🌱 Solo........................ ℹ️  Não registrado")
        alertas.append("Dados do solo não registrados — cadastre para análise completa")

    # ── Análise Climática ──
    clima = area.get("clima")
    if clima:
        print("  🌤️  Clima....................... ", end="")
        if clima["previsao"] in ["Seco/Quente", "Tempestade"]:
            pontos += 2
            alertas.append(f"Previsão climática de risco: {clima['previsao']}")
            print("⚠️  ALERTA")
        else:
            positivos.append(f"Condição climática favorável: {clima['previsao']}")
            print("✅ OK")

        if clima["temperatura_prevista"] > 38:
            pontos += 1
            alertas.append(f"Temperatura prevista muito alta ({clima['temperatura_prevista']}°C)")
        if clima["chuva_prevista_mm"] < 5 and clima["previsao"] not in ["Chuvoso", "Tempestade"]:
            pontos += 1
            alertas.append("Pouca chuva prevista — avaliar necessidade de irrigação")
    else:
        print("  🌤️  Clima....................... ℹ️  Não registrado")

    # ── Análise de Incêndio ──
    incendio = area.get("incendio")
    if incendio:
        print("  🔥 Incêndio................... ", end="")
        if incendio["nivel_risco"] == "Crítico":
            pontos += 4
            alertas.append("🚨 Risco de incêndio CRÍTICO!")
            print("🚨 CRÍTICO")
        elif incendio["nivel_risco"] == "Alto":
            pontos += 2
            alertas.append("Risco de incêndio alto — aceiros devem estar limpos")
            print("⚠️  ALERTA")
        elif incendio["nivel_risco"] == "Médio":
            pontos += 1
            alertas.append("Risco de incêndio médio — mantenha monitoramento")
            print("🟡 MÉDIO")
        else:
            positivos.append("Risco de incêndio baixo")
            print("✅ BAIXO")

        if incendio["foco_proximo"]:
            pontos += 3
            alertas.append("🚨 Foco de incêndio detectado nas proximidades!")
    else:
        print("  🔥 Incêndio................... ℹ️  Não registrado")

    # ── Análise da Produção ──
    producao = area.get("producao")
    if producao:
        print("  🌾 Produtividade.............. ", end="")
        if producao["produtividade_por_ha"] < 60:
            pontos += 2
            alertas.append(f"Produtividade abaixo da média ({producao['produtividade_por_ha']:.1f} t/ha)")
            print("⚠️  ABAIXO DA MÉDIA")
        elif producao["produtividade_por_ha"] > 90:
            positivos.append(f"Produtividade excelente: {producao['produtividade_por_ha']:.1f} t/ha")
            print("🏆 EXCELENTE")
        else:
            positivos.append(f"Produtividade adequada: {producao['produtividade_por_ha']:.1f} t/ha")
            print("✅ OK")

    # ── Nível Geral de Risco ──
    print("\n  " + "─" * 44)
    if pontos == 0:
        nivel_geral = "🟢 BAIXO"
        msg = "Situação favorável. Continue monitorando regularmente."
    elif pontos <= 3:
        nivel_geral = "🟡 MÉDIO"
        msg = "Atenção necessária. Verifique os alertas abaixo."
    elif pontos <= 6:
        nivel_geral = "🟠 ALTO"
        msg = "Situação preocupante. Tome ações preventivas imediatas."
    else:
        nivel_geral = "🔴 CRÍTICO"
        msg = "Situação crítica! Ação imediata necessária."

    print(f"\n  NÍVEL GERAL DE RISCO: {nivel_geral}")
    print(f"  {msg}")

    if alertas:
        print("\n  ⚠️  Alertas detectados:")
        for alerta in alertas:
            print(f"     • {alerta}")

    if positivos:
        print("\n  ✅ Pontos positivos:")
        for pos in positivos:
            print(f"     • {pos}")

    # Salva o resultado na área para uso posterior
    area["ultima_analise_risco"] = {
        "nivel_geral": nivel_geral,
        "pontos": pontos,
        "alertas": alertas,
        "data": __import__("datetime").date.today().isoformat()
    }


# ──────────────────────────────────────────────
#  8b. RECOMENDAÇÕES DE MANEJO
# ──────────────────────────────────────────────

def gerar_recomendacoes(dados):
    """
    Gera recomendações práticas de manejo baseadas
    nos dados e alertas registrados na área.
    """
    areas = dados.get("areas", [])
    if not areas:
        return

    # Pega a área que acabou de ser analisada (com análise registrada)
    areas_analisadas = [a for a in areas if a.get("ultima_analise_risco")]
    if not areas_analisadas:
        return

    area = areas_analisadas[-1]  # Última analisada
    analise = area["ultima_analise_risco"]
    alertas = analise.get("alertas", [])

    print("\n  " + "─" * 44)
    print("  💡 RECOMENDAÇÕES DE MANEJO")
    print("  " + "─" * 44)

    recomendacoes = []

    # Recomendações baseadas nos alertas
    for alerta in alertas:
        alerta_lower = alerta.lower()

        if "umidade muito baixa" in alerta_lower or "estresse hídrico" in alerta_lower:
            recomendacoes.append(
                "🚿 IRRIGAÇÃO URGENTE: Umidade do solo crítica. "
                "Aplique irrigação imediatamente para evitar perda de produção. "
                "Verifique o sistema de irrigação e a disponibilidade de água."
            )
        if "encharcamento" in alerta_lower:
            recomendacoes.append(
                "💧 DRENAGEM: Solo com excesso de água. "
                "Verifique e melhore o sistema de drenagem da área. "
                "Evite tráfego de máquinas pesadas para não compactar o solo."
            )
        if "nutricional" in alerta_lower and "ruim" in alerta_lower:
            recomendacoes.append(
                "🌿 ADUBAÇÃO URGENTE: Realize análise de solo completa "
                "(N, P, K e micronutrientes). Aplique fertilizantes conforme "
                "laudo técnico de um agrônomo."
            )
        if "nutricional" in alerta_lower and "regular" in alerta_lower:
            recomendacoes.append(
                "🌿 ADUBAÇÃO: Considere adubação de cobertura. "
                "Recomenda-se análise de solo para confirmar deficiências."
            )
        if "incêndio" in alerta_lower and "crítico" in alerta_lower:
            recomendacoes.append(
                "🔥 EMERGÊNCIA DE INCÊNDIO: Acione brigada imediatamente! "
                "Mantenha aceiros limpos (faixas de 5m sem vegetação). "
                "Contato Bombeiros: 193 | PREVFOGO/IBAMA: 0800-618080"
            )
        if "foco de incêndio" in alerta_lower:
            recomendacoes.append(
                "🔥 ALERTA DE FOCO: Monitoramento intensivo necessário. "
                "Prepare equipamentos de combate a incêndio. "
                "Notifique as autoridades locais e usina contratada."
            )
        if "seco/quente" in alerta_lower:
            recomendacoes.append(
                "☀️ CALOR EXTREMO: Evite operações no período mais quente "
                "(11h às 15h). Proteja trabalhadores. "
                "Avalie irrigação suplementar para reduzir estresse da cultura."
            )
        if "produtividade abaixo" in alerta_lower:
            recomendacoes.append(
                "📉 PRODUTIVIDADE BAIXA: Analise as causas: solo, clima, pragas? "
                "Consulte um engenheiro agrônomo para diagnóstico. "
                "Considere variedades mais adaptadas para a próxima safra."
            )

    # Recomendação genérica se não houver alertas
    if not recomendacoes:
        recomendacoes.append(
            "✅ Situação sob controle! Continue com as práticas atuais "
            "de monitoramento. Mantenha registros atualizados no sistema."
        )

    # Recomendação sempre presente
    recomendacoes.append(
        "📋 REGISTROS: Mantenha todos os dados atualizados no CanaGuard AI "
        "para análises mais precisas a cada ciclo."
    )

    for i, rec in enumerate(recomendacoes, 1):
        print(f"\n  {i}. {rec}")

    print()


# ──────────────────────────────────────────────
#  LISTAR E EXIBIR ÁREAS
# ──────────────────────────────────────────────

def listar_areas(dados):
    """
    Exibe uma tabela resumida de todas as áreas cadastradas.
    """
    areas = dados.get("areas", [])
    if not areas:
        print("\n  ℹ️  Nenhuma área cadastrada ainda.")
        print("  💡 Use o menu '1 → 1. Cadastrar nova área' para começar.")
        return

    print(f"\n  Total de áreas cadastradas: {len(areas)}\n")
    print("  " + "─" * 66)
    print(f"  {'#':<3} {'Código':<12} {'Fazenda':<20} {'Talhão':<15} {'Ha':>6} {'Fase':<12}")
    print("  " + "─" * 66)

    for i, area in enumerate(areas, 1):
        print(
            f"  {i:<3} "
            f"{area['codigo']:<12} "
            f"{area['fazenda'][:18]:<20} "
            f"{area['talhao'][:13]:<15} "
            f"{area['hectares']:>6.1f} "
            f"{area['fase']:<12}"
        )

    print("  " + "─" * 66)


def exibir_resumo_area(dados):
    """
    Exibe o resumo completo de uma área selecionada.
    """
    area = _selecionar_area_menu(dados)
    if not area:
        return

    print(f"""
  ┌────────────────────────────────────────────────┐
  │             📊 RESUMO DA ÁREA                  │
  └────────────────────────────────────────────────┘

  Código    : {area['codigo']}
  Produtor  : {area['produtor']}
  Fazenda   : {area['fazenda']}
  Talhão    : {area['talhao']}
  Hectares  : {area['hectares']} ha
  Variedade : {area['variedade']}
  Fase      : {area['fase']}
  Cadastro  : {area.get('data_cadastro', 'N/A')}
    """)

    # Solo
    solo = area.get("solo")
    if solo:
        print(f"  🌱 Solo: Umidade {solo['umidade']}% | Temperatura {solo['temperatura']}°C | Nutrientes: {solo['nutrientes']}")
    else:
        print("  🌱 Solo: Não registrado")

    # Clima
    clima = area.get("clima")
    if clima:
        print(f"  🌤️  Clima: {clima['previsao']} | {clima['temperatura_prevista']}°C | Chuva: {clima['chuva_prevista_mm']}mm")
    else:
        print("  🌤️  Clima: Não registrado")

    # Incêndio
    incendio = area.get("incendio")
    if incendio:
        foco = "Sim ⚠️" if incendio["foco_proximo"] else "Não"
        print(f"  🔥 Incêndio: Risco {incendio['nivel_risco']} | Foco próximo: {foco}")
    else:
        print("  🔥 Incêndio: Não registrado")

    # Insumos
    insumos = area.get("insumos", [])
    custo_total = sum(i["custo"] for i in insumos)
    print(f"  🧪 Insumos: {len(insumos)} registrado(s) | Custo total: R$ {custo_total:,.2f}")

    # Produção
    producao = area.get("producao")
    if producao:
        print(f"  🌾 Produção: {producao['toneladas']} t | R$ {producao['receita_total']:,.2f}")
    else:
        print("  🌾 Produção: Não registrada")

    input("\n  Pressione ENTER para continuar...")
