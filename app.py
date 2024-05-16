import json
from ghunt.objects.encoders import GHuntEncoder
from quart import Quart, request, jsonify
import asyncio
from ghunt.modules import email

app = Quart(__name__)

async def get_email_info(email_address):
    try:
        info = await email.hunt(None, email_address)
        return {'status': True, 'info': info}
    except Exception as e:
        return {'status': False, 'error': str(e)}

@app.route('/get_ghunt_data', methods=['POST'])
async def get_ghunt_data():
    try:
        data = await request.get_json()
        email_address = data.get('email_address')
        if email_address:
            result = await get_email_info(email_address)
            return json.dumps(result, cls=GHuntEncoder, indent=4)
        else:
            return jsonify({'status': False, 'error': 'Missing email_address parameter'}), 400
    except Exception as e:
        return jsonify({'status': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5001)
