#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  2 20:23:14 2022

@author: Ramires

Criacao de uma API usando flask

"""

import os

from flask import Flask, request, jsonify
from flask_basicauth import BasicAuth

from textblob import TextBlob

import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

import pickle


# para testar a aplicacao, deve ser feito um post, pode utilizar o postman

# modelo pode ser feito antes e salvo formato sav usando pickle
model = pickle.load(open(r'../../models/modelo.sav','rb'))

columns = ['tamanho', 'ano', 'garagem']



#criando instancia do flask
app = Flask(__name__)

#configurando a autenticacao
app.config['BASIC_AUTH_USERNAME'] = os.environ.get('BASIC_AUTH_USERNAME')
app.config['BASIC_AUTH_PASSWORD'] = os.environ.get('BASIC_AUTH_PASSWORD')

basic_auth = BasicAuth(app)

# definindo rota (tambem chamada de endpoint)
@app.route('/')
def home():
    return 'Minha primeira API.'


#depois do caminho 'sentimento'foi colocado uma tag com frase que vai receber
# a frase que alguem quer testar na api
@app.route('/sentimento/<frase>')
@basic_auth.required
#faz com que seja obrigatorio a autenticacao para acessar essa pagina
def sentimento(frase):
    
    tb = TextBlob(frase)
    # essa bibliotea nao trabalha bem com textos em portugues, portanto precisa traduzir-la
    tb_en = tb.translate(to='en')
    polaridade = tb_en.sentiment.polarity
    
    return "polaridade: {}".format(polaridade) 


# int: define que a variavel sera um int 
# @app.route('/cotacao/<int:tamanho>')
# o m[etodo é para poder enviar mais de umaa variavel
@app.route('/cotacao/', methods=['POST'])
@basic_auth.required
#faz com que seja obrigatorio a autenticacao para acessar essa pagina
def cotacao():
    
    dados = request.get_json()
    # passo para verificar se o que a pessoa est[a enviando no post está na ordem corret]
    dados_input = [dados[col] for col in columns]
    
    preco = model.predict([dados_input])
    
    #como é algo http o return deve ser string
    #return "O preço da casa é: {}" .format(str(preco)[1:-1])
    
    #para retornar os dados no formato de json
    return jsonify(preco=preco[0])

# para habilitar o debugmode assim quando salvar o arquivo o flask reseta automaticamente
app.run(debug=True, hosts='0.0.0.0')