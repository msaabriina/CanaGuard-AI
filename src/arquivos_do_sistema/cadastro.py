"""
cadastro.py
───────────
Funções de cadastro e coleta de dados do CanaGuard AI.
Cada função coleta informações do usuário com validações,
exemplos explicativos e mensagens amigáveis.
"""

import uuid
from datetime import date


# ──────────────────────────────────────────────
#  UTILITÁRIOS INTERNOS
# ──────────────────────────────────────────────

def _input_float(mensagem, minimo=None, maximo=None):
    """
    Solicita um número decimal ao usuário com validação.
    Continua pedindo até receber um valor válido.
    """
    while True:
        try:
            valor = float(input(mensagem).replace(",", "."))
            if minimo is not None and valor < minimo:
                print(f"  ⚠️  O valor mínimo aceito é {minimo}. Tente novamente.")
                continue
            if maximo is not None and valor > maximo:
                print(f"  ⚠️  O valor máximo aceito é {maximo}. Tente novamente.")
                continue
            return valor
        except ValueError:
            print("  ❌ Valor inválido. Use números (ex: 12.5 ou 12,5).")


def _input_inteiro(mensagem, opcoes=None):
    """
    Solicita um número inteiro ao usuário com validação.
    Se 'opcoes' for fornecido, valida se o valor está na lista.
    """
    while True:
        try:
            valor = int(input(mensagem))
            if opcoes and valor not in opcoes:
                print(f"  ❌ Opção inválida. Escolha entre: {opcoes}")
                continue
            return valor
        except ValueError:
            print("  ❌ Digite apenas números inteiros.")


def _input_texto(mensagem, minimo_chars=2):
    """
    Solicita um texto ao usuário garantindo que não está vazio.
    """
    while True:
        valor = input(mensagem).strip()
        if len(valor) >= minimo_chars:
            return valor
        print(f"  ❌ Texto muito curto. Digite pelo menos {minimo_chars} caracteres.")


def _selecionar_area(dados):
    """
    Lista as áreas cadastradas e pede para o usuário escolher uma.
    Retorna a área selecionada ou None se não houver áreas.
    """
    areas = dados.get("areas", [])
    if not areas:
        print("\n  ⚠️  Nenhuma área cadastrada ainda.")
        print("  💡 Cadastre uma área primeiro no menu '1. Gerenciar Áreas'.")
        return None

    print("\n  Áreas cadastradas:")
    for i, area in enumerate(areas, 1):
        print(f"  {i}. [{area['codigo']}] {area['fazenda']} - Talhão {area['talhao']} ({area['hectares']} ha)")

    print()
    escolha = _input_inteiro(
        f"  Qual área deseja usar? (1 a {len(areas)}): ",
        opcoes=list(range(1, len(areas) + 1))
    )
    return areas[escolha - 1]


# ──────────────────────────────────────────────
#  1. CADASTRO DE ÁREA
# ──────────────────────────────────────────────

def cadastrar_area(dados):
    """
    Coleta e registra os dados de uma nova área de cultivo.
    """
    print("""
  ┌────────────────────────────────────────────┐
  │         📋 CADASTRO DE NOVA ÁREA           │
  └────────────────────────────────────────────┘

  Vamos registrar os dados da sua área de cultivo.
  Preencha as informações abaixo:
    """)

    # Gera código automático único para a área
    codigo = "AREA-" + str(uuid.uuid4())[:6].upper()
    print(f"  🔖 Código gerado automaticamente: {codigo}")

    print("\n  ── Dados do Produtor ──")
    produtor = _input_texto(
        "  Nome do produtor\n  (ex: João da Silva): "
    )

    print("\n  ── Dados da Propriedade ──")
    fazenda = _input_texto(
        "  Nome da fazenda\n  (ex: Fazenda Santa Rosa): "
    )
    talhao = _input_texto(
        "  Identificação do talhão\n  (ex: Talhão 03, Gleba Norte): "
    )
    hectares = _input_float(
        "  Tamanho da área em hectares\n  (ex: 25.5 para 25 hectares e meio): ",
        minimo=0.1
    )

    print("\n  ── Dados da Cultura ──")
    print("  Variedades comuns de cana-de-açúcar:")
    print("  • RB867515 — alta produtividade, resistente à seca")
    print("  • SP803280  — boa adaptação a solos arenosos")
    print("  • CTC4       — excelente para regiões Centro-Oeste")
    variedade = _input_texto(
        "  Variedade plantada\n  (ex: RB867515): "
    )

    print("\n  Fases da cultura:")
    print("  1 - Plantio       (primeiro ano, cana planta)")
    print("  2 - Crescimento   (desenvolvimento vegetativo)")
    print("  3 - Maturação     (acúmulo de sacarose)")
    print("  4 - Colheita      (pronto para corte)")
    print("  5 - Ressoca       (rebrota após o corte)")
    fases = {1: "Plantio", 2: "Crescimento", 3: "Maturação", 4: "Colheita", 5: "Ressoca"}
    num_fase = _input_inteiro(
        "  Em qual fase está a cultura? (1 a 5): ",
        opcoes=[1, 2, 3, 4, 5]
    )
    fase = fases[num_fase]

    # Monta o dicionário da área
    nova_area = {
        "codigo": codigo,
        "produtor": produtor,
        "fazenda": fazenda,
        "talhao": talhao,
        "hectares": hectares,
        "variedade": variedade,
        "fase": fase,
        "data_cadastro": str(date.today()),
        "solo": None,
        "insumos": [],
        "clima": None,
        "incendio": None,
        "producao": None
    }

    # Adiciona a área à lista
    if "areas" not in dados:
        dados["areas"] = []
    dados["areas"].append(nova_area)

    print(f"""
  ✅ Área cadastrada com sucesso!
  ─────────────────────────────
  Código : {codigo}
  Produtor: {produtor}
  Fazenda : {fazenda} | Talhão: {talhao}
  Tamanho : {hectares} ha
  Variedade: {variedade} | Fase: {fase}
    """)


# ──────────────────────────────────────────────
#  2. REGISTRO DE DADOS DO SOLO
# ──────────────────────────────────────────────

def registrar_solo(dados):
    """
    Registra as condições do solo para uma área selecionada.
    """
    print("""
  ┌────────────────────────────────────────────┐
  │       🌱 REGISTRO DE DADOS DO SOLO         │
  └────────────────────────────────────────────┘

  O monitoramento do solo ajuda a identificar
  necessidade de irrigação e correção de nutrientes.
    """)

    area = _selecionar_area(dados)
    if not area:
        return

    print(f"\n  Registrando solo para: {area['fazenda']} - {area['talhao']}")

    print("""
  ── Umidade do Solo ──
  Referência rápida:
    • Abaixo de 30% → solo muito seco, risco de estresse hídrico
    • Entre 30% e 70% → faixa ideal para cana-de-açúcar
    • Acima de 70%  → solo encharcado, risco de doenças radiculares
    """)
    umidade = _input_float(
        "  Umidade atual do solo (0 a 100%)\n  (ex: 45.0): ",
        minimo=0, maximo=100
    )

    print("""
  ── Temperatura do Solo ──
  Referência rápida:
    • Abaixo de 18°C → desenvolvimento lento
    • Entre 25°C e 35°C → faixa ideal para crescimento
    • Acima de 40°C  → pode inibir absorção de nutrientes
    """)
    temperatura = _input_float(
        "  Temperatura do solo em °C\n  (ex: 28.5): ",
        minimo=-10, maximo=60
    )

    print("""
  ── Condição dos Nutrientes ──
  Avalie o nível geral de fertilidade:
    1 - Bom       (solo bem nutrido, sem deficiências visíveis)
    2 - Regular   (algumas deficiências, pode precisar de correção)
    3 - Ruim      (solo deficiente, necessita adubação urgente)
    """)
    niveis = {1: "Bom", 2: "Regular", 3: "Ruim"}
    num_nivel = _input_inteiro(
        "  Condição dos nutrientes (1, 2 ou 3): ",
        opcoes=[1, 2, 3]
    )
    nutrientes = niveis[num_nivel]

    print("\n  Observações (campo livre — descreva algo relevante)")
    print("  (ex: 'Solo com manchas amareladas, possível falta de N')")
    observacoes = input("  Observação: ").strip()
    if not observacoes:
        observacoes = "Nenhuma observação registrada."

    area["solo"] = {
        "umidade": umidade,
        "temperatura": temperatura,
        "nutrientes": nutrientes,
        "observacoes": observacoes,
        "data_registro": str(date.today())
    }

    print(f"""
  ✅ Solo registrado com sucesso!
  ─────────────────────────────
  Área     : {area['fazenda']} - {area['talhao']}
  Umidade  : {umidade}%
  Temperatura: {temperatura}°C
  Nutrientes : {nutrientes}
  Observações: {observacoes}
    """)


# ──────────────────────────────────────────────
#  3. REGISTRO DE INSUMOS
# ──────────────────────────────────────────────

def registrar_insumo(dados):
    """
    Registra o uso de insumos (fertilizantes, defensivos, etc.)
    para uma área selecionada.
    """
    print("""
  ┌────────────────────────────────────────────┐
  │        🧪 REGISTRO DE INSUMO              │
  └────────────────────────────────────────────┘

  Registre aqui cada insumo utilizado na área.
  Isso permite calcular o custo total de produção.
    """)

    area = _selecionar_area(dados)
    if not area:
        return

    print(f"\n  Registrando insumo para: {area['fazenda']} - {area['talhao']}")

    print("\n  ── Identificação do Insumo ──")
    print("  (ex: Ureia, Roundup, Sulfato de Amônio, Vinhaça)")
    nome = _input_texto("  Nome do insumo: ")

    print("""
  Tipo do insumo:
    1 - Fertilizante   (adubos, corretivos)
    2 - Defensivo      (herbicidas, inseticidas, fungicidas)
    3 - Irrigação      (água, sistema de irrigação)
    4 - Outros
    """)
    tipos = {1: "Fertilizante", 2: "Defensivo", 3: "Irrigação", 4: "Outros"}
    num_tipo = _input_inteiro(
        "  Tipo (1 a 4): ",
        opcoes=[1, 2, 3, 4]
    )
    tipo = tipos[num_tipo]

    print("\n  ── Quantidade Utilizada ──")
    quantidade = _input_float(
        "  Quantidade\n  (ex: 200 para 200 kg ou 50 para 50 litros): ",
        minimo=0.01
    )

    print("  Unidade de medida:")
    print("  1 - kg  |  2 - litros  |  3 - sacos  |  4 - toneladas")
    unidades = {1: "kg", 2: "litros", 3: "sacos", 4: "toneladas"}
    num_un = _input_inteiro("  Unidade (1 a 4): ", opcoes=[1, 2, 3, 4])
    unidade = unidades[num_un]

    print("\n  ── Custo ──")
    custo = _input_float(
        "  Custo total gasto com esse insumo em R$\n  (ex: 1500.00): ",
        minimo=0.0
    )

    insumo = {
        "nome": nome,
        "tipo": tipo,
        "quantidade": quantidade,
        "unidade": unidade,
        "custo": custo,
        "data_registro": str(date.today())
    }

    if "insumos" not in area:
        area["insumos"] = []
    area["insumos"].append(insumo)

    print(f"""
  ✅ Insumo registrado com sucesso!
  ─────────────────────────────
  Área     : {area['fazenda']} - {area['talhao']}
  Insumo   : {nome} ({tipo})
  Quantidade: {quantidade} {unidade}
  Custo    : R$ {custo:.2f}
    """)

    # Pergunta se quer registrar mais
    mais = input("  Deseja registrar outro insumo nessa área? (s/n): ").strip().lower()
    if mais == "s":
        registrar_insumo(dados)


# ──────────────────────────────────────────────
#  4. REGISTRO CLIMÁTICO
# ──────────────────────────────────────────────

def registrar_clima(dados):
    """
    Registra as condições climáticas previstas para uma área.
    """
    print("""
  ┌────────────────────────────────────────────┐
  │       🌤️  CONDIÇÕES CLIMÁTICAS             │
  └────────────────────────────────────────────┘

  Registre a previsão do tempo para a área.
  Esses dados são usados na análise de risco agrícola.
    """)

    area = _selecionar_area(dados)
    if not area:
        return

    print(f"\n  Condições climáticas para: {area['fazenda']} - {area['talhao']}")

    print("""
  Previsão do tempo:
    1 - Ensolarado   (sem chuvas previstas)
    2 - Nublado      (sem chuvas, temperaturas amenas)
    3 - Chuvoso      (chuvas esperadas)
    4 - Tempestade   (chuvas intensas, raios)
    5 - Seco/Quente  (sem chuvas + alta temperatura)
    """)
    previsoes = {1: "Ensolarado", 2: "Nublado", 3: "Chuvoso",
                 4: "Tempestade", 5: "Seco/Quente"}
    num_prev = _input_inteiro("  Previsão (1 a 5): ", opcoes=[1, 2, 3, 4, 5])
    previsao = previsoes[num_prev]

    print("""
  Temperatura prevista para os próximos dias:
    • Ideal para cana-de-açúcar: entre 25°C e 35°C
    """)
    temp_prevista = _input_float(
        "  Temperatura prevista em °C\n  (ex: 32.0): ",
        minimo=-5, maximo=50
    )

    print("""
  Chuva prevista (acumulado esperado):
    • Abaixo de 10mm → chuva leve ou sem chuva
    • Entre 10 e 30mm → chuva moderada
    • Acima de 30mm  → chuva intensa
    """)
    chuva_prevista = _input_float(
        "  Chuva prevista em mm\n  (ex: 15.0 para 15 milímetros): ",
        minimo=0
    )

    area["clima"] = {
        "previsao": previsao,
        "temperatura_prevista": temp_prevista,
        "chuva_prevista_mm": chuva_prevista,
        "data_registro": str(date.today())
    }

    print(f"""
  ✅ Condições climáticas registradas!
  ─────────────────────────────
  Área        : {area['fazenda']} - {area['talhao']}
  Previsão    : {previsao}
  Temperatura : {temp_prevista}°C
  Chuva prev. : {chuva_prevista} mm
    """)


# ──────────────────────────────────────────────
#  5. RISCO DE INCÊNDIO
# ──────────────────────────────────────────────

def registrar_incendio(dados):
    """
    Registra informações sobre risco de incêndio para uma área.
    """
    print("""
  ┌────────────────────────────────────────────┐
  │        🔥 MONITORAMENTO DE INCÊNDIO        │
  └────────────────────────────────────────────┘

  Incêndios são um dos maiores riscos para a lavoura
  de cana. Monitore e registre o nível de risco.
    """)

    area = _selecionar_area(dados)
    if not area:
        return

    print(f"\n  Risco de incêndio para: {area['fazenda']} - {area['talhao']}")

    print("""
  Nível de risco de incêndio:
    1 - Baixo      (umidade alta, sem histórico de focos próximos)
    2 - Médio      (umidade moderada, período seco)
    3 - Alto       (seca prolongada, ventos fortes)
    4 - Crítico    (condições extremas, alerta máximo)
    """)
    niveis = {1: "Baixo", 2: "Médio", 3: "Alto", 4: "Crítico"}
    num_nivel = _input_inteiro(
        "  Nível de risco (1 a 4): ",
        opcoes=[1, 2, 3, 4]
    )
    nivel_risco = niveis[num_nivel]

    print("""
  Existe foco de incêndio próximo à área?
  (Considere focos em até 10 km de distância)
    1 - Sim
    2 - Não
    """)
    foco_num = _input_inteiro("  Foco próximo? (1 ou 2): ", opcoes=[1, 2])
    foco_proximo = foco_num == 1

    area["incendio"] = {
        "nivel_risco": nivel_risco,
        "foco_proximo": foco_proximo,
        "data_registro": str(date.today())
    }

    # Alerta automático para risco crítico
    if nivel_risco == "Crítico" or foco_proximo:
        print("""
  🚨 ATENÇÃO — ALERTA DE RISCO!
  ─────────────────────────────
  Ações recomendadas IMEDIATAMENTE:
  • Acione a brigada de incêndio da propriedade
  • Mantenha aceiros limpos ao redor da área
  • Acesse o sistema PREVFOGO (IBAMA) para monitoramento
  • Contato emergência: Bombeiros - 193
        """)
    else:
        print(f"""
  ✅ Risco de incêndio registrado!
  ─────────────────────────────
  Área        : {area['fazenda']} - {area['talhao']}
  Nível       : {nivel_risco}
  Foco próximo: {'Sim ⚠️' if foco_proximo else 'Não ✅'}
        """)


# ──────────────────────────────────────────────
#  6. REGISTRO DE PRODUÇÃO
# ──────────────────────────────────────────────

def registrar_producao(dados):
    """
    Registra os dados de produção colhida para uma área.
    """
    print("""
  ┌────────────────────────────────────────────┐
  │        🌾 REGISTRO DE PRODUÇÃO             │
  └────────────────────────────────────────────┘

  Registre a quantidade colhida e o preço de venda.
  O sistema calculará a receita total automaticamente.
    """)

    area = _selecionar_area(dados)
    if not area:
        return

    print(f"\n  Produção para: {area['fazenda']} - {area['talhao']} ({area['hectares']} ha)")

    print("""
  ── Toneladas Colhidas ──
  Produtividade média da cana no Brasil: 70 a 85 t/ha
  Exemplo: área de 25 ha com produtividade média
           → estimativa: 25 × 77 = 1.925 toneladas
    """)
    toneladas = _input_float(
        "  Total de toneladas colhidas\n  (ex: 1925.0): ",
        minimo=0.1
    )

    # Calcula produtividade por hectare
    produtividade = toneladas / area["hectares"]
    print(f"\n  📊 Produtividade calculada: {produtividade:.1f} t/ha")
    if produtividade < 60:
        print("  ⚠️  Produtividade abaixo da média nacional (70-85 t/ha)")
    elif produtividade > 90:
        print("  🎉 Produtividade acima da média — excelente resultado!")
    else:
        print("  ✅ Produtividade dentro da faixa normal")

    print("""
  ── Preço de Venda ──
  O preço da tonelada de cana varia conforme:
    • Usina compradora
    • Teor de sacarose (ATR)
    • Contrato firmado
  Faixa atual de referência: R$ 100 a R$ 160 por tonelada
    """)
    preco_tonelada = _input_float(
        "  Preço recebido por tonelada em R$\n  (ex: 130.00): ",
        minimo=1.0
    )

    receita = toneladas * preco_tonelada

    area["producao"] = {
        "toneladas": toneladas,
        "produtividade_por_ha": round(produtividade, 2),
        "preco_por_tonelada": preco_tonelada,
        "receita_total": round(receita, 2),
        "data_registro": str(date.today())
    }

    print(f"""
  ✅ Produção registrada com sucesso!
  ─────────────────────────────────
  Área         : {area['fazenda']} - {area['talhao']}
  Colhido      : {toneladas:.1f} toneladas
  Produtividade: {produtividade:.1f} t/ha
  Preço/ton    : R$ {preco_tonelada:.2f}
  Receita Total: R$ {receita:,.2f}
    """)
