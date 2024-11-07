"""
Air Defense System Simulation
Authors: Maciej Uzarski, Maksymilian Mrówka

Description:
This simulation demonstrates a fuzzy logic-based air defense system that calculates a threat level based on a missile's distance, speed, and angle of approach.
The system continuously calculates the threat level as the missile approaches a target. This project is intended to model how a threat level would change
under different missile approach conditions.

Environment Setup:
1. Navigate to the directory
    - cd path/to/fuzzy_logic

2. Install necessary dependencies:
    - pip install -r requirements.txt

3. Run the code:
   - Execute the script with `python main.py`

4. Controls:
   - Input fields for Distance (0-1000), Speed (0-5), and Angle (0-180) can be clicked and updated.
   - Press 'Update' to set the new values.

The simulation updates the missile's position and recalculates the threat level on each iteration, offering a real-time view of threat assessment based on proximity, speed, and trajectory.

"""

import pygame
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import math

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((1200, 800))
pygame.display.set_caption("Air Defense System Simulation")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Define fonts
font = pygame.font.SysFont(None, 36)

# Define fuzzy variables for the inputs and output

# Input 1: Distance of the missile
distance = ctrl.Antecedent(np.arange(0, 1001, 1), 'distance')
distance['near'] = fuzz.trapmf(distance.universe, [0, 0, 30, 100])
distance['moderate'] = fuzz.trimf(distance.universe, [80, 300, 500])
distance['far'] = fuzz.trapmf(distance.universe, [400, 700, 1000, 1000])

# Input 2: Speed of the missile
speed = ctrl.Antecedent(np.arange(0, 5, 0.1), 'speed')
speed['slow'] = fuzz.trapmf(speed.universe, [0, 0, 0.5, 1.0])
speed['medium'] = fuzz.trimf(speed.universe, [0.5, 1.5, 3.0])
speed['fast'] = fuzz.trapmf(speed.universe, [2.0, 3.5, 5.0, 5.0])

# Input 3: Angle of approach
angle = ctrl.Antecedent(np.arange(0, 181, 1), 'angle')
angle['small'] = fuzz.trapmf(angle.universe, [0, 0, 30, 60])
angle['medium'] = fuzz.trimf(angle.universe, [30, 60, 120])
angle['large'] = fuzz.trapmf(angle.universe, [90, 150, 180, 180])

# Output: Threat Level
threat_level = ctrl.Consequent(np.arange(0, 101, 1), 'threat_level')
threat_level['low'] = fuzz.trapmf(threat_level.universe, [0, 0, 10, 30])
threat_level['moderate'] = fuzz.trimf(threat_level.universe, [25, 50, 75])
threat_level['high'] = fuzz.trapmf(threat_level.universe, [60, 85, 100, 100])

# Updated rules for more granularity in near distances and extreme conditions
rules = [
    # Near distance with different speeds and angles for smoother increase
    ctrl.Rule(distance['near'] & speed['slow'] & angle['small'], threat_level['moderate']),
    ctrl.Rule(distance['near'] & speed['slow'] & angle['medium'], threat_level['moderate']),
    ctrl.Rule(distance['near'] & speed['slow'] & angle['large'], threat_level['low']),
    ctrl.Rule(distance['near'] & speed['medium'] & angle['small'], threat_level['high']),
    ctrl.Rule(distance['near'] & speed['medium'] & angle['medium'], threat_level['high']),
    ctrl.Rule(distance['near'] & speed['medium'] & angle['large'], threat_level['moderate']),
    ctrl.Rule(distance['near'] & speed['fast'] & angle['small'], threat_level['high']),
    ctrl.Rule(distance['near'] & speed['fast'] & angle['medium'], threat_level['high']),
    ctrl.Rule(distance['near'] & speed['fast'] & angle['large'], threat_level['high']),

    # Ensure high threat level when missile is near, regardless of angle, at high speed
    ctrl.Rule(distance['near'] & speed['fast'], threat_level['high']),
    ctrl.Rule(distance['near'] & speed['medium'], threat_level['high']),
    ctrl.Rule(distance['near'] & speed['slow'], threat_level['moderate']),

    # Moderate distance with different speeds and angles
    ctrl.Rule(distance['moderate'] & speed['slow'] & angle['small'], threat_level['moderate']),
    ctrl.Rule(distance['moderate'] & speed['slow'] & angle['medium'], threat_level['low']),
    ctrl.Rule(distance['moderate'] & speed['slow'] & angle['large'], threat_level['low']),
    ctrl.Rule(distance['moderate'] & speed['medium'] & angle['small'], threat_level['high']),
    ctrl.Rule(distance['moderate'] & speed['medium'] & angle['medium'], threat_level['moderate']),
    ctrl.Rule(distance['moderate'] & speed['medium'] & angle['large'], threat_level['moderate']),
    ctrl.Rule(distance['moderate'] & speed['fast'] & angle['small'], threat_level['high']),
    ctrl.Rule(distance['moderate'] & speed['fast'] & angle['medium'], threat_level['high']),
    ctrl.Rule(distance['moderate'] & speed['fast'] & angle['large'], threat_level['moderate']),

    # Additional rule to ensure high threat level at moderate distance with high speed
    ctrl.Rule(distance['moderate'] & speed['fast'], threat_level['high']),

    # Far distance with different speeds and angles
    ctrl.Rule(distance['far'] & speed['slow'] & angle['small'], threat_level['low']),
    ctrl.Rule(distance['far'] & speed['slow'] & angle['medium'], threat_level['low']),
    ctrl.Rule(distance['far'] & speed['slow'] & angle['large'], threat_level['low']),
    ctrl.Rule(distance['far'] & speed['medium'] & angle['small'], threat_level['moderate']),
    ctrl.Rule(distance['far'] & speed['medium'] & angle['medium'], threat_level['moderate']),
    ctrl.Rule(distance['far'] & speed['medium'] & angle['large'], threat_level['low']),
    ctrl.Rule(distance['far'] & speed['fast'] & angle['small'], threat_level['high']),
    ctrl.Rule(distance['far'] & speed['fast'] & angle['medium'], threat_level['moderate']),
    ctrl.Rule(distance['far'] & speed['fast'] & angle['large'], threat_level['moderate']),

    # Added rule to push high threat when near distance is reached
    ctrl.Rule(distance['near'], threat_level['high'])
]

# Control system and simulation setup
threat_ctrl = ctrl.ControlSystem(rules)
threat_simulation = ctrl.ControlSystemSimulation(threat_ctrl)

# Missile parameters
distance_value = 500
speed_value = 3
angle_value = 90

# Text input fields
distance_input = ""
speed_input = ""
angle_input = ""
active_input = None  # Track active input field
button_rect = pygame.Rect(950, 600, 150, 40)  # "Update" button position

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

    if distance_value < 20 and speed_value > 4.5:
        return 100.0

    threat_simulation.input['distance'] = distance_value
    threat_simulation.input['speed'] = speed_value
    threat_simulation.input['angle'] = angle_value

    # Perform the calculation
    threat_simulation.compute()
    return threat_simulation.output['threat_level']


def draw_text_input(label, text, x, y):
    """
    Draws a text input field with a label on the screen.

    Parameters:
    - label (str): Label text for the input field.
    - text (str): The current text in the input field.
    - x (int): X-coordinate of the input field.
    - y (int): Y-coordinate of the input field.
    """
    label_surface = font.render(label, True, BLACK)
    text_surface = font.render(text, True, BLACK)
    screen.blit(label_surface, (x, y - 30))
    pygame.draw.rect(screen, WHITE, pygame.Rect(x, y, 140, 40))  # Input field background
    pygame.draw.rect(screen, BLACK, pygame.Rect(x, y, 140, 40), 2)  # Input field border
    # screen.blit(label_surface, (x - 100, y + 5))
    screen.blit(text_surface, (x + 5, y + 5))

# Main game loop
running = True
target_position = (600, 400)  # Center of the screen as the base position

while running:
    screen.fill(WHITE)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):  # Check if "Update" button is clicked
                try:
                    distance_value = float(distance_input) if distance_input else distance_value
                    speed_value = float(speed_input) if speed_input else speed_value
                    angle_value = float(angle_input) if angle_input else angle_value
                except ValueError:
                    pass  # Ignore invalid input
            elif pygame.Rect(900, 100, 140, 40).collidepoint(event.pos):
                active_input = "distance"
            elif pygame.Rect(900, 200, 140, 40).collidepoint(event.pos):
                active_input = "speed"
            elif pygame.Rect(900, 300, 140, 40).collidepoint(event.pos):
                active_input = "angle"
            else:
                active_input = None  # Deselect input field

        elif event.type == pygame.KEYDOWN and active_input:
            if event.key == pygame.K_BACKSPACE:
                if active_input == "distance":
                    distance_input = distance_input[:-1]
                elif active_input == "speed":
                    speed_input = speed_input[:-1]
                elif active_input == "angle":
                    angle_input = angle_input[:-1]
            else:
                if active_input == "distance":
                    distance_input += event.unicode
                elif active_input == "speed":
                    speed_input += event.unicode
                elif active_input == "angle":
                    angle_input += event.unicode

    # Calculate threat level
    threat_level_value = calculate_threat(distance_value, speed_value, angle_value)

    # Display threat level
    text = font.render(f"Threat Level: {threat_level_value:.2f}%", True, RED)
    screen.blit(text, (10, 10))

    # Display missile position
    missile_x = target_position[0] + distance_value * math.cos(math.radians(angle_value))
    missile_y = target_position[1] - distance_value * math.sin(math.radians(angle_value))
    pygame.draw.circle(screen, BLUE, (int(missile_x), int(missile_y)), 10)  # Missile
    pygame.draw.circle(screen, GREEN, target_position, 20)  # Base

    # Draw text input fields and labels
    draw_text_input("Distance (0-1000, +/-1):", distance_input, 900, 100)
    draw_text_input("Speed (0-5, +/- 0.1):", speed_input, 900, 200)
    draw_text_input("Angle (0-180, +/-1):", angle_input, 900, 300)

    # Draw "Update" button
    pygame.draw.rect(screen, GRAY, button_rect)
    button_text = font.render("Update", True, BLACK)
    screen.blit(button_text, (button_rect.x + 20, button_rect.y + 5))

    # Update distance to simulate missile approaching
    distance_value -= 6
    if distance_value <= 0:
        distance_value = 1000  # Reset for continuous simulation

    # Refresh the screen
    pygame.display.flip()
    pygame.time.delay(50)

pygame.quit()
