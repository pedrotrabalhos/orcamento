# Trabalho de OOP

Essa é uma aplicação para orçamentos que permite o usuário gerar um relatório ao responder perguntas relacionadas à customização da moradia sendo negociada.

## Como usar a ferramenta

O arquivo "requirements.txt" define as dependências do projeto, que podem ser instaladas com o seguinte comando

```bash
pip install -r requirements.txt
```

Agora a ferramente deve rodar usando

```bash
python app.py
```

Para plataformas Linux ou MacOS:

```bash
python3 app.py
```

## Tecnologias e arquitetura

O projeto foi desenvolvido usando conceitos de POO e a arquitetura está divida nas seguintes camadas

**Domínio**

As regras de negócio foram implementadas na camada de domínio, que desconhece as camadas superiores, o que possibilita vários front-ends ou clientes para essa aplicação

**Apresentação**

Por simplicidade, o front-end desenvolvido foi para a linha de comando, usando as bibliotecas Questionary e Rich para melhor experiência no terminal
