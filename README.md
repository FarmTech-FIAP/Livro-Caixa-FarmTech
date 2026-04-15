# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href= "https://www.fiap.com.br/"><img src="assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Admnistração Paulista" border="0" width=40% height=40%></a>
</p>

<br>

# Livro Caixa FarmTech

## Grupo FarmTech Solutions

## 👨‍🎓 Integrantes: 
- Arthur Prudêncio Soares — RM569295
- Caroline Coelho Mendes — RM570370
- Leandro Paiva — RM572159
- Lucas Viana de Lima — RM571835
- Matheus Tavares Lima — RM572808

## 👩‍🏫 Professores:
### Tutor(a) 
- <a href="https://www.linkedin.com/company/inova-fusca">Nome do Tutor</a>
### Coordenador(a)
- <a href="https://www.linkedin.com/company/inova-fusca">Nome do Coordenador</a>


## 📜 Descrição

O **Livro Caixa FarmTech** é um sistema de controle financeiro voltado para o agronegócio, desenvolvido para auxiliar produtores rurais na gestão do fluxo de caixa de suas culturas agrícolas.

### O problema

O produtor rural brasileiro enfrenta um grande desafio na gestão financeira de suas atividades. Com múltiplas culturas sendo cultivadas simultaneamente, acompanhar receitas e despesas de cada uma delas de forma organizada é uma tarefa complexa. A falta de controle financeiro pode levar o agricultor a operar no prejuízo sem perceber, comprometendo a sustentabilidade do negócio. Esse problema se agrava especialmente na agricultura familiar, que é a principal fonte de alimentos e renda para grande parte da população rural brasileira.

### A solução

O Livro Caixa FarmTech oferece um sistema completo de controle financeiro por cultura agrícola, permitindo ao produtor:

- **Cadastrar culturas**: registrar as culturas cultivadas na propriedade (milho, soja, café, etc.), com sugestões de culturas comuns para facilitar o cadastro.
- **Registrar lançamentos**: controlar receitas (vendas de produção, subvenções governamentais) e despesas (sementes, fertilizantes, defensivos, mão de obra, combustível, manutenção, frete) de cada cultura individualmente, com categorias pré-definidas.
- **Visualizar balanço financeiro**: consultar o resultado financeiro de cada cultura e o consolidado geral da propriedade, com indicadores visuais de lucro (+) e prejuízo (-).
- **Alertas de prejuízo**: o sistema monitora automaticamente as culturas e emite alertas quando alguma está operando em prejuízo, informando o valor do prejuízo e o percentual em que a despesa supera a receita. Os alertas são exibidos na inicialização do sistema, no balanço geral e imediatamente após o registro de um lançamento.
- **Exportar relatórios**: gerar relatórios financeiros em formato texto (TXT), com o balanço completo de todas as culturas.
- **Sincronização com banco de dados Oracle**: enviar e carregar dados do banco de dados Oracle da FIAP, garantindo persistência e possibilidade de acesso remoto.

### Inovação

O diferencial do sistema está no **alerta inteligente de prejuízo**, que funciona como um sistema de monitoramento financeiro em tempo real. A cada operação, o produtor é informado proativamente se alguma cultura está operando no vermelho, permitindo a tomada de decisão rápida — seja renegociando custos, ajustando a produção ou realocando recursos entre culturas. Essa abordagem transforma o sistema de um simples registro contábil em uma ferramenta de apoio à decisão.

### Conteúdos técnicos aplicados

O projeto aplica os conteúdos dos capítulos 3 a 6 de Python:

- **Subalgoritmos**: funções com retorno (`criar_lancamento`, `calcular_totais_cultura`, `carregar_json`) e procedimentos (`cadastrar_cultura`, `registrar_lancamento`, `exibir_balanco`), todos com passagem de parâmetros.
- **Estruturas de dados**: listas (lançamentos de cada cultura), tuplas (culturas padrão, categorias, retorno de totais), dicionários (estrutura de cultura, lançamento, totais gerais) e tabela de memória (balanço consolidado como lista de tuplas).
- **Manipulação de arquivos**: leitura e escrita em JSON (persistência dos dados) e em texto (exportação de relatórios).
- **Conexão com banco de dados Oracle**: criação de tabelas, inserção, consulta e sincronização bidirecional de dados com o Oracle, utilizando o driver `oracledb`.


## 📁 Estrutura de pastas

Dentre os arquivos e pastas presentes na raiz do projeto, definem-se:

- <b>.github</b>: Nesta pasta ficarão os arquivos de configuração específicos do GitHub que ajudam a gerenciar e automatizar processos no repositório.

- <b>assets</b>: aqui estão os arquivos relacionados a elementos não-estruturados deste repositório, como imagens.

- <b>config</b>: Posicione aqui arquivos de configuração que são usados para definir parâmetros e ajustes do projeto.

- <b>document</b>: aqui estão todos os documentos do projeto que as atividades poderão pedir. Na subpasta "other", adicione documentos complementares e menos importantes.

- <b>scripts</b>: Posicione aqui scripts auxiliares para tarefas específicas do seu projeto. Exemplo: deploy, migrações de banco de dados, backups.

- <b>src</b>: Todo o código fonte criado para o desenvolvimento do projeto ao longo das 7 fases.

- <b>README.md</b>: arquivo que serve como guia e explicação geral sobre o projeto (o mesmo que você está lendo agora).

## 🔧 Como executar o código

### Pré-requisitos

- Python 3.8 ou superior
- Acesso ao banco de dados Oracle da FIAP (opcional, para sincronização)

### Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/Livro-Caixa-FarmTech.git
cd Livro-Caixa-FarmTech
```

2. Crie e ative o ambiente virtual:
```bash
python -m venv .venv
source .venv/bin/activate        # Linux/Mac
.venv\Scripts\activate           # Windows
```

3. Instale as dependências:
```bash
pip install -r config/requirements.txt
```

4. (Opcional) Configure o banco de dados Oracle editando o arquivo `config/.env`:
```env
DB_USER="seu_rm"
DB_PASSWORD="sua_senha"
DB_DSN=oracle.fiap.com.br:1521/ORCL
```

### Execução

```bash
cd src
python fluxo_caixa.py
```

O sistema abrirá o menu principal no terminal com as opções de cadastro, lançamentos, balanço, relatórios e sincronização com Oracle.

## 🗃 Histórico de lançamentos

* 1.0.0 - 14/04/2026
    * Sistema completo: cadastro de culturas, lançamentos financeiros, balanço, alertas de prejuízo, exportação TXT, integração Oracle

## 📋 Licença

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/agodoi/template">MODELO GIT FIAP</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">Fiap</a> está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>


