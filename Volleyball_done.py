import pygame
import math
import csv
import numpy as np
from sklearn.neighbors import KNeighborsRegressor

# Read data from the CSV file
coordinates = []
times = []

with open("C:\\Users\\Ashish\\Desktop\\AIML\\volleyball_data.csv", mode='r') as file:
    reader = csv.reader(file)
    next(reader)  # Skip the header row
    for row in reader:
        x_coord, y_coord, time = map(int, row)
        coordinates.append((x_coord, y_coord))
        times.append(time)

# Convert lists to NumPy arrays
X = np.array(coordinates)[:, 1].reshape(-1, 1)  # Y_coordinates as features
y_x = np.array(coordinates)[:, 0]  # X_coordinates
y_time = np.array(times)  # Times

# Create kNN models for x-coordinate and time prediction
knn_x = KNeighborsRegressor(n_neighbors=3, weights='distance')
knn_time = KNeighborsRegressor(n_neighbors=3, weights='distance')

# Fit the models
knn_x.fit(X, y_x)
knn_time.fit(X, y_time)

# Function to predict x-coordinate and time based on a given y-coordinate
def predict_x_time(y_coordinate):
    x_coordinate_pred = knn_x.predict(np.array([[y_coordinate]]))
    time_pred = knn_time.predict(np.array([[y_coordinate]]))
    return x_coordinate_pred[0], time_pred[0]


# Initializing pygame
pygame.init()

# Displaying a window of height and width
window_width = 1200
window_height = 800
window = pygame.display.set_mode((window_width, window_height))

# Setting name for window
pygame.display.set_caption('High Set')

# Initial position, velocity, and angle of the ball
initial_velocity = 125
angle = math.pi / 3  # 45 degrees
g = 9.8

# Predict x_value and time_value using the machine learning model
y_coordinate = 320  # Example y-coordinate to predict the x-coordinate and time
x_value, time_value = predict_x_time(y_coordinate)

running = True
x = 0
y = window_height

x_value = int(x_value) + 297
time_value = int(time_value) + 2000

# Initial position and velocity of the stickman
stickman_x = 0
stickman_y = 530
stickman_velocity_x = 0.35  # Initial velocity along x-axis
stickman_velocity_y = 0  # Initial velocity along y-axis
jumped_once = False

# Define colors
BLACK = (0, 0, 0)

# Initialize font object
font = pygame.font.SysFont(None, 36)  # You can adjust the font size as needed

# Keep game running till running is true
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    window.fill((255, 255, 255))
    
    # Draw the rectangle
    pygame.draw.rect(window, (0, 0, 0), (0, 300, 1200, 4))

    # Calculate the position of the ball based on the equation
    y = x * math.tan(angle) - (g * x ** 2) / (2 * initial_velocity ** 2 * math.cos(angle) ** 2)

    # Update stickman position based on velocity
    stickman_x += stickman_velocity_x
    
    # Check if stickman reached stopping point
    if stickman_x >= x_value and not jumped_once:
        # Stop stickman's x-axis movement
        stickman_velocity_x = 0
        # Set jump velocity
        stickman_velocity_y = -20
        jumped_once = True

    # Apply gravity to the stickman during jump
    if jumped_once:
        stickman_velocity_y += g / 14
        stickman_y += stickman_velocity_y

    # Ensure the stickman doesn't go below the ground
    if stickman_y > 530:
        stickman_y = 530
        stickman_velocity_y = 0

    # Draw the stickman
    # Head
    pygame.draw.circle(window, BLACK, (stickman_x, stickman_y), 10)
    # Body
    pygame.draw.line(window, BLACK, (stickman_x, stickman_y + 10), (stickman_x, stickman_y + 50), 2)
    # Arms
    pygame.draw.line(window, BLACK, (stickman_x, stickman_y + 20), (stickman_x - 20, stickman_y + 30), 2)
    pygame.draw.line(window, BLACK, (stickman_x, stickman_y + 20), (stickman_x + 20, stickman_y + 30), 2)
    # Legs
    pygame.draw.line(window, BLACK, (stickman_x, stickman_y + 50), (stickman_x - 15, stickman_y + 80), 2)
    pygame.draw.line(window, BLACK, (stickman_x, stickman_y + 50), (stickman_x + 15, stickman_y + 80), 2)

    # Draw the ball
    # Calculate the position of the circle
    cx = window_width - int(x)
    cy = int(window_height + 20 - y)
    pygame.draw.circle(window, (255, 0, 0), (cx, cy), 20)

    # Collision detection
    distance_centers = math.sqrt((cx - stickman_x) ** 2 + (cy - stickman_y) ** 2)
    sum_radii = 30  # Assuming the sum of radii of stickman's head and ball is 30
    collision = distance_centers <= sum_radii

    # Display collision status on the screen
    collision_text = font.render("Collision: " + str(collision), True, (0, 0, 0))  # Render collision status
    collision_text_rect = collision_text.get_rect(center=(window_width // 2, window_height // 2))  # Center text

    # Update collision text when collision occurs
    if collision:
        collision_text = font.render("Collision: True", True, (255, 0, 0))  # Render collision status as True

    window.blit(collision_text, collision_text_rect)  # Blit text onto the screen
     # Draw the circle indicating jump
    pygame.draw.circle(window, (0, 255, 0), (30, 30), 30) if jumped_once else pygame.draw.circle(window, (255, 0, 0),
                                                                                             (30, 30), 30)
    pygame.display.update()

    # Move the simulation forward
    x += 1
    pygame.time.delay(2)

    # Check if the simulation should end
    if x > window_width:
        running = False

pygame.quit()

