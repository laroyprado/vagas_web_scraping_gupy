import requests
from bs4 import BeautifulSoup
import pandas as pd

encontre_vaga = input("Qual área deseja?")
titulo_pesquisa = encontre_vaga.replace(" ","%20")
url = f"https://portal.api.gupy.io/api/v1/jobs/companies?jobName={titulo_pesquisa}&limit=1000"

response = requests.get(url)
data = response.json()

job_list = data["data"]
career_page_urls = []

contador_empresas = 0




for item in job_list:

    empresa_site = item["careerPageUrl"].split('/')

    if len(empresa_site) >= 3:
        base_url = '/'.join(empresa_site[:3])
        career_page_urls.append(base_url)


lista_vagas= []

for empresa in career_page_urls:
    response = requests.get(empresa)



    content = response.content
    site = BeautifulSoup(content, "html.parser")
    titulo_pagina = site.title.text

    vagas = site.findAll("li", attrs={"class": "sc-cc6aad61-3 iBlSMP"})

    for vaga in vagas:

        corpo_da_vaga = vaga.find("div", attrs={"class": "sc-cc6aad61-4 fFfOku"})
        link_tag = vaga.find("a", attrs={"data-testid": "job-list__listitem-href"})
        corpo_titulo_vaga = corpo_da_vaga.find("div", attrs={"class": "sc-cc6aad61-5 PaHqX"})

        if corpo_titulo_vaga:
            contador_empresas += 1
            nome_vaga = corpo_titulo_vaga.text
            lista_vagas.append([nome_vaga,titulo_pagina])





todas_as_vagas = pd.DataFrame(lista_vagas,columns=["Título","Empresa"])


empresas_registradas = pd.read_excel("vagas.xlsx")
todas_as_vagas = pd.concat([empresas_registradas, todas_as_vagas])

todas_as_vagas.to_excel("vagas.xlsx",index=False)


print(" Foram contabilizado" ,contador_empresas,"Empresas")
