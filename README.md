<h1 align="center">
    Vagas Gupy com web scraping
</h1>


## 💻 About

Esté repositório tem como finalidade de raspagem de dados de vagas de emprego no site da [Gupy.io](https://portal.gupy.io/) . Ao digitar o termo que deseja, a aplicação irá buscar
por vagas naquela área. Em um segundo momento a aplicação irá registrar todas as vagas de cada empresa cujo termo foi estabelecido
e cada vaga que houver, será registrado em um arquivo excel. 
No arquivo Excel, terá as colunas de : Título,Empresa,Localização,Link da Vaga e Descrição da Vaga

### Pré-requisitos

Antes de baixar o projeto você vai precisar ter instalado na sua máquina as seguintes ferramentas:

-Git
-Python
-Pycharm
-Excel


### 🎲 Rodando a aplicação


```bash
# Clone o repositorio

$ git clone https://github.com/laroyprado/vagas_web_scraping_gupy

# Instale as bibliotecas

$ pip install requests
$ pip install beautifulsoup4
$ pip install pandas
$ pip install openpyxl

Abra a pasta vagas_web_scraping_gupy m seu Pycharm
Execute o arquivo main.py 
```
