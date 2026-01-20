# tracker.py

# Adjustable weights for vehicle and pedestrian density
VEHICLE_WEIGHT = 0.7
PEDESTRIAN_WEIGHT = 0.3

# Function to calculate priority score
def calculate_priority(vehicle_density, pedestrian_density):
    """
    Calculate the priority score based on vehicle and pedestrian densities.

    P = (wv * Dv) + (wp * Dp)
    """
    priority_score = (VEHICLE_WEIGHT * vehicle_density) + (PEDESTRIAN_WEIGHT * pedestrian_density)
    return priority_score

# Function to adjust traffic light duration
def adjust_traffic_light(vehicle_density, pedestrian_density):
    """
    Adjust traffic light durations based on priority scores.
    """
    priority_score = calculate_priority(vehicle_density, pedestrian_density)

    # Calculate green light duration proportionally (scaling factor of 5 for demonstration)
    green_light_duration = max(10, min(60, int(priority_score * 5)))  # Duration between 10 and 60 seconds

    print(f"Vehicle Density: {vehicle_density}, Pedestrian Density: {pedestrian_density}")
    print(f"Priority Score: {priority_score:.2f}")
    print(f"Green Light Duration: {green_light_duration} seconds")

    return green_light_duration
