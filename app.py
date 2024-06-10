from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# URL da sua comunidade do Invision e chave da API
INVISION_API_URL = "https://i330926.invisionservice.com/api"
API_KEY = "dff17ac146cf8b4ce9b488362d86d974"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    event = data.get('event')

    if event in ['PURCHASE_APPROVED', 'PURCHASE_COMPLETED']:
        buyer_email = data['data']['buyer']['email']
        buyer_name = data['data']['buyer']['name']

        # Log dos dados recebidos
        app.logger.info(f"Dados do comprador: {buyer_name}, {buyer_email}")

        # Fazer uma requisição para a API do Invision para criar um novo membro
        headers = {
            'Authorization': f'Bearer {API_KEY}',
            'Content-Type': 'application/json'
        }
        payload = {
            'name': buyer_name,
            'email': buyer_email,
            'password': 'um_password_seguro',  # Certifique-se de escolher uma senha adequada
        }

        response = requests.post(f'{INVISION_API_URL}/core/members', json=payload, headers=headers)

        # Log da resposta da API
        app.logger.info(f"Resposta da API do Invision: {response.status_code}, {response.text}")

        if response.status_code == 200:
            return jsonify({'message': 'Membro criado com sucesso'}), 200
        else:
            return jsonify({'message': 'Falha ao criar membro', 'details': response.json()}), 400

    return jsonify({'message': 'Evento não suportado'}), 200

if __name__ == '__main__':
    app.run(debug=True)
