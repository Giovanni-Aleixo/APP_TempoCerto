from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import requests
from datetime import datetime, timedelta
import pycountry
import pycountry_convert as pc

#CORES UTILIZADAS
cor0 = "#333344"
cor1 = "#f8f9fa"
cor2 = "#5d85a8"
cor_sombra = "#d1d9e6"

fundo_dia = "#6cc4cc"
fundo_noite = "#484f60"
fundo_tarde = "#bfb86d"

fundo = fundo_dia

#JANELA
janela = Tk()
janela.title('Clima App')
janela.geometry('400x500')
janela.configure(bg=fundo)

ttk.Separator(janela, orient=HORIZONTAL).grid(row=0, column=1, ipadx=197)

#FRAME
frame_topo = Frame(janela, width=400, height=50, bg=cor1, pady=0, padx=0)
frame_topo.grid(row=1, column=0)

frame_meio = Frame(janela, width=400, height=450, bg=fundo, pady=12, padx=0)
frame_meio.grid(row=2, column=0, sticky=NW)

estilizacao = ttk.Style(janela)
estilizacao.theme_use('clam')

#FUNÇÃO DA INFORMAÇÃO
def info():
    global fundo, imagem

    key = 'd6f14dd85488537e5918c7bcfa668089'
    cidade = pesquisa.get()
    acesso_api = f'http://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={key}'

    try:
        #CONEXÃO COM API
        relacao = requests.get(acesso_api)
        dados = relacao.json()

        #VERIFICAÇÃO DA CIDADE
        if dados.get("cod") != 200:
            localidade['text'] = "Cidade não encontrada"
            return

        #LOCALIDADE
        endereco_pais = dados['sys']['country']
        
        #Obter nome do país usando pycountry
        nome_pais = pycountry.countries.get(alpha_2=endereco_pais).name if pycountry.countries.get(alpha_2=endereco_pais) else "País não localizado"
        
        timezone_offset = dados.get('timezone', 0)  # Obtém o fuso horário em segundos, 0 se não estiver presente
        local_time = datetime.utcnow() + timedelta(seconds=timezone_offset)  # Calcula a hora local com offset
        fuso_hora = local_time.strftime("%d/%m/%Y | %H:%M")

        #INFORMAÇÕES DO CLIMA
        temp_celsius = int(dados['main']['temp'] - 273.15)
        fuso_press = dados['main']['pressure']
        fuso_veloc = dados['wind']['speed']
        fuso_descr = dados['weather'][0]['description']

        #AUXILIAR PARA ENCONTRAR O CONTINENTE
        def pais_conti(codigo_pais):
            try:
                pais_conti_cod = pc.country_alpha2_to_continent_code(codigo_pais)
                return pc.convert_continent_code_to_continent_name(pais_conti_cod)
            except KeyError:
                return "Continente não localizado"

        continente = pais_conti(endereco_pais)

        #ATUALIZAR AS INFORMAÇÕES DO LAYOUT
        localidade['text'] = f"{cidade} - {nome_pais} | {continente}"
        data['text'] = fuso_hora
        temp_local['text'] = f"{temp_celsius}°C"
        pressão_local['text'] = f"Pressão: {fuso_press} hPa"
        velocidade_local['text'] = f"Vento: {fuso_veloc} m/s"
        status_local['text'] = fuso_descr.capitalize()

        #ALTERAÇÃO DO FUNDO CONFORME O PERÍODO DA LOCALIDADE
        layout_clima = int(local_time.strftime("%H"))

        if layout_clima <= 5:
            desenho = Image.open('Desenho/Lua.png')
            fundo = fundo_noite
        elif layout_clima <= 11:
            desenho = Image.open('Desenho/Sol.png')
            fundo = fundo_dia
        elif layout_clima <= 17:
            desenho = Image.open('Desenho/Por do Sol.png')
            fundo = fundo_tarde
        else:
            desenho = Image.open('Desenho/Lua.png')
            fundo = fundo_noite

        desenho = desenho.resize((180, 180))
        imagem = ImageTk.PhotoImage(desenho)

        janela.configure(bg=fundo)
        frame_topo.configure(bg=fundo)
        frame_meio.configure(bg=fundo)
        clima_desenho.configure(image=imagem, bg=fundo)

        for widget in [localidade, data, temp_local, pressão_local, velocidade_local, status_local]:
            widget.configure(bg=fundo, fg=cor1)

    except requests.exceptions.RequestException:
        localidade['text'] = "Erro na conexão com a API"

#OPÇÃO DE PESQUISA
pesquisa_frame = Frame(frame_topo, bg=cor_sombra, bd=0, highlightthickness=0)
pesquisa_frame.place(x=20, y=10, width=270, height=35)

pesquisa = Entry(pesquisa_frame, width=20, font=("Helvetica", 14), bg=cor1, fg=cor0, bd=0, relief='flat')
pesquisa.place(relwidth=0.92, relheight=1)

botao_pesquisa = Button(frame_topo, command=info, text='Pesquisar', bg=cor2, fg=cor1, font=("Helvetica", 10, "bold"), relief='raised', overrelief=RIDGE, bd=0)
botao_pesquisa.place(x=300, y=10, width=80, height=35)

#MOSTRAR INFORMAÇÕES
localidade = Label(frame_meio, text='', anchor='center', bg=fundo, fg=cor1, font=("Helvetica", 14))
localidade.place(x=10, y=4)

data = Label(frame_meio, text='', anchor='center', bg=fundo, fg=cor1, font=("Helvetica", 10))
data.place(x=10, y=54)

temp_local = Label(frame_meio, text='', anchor='center', bg=fundo, fg=cor1, font=("Helvetica", 45))
temp_local.place(x=10, y=100)

pressão_local = Label(frame_meio, text='', anchor='center', bg=fundo, fg=cor1, font=("Helvetica", 10))
pressão_local.place(x=10, y=200)

velocidade_local = Label(frame_meio, text='', anchor='center', bg=fundo, fg=cor1, font=("Helvetica", 10))
velocidade_local.place(x=10, y=230)

status_local = Label(frame_meio, text='', anchor='center', bg=fundo, fg=cor1, font=("Helvetica", 10))
status_local.place(x=230, y=200)

clima_desenho = Label(frame_meio, bg=fundo)
clima_desenho.place(x=200, y=80)

janela.mainloop()







