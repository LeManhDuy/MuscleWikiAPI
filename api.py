from flask import Flask, request,json

app = Flask(__name__)

# Load workout data
with open('workout-data.json', 'r') as f:
    workout_data = json.load(f)

# Load workout attributes
with open('workout-attributes.json', 'r') as f:
    workout_attributes = json.load(f)

@app.route('/')
def home():
    response = app.response_class(
        response=json.dumps({
            'message': "Muscle Wiki API"
        }),
        mimetype='application/json',
        status=200
    )
    return response

@app.route('/exercises')
def get_exercises():
    # Get query parameters
    muscle = request.args.get('muscle')
    name = request.args.get('name')
    category = request.args.get('category')
    difficulty = request.args.get('difficulty')
    force = request.args.get(('force'))
    # Filter exercises based on query parameters
    filtered_exercises = []
    for exercise in workout_data:
        
        if muscle and not any(muscle in lst for lst in exercise['target'].values()):
            continue
        
        if name and name.lower() not in exercise['exercise_name'].lower():
            continue
        
        if category and category.lower() != exercise['Category'].lower():
            continue
        
        if difficulty and difficulty.lower() != exercise['Difficulty'].lower():
            continue
        
        if force and 'Force' in exercise and force.lower() != exercise['Force'].lower():
            continue
        if force and 'Force' not in exercise:
            continue

        filtered_exercises.append(exercise)

    response = app.response_class(
        response=json.dumps(filtered_exercises),
        mimetype='application/json',
        status=200
    )
    return response

@app.route('/exercises/attributes')
def get_exercise_attributes():
    response = app.response_class(
        response=json.dumps(workout_attributes),
        mimetype='application/json',
        status=200
    )
    return response

@app.route('/exercises/<int:exercise_id>')
def get_exercise_by_id(exercise_id):
    # Find exercise by ID
    for exercise in workout_data:
        if exercise['id'] == exercise_id:
            response = app.response_class(
                        response=json.dumps(exercise),
                        mimetype='application/json',
                        status=200
                    )
            return response
    return json.dumps({'error': 'Exercise not found'})

if __name__ == '__main__':
    app.run(debug=True)
