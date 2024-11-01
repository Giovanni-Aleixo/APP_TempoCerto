import pytz
import requests
from datetime import datetime
import json
import pycountry_convert as pc


key = 'd6f14dd85488537e5918c7bcfa668089'
localidade = ''
acesso_api = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'.format(localidade, key)


#CONEXAO COM API
relacao = requests.get(acesso_api)
dados = relacao.json() 
print(dados)

#LOCALIDADE
endereco_pais = dados['sys']['country']

fuso_cidade = pytz.country_timezones[endereco_pais]

fuso_pais = pytz.country_names[endereco_pais]

fuso_data = pytz.timezone(fuso_cidade[0])
fuso_hora = datetime.now(fuso_data)
fuso_hora = fuso_hora.strftime("%d %m %Y | %H:%M %p")

fuso_temp = dados['main']['temp']
fuso_press = dados['main']['pressure']
fuso_humil = dados['main']['humidity']
fuso_veloc = dados['wind']['speed']
fuso_descr = dados['weather'][0]['description']


#ALTERAÇÃO INFORMAÇÃO
def pais_conti(i):
    pais_pesq = pc.country_name_to_country_alpha2(i)
    pais_conti_cod = pc.country_alpha2_to_continent_code(pais_pesq)
    pais_conti_nome = pc.convert_continent_code_to_continent_name(pais_conti_cod)

    return(pais_conti_nome)

continente = pais_conti(fuso_pais)




