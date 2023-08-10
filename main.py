import requests
from bs4 import BeautifulSoup
import pandas as pd


def scraping_jobs(find_job, excel_file="jobs.xlsx"):
    title_search = find_job.replace(" ", "%20")
    url = f"https://portal.api.gupy.io/api/v1/jobs/companies?jobName={title_search}&limit=1000"

    response = requests.get(url)
    data = response.json()

    job_list = data["data"]
    career_page_urls = []

    def body_job(jobs, company):
        job_list = []
        for job in jobs:
            body_of_job = job.find("div", attrs={"class": "sc-cc6aad61-4 fFfOku"})
            body_title_job = body_of_job.find("div", attrs={"class": "sc-cc6aad61-5 PaHqX"})

            link_tag = job.find("a", attrs={"data-testid": "job-list__listitem-href"})
            location_tag = job.find("div", attrs={"class": "sc-cc6aad61-6 bhyeAN"})

            if body_title_job:
                job_name = body_title_job.text
                location = location_tag.text
                link_job = f'{company}{link_tag["href"]}'


                response = requests.get(link_job)
                content = response.content
                site = BeautifulSoup(content, "html.parser")

                description_div = site.find("div",
                                            attrs={"data-testid": "text-section", "class": "sc-2fba68cb-1 HAGHS"})
                paragraphs = description_div.find_all("p")

                description = ""
                for paragraph in paragraphs:
                    description += paragraph.text


                job_list.append([job_name, page_title, location, link_job,description])
            else:
                job_name = job.text
                location = location_tag.text
                link_job = f'{company}{link_tag["href"]}'

                response = requests.get(link_job)
                content = response.content
                site = BeautifulSoup(content, "html.parser")

                description_div = site.find("div",
                                            attrs={"data-testid": "text-section", "class": "sc-2fba68cb-1 HAGHS"})
                paragraphs = description_div.find_all("p")

                description = ""
                for paragraph in paragraphs:
                    description += paragraph.text

                job_list.append([job_name, page_title, location, link_job,description])



        return job_list

    for item in job_list:
        company_website = item["careerPageUrl"].split('/')
        if len(company_website) >= 3:
            base_url = '/'.join(company_website[:3])
            career_page_urls.append(base_url)

    all_jobs = []
    print(f"Já catalogamos todas as empresas. Ao todo temos {len(career_page_urls) + 1} empresas")

    for company in career_page_urls:
        response = requests.get(company)
        content = response.content
        site = BeautifulSoup(content, "html.parser")
        page_title = site.title.text
        jobs_ul = site.find_all("ul", attrs={"data-testid": "job-list__list"})
        jobs = []
        for job in jobs_ul:
            li_of_job = job.find_all("li", attrs={"class": "sc-cc6aad61-3 iBlSMP"})
            for info in li_of_job:
                jobs.append(info)

        company_jobs = body_job(jobs, company)
        all_jobs.extend(company_jobs)

    all_companies_saved = pd.DataFrame(all_jobs, columns=["Título", "Empresa", "Localização", "Link Da Vaga","Descrição Vaga"])

    try:
        companys_registradas = pd.read_excel(excel_file)
        all_companies_saved = pd.concat([companys_registradas, all_companies_saved])
    except FileNotFoundError:
        pass

    all_companies_saved.to_excel(excel_file, index=False)

    print(f"Foram contabilizadas {len(all_jobs)} vagas de emprego.")
    print("Todas elas já foram adicionadas ao arquivo", excel_file)



find_job = input("Qual área deseja?")
scraping_jobs(find_job)
