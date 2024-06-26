from flask import Flask, request, jsonify
import requests
import logging
import random
import string

app = Flask(__name__)

# Configurações de logging
logging.basicConfig(level=logging.INFO)

# URL da sua comunidade do Invision e chave da API
INVISION_API_URL = "https://i330926.invisionservice.com/api"
API_KEY = "4563143c988b1cbe607c6777705493f8" 

def generate_random_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(length))

    return password

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    event = data.get('event')

    logging.info(f"Recebido evento: {event}")

    if event in ['PURCHASE_APPROVED', 'PURCHASE_COMPLETED']:
        buyer_email = data['data']['buyer']['email']
        buyer_name = data['data']['buyer']['name']


        password = generate_random_password()
        user_data = {
            "name": buyer_name,
            "email": buyer_email,
            "password": password  # Usando a senha aleatória gerada
        }

        # Cabeçalhos para a solicitação à API do Invision
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        logging.info(f"Criando usuário no Invision: {user_data}")

        response = requests.post(f"{INVISION_API_URL}/core/members", json=user_data, headers=headers)

        logging.info(f"Resposta da API do Invision: {response.status_code} - {response.text}")

        if response.status_code == 200:
            return jsonify({"message": "Usuário criado com sucesso!", "password": password}), 200
        else:
            return jsonify({"message": "Erro ao criar usuário no Invision.", "details": response.json()}), response.status_code

    return jsonify({"message": "Evento ignorado."}), 200

if __name__ == '__main__':
    app.run(debug=True)
