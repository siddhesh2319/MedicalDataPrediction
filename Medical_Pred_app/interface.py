from flask import Flask, render_template, request, jsonify
from App_Data.utils import MedicalData
import App_Data.config as config

app = Flask(__name__)
app.config.from_object(config)

@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict_charges():
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                "status": "error",
                "message": "No JSON data received or invalid JSON."
            }), 400

        required_data = ['age', 'bmi', 'children', 'gender', 'smoker', 'region']

        for feature in required_data:
            if feature not in data:
                return jsonify({
                    "status": "error",
                    "message": f"{feature} is missing"
                }), 400

        age = int(data['age'])
        bmi = float(data['bmi'])
        children = int(data['children'])
        smoker = data['smoker'].lower()
        gender = data['gender'].lower()
        region = data['region'].lower()

        med_data = MedicalData(age, gender, bmi, children, smoker, region)
        charges = med_data.get_predict()

        # Handle both list/array and scalar predictions
        if isinstance(charges, (list, tuple)) or hasattr(charges, '__getitem__'):
            prediction = float(charges[0])
        else:
            prediction = float(charges)

        return jsonify({
            "status": "success",
            "prediction": prediction,
            "message": "Prediction successful"
        }), 200
    except ValueError as ve:
        return jsonify({
            "status": "error",
            "message": str(ve)
        }), 400
    except Exception as e:
        if app.config.get('DEBUG', False):
            return jsonify({
                "status": "error",
                "message": str(e)
            }), 500
        else:
            return jsonify({
                "status": "error",
                "message": "Something went wrong"
            }), 500

if __name__ == "__main__":
    app.run(debug=True)