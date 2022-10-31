import os
import sys
import requests
from bs4 import BeautifulSoup

usr = os.environ['USER'] if 'USER' in os.environ else ''
pwd = os.environ['PASSWORD'] if 'PASSWORD' in os.environ else ''

def login(usr, pwd, session: requests.Session):
  r = session.post('https://ludopedia.com.br/login', [
      ('email', usr),
      ('pass', pwd),
  ])

  return "document.location.href = 'https://ludopedia.com.br/'" in r.text


def logout(session: requests.Session):
  session.get('https://ludopedia.com.br/logout')


def listActivities(session: requests.Session):
  r = session.get('https://ludopedia.com.br/meeps')

  soup = BeautifulSoup(r.text)
  tags = soup.select('a.btn-atividade[data-cd_atividade]')

  ids = map(lambda x: x.attrs['data-cd_atividade'], tags)
  return list(set(ids)) # Unique IDS


def doActivity(id, session: requests.Session):
  session.post(f'https://ludopedia.com.br/api/v1/atividades/{id}')


with requests.Session() as session:
  if not login(usr, pwd, session):
    print('Não foi possível realizar o login. Encerrando...')
    sys.exit(1)

  for id in listActivities(session):
    doActivity(id, session)

  logout(session)
