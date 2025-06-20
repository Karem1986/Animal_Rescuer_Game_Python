from opentelemetry import trace
from opentelemetry.trace import TracerProvider
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from test import cows, pigs, dogs, cats

# For monitoring with Grafana
from prometheus_client import start_http_server

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

# Add Error handling for the whole program 

user_name = input('Please enter your name')

# check for number
def is_number():
    check_for_number = user_name.isnumeric()
    return check_for_number

# Assign score based on how many pets are rescued
SCORE = 0
def score_user(rescued_count):
    global SCORE
    SCORE += rescued_count
    return SCORE

# data
cat_names = ['Kermit', 'Leia', 'Bobby', 'Tiger', 'Asos', 'Guizmo', 'Suffo', 'Marraket', 'Kiki', 'Ursula']
cat_age = [3, 8, 12, 1, 4, 8, 2, 2, 8, 4]
cat_healthScore = [3, 6, 9, 7, 5, 2, 1, 1, 2, 3]
cow_names = ['Bella', 'Leia', 'Madonna', 'Bobby', 'Tiger', 'Asos', 'Guizmo', 'Suffo', 'Marraket', 'Kiki']
cow_age = [3, 8, 12, 1, 4, 8, 2, 2, 8, 4]
cow_healthScore = [3, 6, 9, 7, 5, 2, 1, 1, 2, 3]
pig_names = ['Babe', 'Tomillito', 'Patrizio', 'Lindo', 'Asos', 'Guizmo', 'Suffo', 'Marraket', 'Kiki', 'Ursula']
pig_age = [3, 8, 12]
pig_healthScore = [3, 6, 9, 7, 5, 2, 1, 1, 2, 3]
dog_names = ['Kermit', 'Leia', 'Bobby', 'Tiger', 'Asos', 'Guizmo', 'Suffo', 'Marraket', 'Kiki', 'Ursula']
dog_age = [3, 8, 12, 1, 4, 8, 2, 2, 8, 4]
dog_healthScore = [3, 6, 9, 7, 5, 2, 1, 1, 2, 3]

# Testing the functions
print("cows", cows(cow_names, cow_healthScore))

def display_rescued_animal(animal_type, names, health_scores):
    # Create a string to display the animals
    result = f"These are the {animal_type} in the shelter:\n"
    result += f"Names: {names}\n"
    result += f"Health scores: {health_scores}\n"
    return result

def rescue():
    # Input validation
    if is_number():
        print('Not a name, please enter your name')
        return  # Exit the function if the name is invalid

    # Greet the user
    greet = f"Welcome {user_name}! You will be in no time a real Hero Animal Rescuer!"
    print(greet)

    # Game explanation
    game_explt = "Choose how many animals you want to rescue. You will receive a score from 1 to 10. More pets == higher score."
    print(game_explt)

# Display options for the user
    print(display_rescued_animal("cats", cat_names, cat_healthScore))
    print(display_rescued_animal("dogs", dog_names, dog_healthScore))
    print(display_rescued_animal("cows", cow_names, cow_healthScore))
    print(display_rescued_animal("pigs", pig_names, pig_healthScore))

    # Ask how many pets the user wants to rescue
    while True:
        howManyrescue = input("How many animals can you rescue? ")
        if howManyrescue.isdigit():
            numberOfRescues = int(howManyrescue)
            break
        else:
            print("Please enter a valid number.")

# Handle rescue logic
    if numberOfRescues == 0:
      print("Minimum to rescue one pet!")
    elif numberOfRescues >= 1:
      print(f"You have chosen to rescue {numberOfRescues} animals.")
      choice = input("Do you want to rescue cats, cows, pigs or dogs? ").strip().lower()
      
      if choice == 'cats':
        print("cats", cats(cat_names[:numberOfRescues], cat_healthScore[:numberOfRescues]))
      elif choice == 'cows':
        print("cows", cows(cow_names[:numberOfRescues], cow_healthScore[:numberOfRescues]))
      elif choice == 'pigs':
        print("pigs", pigs(pig_names[:numberOfRescues], pig_healthScore[:numberOfRescues]))
      elif choice == 'dogs':
        print("dogs", dogs(dog_names[:numberOfRescues], dog_healthScore[:numberOfRescues]))

    return f"Your score is: {score_user(numberOfRescues)}"

# Implementing Error handling for the rescue function
try:
    print(rescue())
except Exception as e:
    print(f"An error occurred: {e}")
    # Optionally, you can log the error or handle it in a specific way
else:
    print("Rescue operation completed successfully!")
finally:
    print("Thank you for playing! Your rescue mission is complete.")