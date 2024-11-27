
# Programa de Scraping no Mercado Livre

Este projeto é um script Python para realizar scraping de informações de produtos no Mercado Livre, incluindo nome, preço, avaliações, vendedor, vendas, entre outros dados. Ele também permite gerar uma análise detalhada desses dados utilizando a API Google Generative AI.

## Funcionalidades

- Coleta dados de produtos do Mercado Livre, incluindo:
  - Nome
  - Preço
  - Avaliações
  - Vendedor
  - Quantidade de vendas
  - Informações sobre o programa Full
  - URL do produto
- Geração de análises detalhadas com base nos dados coletados.
- Salvamento dos resultados em arquivos `.txt` e `.csv` para fácil leitura e manipulação.

---

## Pré-requisitos

1. **Python 3.8 ou superior**
2. As seguintes bibliotecas Python devem estar instaladas:
   - `beautifulsoup4`
   - `requests`
   - `pandas`
   - `google.generativeai`

   Para instalar as dependências, execute:
   ```bash
   pip install beautifulsoup4 requests pandas google-generativeai
   ```

3. **Chave de API do Google Generative AI**
   - Configure sua chave na função `genai.configure(api_key='SUA_CHAVE_DE_API')`.

---

## Uso

1. Clone este repositório:
   ```bash
   git clone https://github.com/SeuUsuario/SeuRepositorio.git
   ```

2. Navegue até o diretório do projeto:
   ```bash
   cd SeuRepositorio
   ```

3. Execute o script:
   ```bash
   python scraping.py
   ```

4. Insira as informações solicitadas:
   - Nome do arquivo para salvar os dados.
   - Nome do produto a ser pesquisado no Mercado Livre.

5. Após a execução, os dados coletados serão salvos em dois arquivos:
   - `nome_do_arquivo.txt` - Contém os dados detalhados de cada produto.
   - `nome_do_arquivo.csv` - Contém os dados estruturados em formato tabular.

---

## Estrutura do Projeto

- `scraping.py`: Script principal que realiza o scraping e análise.
- Arquivos de saída:
  - `dados.txt`: Contém os detalhes completos dos produtos.
  - `dados.csv`: Dados organizados para análise em planilhas.

---

## Observações

- Certifique-se de que sua chave de API do Google Generative AI está configurada corretamente.
- A função `scrape_mercadolivre` coleta dados da página inicial de resultados da pesquisa no Mercado Livre e pode não captar todos os produtos em páginas subsequentes.
- O script elimina produtos que não pertencem ao nicho pesquisado, garantindo uma análise mais precisa.

---

## Melhorias Futuras

- Adicionar suporte para múltiplas páginas de resultados.
- Implementar tratamento de erros mais robusto para lidar com mudanças na estrutura do HTML do Mercado Livre.
- Otimizar o tempo de resposta para grandes volumes de dados.

---

## Contribuição

Sinta-se à vontade para contribuir com este projeto! Faça um fork do repositório, crie uma branch para suas alterações e envie um pull request.

---

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).
```

Você pode personalizar este modelo com os detalhes específicos do seu projeto, como o nome do script, seu nome de usuário no GitHub, ou outros pontos relevantes. Se precisar de algo mais, é só pedir! 😊