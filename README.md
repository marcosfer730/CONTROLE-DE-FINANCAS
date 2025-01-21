# Gerenciador de Finanças Pessoais

Este repositório contém dois projetos para gerenciamento de finanças pessoais utilizando interfaces em Tkinter (Python Desktop) e Streamlit (Web).

## Funcionalidades

### Aplicativo Tkinter (`apptkinter.py`)
- Adicionar transações financeiras (Receitas e Despesas).
- Visualização de resumo financeiro (total de receitas, despesas e saldo).
- Exportação dos dados para CSV.
- Geração de gráficos de despesas por categoria.

### Aplicativo Streamlit (`streamlit.py`)
- Interface intuitiva para gestão financeira via web.
- Adicionar transações financeiras com categorias predefinidas.
- Controle de despesas fixas.
- Upload e download de arquivos CSV, Excel e JSON.
- Gráficos interativos para análise financeira.
- Evolução do saldo ao longo do tempo.
- Persistência de dados via JSON.

## Requisitos

Certifique-se de ter as seguintes dependências instaladas:

```bash
pip install pandas matplotlib streamlit plotly xlsxwriter
```

## Como Executar

### Aplicativo Tkinter

1. Execute o seguinte comando:
   ```bash
   python apptkinter.py
   ```
2. A interface desktop será aberta.

### Aplicativo Streamlit

1. Execute o seguinte comando:
   ```bash
   streamlit run streamlit.py
   ```
2. Abra o navegador e acesse `http://localhost:8501`.

## Estrutura do Repositório

```
/
├── apptkinter.py      # Aplicativo desktop em Tkinter
├── streamlit.py       # Aplicativo web em Streamlit
├── README.md          # Documentação do projeto
```

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).

Se tiver dúvidas ou problemas, sinta-se à vontade para abrir uma issue no repositório.
