from dotenv import load_dotenv
from flask_cors import CORS
from flask import Flask, request, jsonify
import requests
from roboflow import Roboflow
import supervision as sv
import cv2
import base64
import numpy as np
import os
import uuid
import random
import json

print(f"Supervision version: {sv.__version__}")

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize Roboflow API
rf = Roboflow(api_key="tLtLxPNVTcQ8uRZfvPCa")
project = rf.workspace().project("xview2-xbd")
model = project.version(10).model

# Function to generate a random bright color
def generate_bright_color():
    h = random.random()  # Random hue
    s = 0.7 + random.random() * 0.3  # High saturation
    v = 0.7 + random.random() * 0.3  # High value
    
    # Convert HSV to RGB
    h_i = int(h * 6)
    f = h * 6 - h_i
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    
    if h_i == 0:
        r, g, b = v, t, p
    elif h_i == 1:
        r, g, b = q, v, p
    elif h_i == 2:
        r, g, b = p, v, t
    elif h_i == 3:
        r, g, b = p, q, v
    elif h_i == 4:
        r, g, b = t, p, v
    else:
        r, g, b = v, p, q
    
    return (int(b * 255), int(g * 255), int(r * 255))  # BGR format for OpenCV

@app.route('/')
def server_status():
    return 'Server is running.'

@app.route('/chat/completion', methods=['POST'])
def chat_completion():
    chat_messages = request.json.get('chat', [])
    base64_image = request.json.get('image')  # Optional image

    context = ""

    # Create the system message
    system_message = {
        "content": "I am Kashaf AI. Today date is Feb 18, 2025. I can provide information regarding animal species classification.",
        "role": "system"
    }

    # Method 1: Insert at beginning using insert()
    chat_messages.insert(0, system_message)
    
    # Initialize response variables
    message_content = None
    annotated_image_base64 = None
    
    # Process image if provided
    if base64_image:
        try:
            # Generate unique filename
            unique_filename = f"{uuid.uuid4()}.jpg"
            
            # Save base64 image
            if ',' in base64_image:
                base64_image = base64_image.split(',')[1]
            with open(unique_filename, "wb") as image_file:
                image_file.write(base64.b64decode(base64_image))
            
            # Get predictions
            result = model.predict(unique_filename, confidence=40, overlap=30).json()
            print("Predictions:", result["predictions"])
            context = "User has upload a satellite image for building damage prediction."
            context += " The image is analyzed and following are the predictions."
            context += json.dumps(result["predictions"])
            
            # Process annotations
            class_list = list(set(item["class"] for item in result["predictions"]))
            print("Class list:", class_list)
            
            # Create color mapping for classes
            color_map = {class_name: generate_bright_color() for class_name in class_list}

            image = cv2.imread(unique_filename)
            
            # Draw boxes and labels manually
            for pred in result["predictions"]:
                # Get coordinates
                x = pred["x"]
                y = pred["y"]
                width = pred["width"]
                height = pred["height"]
                class_name = pred["class"]
                
                # Calculate box coordinates
                x1 = int(x - width/2)
                y1 = int(y - height/2)
                x2 = int(x + width/2)
                y2 = int(y + height/2)
                
                # Get color for this class
                color = color_map[class_name]
                
                # Draw rectangle
                cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
                
                # Add label with confidence
                label = f"{class_name} {pred['confidence']:.2f}"
                
                # Get text size for better label background
                (text_width, text_height), baseline = cv2.getTextSize(
                    label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2
                )
                
                # Draw label background
                cv2.rectangle(
                    image, 
                    (x1, y1-text_height-baseline-10), 
                    (x1+text_width, y1), 
                    color, 
                    -1  # Fill rectangle
                )
                
                # Draw text
                cv2.putText(
                    image, 
                    label, 
                    (x1, y1-10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 
                    0.5, 
                    (255, 255, 255),  # White text
                    2
                )
            
            # Convert annotated image back to base64
            _, buffer = cv2.imencode('.jpg', image)
            annotated_image_base64 = base64.b64encode(buffer).decode('utf-8')
            
            # Clean up
            os.remove(unique_filename)
            
        except Exception as e:
            print(f"Error details: {str(e)}")
            import traceback
            print(traceback.format_exc())
            return jsonify({'error': str(e)}), 500
            

    # get last user message
    user_message = chat_messages[-1]['content']

    # Online search response:
    payload = {
        "api_key": "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",
        "query": user_message,  # Assuming `request` is defined
        "search_depth": "basic",
        "include_answer": True,
        "include_images": False,
        "include_image_descriptions": False,
        "include_raw_content": False,
        "max_results": 5,
        "include_domains": [],
        "exclude_domains": []
    }

    # Make the API request
    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post('https://api.tavily.com/search', json=payload, headers=headers)

    # Parse the response
    response_body = response.json()

    # Extract the message content
    message_content = response_body.get('answer')

    context += " \n Online search results: " + message_content + " \n"

    contexted_user_message = context + " \nUser Question: " + user_message + " \n Response:"
    chat_messages[-1]['content'] = contexted_user_message
    # Process chat completion
    payload = {
        'model': 'meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo',
        'max_tokens': 512,
        'temperature': 0.7,
        'top_p': 0.7,
        'top_k': 50,
        'repetition_penalty': 1,
        'messages': chat_messages
    }

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer '
    }

    # Get chat response
    response = requests.post('https://api.together.xyz/v1/chat/completions', json=payload, headers=headers)
    
    if response.status_code != 200:
        return jsonify({'error': response.json()}), response.status_code
        
    message_content = response.json()['choices'][0]['message']['content']
    
    # Return response based on whether image was processed
    if annotated_image_base64:
        return jsonify({
            'message': message_content,
            'annotated_image': f"data:image/jpeg;base64,{annotated_image_base64}"
        })
    else:
        return jsonify({'message': message_content})

@app.route('/chat/image', methods=['POST'])
def chat_image():
    return 'Chat image.'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)