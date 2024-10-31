import pickle

import numpy as np
import pandas as pd
from flask import Flask, jsonify, render_template, request
from pandas.api.types import is_object_dtype
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler

app = Flask(__name__)
scaler = StandardScaler()
label_encoder = LabelEncoder()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/login_form', methods=['POST'])
def login_form():
    
    return

@app.route('/previsao')
def previsao():
    return render_template('previsao.html')

@app.route('/previsao_form', methods=['POST'])
def previsao_form():

    dicionario_KitchenQual = {
        'Ex':0,
        'Fa':1,
        'Gd':2,
        'TA':3
        }
    
    # Carregar o modelo de regressão linear salvo
    try:
        with open('./modelo_regressao_linear_hackathon.pkl', 'rb') as f:
            model_p = pickle.load(f)
    except:
        with open('./app_hackathon/modelo_regressao_linear_hackathon.pkl', 'rb') as f:
            model_p = pickle.load(f)

    # Obter os dados do formulário
    try:
        OverallQual = int(request.form['OverallQual'])
        YearBuilt = int(request.form['YearBuilt'])
        YearRemodAdd = int(request.form['YearRemodAdd'])
        FirstFlrSF = round(
            float(
                str(request.form['FirstFlrSF']).replace(',','.')
                ) * 10.7639
            ,2) #
        GrLivArea = round(
            float(
                str(request.form['GrLivArea']).replace(',','.')
                ) * 10.7639
            ,2) #
        FullBath = int(request.form['FullBath'])
        KitchenQual =str(request.form['KitchenQual'])
        TotRmsAbvGrd = int(request.form['TotRmsAbvGrd'])
        GarageCars = int(request.form['GarageCars'])
        GarageArea = round(
            float(
                str(request.form['GarageArea']).replace(',','.')
                ) * 10.7639
            ,2) #

        cols_data = [
                    OverallQual,
                    YearBuilt,
                    YearRemodAdd,
                    FirstFlrSF,
                    GrLivArea,
                    FullBath,
                    KitchenQual,
                    TotRmsAbvGrd,
                    GarageCars,
                    GarageArea
                    ]

        cols_name = [    
            'OverallQual',  #    Qualidade geral do material e do acabamento
            'YearBuilt',    #    Data Original de construção
            'YearRemodAdd', #    Data da reforma (igual à data de construção, se não houver reformas)
            '1stFlrSF',     #    Primeiro andar pés quadrados - converter para metros²
            'GrLivArea',    #    Área de estar acima do nível do solo (pés quadrados) - converter para metros²
            'FullBath',     #    Banheiros completos
            'KitchenQual',  #    Qualidade da cozinha
            'TotRmsAbvGrd', #    Total de cômodos acima do nível do solo (não inclui banheiros)
            'GarageCars',   #    Tamanho da garagem em capacidade de carros
            'GarageArea',   #    Tamanho da garagem em pés quadrados - converter para metros²
            ]


        df = pd.DataFrame(data=[cols_data], columns=cols_name)
        df['KitchenQual'] = df['KitchenQual'].map(dicionario_KitchenQual)
        
        # Fazer a previsão
        prediction = model_p.predict(df)
        print(f"Predição de SalePrice: {prediction[0]}")

        f.close()
        # Retornar o resultado da previsão
        return render_template('previsao.html', prediction_text=f'Preço Previsto: R$ {round(float(prediction[0]),2)}')
    
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == "__main__":
    app.run(debug=True)
