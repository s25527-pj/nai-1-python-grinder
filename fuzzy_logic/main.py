import pygame
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import math

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Air Defense System Simulation")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Define fuzzy variables for the inputs and output

# Input 1: Distance of the missile
distance = ctrl.Antecedent(np.arange(0, 1001, 1), 'distance')
distance['near'] = fuzz.trapmf(distance.universe, [0, 0, 50, 200])
distance['moderate'] = fuzz.trimf(distance.universe, [100, 300, 500])
distance['far'] = fuzz.trapmf(distance.universe, [400, 700, 1000, 1000])

# Input 2: Speed of the missile
speed = ctrl.Antecedent(np.arange(0, 5, 0.1), 'speed')
speed['slow'] = fuzz.trapmf(speed.universe, [0, 0, 0.5, 1.5])
speed['medium'] = fuzz.trimf(speed.universe, [0.5, 1.5, 3.0])
speed['fast'] = fuzz.trapmf(speed.universe, [1.5, 3.5, 5.0, 5.0])

# Input 3: Angle of approach
angle = ctrl.Antecedent(np.arange(0, 181, 1), 'angle')
angle['small'] = fuzz.trapmf(angle.universe, [0, 0, 30, 60])
angle['medium'] = fuzz.trimf(angle.universe, [30, 60, 120])
angle['large'] = fuzz.trapmf(angle.universe, [90, 150, 180, 180])

# Output: Threat Level
threat_level = ctrl.Consequent(np.arange(0, 101, 1), 'threat_level')
threat_level['low'] = fuzz.trapmf(threat_level.universe, [0, 0, 20, 40])
threat_level['moderate'] = fuzz.trimf(threat_level.universe, [20, 50, 80])
threat_level['high'] = fuzz.trapmf(threat_level.universe, [60, 80, 100, 100])

# Updated rules for more granularity in near distances and extreme conditions
rules = [
    ctrl.Rule(distance['near'] & speed['slow'] & angle['small'], threat_level['moderate']),
    ctrl.Rule(distance['near'] & speed['slow'] & angle['medium'], threat_level['moderate']),
    ctrl.Rule(distance['near'] & speed['slow'] & angle['large'], threat_level['low']),
    ctrl.Rule(distance['near'] & speed['medium'] & angle['small'], threat_level['high']),
    ctrl.Rule(distance['near'] & speed['medium'] & angle['medium'], threat_level['high']),
    ctrl.Rule(distance['near'] & speed['medium'] & angle['large'], threat_level['moderate']),
    ctrl.Rule(distance['near'] & speed['fast'] & angle['small'], threat_level['high']),
    ctrl.Rule(distance['near'] & speed['fast'] & angle['medium'], threat_level['high']),
    ctrl.Rule(distance['near'] & speed['fast'] & angle['large'], threat_level['high']),

    # Added rule to ensure high threat level when missile is near with high speed
    ctrl.Rule(distance['near'] & speed['fast'], threat_level['high']),

    ctrl.Rule(distance['moderate'] & speed['slow'] & angle['small'], threat_level['moderate']),
    ctrl.Rule(distance['moderate'] & speed['slow'] & angle['medium'], threat_level['low']),
    ctrl.Rule(distance['moderate'] & speed['slow'] & angle['large'], threat_level['low']),
    ctrl.Rule(distance['moderate'] & speed['medium'] & angle['small'], threat_level['high']),
    ctrl.Rule(distance['moderate'] & speed['medium'] & angle['medium'], threat_level['moderate']),
    ctrl.Rule(distance['moderate'] & speed['medium'] & angle['large'], threat_level['moderate']),
    ctrl.Rule(distance['moderate'] & speed['fast'] & angle['small'], threat_level['high']),
    ctrl.Rule(distance['moderate'] & speed['fast'] & angle['medium'], threat_level['high']),
    ctrl.Rule(distance['moderate'] & speed['fast'] & angle['large'], threat_level['moderate']),

    # Additional high-threat conditions at moderate distances with high speed
    ctrl.Rule(distance['moderate'] & speed['fast'], threat_level['high']),

    ctrl.Rule(distance['far'] & speed['slow'] & angle['small'], threat_level['low']),
    ctrl.Rule(distance['far'] & speed['slow'] & angle['medium'], threat_level['low']),
    ctrl.Rule(distance['far'] & speed['slow'] & angle['large'], threat_level['low']),
    ctrl.Rule(distance['far'] & speed['medium'] & angle['small'], threat_level['moderate']),
    ctrl.Rule(distance['far'] & speed['medium'] & angle['medium'], threat_level['moderate']),
    ctrl.Rule(distance['far'] & speed['medium'] & angle['large'], threat_level['low']),
    ctrl.Rule(distance['far'] & speed['fast'] & angle['small'], threat_level['high']),
    ctrl.Rule(distance['far'] & speed['fast'] & angle['medium'], threat_level['moderate']),
    ctrl.Rule(distance['far'] & speed['fast'] & angle['large'], threat_level['moderate']),
]

# Control system and simulation setup
threat_ctrl = ctrl.ControlSystem(rules)
threat_simulation = ctrl.ControlSystemSimulation(threat_ctrl)


def calculate_threat(distance_value, speed_value, angle_value):
    """
    Calculates the threat level for a given distance, speed, and angle of approach.

    Parameters:
    - distance_value (float): The distance of the missile in kilometers.
    - speed_value (float): The speed of the missile in Mach.
    - angle_value (float): The angle of approach in degrees.

    Returns:
    - float: Calculated threat level percentage.
    """
    threat_simulation.input['distance'] = distance_value
    threat_simulation.input['speed'] = speed_value
    threat_simulation.input['angle'] = angle_value

    # Perform the calculation
    threat_simulation.compute()
    return threat_simulation.output['threat_level']


# Initial parameters for the missile
distance_value = 500  # Initial distance
speed_value = 5  # Speed in Mach
angle_value = 10  # Angle of approach in degrees

# Main game loop
running = True
target_position = (400, 300)  # Center of the screen as the base position

while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Calculate threat level
    threat_level_value = calculate_threat(distance_value, speed_value, angle_value)

    # Display threat level
    font = pygame.font.SysFont(None, 36)
    text = font.render(f"Threat Level: {threat_level_value:.2f}%", True, RED)
    screen.blit(text, (10, 10))

    # Calculate missile's position based on distance and angle
    missile_x = target_position[0] + distance_value * math.cos(math.radians(angle_value))
    missile_y = target_position[1] - distance_value * math.sin(math.radians(angle_value))

    # Draw the missile and base
    pygame.draw.circle(screen, BLUE, (int(missile_x), int(missile_y)), 10)  # Missile
    pygame.draw.circle(screen, GREEN, target_position, 20)  # Base

    # Update distance to simulate missile approaching
    distance_value -= 2
    if distance_value <= 0:
        distance_value = 1000  # Reset for continuous simulation

    # Refresh the screen
    pygame.display.flip()
    pygame.time.delay(50)

pygame.quit()
