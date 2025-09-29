from flask import Flask, render_template_string, request, redirect, url_for
from opentelemetry import trace
from opentelemetry.trace import TracerProvider
from opentelemetry.sdk.trace import export, TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

# For monitoring with Grafana
from prometheus_client import start_http_server, Counter

# Start a Prometheus metrics server on port 8000
start_http_server(8000)
print("Prometheus metrics server started on port 8000")

# Initialize OpenTelemetry tracing
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

# Configure the OTLP exporter to deploy with kubernetes, otel-collector is the service name to connect with Kubernetes
otlp_exporter = OTLPSpanExporter(endpoint="http://otel-collector:4317", insecure=True)
span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

# Create a Flask app
app = Flask(__name__)

# Initialize score for tracking game progress
SCORE = 0

# Animal data
cat_names = ['Kermit', 'Leia', 'Bobby', 'Tiger', 'Asos', 'Guizmo', 'Suffo', 'Marraket', 'Kiki', 'Ursula']
cat_age = [3, 8, 12, 1, 4, 8, 2, 2, 8, 4]
cat_healthScore = [3, 6, 9, 7, 5, 2, 1, 1, 2, 3]
cow_names = ['Bella', 'Leia', 'Madonna', 'Bobby', 'Tiger', 'Asos', 'Guizmo', 'Suffo', 'Marraket', 'Kiki']
cow_age = [3, 8, 12, 1, 4, 8, 2, 2, 8, 4]
cow_healthScore = [3, 6, 9, 7, 5, 2, 1, 1, 2, 3]
pig_names = ['Babe', 'Tomillito', 'Patrizio', 'Lindo', 'Asos', 'Guizmo', 'Suffo', 'Marraket', 'Kiki', 'Ursula']
pig_age = [3, 8, 12, 1, 4, 8, 2, 2, 8, 4]  # Fixed the incomplete pig_age array
pig_healthScore = [3, 6, 9, 7, 5, 2, 1, 1, 2, 3]
dog_names = ['Kermit', 'Leia', 'Bobby', 'Tiger', 'Asos', 'Guizmo', 'Suffo', 'Marraket', 'Kiki', 'Ursula']
dog_age = [3, 8, 12, 1, 4, 8, 2, 2, 8, 4]
dog_healthScore = [3, 6, 9, 7, 5, 2, 1, 1, 2, 3]

# Utility functions
def score_user():
    global SCORE
    SCORE += 3
    return SCORE

def reset_score():
    global SCORE
    SCORE = 0

# HTML Templates
index_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Animal Rescuer Game</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 40px;
            line-height: 1.6;
            color: #333;
        }
        h1 {
            color: #2c3e50;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f9f9f9;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }
        input[type="text"], input[type="number"] {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
        }
        .button {
            background-color: #3498db;
            color: white;
            padding: 10px 15px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
        }
        .button:hover {
            background-color: #2980b9;
        }
        .error {
            color: #e74c3c;
        }
        .animal-info {
            margin-bottom: 20px;
            padding: 10px;
            background-color: #eee;
            border-radius: 4px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Animal Rescuer Game</h1>
        <p>Welcome to the Animal Rescuer Game! Enter your name to start.</p>
        {% if error %}
            <p class="error">{{ error }}</p>
        {% endif %}
        <form action="/welcome" method="post">
            <div class="form-group">
                <label for="username">Your Name:</label>
                <input type="text" id="username" name="username" required>
            </div>
            <button type="submit" class="button">Start Game</button>
        </form>
    </div>
</body>
</html>
"""

welcome_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Animal Rescuer Game</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 40px;
            line-height: 1.6;
            color: #333;
        }
        h1, h2 {
            color: #2c3e50;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f9f9f9;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }
        input[type="number"] {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
        }
        .button {
            background-color: #3498db;
            color: white;
            padding: 10px 15px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
        }
        .button:hover {
            background-color: #2980b9;
        }
        .animal-info {
            margin-bottom: 20px;
            padding: 10px;
            background-color: #eee;
            border-radius: 4px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Welcome {{ username }}!</h1>
        <p>You will be in no time a real Hero Animal Rescuer!</p>
        
        <p>Choose how many animals you want to rescue. You will receive a score from 1 to 10. More pets == higher score.</p>
        
        <div class="animal-info">
            <h2>Cats available for rescue:</h2>
            <p>Names: {{ cats_names }}</p>
            <p>Health scores: {{ cats_health }}</p>
        </div>
        
        <div class="animal-info">
            <h2>Dogs available for rescue:</h2>
            <p>Names: {{ dogs_names }}</p>
            <p>Health scores: {{ dogs_health }}</p>
        </div>
        
        <div class="animal-info">
            <h2>Cows available for rescue:</h2>
            <p>Names: {{ cows_names }}</p>
            <p>Health scores: {{ cows_health }}</p>
        </div>
        
        <div class="animal-info">
            <h2>Pigs available for rescue:</h2>
            <p>Names: {{ pigs_names }}</p>
            <p>Health scores: {{ pigs_health }}</p>
        </div>
        
        <form action="/rescue" method="post">
            <div class="form-group">
                <label for="rescue_count">How many animals can you rescue?</label>
                <input type="number" id="rescue_count" name="rescue_count" min="1" required>
                <input type="hidden" name="username" value="{{ username }}">
            </div>
            <button type="submit" class="button">Continue</button>
        </form>
    </div>
</body>
</html>
"""

rescue_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Animal Rescuer Game</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 40px;
            line-height: 1.6;
            color: #333;
        }
        h1 {
            color: #2c3e50;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f9f9f9;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }
        .button {
            background-color: #3498db;
            color: white;
            padding: 10px 15px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
        }
        .button:hover {
            background-color: #2980b9;
        }
        .radio-group {
            margin-bottom: 15px;
        }
        .radio-group label {
            display: inline;
            margin-left: 5px;
        }
        .animal-info {
            margin-bottom: 20px;
            padding: 10px;
            background-color: #eee;
            border-radius: 4px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Animal Rescue Selection</h1>
        <p>You've chosen to rescue {{ count }} animal(s).</p>
        
        {% if count == 1 %}
            <form action="/result" method="post">
                <h2>Select one animal to rescue:</h2>
                
                <div class="radio-group">
                    <input type="radio" id="cat" name="animal_type" value="cat" required>
                    <label for="cat">Cat</label>
                </div>
                
                <div class="radio-group">
                    <input type="radio" id="dog" name="animal_type" value="dog">
                    <label for="dog">Dog</label>
                </div>
                
                <div class="radio-group">
                    <input type="radio" id="cow" name="animal_type" value="cow">
                    <label for="cow">Cow</label>
                </div>
                
                <div class="radio-group">
                    <input type="radio" id="pig" name="animal_type" value="pig">
                    <label for="pig">Pig</label>
                </div>
                
                <input type="hidden" name="count" value="1">
                <input type="hidden" name="username" value="{{ username }}">
                <button type="submit" class="button">Rescue</button>
            </form>
        {% else %}
            <form action="/result" method="post">
                <h2>Select which type of animals to rescue:</h2>
                
                <div class="radio-group">
                    <input type="radio" id="cats" name="animal_type" value="cats" required>
                    <label for="cats">Cats</label>
                </div>
                
                <div class="radio-group">
                    <input type="radio" id="dogs" name="animal_type" value="dogs">
                    <label for="dogs">Dogs</label>
                </div>
                
                <div class="radio-group">
                    <input type="radio" id="cows" name="animal_type" value="cows">
                    <label for="cows">Cows</label>
                </div>
                
                <div class="radio-group">
                    <input type="radio" id="pigs" name="animal_type" value="pigs">
                    <label for="pigs">Pigs</label>
                </div>
                
                <input type="hidden" name="count" value="{{ count }}">
                <input type="hidden" name="username" value="{{ username }}">
                <button type="submit" class="button">Rescue</button>
            </form>
        {% endif %}
    </div>
</body>
</html>
"""

result_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Animal Rescuer Game</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 40px;
            line-height: 1.6;
            color: #333;
        }
        h1, h2 {
            color: #2c3e50;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f9f9f9;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .score {
            font-size: 24px;
            font-weight: bold;
            color: #e74c3c;
            margin: 20px 0;
        }
        .button {
            background-color: #3498db;
            color: white;
            padding: 10px 15px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
            text-decoration: none;
            display: inline-block;
            margin-top: 20px;
        }
        .button:hover {
            background-color: #2980b9;
        }
        .rescued-animals {
            margin-top: 20px;
            padding: 15px;
            background-color: #eee;
            border-radius: 4px;
        }
        .animal-item {
            margin-bottom: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Rescue Complete!</h1>
        
        <div class="rescued-animals">
            <h2>Rescued Animals:</h2>
            {{ result_message }}
        </div>
        
        <div class="score">
            Your final score: {{ score }}
        </div>
        
        <a href="/" class="button">Play Again</a>
    </div>
</body>
</html>
"""

# Routes
@app.route('/')
def index():
    reset_score()  # Reset score , start from 0 at the beginning!
    return render_template_string(index_template)

@app.route('/welcome', methods=['POST'])
def welcome():
    username = request.form.get('username', '')
    
    if username.isdigit():
        return render_template_string(index_template, error="Please enter a valid name, not a number.")
    
    with tracer.start_as_current_span("welcome_page"):
        return render_template_string(welcome_template, 
            username=username,
            cats_names=', '.join(cat_names),
            cats_health=', '.join(map(str, cat_healthScore)),
            dogs_names=', '.join(dog_names),
            dogs_health=', '.join(map(str, dog_healthScore)),
            cows_names=', '.join(cow_names),
            cows_health=', '.join(map(str, cow_healthScore)),
            pigs_names=', '.join(pig_names),
            pigs_health=', '.join(map(str, pig_healthScore))
        )

@app.route('/rescue', methods=['POST'])
def rescue():
    count = int(request.form.get('rescue_count', 1))
    username = request.form.get('username', 'Player')
    
    if count < 1:
        return redirect('/')
    
    with tracer.start_as_current_span("rescue_selection"):
        return render_template_string(rescue_template, count=count, username=username)

@app.route('/result', methods=['POST'])
def result():
    animal_type = request.form.get('animal_type', '')
    count = int(request.form.get('count', 1))
    username = request.form.get('username', 'Player')
    
    with tracer.start_as_current_span("rescue_result"):
        # Track the animal rescue in Prometheus
        # Using Counter metrics for monitoring rescues
        RESCUE_COUNT = Counter('animal_rescue_count', 'Number of animals rescued', ['animal_type'])
        RESCUE_COUNT.labels(animal_type=animal_type).inc(count)
        
        result_message = ""
        
        if count == 1:
            if animal_type == 'cat':
                result_message = f"<div class='animal-item'>Cat's name: {cat_names[0]}, Health score: {cat_healthScore[0]}</div>"
            elif animal_type == 'dog':
                result_message = f"<div class='animal-item'>Dog's name: {dog_names[0]}, Health score: {dog_healthScore[0]}</div>"
            elif animal_type == 'cow':
                result_message = f"<div class='animal-item'>Cow's name: {cow_names[0]}, Health score: {cow_healthScore[0]}</div>"
            elif animal_type == 'pig':
                result_message = f"<div class='animal-item'>Pig's name: {pig_names[0]}, Health score: {pig_healthScore[0]}</div>"
        else:
            if animal_type == 'cats':
                names_list = cat_names[:count]
                health_list = cat_healthScore[:count]
                result_message = "<h3>Cats:</h3>"
                for i in range(count):
                    result_message += f"<div class='animal-item'>Name: {names_list[i]}, Health score: {health_list[i]}</div>"
            elif animal_type == 'dogs':
                names_list = dog_names[:count]
                health_list = dog_healthScore[:count]
                result_message = "<h3>Dogs:</h3>"
                for i in range(count):
                    result_message += f"<div class='animal-item'>Name: {names_list[i]}, Health score: {health_list[i]}</div>"
            elif animal_type == 'cows':
                names_list = cow_names[:count]
                health_list = cow_healthScore[:count]
                result_message = "<h3>Cows:</h3>"
                for i in range(count):
                    result_message += f"<div class='animal-item'>Name: {names_list[i]}, Health score: {health_list[i]}</div>"
            elif animal_type == 'pigs':
                names_list = pig_names[:count]
                health_list = pig_healthScore[:count]
                result_message = "<h3>Pigs:</h3>"
                for i in range(count):
                    result_message += f"<div class='animal-item'>Name: {names_list[i]}, Health score: {health_list[i]}</div>"
        
        final_score = score_user() * count  # Calculate score based on count
        
        return render_template_string(result_template, 
            result_message=result_message,
            score=final_score,
            username=username
        )

# Memory crash simulation function - commented out but can be enabled for testing
"""
def memory_crash():
    data = []
    counter = 0
    while True:
        data.append(" " * 10**6)  # Allocate 1MB of memory
        counter += 1
        print(f"Allocated {counter} MB of memory")
        time.sleep(0.1)
"""

# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)