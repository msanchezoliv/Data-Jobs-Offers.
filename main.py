from bs4 import BeautifulSoup
import requests
import datetime
import csv
import time


# La siguiente función nos servirá para hacer "webscraping" en el link de la oferta
# y guardar su descripción.

def desc_extract(url):
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'lxml')
    desc_raw = soup.find('div', class_="job-description t-job-description")
    desc_tags = desc_raw.find_all('p')
    desc = desc_tags[0].text
    for p in desc_tags[1:]:
        desc = desc + '\n' + p.text
    return desc


# Cuando la siguiente función se ejecuta, crea el csv con las ofertas de trabajo
# de data de la web 'domestica.org' de los últimos n meses.

def jobs_extract():
    n = int(input("Number of months since you want to have the dataset: "))
    n_days_ago = datetime.date.today() - datetime.timedelta(days=30*n)
    # Llamamos al archivo. OJO con poner la fecha con '/', que se usa para el path.
    file_name = f'data jobs since {n_days_ago.strftime("%d-%m-%Y")}.csv12'
    with open(file_name, 'w', encoding="utf-8") as csv_file:
        fields = ['title', 'link', 'company', 'contract', 'location', 'date', 'description']
        csv_writer = csv.DictWriter(csv_file, fieldnames=fields, dialect='excel')
        csv_writer.writeheader()
        # Ahora, recorre las 60 primeras páginas de trabajos de data de 'domestica.org'.
        for i in range(1, 61):
            url = 'https://www.domestika.org/es/search/jobs?button=&page='+str(i)+'&query=data'
            html_text = requests.get(url).text
            soup = BeautifulSoup(html_text, 'lxml')
            jobs = soup.find_all('li', class_="job-item")
            for job in jobs:
                # Sacamos la fecha de la oferta.
                date_string = job.find('div', class_="col-md-2 job-item__date").text.strip()
                date_time = datetime.datetime.strptime(date_string, '%d/%m/%y')
                date = date_time.date()
                if date >= n_days_ago:
                    # Si es de hace menos de n días, sacamos su info en un diccionario.
                    # Info:
                    title_comp_desc = job.find('div', class_="col-md-6")
                    title_raw = title_comp_desc.find('h2', class_="job-item__title")
                    title = title_raw.text.strip()
                    link = title_raw.find('a', class_="job-title")['href']
                    company = title_comp_desc.find('h3', class_="h4 job-item__company").text
                    description = desc_extract(link)
                    contract = job.find('div', class_="col-md-2 job-item__kind").text.strip()
                    location = job.find('div', class_="col-md-2 job-item__city").text.strip()
                    # Generamos un diccionario de info de cada job
                    dic_job = {'link': link, 'company': company, 'description': description,
                               'contract': contract, 'location': location, 'title': title, 'date': date_string}
                    # Lo escribimos como fila de nuestro csv.
                    csv_writer.writerow(dic_job)
    print("{} saved".format(file_name))


# Ahora llamamos al 'main' para ejecutarlo en la terminal con python

if __name__ == '__main__':
    jobs_extract()


