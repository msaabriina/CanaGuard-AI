# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href= "https://www.fiap.com.br/"><img src="assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Admnistração Paulista" border="0" width=40% height=40%></a>
</p>

<br>

# 🌿 CanaGuard AI
> **Plataforma inteligente de apoio à decisão para a cultura da cana-de-açúcar**

## Nome do grupo

## 👨‍🎓 Integrantes: 
| Felipe de Sa Gomes Bruno 
| Karina Gaeta Szewczuk 
| Maria Sabrina Feitosa da Silva 
| Nicolas Lima Apolinário 
| Roger Gabriel de Souza de Jesus Costa 

## 👩‍🏫 Professores:
### Tutor(a) 
Sabrina Otoni 
### Coordenador(a)
Andre Godoi 


## 📜 Descrição

O CanaGuard AI é um sistema em Python desenvolvido para ajudar produtores de cana-de-açúcar a monitorar suas áreas, controlar custos e tomar decisões mais embasadas durante a safra.

O sistema foi pensado para ser simples de usar, com menus interativos, exemplos práticos em cada campo e mensagens claras de orientação, porque entendemos que nem todo produtor é especialista em tecnologia.


## 📁 Estrutura de pastas

Dentre os arquivos e pastas presentes na raiz do projeto, definem-se:

.github: arquivos de configuração do GitHub para gerenciamento do repositório.
assets: arquivos relacionados a elementos não-estruturados, como imagens e capturas de tela do sistema.
config: arquivos de configuração e parâmetros do projeto.
document: documentos do projeto entregues nas atividades. Na subpasta other, documentos complementares.
scripts: scripts auxiliares, incluindo exemplos de integração Oracle e utilitários de apoio.
src: todo o código-fonte do projeto, organizado nos seguintes módulos:
sistema_principal.py — ponto de entrada do sistema
arquivos_do_sistema/cadastro.py — coleta e validação de dados
arquivos_do_sistema/funcoes_menu.py — análise financeira, risco e recomendações
arquivos_do_sistema/salvar_dados.py — persistência em JSON
arquivos_do_sistema/relatorio.py — geração de relatório .txt
arquivos_do_sistema/banco_oracle.py — simulação de integração Oracle


README.md: guia geral do projeto.

## 🔧 Como executar o código

### Pré-requisitos
- Python 3.8 ou superior instalado
- Nenhuma biblioteca externa necessária (usa apenas bibliotecas padrão)

### Passos

```bash
# 1. Clone ou baixe o projeto
git clone https://github.com/seu-usuario/CanaGuard-AI.git

# 2. Entre na pasta do projeto
cd CanaGuard-AI

# 3. Execute o sistema
python sistema_principal.py
```

> 💡 **Dica:** No Windows, pode ser necessário usar `python3` ao invés de `python`.

---


## 💡 Como usar (passo a passo sugerido)

1. Execute o sistema e veja a tela de boas-vindas
2. Acesse **"1. Gerenciar Áreas"** e cadastre sua primeira área
3. Registre os dados do **solo** (opção 2)
4. Registre os **insumos** usados (opção 3) — pode adicionar vários
5. Informe as **condições climáticas** (opção 4)
6. Avalie o **risco de incêndio** (opção 5)
7. Registre a **produção colhida** (opção 6)
8. Acesse a **análise financeira** (opção 7) para ver lucro e margem
9. Rode a **análise de risco** (opção 8) para ver alertas e recomendações
10. Gere o **relatório** completo (opção 9)

---

## 🐍 Conteúdos de Python aplicados

### Subalgoritmos (funções)
Cada funcionalidade está organizada em funções com parâmetros e retorno bem definidos. Exemplo:
```python
def calcular_financeiro(dados):
    # recebe o dicionário de dados e calcula receita, custo, lucro e margem
```

### Estruturas de dados
- **Dicionário**: cada área é um `dict` com todos os seus atributos
- **Lista**: `dados["areas"]` é uma lista de dicionários
- **Tupla**: usada internamente em opções de menu (imutável, ideal para constantes)

### Manipulação de arquivos
- **JSON** (`dados_canaguard.json`): persistência dos dados entre sessões
- **TXT** (`relatorios_gerados/`): relatório formatado exportável
- **SQL** (`dados_do_sistema/`): comandos Oracle gerados para banco

### Banco de dados (simulação Oracle)
Geração de comandos DDL e DML (CREATE TABLE + INSERT INTO) compatíveis com Oracle, com uso correto de tipos de dados como `VARCHAR2`, `NUMBER` e `TO_DATE`.

---

## 📊 Lógica de análise de risco

O sistema atribui pontos de risco com base em cada fator:

| Fator | Condição | Pontos |
|-------|----------|--------|
| Solo | Umidade < 30% | +2 |
| Solo | Umidade > 80% | +1 |
| Solo | Nutrientes ruins | +2 |
| Clima | Seco/Quente ou Tempestade | +2 |
| Incêndio | Nível Crítico | +4 |
| Incêndio | Foco próximo | +3 |
| Produção | Abaixo de 60 t/ha | +2 |

**Classificação:**
- 0 pontos → 🟢 Risco Baixo  
- 1–3 pontos → 🟡 Risco Médio  
- 4–6 pontos → 🟠 Risco Alto  
- 7+ pontos → 🔴 Risco Crítico  

---

## 📝 Observações de desenvolvimento

- O sistema foi desenvolvido sem uso de bibliotecas externas para manter a simplicidade e facilitar a execução em qualquer computador
- Os dados são salvos automaticamente após cada operação
- A interface foi projetada com foco na experiência do usuário: exemplos reais, mensagens de alerta e orientações em cada etapa
- A análise de risco e as recomendações são geradas dinamicamente com base nos dados cadastrados, sem valores fixos

---


## 🗃 Histórico de lançamentos

* 0.1.0 - 21/04/2024
    *Lancamento do APP 

## 📋 Licença

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/agodoi/template">MODELO GIT FIAP</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">Fiap</a> está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>

