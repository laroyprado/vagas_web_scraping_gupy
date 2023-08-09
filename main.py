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
print(f"Já catalogamos todas as empresas. Ao todo temos {len(career_page_urls)} empresas")
print("Agora vamos catalogar cada vaga das empresas listadas para você")

for empresa in career_page_urls:
    response = requests.get(empresa)



    content = response.content
    site = BeautifulSoup(content, "html.parser")
    titulo_pagina = site.title.text

    vagas = site.findAll("li", attrs={"class": "sc-cc6aad61-3 iBlSMP"})

    for vaga in vagas:

        corpo_da_vaga = vaga.find("div", attrs={"class": "sc-cc6aad61-4 fFfOku"})
        corpo_titulo_vaga = corpo_da_vaga.find("div", attrs={"class": "sc-cc6aad61-5 PaHqX"})

        link_tag = vaga.find("a", attrs={"data-testid": "job-list__listitem-href"})

        localizacao_tag = vaga.find("div", attrs={"class": "sc-cc6aad61-6 bhyeAN"})

        if corpo_titulo_vaga:
            contador_empresas += 1
            nome_vaga = corpo_titulo_vaga.text
            localizacao = localizacao_tag.text
            link_vaga = f'{empresa}{link_tag["href"]}'

            lista_vagas.append([nome_vaga,titulo_pagina,localizacao,link_vaga])





todas_as_vagas = pd.DataFrame(lista_vagas,columns=["Título","Empresa","Localização","Link Da Vaga"])


empresas_registradas = pd.read_excel("vagas.xlsx")
todas_as_vagas = pd.concat([empresas_registradas, todas_as_vagas])

print("Estamos adicionando as vagas ao seu arquivo vagas.xlsx")
todas_as_vagas.to_excel("vagas.xlsx",index=False)


print("Foram contabilizado" ,contador_empresas,"Empresas")
print("Todas elas já foram adicionadas ao seu arquivo vagas.xlsx")
