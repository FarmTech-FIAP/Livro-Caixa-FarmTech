import json
import os
from datetime import datetime
import oracledb

# =============================================================================
#  FLUXO DE CAIXA AGRÍCOLA - Controle Financeiro por Cultura FarmTech
# =============================================================================
#  Sistema de lançamentos financeiros (receitas e despesas) por cultura agrícola.
#  Permite cadastro de culturas, registro de lançamentos, visualização de balanço
# =============================================================================

ARQUIVO_JSON = "dados_culturas.json"
ARQUIVO_RELATORIO_TXT = "relatorio_financeiro.txt"

CULTURAS_PADRAO = ("Milho", "Soja", "Ervilha", "Café", "Algodão", "Trigo", "Arroz", "Feijão")
CATEGORIAS_DESPESA = (
    "Sementes", "Fertilizantes", "Defensivos", "Mão de obra",
    "Combustível", "Manutenção", "Frete", "Outros"
)

CATEGORIAS_RECEITA = (
    "Venda de produção", "Subvenção governamental", "Outros"
)

# Validacoes de entrada e funções de leitura do usuário para garantir dados corretos e usabilidade aprimorada.
def ler_opcao_menu(mensagem, minimo, maximo):
    """Lê uma opção numérica do usuário dentro de um intervalo válido."""
    while True:
        entrada = input(mensagem).strip()
        if not entrada:
            print("  ⚠ Entrada vazia. Tente novamente.")
            continue
        try:
            valor = int(entrada)
            if minimo <= valor <= maximo:
                return valor
            print(f"  ⚠ Digite um número entre {minimo} e {maximo}.")
        except ValueError:
            print("  ⚠ Entrada inválida. Digite apenas números.")


def ler_valor_monetario(mensagem):
    """Lê um valor monetário positivo do usuário."""
    while True:
        entrada = input(mensagem).strip().replace(",", ".")
        if not entrada:
            print("  ⚠ Entrada vazia. Tente novamente.")
            continue
        try:
            valor = float(entrada)
            if valor < 0:
                print("  ⚠ O valor não pode ser negativo.")
            elif valor == 0:
                print("  ⚠ O valor deve ser maior que zero.")
            else:
                return valor
        except ValueError:
            print("  ⚠ Entrada inválida. Use apenas números (ex: 1500.50).")


def ler_texto(mensagem, minimo=1, maximo=100):
    """Lê um texto não vazio do usuário com tamanho controlado."""
    while True:
        entrada = input(mensagem).strip()
        if len(entrada) < minimo:
            print(f"  ⚠ Digite pelo menos {minimo} caractere(s).")
        elif len(entrada) > maximo:
            print(f"  ⚠ Máximo de {maximo} caracteres.")
        else:
            return entrada


def confirmar(mensagem):
    """Pede confirmação S/N ao usuário."""
    while True:
        resp = input(f"{mensagem} (S/N): ").strip().upper()
        if resp in ("S", "N"):
            return resp == "S"
        print("  ⚠ Digite S ou N.")


#Estruturas de dados e funções para manipulação dos lançamentos financeiros e culturas agrícolas.
def criar_lancamento(tipo, categoria, descricao, valor):
    """Cria e retorna um dicionário representando um lançamento financeiro."""
    return {
        "tipo": tipo,
        "categoria": categoria,
        "descricao": descricao,
        "valor": valor,
        "data": datetime.now().strftime("%d/%m/%Y %H:%M")
    }


def criar_cultura(nome):
    """Cria e retorna um dicionário representando uma cultura agrícola."""
    return {
        "nome": nome,
        "lancamentos": []
    }


def calcular_totais_cultura(cultura):
    """Calcula receita, despesa e lucro de uma cultura. Retorna tupla."""
    receita = sum(l["valor"] for l in cultura["lancamentos"] if l["tipo"] == "Receita")
    despesa = sum(l["valor"] for l in cultura["lancamentos"] if l["tipo"] == "Despesa")
    lucro = receita - despesa
    return (receita, despesa, lucro)


def calcular_totais_gerais(dados):
    """Calcula os totais consolidados de todas as culturas. Retorna dicionário."""
    receita_total = 0.0
    despesa_total = 0.0
    for cultura in dados["culturas"]:
        r, d, _ = calcular_totais_cultura(cultura)
        receita_total += r
        despesa_total += d
    return {
        "receita": receita_total,
        "despesa": despesa_total,
        "lucro": receita_total - despesa_total
    }


def montar_tabela_balanco(dados):
    """Monta e retorna uma lista de tuplas com o balanço por cultura (tabela de memória)."""
    tabela = []
    for cultura in dados["culturas"]:
        r, d, l = calcular_totais_cultura(cultura)
        tabela.append((cultura["nome"], r, d, l))
    return tabela


# Manipular arquivos
def salvar_json(dados, caminho=ARQUIVO_JSON):
    """Salva os dados em arquivo JSON."""
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)


def carregar_json(caminho=ARQUIVO_JSON):
    """Carrega dados do arquivo JSON. Retorna estrutura padrão se não existir."""
    if os.path.exists(caminho):
        with open(caminho, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"culturas": []}


def exportar_relatorio_txt(dados, caminho=ARQUIVO_RELATORIO_TXT):
    """Exporta o balanço financeiro para um arquivo de texto formatado."""
    tabela = montar_tabela_balanco(dados)
    totais = calcular_totais_gerais(dados)
    largura = 72

    linhas = []
    linhas.append("=" * largura)
    linhas.append("  RELATÓRIO FINANCEIRO - FLUXO DE CAIXA AGRÍCOLA")
    linhas.append(f"  Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    linhas.append("=" * largura)
    linhas.append("")
    linhas.append(f"  {'Cultura':<15} {'Receita':>15} {'Despesa':>15} {'Lucro':>15}")
    linhas.append("  " + "-" * (largura - 4))

    for nome, receita, despesa, lucro in tabela:
        linhas.append(
            f"  {nome:<15} {formatar_moeda(receita):>15} "
            f"{formatar_moeda(despesa):>15} {formatar_moeda(lucro):>15}"
        )

    linhas.append("  " + "-" * (largura - 4))
    linhas.append(
        f"  {'TOTAL':<15} {formatar_moeda(totais['receita']):>15} "
        f"{formatar_moeda(totais['despesa']):>15} {formatar_moeda(totais['lucro']):>15}"
    )
    linhas.append("=" * largura)

    conteudo = "\n".join(linhas)

    with open(caminho, "w", encoding="utf-8") as f:
        f.write(conteudo)

    return conteudo


# Bd Oracle - funções para conectar, criar tabelas, sincronizar e carregar dados.
def conectar_oracle():
    """Tenta conectar ao banco Oracle. Retorna conexão ou None."""
    try:
        conn = oracledb.connect(
            user="SEU_RM",
            password="SUA_SENHA",
            dsn="oracle.fiap.com.br:1521/ORCL"
        )
        return conn
    except Exception as e:
        print(f"  ⚠ Erro ao conectar ao Oracle: {e}")
        return None


def criar_tabelas_oracle(conn):
    """Cria as tabelas no Oracle se não existirem."""
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*) FROM user_tables WHERE table_name = 'T_CULTURA'
    """)
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
            CREATE TABLE T_CULTURA (
                id_cultura  NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                nome        VARCHAR2(100) NOT NULL UNIQUE
            )
        """)

    cursor.execute("""
        SELECT COUNT(*) FROM user_tables WHERE table_name = 'T_LANCAMENTO'
    """)
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
            CREATE TABLE T_LANCAMENTO (
                id_lancamento  NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                id_cultura     NUMBER NOT NULL,
                tipo           VARCHAR2(20)  NOT NULL,
                categoria      VARCHAR2(50)  NOT NULL,
                descricao      VARCHAR2(200) NOT NULL,
                valor          NUMBER(15,2)  NOT NULL,
                data_registro  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                CONSTRAINT fk_cultura FOREIGN KEY (id_cultura)
                    REFERENCES T_CULTURA(id_cultura)
            )
        """)

    conn.commit()
    cursor.close()


def sincronizar_para_oracle(dados):
    """Envia todos os dados locais para o Oracle."""
    conn = conectar_oracle()
    if not conn:
        return False

    try:
        criar_tabelas_oracle(conn)
        cursor = conn.cursor()

        for cultura in dados["culturas"]:
            cursor.execute(
                "SELECT id_cultura FROM T_CULTURA WHERE nome = :1",
                [cultura["nome"]]
            )
            row = cursor.fetchone()
            if row:
                id_cultura = row[0]
            else:
                cursor.execute(
                    "INSERT INTO T_CULTURA (nome) VALUES (:1)",
                    [cultura["nome"]]
                )
                conn.commit()
                cursor.execute(
                    "SELECT id_cultura FROM T_CULTURA WHERE nome = :1",
                    [cultura["nome"]]
                )
                id_cultura = cursor.fetchone()[0]

            # Limpa lançamentos anteriores desta cultura para re-inserir
            cursor.execute(
                "DELETE FROM T_LANCAMENTO WHERE id_cultura = :1",
                [id_cultura]
            )

            for lanc in cultura["lancamentos"]:
                cursor.execute("""
                    INSERT INTO T_LANCAMENTO
                        (id_cultura, tipo, categoria, descricao, valor)
                    VALUES (:1, :2, :3, :4, :5)
                """, [id_cultura, lanc["tipo"], lanc["categoria"],
                      lanc["descricao"], lanc["valor"]])

        conn.commit()
        cursor.close()
        print("  ✔ Dados sincronizados com o Oracle com sucesso!")
        return True
    except Exception as e:
        print(f"  ⚠ Erro ao sincronizar: {e}")
        return False
    finally:
        conn.close()


def carregar_do_oracle():
    """Carrega todos os dados do Oracle e retorna estrutura local."""
    conn = conectar_oracle()
    if not conn:
        return None

    try:
        criar_tabelas_oracle(conn)
        cursor = conn.cursor()
        dados = {"culturas": []}

        cursor.execute("SELECT id_cultura, nome FROM T_CULTURA ORDER BY nome")
        culturas_db = cursor.fetchall()

        for id_cultura, nome in culturas_db:
            cultura = criar_cultura(nome)
            cursor.execute("""
                SELECT tipo, categoria, descricao, valor,
                       TO_CHAR(data_registro, 'DD/MM/YYYY HH24:MI')
                FROM T_LANCAMENTO
                WHERE id_cultura = :1
                ORDER BY data_registro
            """, [id_cultura])

            for tipo, cat, desc, val, data in cursor.fetchall():
                lanc = {
                    "tipo": tipo,
                    "categoria": cat,
                    "descricao": desc,
                    "valor": float(val),
                    "data": data
                }
                cultura["lancamentos"].append(lanc)

            dados["culturas"].append(cultura)

        cursor.close()
        print("  ✔ Dados carregados do Oracle com sucesso!")
        return dados
    except Exception as e:
        print(f"  ⚠ Erro ao carregar do Oracle: {e}")
        return None
    finally:
        conn.close()


def formatar_moeda(valor):
    """Formata valor como moeda brasileira."""
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def exibir_cabecalho(titulo):
    """Exibe cabeçalho padronizado no terminal."""
    largura = 56
    print()
    print("=" * largura)
    print(f"  {titulo}")
    print("=" * largura)


def exibir_balanco(dados):
    """Exibe o balanço financeiro formatado no terminal."""
    tabela = montar_tabela_balanco(dados)
    totais = calcular_totais_gerais(dados)

    exibir_cabecalho("BALANÇO FINANCEIRO POR CULTURA")
    print()

    if not tabela:
        print("  Nenhuma cultura cadastrada.")
        print()
        return

    print(f"  {'Cultura':<15} {'Receita':>15} {'Despesa':>15} {'Lucro':>15}")
    print("  " + "-" * 52)

    for nome, receita, despesa, lucro in tabela:
        indicador = "+" if lucro >= 0 else "-"
        print(
            f"  {nome:<15} {formatar_moeda(receita):>15} "
            f"{formatar_moeda(despesa):>15} {formatar_moeda(lucro):>15} {indicador}"
        )

    print("  " + "-" * 52)
    ind_total = "+" if totais["lucro"] >= 0 else "-"
    print(
        f"  {'TOTAL':<15} {formatar_moeda(totais['receita']):>15} "
        f"{formatar_moeda(totais['despesa']):>15} {formatar_moeda(totais['lucro']):>15} {ind_total}"
    )
    print()


def exibir_lancamentos_cultura(cultura):
    """Exibe os lançamentos detalhados de uma cultura."""
    exibir_cabecalho(f"LANÇAMENTOS - {cultura['nome'].upper()}")
    print()

    if not cultura["lancamentos"]:
        print("  Nenhum lançamento registrado.")
        print()
        return

    receitas = [l for l in cultura["lancamentos"] if l["tipo"] == "Receita"]
    despesas = [l for l in cultura["lancamentos"] if l["tipo"] == "Despesa"]

    if receitas:
        print("  RECEITAS:")
        for i, l in enumerate(receitas, 1):
            print(f"    {i}. [{l['categoria']}] {l['descricao']}")
            print(f"       Valor: {formatar_moeda(l['valor'])}  |  Data: {l['data']}")
        print()

    if despesas:
        print("  DESPESAS:")
        for i, l in enumerate(despesas, 1):
            print(f"    {i}. [{l['categoria']}] {l['descricao']}")
            print(f"       Valor: {formatar_moeda(l['valor'])}  |  Data: {l['data']}")
        print()

    r, d, lucro = calcular_totais_cultura(cultura)
    print(f"  Receita total: {formatar_moeda(r)}")
    print(f"  Despesa total: {formatar_moeda(d)}")
    print(f"  Resultado:     {formatar_moeda(lucro)} {'(lucro)' if lucro >= 0 else '(prejuízo)'}")
    print()


def selecionar_cultura(dados):
    """Exibe lista de culturas e retorna o índice da escolhida, ou -1."""
    if not dados["culturas"]:
        print("\n  Nenhuma cultura cadastrada. Cadastre uma primeiro.")
        return -1

    print("\n  Culturas cadastradas:")
    for i, c in enumerate(dados["culturas"], 1):
        r, d, l = calcular_totais_cultura(c)
        print(f"    {i}. {c['nome']:<15} (Lucro: {formatar_moeda(l)})")
    print(f"    0. Voltar")

    opcao = ler_opcao_menu("\n  Escolha a cultura: ", 0, len(dados["culturas"]))
    return opcao - 1


def selecionar_categoria(tipo):
    """Permite selecionar categoria de receita ou despesa."""
    categorias = CATEGORIAS_RECEITA if tipo == "Receita" else CATEGORIAS_DESPESA
    print(f"\n  Categorias de {tipo.lower()}:")
    for i, cat in enumerate(categorias, 1):
        print(f"    {i}. {cat}")

    opcao = ler_opcao_menu("  Escolha a categoria: ", 1, len(categorias))
    return categorias[opcao - 1]


def cadastrar_cultura(dados):
    """Procedimento para cadastrar uma nova cultura."""
    exibir_cabecalho("CADASTRAR NOVA CULTURA")

    print("\n  Culturas sugeridas:")
    disponiveis = [c for c in CULTURAS_PADRAO
                   if c not in [cu["nome"] for cu in dados["culturas"]]]
    if disponiveis:
        for i, c in enumerate(disponiveis, 1):
            print(f"    {i}. {c}")
        print(f"    0. Digitar manualmente")
        opcao = ler_opcao_menu("\n  Escolha: ", 0, len(disponiveis))

        if opcao == 0:
            nome = ler_texto("  Nome da cultura: ", 2, 50).title()
        else:
            nome = disponiveis[opcao - 1]
    else:
        nome = ler_texto("  Nome da cultura: ", 2, 50).title()

    # Verifica duplicidade
    for c in dados["culturas"]:
        if c["nome"].lower() == nome.lower():
            print(f"\n  ⚠ A cultura '{nome}' já está cadastrada.")
            return

    dados["culturas"].append(criar_cultura(nome))
    salvar_json(dados)
    print(f"\n  ✔ Cultura '{nome}' cadastrada com sucesso!")


def registrar_lancamento(dados):
    """Procedimento para registrar um lançamento financeiro."""
    exibir_cabecalho("REGISTRAR LANÇAMENTO")

    idx = selecionar_cultura(dados)
    if idx < 0:
        return

    cultura = dados["culturas"][idx]
    print(f"\n  Cultura selecionada: {cultura['nome']}")

    print("\n  Tipo de lançamento:")
    print("    1. Receita")
    print("    2. Despesa")
    tipo_opcao = ler_opcao_menu("  Escolha: ", 1, 2)
    tipo = "Receita" if tipo_opcao == 1 else "Despesa"

    categoria = selecionar_categoria(tipo)
    descricao = ler_texto(f"  Descrição do lançamento: ", 3, 200)
    valor = ler_valor_monetario(f"  Valor (R$): ")

    lancamento = criar_lancamento(tipo, categoria, descricao, valor)

    print(f"\n  Resumo: {tipo} | {categoria} | {formatar_moeda(valor)}")
    print(f"  Descrição: {descricao}")

    if confirmar("  Confirma o lançamento?"):
        cultura["lancamentos"].append(lancamento)
        salvar_json(dados)
        print(f"\n  ✔ Lançamento registrado com sucesso!")
    else:
        print("\n  Lançamento cancelado.")


def ver_lancamentos(dados):
    """Procedimento para visualizar lançamentos de uma cultura."""
    exibir_cabecalho("VER LANÇAMENTOS")
    idx = selecionar_cultura(dados)
    if idx >= 0:
        exibir_lancamentos_cultura(dados["culturas"][idx])


def remover_cultura(dados):
    """Procedimento para remover uma cultura e seus lançamentos."""
    exibir_cabecalho("REMOVER CULTURA")
    idx = selecionar_cultura(dados)
    if idx < 0:
        return

    cultura = dados["culturas"][idx]
    qtd = len(cultura["lancamentos"])
    print(f"\n  Cultura: {cultura['nome']} ({qtd} lançamento(s))")

    if confirmar("  Tem certeza que deseja remover?"):
        dados["culturas"].pop(idx)
        salvar_json(dados)
        print(f"\n  ✔ Cultura removida com sucesso!")
    else:
        print("\n  Operação cancelada.")


def menu_oracle(dados):
    """Submenu de operações com banco de dados Oracle."""
    exibir_cabecalho("BANCO DE DADOS ORACLE")
    print()
    print("    1. Enviar dados locais para o Oracle")
    print("    2. Carregar dados do Oracle")
    print("    0. Voltar")

    opcao = ler_opcao_menu("\n  Escolha: ", 0, 2)

    if opcao == 1:
        if confirmar("\n  Enviar todos os dados para o Oracle?"):
            sincronizar_para_oracle(dados)
    elif opcao == 2:
        if confirmar("\n  Substituir dados locais pelos do Oracle?"):
            dados_oracle = carregar_do_oracle()
            if dados_oracle is not None:
                dados.clear()
                dados.update(dados_oracle)
                salvar_json(dados)


def exportar_relatorio(dados):
    """Procedimento para exportar relatório TXT."""
    exibir_cabecalho("EXPORTAR RELATÓRIO")

    if not dados["culturas"]:
        print("\n  Nenhuma cultura cadastrada para gerar relatório.")
        return

    conteudo = exportar_relatorio_txt(dados)
    print()
    print(conteudo)
    print(f"\n  ✔ Relatório salvo em: {ARQUIVO_RELATORIO_TXT}")


# Menu 
def menu_principal():
    """Loop principal do sistema."""
    dados = carregar_json()

    exibir_cabecalho("FLUXO DE CAIXA AGRÍCOLA")
    print("  Sistema de controle financeiro por cultura")
    print()

    while True:
        print("=" * 56)
        print("  MENU PRINCIPAL")
        print("=" * 56)
        print("    1. Cadastrar cultura")
        print("    2. Registrar lançamento (receita/despesa)")
        print("    3. Ver lançamentos de uma cultura")
        print("    4. Balanço financeiro geral")
        print("    5. Remover cultura")
        print("    6. Exportar relatório (TXT)")
        print("    7. Banco de dados Oracle")
        print("    0. Sair")

        opcao = ler_opcao_menu("\n  Escolha uma opção: ", 0, 7)

        if opcao == 1:
            cadastrar_cultura(dados)
        elif opcao == 2:
            registrar_lancamento(dados)
        elif opcao == 3:
            ver_lancamentos(dados)
        elif opcao == 4:
            exibir_balanco(dados)
        elif opcao == 5:
            remover_cultura(dados)
        elif opcao == 6:
            exportar_relatorio(dados)
        elif opcao == 7:
            menu_oracle(dados)
        elif opcao == 0:
            print("\n  Até logo! Bons negócios no campo.\n")
            break


if __name__ == "__main__":
    menu_principal()