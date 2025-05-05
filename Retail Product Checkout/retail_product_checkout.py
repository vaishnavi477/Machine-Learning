from flask import Flask, request, jsonify, send_file
from flask_ngrok import run_with_ngrok
import cv2
import numpy as np
import pandas as pd
import torch
from pyngrok import ngrok
import os
from flask import send_from_directory
from collections import Counter
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from ultralytics import YOLO

# Initialize Flask app
app = Flask(__name__)
run_with_ngrok(app)  # Automatically starts ngrok

# Load YOLOv8 trained model 
model = YOLO('/models/best.pt')

# Load billing data
billing_data = pd.read_csv('product_prices.csv')
billing_data.columns = ['Product', 'Price']

# Start ngrok
public_url = ngrok.connect(5000)
print(f"Public URL: {public_url}")

# Ensure upload directory exists
UPLOAD_FOLDER = "/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return send_file('/templates/webpage_design.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    try:
        file = request.files['image']
        image_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(image_path)

        img = cv2.imread(image_path)

        # Run YOLOv8 detection
        results = model(img)
        result = results[0]

        # Get class indices and map to names
        class_ids = result.boxes.cls.cpu().numpy().astype(int)
        detected_products = [model.names[i] for i in class_ids]

        # Generate bill
        bill = []
        total_price = 0

        # Count occurrences of each product
        product_counts = Counter(detected_products)

        for product, count in product_counts.items():
            product_info = billing_data[billing_data['Product'] == product]
            if not product_info.empty:
                unit_price = float(product_info['Price'].values[0])
                total = unit_price * count
                bill.append({
                    'Product': product,
                    'Quantity': count,
                    'Unit_Price': unit_price,
                    'Total': total
                })
                total_price += total

        response = {'detected_products': detected_products, 'bill': bill, 'total_price': total_price, 'total_items': sum(product_counts.values())}
        return jsonify(response)

    except Exception as e:
        print("Error during upload_image:", str(e))
        return jsonify({'error': str(e)}), 500


# @app.route('/payment')
# def payment_page():
#     amount = request.args.get('amount', '0.00')
#     return send_file('/content/drive/MyDrive/Reduce_new_data/payment.html')


# @app.route('/payment/success', methods=['GET'])
# def payment_success():
#     return send_file('/content/drive/MyDrive/Reduce_new_data/success.html')

@app.route('/download_bill', methods=['POST'])
def download_bill():
    data = request.get_json()

    bill = data.get('bill', [])
    total_price = data.get('total_price', 0)
    total_items = data.get('total_items', 0)

    # Generate PDF
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    y = height - 50
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "Smart Retail Checkout - Final Bill")
    y -= 40

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Product")
    c.drawString(200, y, "Qty")
    c.drawString(250, y, "Unit Price")
    c.drawString(350, y, "Total")
    y -= 20

    c.setFont("Helvetica", 12)
    for item in bill:
        c.drawString(50, y, item['Product'])
        c.drawString(200, y, str(item['Quantity']))
        c.drawString(250, y, f"${item['Unit_Price']:.2f}")
        c.drawString(350, y, f"${item['Total']:.2f}")
        y -= 20

    y -= 10
    c.line(50, y, 500, y)
    y -= 30
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, f"Total Items: {total_items}")
    c.drawString(250, y, f"Total Price: ${total_price:.2f}")

    c.save()
    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name="final_bill.pdf", mimetype='application/pdf')

if __name__ == '__main__':
    print("Server is starting...")
    app.run()
