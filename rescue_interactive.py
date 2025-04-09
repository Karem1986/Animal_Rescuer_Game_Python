from flask import Flask
from opentelemetry import trace
from opentelemetry.trace import TracerProvider
from opentelemetry.sdk.trace import export, TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
import time

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

# # Create a function to simulate a memory crash based on a heap overflow-The whole computer
# def memory_crash():
#     """Function to simulate memory consumption."""
#     data = []
#     counter = 0
#     while True:
#         data.append(" " * 10**6)  # Allocate 1MB of memory
#         counter += 1
#         print(f"Allocated {counter} MB of memory")
#         time.sleep(0.1)

# if __name__ == "__main__":
#     with tracer.start_as_current_span("memory_crash_span"):
#         memory_crash()

user_name = input('Please enter your name')

# check for number
def is_number():
    check_for_number = user_name.isnumeric()
    return check_for_number

# Assign score based on how many pets are rescued
SCORE = 0
def score_user():
   global SCORE
   SCORE +=3
   return SCORE

# data
cat_names = ['Kermit', 'Leia', 'Bobby', 'Tiger', 'Asos', 'Guizmo', 'Suffo', 'Marraket', 'Kiki', 'Ursula']
cat_age = [3, 8, 12, 1, 4, 8, 2, 2, 8, 4]
cow_names = ['Kermit', 'Leia', 'Bobby', 'Tiger', 'Asos', 'Guizmo', 'Suffo', 'Marraket', 'Kiki', 'Ursula']
cow_age = [3, 8, 12, 1, 4, 8, 2, 2, 8, 4]
pig_names = ['Kermit', 'Leia', 'Bobby', 'Tiger', 'Asos', 'Guizmo', 'Suffo', 'Marraket', 'Kiki', 'Ursula']
pig_age = [3, 8, 12, 1, 4, 8, 2, 2, 8, 4]
pig_healthScore = [3, 6, 9, 7, 5, 2, 1, 1, 2, 3]
cow_healthScore = [3, 6, 9, 7, 5, 2, 1, 1, 2, 3]
cat_healthScore = [3, 6, 9, 7, 5, 2, 1, 1, 2, 3]
dog_names = ['Kermit', 'Leia', 'Bobby', 'Tiger', 'Asos', 'Guizmo', 'Suffo', 'Marraket', 'Kiki', 'Ursula']
dog_age = [3, 8, 12, 1, 4, 8, 2, 2, 8, 4]
dog_healthScore = [3, 6, 9, 7, 5, 2, 1, 1, 2, 3]

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
    game_explt = "Choose how many cats or dogs you want to rescue. You will receive a score from 1 to 10. More pets == higher score."
    print(game_explt)

  # Display options for the user
# Display options for the user
    print("You can rescue:\n" + display_rescued_animal("cats", cat_names, cat_healthScore))
    print("You can rescue:\n" + display_rescued_animal("dogs", dog_names, dog_healthScore))

    # Ask how many pets the user wants to rescue
    while True:
        howManyrescue = input("How many pets can you rescue? ")
        if howManyrescue.isdigit():
            toInt = int(howManyrescue)
            break
        else:
            print("Please enter a valid number.")

    # Handle rescue logic
    if toInt == 0:
        print("Minimum to rescue one pet!")
    elif toInt == 1:
        pet = input("A cat or a dog? ").strip().lower()
        if pet == 'cat':
            print(f"The cat's name is: {cat_names[0]}, Health score: {cat_healthScore[0]}, Your score: {score_user()}")
        elif pet == 'dog':
            print(f"The dog's name is: {dog_names[0]}, Health score: {dog_healthScore[0]}, Your score: {score_user()}")
        else:
            print("Invalid choice. Please choose 'cat' or 'dog'.")
    else:
        choice = input("Do you want to rescue cats or dogs? ").strip().lower()
    if choice == 'cats':
       display_rescued_animal("cats", cat_names[:2], cat_healthScore[:2])
    elif choice == 'dogs':
      display_rescued_animal("dogs", dog_names[:2], dog_healthScore[:2])
    elif choice == 'both':
      display_rescued_animal("both cats and dogs", cat_names[:2] + dog_names[:2], cat_healthScore[:2] + dog_healthScore[:2])
    else:
      print("Invalid choice. Please choose 'cats', 'dogs' or 'both'.")

    # Create a list of rescued animals (optional)
    rescued = []
    for a, name in enumerate(cat_names):
      if choice == 'cat':
        rescued.append({'name': name, 'age': cat_age[a], 'health points': cat_healthScore[a] })
      if choice == 'dog':
        rescued.append({'name': name, 'age': dog_age[a], 'health points': dog_healthScore[a] })
      if choice == 'both':
        rescued.append({'name': cat_names[a], 'age': cat_age[a], 'health points': cat_healthScore[a] })
        rescued.append({'name': name, 'age': dog_age[a], 'health points': dog_healthScore[a] })

    return rescued

print(rescue())