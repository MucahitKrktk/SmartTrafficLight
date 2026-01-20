import time
from tracker import adjust_traffic_light

# Main simulation loop
def simulate_intersection():
    """
    Simulate an intersection by manually entering vehicle and pedestrian densities.
    """
    while True:
        try:
            # Input vehicle and pedestrian densities
            vehicle_density = float(input("Enter vehicle density (0.0 to 1.0): "))
            pedestrian_density = float(input("Enter pedestrian density (0.0 to 1.0): "))

            if not (0.0 <= vehicle_density <= 1.0 and 0.0 <= pedestrian_density <= 1.0):
                print("Densities must be between 0.0 and 1.0. Try again.")
                continue

            # Adjust traffic light durations
            green_duration = adjust_traffic_light(vehicle_density, pedestrian_density)

            # Simulate green light period
            print("\nGreen light ON")
            time.sleep(green_duration)

            # Simulate red light period
            red_duration = 60 - green_duration  # Total cycle duration fixed at 60 seconds
            print("Green light OFF - Red light ON")
            time.sleep(red_duration)

        except ValueError:
            print("Invalid input. Please enter a number between 0.0 and 1.0.")

if __name__ == "__main__":
    print("Starting Smart Traffic Light Management System...")
    simulate_intersection()
