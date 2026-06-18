# Navega Aí | RAG de termos burocráticos da UFRN
Este projeto tem como objetivo criar um RAG (Retrieval-Augmented Generation) para termos burocráticos da Universidade Federal do Rio Grande do Norte (UFRN). O projeto foi construido em python e utiliza a biblioteca LangChain para a implementação do RAG.

## Estrutura do Projeto
- `config/`: Contém o arquivo de configuração do projeto.
- `data/`: Contém os dados brutos e processados.
- `rag/`: Contém o código para o RAG.
- `ui/`: Contém o código para a interface do usuário.

## Como usar
1. Clone o repositório:
   ```bash
   git clone https://www.github.com/felipe-sbm/navega-ai-ufrn.git

   cd navega-ai-ufrn
   ```

2. Instale as dependências:
   ```bash
    python3 -m venv venv

    source venv/bin/activate  # no Windows use o `venv\Scripts\activate`

    pip install -r requirements.txt
   ```

3. Execute o script principal:
   ```bash
   streamlit run main.py
   ```

## Dados
Todos os dados foram coletados a partir de documentos oficiais da UFRN, como regulamentos, manuais e portarias. Os dados foram processados e organizados para facilitar a consulta.

Os dados burocraticos são relacionados a alunos de nível técnico e pós-graduação, já que não são tão comuns de se encontrar na internet. Como o suporte da UFRN demora, eu decidi fazer isso como projeto sugerido pelo professor [Jean Mário Moreira de Lima (@jeanmmlima)](https://github.com/jeanmmlima)

## A equipe
- [Felipe SBM](https://github.com/felipe-sbm)
- [Felipe de Medeiros](https://github.com/felipepotigol)
