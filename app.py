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

        # Dados necessários para criar um membro na comunidade do Invision
        member_data = {
            'email': buyer_email,
            'username': buyer_name,
            # Adicione outros dados do comprador, se necessário
        }

        # Enviar uma solicitação POST para a API do Invision para criar o membro
        response = requests.post(f"{INVISION_API_URL}/members", json=member_data, headers={"Authorization": f"Bearer {API_KEY}"})
        
        if response.status_code == 201:
            return jsonify({'message': 'Membro criado com sucesso na comunidade do Invision'}), 200
        else:
            return jsonify({'error': 'Falha ao criar membro na comunidade do Invision'}), 500

    return jsonify({'message': 'Evento não suportado'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

