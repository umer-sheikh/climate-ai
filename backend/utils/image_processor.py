from roboflow import Roboflow
import cv2
import base64
import numpy as np
import os
import uuid
import json
from config import Config

class ImageProcessor:
    def __init__(self):
        self.rf = Roboflow(api_key=Config.ROBOFLOW_API_KEY)
        self.project = self.rf.workspace().project("xview2-xbd")
        self.model = self.project.version(10).model

    def generate_bright_color(self):
        h = np.random.random()
        s = 0.7 + np.random.random() * 0.3
        v = 0.7 + np.random.random() * 0.3
        
        h_i = int(h * 6)
        f = h * 6 - h_i
        p = v * (1 - s)
        q = v * (1 - f * s)
        t = v * (1 - (1 - f) * s)
        
        if h_i == 0: r, g, b = v, t, p
        elif h_i == 1: r, g, b = q, v, p
        elif h_i == 2: r, g, b = p, v, t
        elif h_i == 3: r, g, b = p, q, v
        elif h_i == 4: r, g, b = t, p, v
        else: r, g, b = v, p, q
        
        return (int(b * 255), int(g * 255), int(r * 255))

    async def process_image(self, base64_image):
        try:
            unique_filename = f"{uuid.uuid4()}.jpg"
            
            if ',' in base64_image:
                base64_image = base64_image.split(',')[1]
            with open(unique_filename, "wb") as image_file:
                image_file.write(base64.b64decode(base64_image))
            
            result = self.model.predict(unique_filename, confidence=40, overlap=30).json()
            predictions = result["predictions"]
            
            class_list = list(set(item["class"] for item in predictions))
            color_map = {class_name: self.generate_bright_color() for class_name in class_list}

            image = cv2.imread(unique_filename)
            
            for pred in predictions:
                x, y = pred["x"], pred["y"]
                width, height = pred["width"], pred["height"]
                class_name = pred["class"]
                
                x1 = int(x - width/2)
                y1 = int(y - height/2)
                x2 = int(x + width/2)
                y2 = int(y + height/2)
                
                color = color_map[class_name]
                
                cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
                
                label = f"{class_name} {pred['confidence']:.2f}"
                (text_width, text_height), baseline = cv2.getTextSize(
                    label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2
                )
                
                cv2.rectangle(
                    image, 
                    (x1, y1-text_height-baseline-10), 
                    (x1+text_width, y1), 
                    color, 
                    -1
                )
                
                cv2.putText(
                    image, 
                    label, 
                    (x1, y1-10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 
                    0.5, 
                    (255, 255, 255), 
                    2
                )
            
            _, buffer = cv2.imencode('.jpg', image)
            annotated_image_base64 = base64.b64encode(buffer).decode('utf-8')
            
            os.remove(unique_filename)
            
            return {
                'predictions': predictions,
                'annotated_image': annotated_image_base64
            }
            
        except Exception as e:
            print(f"Error processing image: {str(e)}")
            return None