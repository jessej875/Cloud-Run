import os
from flask import Flask, jsonify
from google.cloud import firestore

app = Flask(__name__)

db = firestore.Client()

@app.route('/info', methods=['GET'])
def info():
    return jsonify({
        "message": "Student Database API: Stores student names, ages (18-25), and math scores (0-100)."
    }), 200

@app.route('/stats', methods=['GET'])
def stats():
    try:
        students_ref = db.collection('students')
        docs = students_ref.stream()

        total_age = 0
        total_math_score = 0
        count = 0

        for doc in docs:
            data = doc.to_dict()
            if 'age' in data and 'math_score' in data:
                total_age += data['age']
                total_math_score += data['math_score']
                count += 1

        if count == 0:
            return jsonify({"error": "No valid student records found in the database."}), 404

        avg_age = round(total_age / count, 2)
        avg_math_score = round(total_math_score / count, 2)

        return jsonify({
            "total_students": count,
            "average_age": avg_age,
            "average_math_score": avg_math_score
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
