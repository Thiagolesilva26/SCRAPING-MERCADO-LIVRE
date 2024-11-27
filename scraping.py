from bs4 import BeautifulSoup  # Importa a biblioteca BeautifulSoup para fazer parsing de HTML.
import requests  # Importa a biblioteca requests para realizar requisições HTTP.
import urllib.parse  # Importa a biblioteca urllib.parse para manipulação de URLs.
import google.generativeai as genai  # Importa a biblioteca para usar o Google Generative AI.
import os  # Importa a biblioteca os para manipulação de variáveis de ambiente e operações de sistema.
import pandas as pd  # Importa a biblioteca pandas para trabalhar com DataFrames.
from dotenv import load_dotenv  # Importa a função load_dotenv para carregar variáveis de ambiente de um arquivo .env.

# Carrega variáveis de ambiente de um arquivo .env
load_dotenv()
api_key = os.getenv('API_KEY')  # Obtém a chave da API do Google AI a partir das variáveis de ambiente.

def scrape_mercadolivre(produto, nome):
    """
    Função para fazer scraping no Mercado Livre e obter dados de produtos relacionados ao termo de pesquisa.
    
    Parâmetros:
    - produto (str): Nome do produto que será pesquisado.
    - nome (str): Nome que será utilizado para salvar os arquivos gerados (txt e csv).
    """
    produto_split = produto.split()  # Divide o nome do produto em palavras.
    produto_join = "-".join(produto_split)  # Junta as palavras com hífens para formar a URL.
    produto_urllib = urllib.parse.quote(produto)  # Codifica o nome do produto para a URL.
    url = f"https://lista.mercadolivre.com.br/{produto_join}#D[A:{produto_urllib}]"
    
    try:
        os.system("cls")  # Limpa o terminal.
        response = requests.get(url)  # Realiza a requisição HTTP para a URL do Mercado Livre.
        soup = BeautifulSoup(response.text, 'html.parser')  # Faz o parsing do HTML da página.
        products = soup.find_all('li', {'class': 'ui-search-layout__item'})  # Encontra todos os produtos na página.
        
        # Listas para armazenar os dados dos produtos
        names = []
        prices = []
        reviews = []
        vendors = []
        sales = []
        esta_no_full = []
        url_lista = []

        for product in products:
            # Extração das informações de cada produto
            name_tag = product.find('h2', {'class': 'poly-box poly-component__title'})
            price_tag = product.find('span', {'class': 'andes-money-amount__fraction'})
            review_tag = product.find('span', {'class': 'poly-reviews__total'}) 
            link_produto_classe = product.find('h2', {'class': 'poly-box poly-component__title'})
            full_tag = product.find('span', {'class': 'poly-component__shipped-from'})

            # Verificando se o link do produto foi encontrado
            if link_produto_classe:
                a_anuncios = link_produto_classe.find('a')
                if a_anuncios and a_anuncios.get('href'):
                    url_anuncios = a_anuncios.get('href')

                    # Fazendo a requisição para a página do produto
                    response_link = requests.get(url_anuncios)
                    soup_link = BeautifulSoup(response_link.text, 'html.parser')

                    vendedor_tag = soup_link.find('div', {'class': 'ui-pdp-seller__header__info-container__title'})
                    vendas_tag = soup_link.find('span', {'class': 'ui-pdp-subtitle'})

                    # Garantindo que as informações de cada produto sejam extraídas corretamente
                    name = name_tag.text.strip() if name_tag else 'N/A'
                    price = price_tag.text.strip() if price_tag else 0
                    review = review_tag.text.strip() if review_tag else 0
                    vendedor = vendedor_tag.text.strip() if vendedor_tag else 'N/A'
                    vendas = vendas_tag.text.strip() if vendas_tag else 'N/A'
                    full = full_tag.text.strip() if full_tag else 0
                    url = url_anuncios if url_anuncios else 'N/A'

                    # Armazenando os dados nas listas
                    names.append(name)
                    prices.append(price)
                    reviews.append(review)
                    vendors.append(vendedor)
                    sales.append(vendas)
                    esta_no_full.append(full)
                    url_lista.append(url)
                else:
                    print(f"Link não encontrado para o produto: {product}")
            else:
                print(f"Bloco do produto não encontrado: {product}")

        # Criando um DataFrame com as informações extraídas
        df = pd.DataFrame({
            'Nome do Produto': names,
            'Preço': prices,
            'Reviews': reviews,
            'Vendedor': vendors,
            'Vendas': sales,
            'Full': esta_no_full,
            'Url': url_lista
        })

        # Salvando os dados extraídos em um arquivo TXT
        with open(f'{nome}.txt', 'w', encoding='utf-8') as file:
            file.write("Dados dos Produtos:\n\n")
            for i in range(len(names)):
                file.write(f"Produto: {names[i]}\n")
                file.write(f"Preço: {prices[i]}\n")
                file.write(f"Review: {reviews[i]}\n")
                file.write(f"Vendedor: {vendors[i]}\n")
                file.write(f"Vendas: {sales[i]}\n")
                file.write(f"Full: {esta_no_full[i]}\n")
                file.write(f"Url: {url_lista[i]}\n")
                file.write("-" * 40 + "\n")

        # Lendo o conteúdo do arquivo TXT para gerar a análise
        with open(f'{nome}.txt', 'r', encoding='utf-8') as file:
            conteudo = file.read()

        # Gerando a análise dos dados utilizando o modelo de IA
        modelo = """## Análise Completa dos Produtos**Informações:*** **Quantidade de produtos analisados:** 45* ..."""
        gerar(conteudo, f"Com as informações que te passei preciso que você me faça uma analise completa com os seguintes requerimentos...", nome)

        # Salvando os dados em um arquivo CSV
        df.to_csv(f'{nome}.csv', index=False)

    except Exception as e:
        print(f'Erro: {e}')

def gerar(texto, prompt, nome):
    """
    Função para gerar conteúdo a partir dos dados extraídos usando o modelo de IA.
    
    Parâmetros:
    - texto (str): O texto que será processado.
    - prompt (str): O modelo de prompt que será fornecido ao modelo de IA.
    - nome (str): Nome do arquivo de saída.
    """
    data = texto
    
    # Configura a chave da API para utilizar o Google Generative AI
    genai.configure(api_key=api_key)  

    if data is not None:
        try:
            # Configuração do modelo de IA para gerar o conteúdo
            model = genai.GenerativeModel('gemini-1.5-flash', generation_config=genai.GenerationConfig(
                candidate_count=1,
                max_output_tokens=1000,
                temperature=0.9,
                top_p=0.95,
                top_k=40
            ))

            # Gerando o conteúdo a partir do modelo
            result = model.generate_content(f'{prompt}{data}')
            
            # Salvando o conteúdo gerado em um arquivo
            with open(f'{nome}.txt', 'w', encoding='utf-8') as f:
                f.write(f"{result.text}")
                        
            return result.text            

        except Exception as e:
            print(f"Erro: {e}")     

# Exemplo de uso:
nome_arquivo = input('Digite o nome do arquivo: ')  # Recebe o nome do arquivo de saída
produto_pesquisa = input('Digite o nome do produto que deseja pesquisar: ')  # Recebe o nome do produto para pesquisa
scrape_mercadolivre(produto_pesquisa, nome_arquivo)  # Chama a função de scraping passando os parâmetros
