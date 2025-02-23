from flask import Flask, request, jsonify
from flask_cors import CORS
from agents.main_agent import MainAgent

app = Flask(__name__)
CORS(app)
main_agent = MainAgent()

@app.route('/')
def server_status():
    return 'Server is running.'

@app.route('/chat/completion', methods=['POST'])
async def chat_completion():
    try:
        chat_messages = request.json.get('chat', [])
        base64_image = request.json.get('image')
        
        # Process request through main agent
        response = await main_agent.process(chat_messages, base64_image)
        return jsonify(response)
            
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)