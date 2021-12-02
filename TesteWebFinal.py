'''
Teste Web Insights
Você é responsável por desenvolver um robô de captação (Crawler) em Python (com
simulação de navegador - selenium).
O robô deve receber um parâmetro “region” e pegar todos os nomes (name), símbolos
(symbol) e preços (price (intraday)) do site https://finance.yahoo.com/screener/new.
Por fim, deve salvar o resultado em um arquivo csv
'''
# Seção de Import
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from time import sleep

class Robo():
    
    def __init__(self, caminho_driver):
        '''
        Ao instanciar a classe o constructor cria um robô utilizando o navegador Chrome.
        Utiliza o driver especificado no parâmetro (caminho_driver)
        É necessário possuir o driver 'chromedriver' que suporte a versão do navegador a ser utilizado
        '''
        # Opções extras para Selenium
        self.options = Options()
        # Abre o navegador com a medida definida
        self.options.add_argument('window-size=800,600') #1366,768
        # Lista que armazenará os dados coletados
        self.dados = []
        # Oculta o navegador (não foi utilizado)
        # self.options.add_argument('--headless')
        # Utiliza o driver especificado no parâmetro (caminho_driver) utilizando a opção de tamanho de janela
        self.navegador = webdriver.Chrome(caminho_driver, options = self.options)
    
    def navegar(self, url):
        '''
        Método responsável por fazer a navegação na página escolhida (url)
        '''
        try:
            # Busca o site conforme parâmetro especificado
            self.navegador.get(url)
            # Espera para carregamento de página
            sleep(10)
            # Limpa a seleção do país padrão (USA)
            self.navegador.find_element_by_xpath('//*[@id="screener-criteria"]/div[2]/div[1]/div[1]/div[1]/div/div[2]/ul/li[1]/button').click()
            # Habilita a seleção dos países desejados
            self.navegador.find_element_by_xpath('//*[@id="screener-criteria"]/div[2]/div[1]/div[1]/div[1]/div/div[2]/ul').click()
            # paises = ('Austria', 'Argentina', Australia', 'Belgium', 'Brazil', 'Canada', 'Switzerland', 'Chile', 'China', 'Czech Republic', 'Germany', 'Denmark', 'Estonia', 'Egypt', 'Spain', 'Finland', 'France', 'United Kingdom', 'Greece', 'Hong Kong', 'Hungary', 'Indonesia', 'Ireland', 'Israel, 'India', 'Iceland', 'Japan', 'South Korea', 'Kuwait', 'Sri Lanka', 'Lithuania', 'Latvia', 'Mexico', 'Malaysia', 'Netherlands', 'Norway', 'New Zealand', 'Peru', 'Philippines', 'Pakistan', 'Poland', 'Portugal', 'Qatar','Russia', 'Saudi Arabia', 'Sweden', 'Singapore', 'Suriname', 'Thailand', 'Turkey', 'Taiwan', 'United States', 'Venezuela', 'Vietnam', 'South Africa')
            # Tupla contendo os check-boxes dos países que serão selecionados
            # Austria, Argentina e Austrália
            checks = ('//*[@id="dropdown-menu"]/div/div[2]/ul/li[2]/label/input',
            '//*[@id="dropdown-menu"]/div/div[2]/ul/li[1]/label/input',
            '//*[@id="dropdown-menu"]/div/div[2]/ul/li[3]/label/input')
            # Controlador para utilização da tupla e utilizar multi seleção de region
            # controle = True
            # if controle == True:
            #     # Laço de repetição para a seleção dos países desejados (region)
            #     for cont in range(len(checks)):
            #         # Tupla servindo como parâmetro de seleção
            #         self.navegador.find_element_by_xpath(checks[cont]).click()
            # else:
            # Linha de teste utilizando a tupla acima, podemos alterar a region
            self.navegador.find_element_by_xpath(checks[0]).click()
            # Mapeia o botão de resultados
            elemento = self.navegador.find_element_by_xpath('//*[@id="screener-criteria"]/div[2]/div[1]/div[3]/button[1]')
            # Espera para carregamento de página
            sleep(10)
            # Clique no botão de resultados
            elemento.click()
            # Controlador do fluxo
            flag = 0
            # Faz uma varredura dos dados em 10 páginas
            while flag < 11:
                self.__ler_pagina_dados()
                botao_proximo = self.navegador.find_element_by_xpath('//*[@id="scr-res-table"]/div[2]/button[3]/span/span')
                # Clica no botão para próxima página de dados
                botao_proximo.click()
                # Espera para carregamento de página
                sleep(10)
                # Controlador do fluxo
                flag += 1

            # Apagar - linha teste de impressão
            print(self.dados,len(self.dados),sep='\n')
            self.__exportar_csv('yahoo')
        # Caso aconteça algum problema, o programa desliga o robô e apresenta uma mensagem de Erro!
        except:
            self.desligar_robo()
            print('Erro!')
    
    def __exportar_csv(self, nome_arquivo):
        '''
        Método que exporta os dados para CSV
        '''
        # Cria um arquivo (sobreescreve)
        with open(nome_arquivo +'.csv', 'w') as file_object:
            # Percorre a lista de dados coletados e escreve no arquivo csv
            for i in range (len(self.dados)):
                # Adiciona <enter> para deixar cada registro em linhas separadas
                file_object.write(self.dados[i] + '\n')
        print('Arquivo criado com sucesso!')

    def __ler_pagina_dados(self):
        '''
        Método que faz a coleta dos dados na página
        '''
        # Espera para carregamento de página
        sleep(10)
        # Requisita o código fonte da página HTML
        conteudo = self.navegador.page_source
        # Utiliza a bs4 para leitura do conteúdo HTML
        url = BeautifulSoup(conteudo,'html.parser')
        # Busca os dados da tabela que será utilizada
        dados_tabela = url.find('div',{'id':'fin-scr-res-table'})
        # Busca o corpo da tabela
        get_corpo_tabela = dados_tabela.tbody
        # Busca todas as linhas da tabela
        linhas = get_corpo_tabela.find_all('tr')
        # Percorrer toda as linhas da tabela lida
        for linha in linhas:
            # Busca toda a linha do corpo da tabela
            colunas = linha.find_all('td')
            # elemento - símbolo(symbol)
            simbolo = colunas[0].get_text()
            # elemento - nome (name)
            nome = colunas[1].get_text()
            # elemento - preço (price (intraday))
            preco = colunas[2].get_text()
            # Adiciona em uma lista cada linha coletada
            self.dados.append(str(simbolo +';'+ nome +';'+ preco))

    def desligar_robo(self):
        '''
        Método para desligar o robô
        '''
        self.navegador.close()

# Início do robô
print('Crawler em execução','...'*20)
# Instancia um objeto da classe Robo
robo = Robo('C:\\datascience\\chromedriver.exe')
# Executa o método de captação de dados
robo.navegar('https://finance.yahoo.com/screener/new')