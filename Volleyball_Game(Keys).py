import pygame
import math
import csv

# initializing imported module
pygame.init()

# displaying a window of height and width
window_width = 1200
window_height = 600
window = pygame.display.set_mode((window_width, window_height))

# Setting name for window
pygame.display.set_caption('High Set')

# initial position, velocity, and angle of the ball
initial_velocity = 35
angle = math.pi / 2.5  # 45 degrees
g = 1

# Lists to store the values of x and y
x_values = [0] * 5
y_values = []

# initial position and velocity of the rectangle
rect_x = 300
rect_y = 530
rect_width = 25
rect_height = 60
rect_velocity = 0.1

# Game loop
# Run the game for 5 iterations
for index in range(5):
    running = True
    x = 0
    y = window_height

    # initial position of the rectangle for each iteration
    if index > 0:
        rect_x = rect_x_end
        rect_y = rect_y_end
        

    rect_width = 30
    rect_height = 70

    # Boolean to track if the rectangle has moved
    rectangle_moved = False

    # Boolean to track if the keys are held down
    left_pressed = False
    right_pressed = False
    check = 0
    count = 100
    upPressed = False

    elapsed_time = 0
    # keep game running till running is true
    while running:
        elapsed_time = pygame.time.get_ticks()
        # Check for event if user has pushed any event in queue
        for event in pygame.event.get():
            # if event is of type quit then set running bool to false
            if event.type == pygame.QUIT:
                running = False
            # If a key is pressed
            elif event.type == pygame.KEYDOWN:
                # If the key is "UP" arrow and the rectangle hasn't moved yet
                if (event.key == pygame.K_UP and not rectangle_moved):
                    # Shrink the rectangle size
                    upPressed = True
                    rectangle_moved = True
                    
                    # Store the time when the "UP" arrow key is clicked
                    up_time = pygame.time.get_ticks() - elapsed_time
                    print(up_time)
                    y_values.append(up_time)
                    
                # If the key is "LEFT" arrow
                elif event.key == pygame.K_LEFT:
                    # Set the left arrow key state to True
                    left_pressed = True
                # If the key is "RIGHT" arrow
                elif event.key == pygame.K_RIGHT:
                    # Set the right arrow key state to True
                    right_pressed = True
            # If a key is released
            elif event.type == pygame.KEYUP:
                # If the key is "LEFT" arrow
                if event.key == pygame.K_LEFT:
                    # Set the left arrow key state to False
                    left_pressed = False
                # If the key is "RIGHT" arrow
                elif event.key == pygame.K_RIGHT:
                    # Set the right arrow key state to False
                    right_pressed = False

        
        
        # Move the rectangle left if the left arrow key is pressed
        if left_pressed:
            rect_x -= 2
        # Move the rectangle right if the right arrow key is pressed
        if right_pressed:
            rect_x += 2
            
        if(upPressed and count >= 0 and count%10 == 0):
            rect_height -= 1
            rect_width -= 1
            if(count < 1):
                # Make the rectangle jump by giving it an initial upward velocity
                rect_velocity = -10
                # Set the flag to True to indicate that the rectangle has moved
                rectangle_moved = True
            
            
        if(upPressed and count>=0):
            count -= 2
        
        # Fill the window with a white background
        window.fill((255, 255, 255))

        # Calculate the new position of the ball based on the equation
        y = x * math.tan(angle) - (g * x ** 2) / (2 * initial_velocity ** 2 * math.cos(angle) ** 2)

        # Apply gravity to the rectangle
        rect_y += rect_velocity / 1.9
        rect_velocity += g / 10

        # Make sure the rectangle doesn't go below the ground
        if rect_y > 530:
            rect_y = 530
            rect_velocity = 0

        # Draw the rectangle
        pygame.draw.rect(window, (100, 0, 100), (rect_x, rect_y, rect_width, rect_height))
        pygame.draw.rect(window, (0, 0, 0), (0, 300, 1200, 4))

        cx = window_width + 100 - int(x)
        cy = window_height - y
        # Draw a circle in the calculated position
        pygame.draw.circle(window, (0, 100, 25), (cx, cy), 20)

        if (cx > rect_x - 20 and cx < rect_x + 20) and (rect_y < cy + 5 and rect_y > cy - 5) and (cy < 300):
            check = 1
            # Store the value of x when the circle turns green
            x_values[index] = (rect_x, window_height - rect_y)
            print(rect_x, window_height - rect_y)
        else:
            x_values[index] = (0,0)
       
        if check:
            pygame.draw.circle(window, (0, 255, 0), (30, 30), 30)  # Turn the circle green
        else:
            pygame.draw.circle(window, (255, 0, 0), (30, 30), 30)  # Turn the circle re

        # Update the display
        pygame.display.update()

        # Increment x to simulate motion along the x-axis
        x += 1

        # Add some delay to see the motion
        pygame.time.delay(3)

        # Store the position of the rectangle at the end of each iteration
        rect_x_end = rect_x
        rect_y_end = rect_y

        # Quit when the ball goes beyond the window width
        if x > window_width:
            running = False

# Quit Pygame
pygame.quit()
print(x_values)
# Append the stored values of x, y, and time to a CSV file
with open("C:\\Users\\Ashish\\Desktop\\AIML\\volleyball_data.csv", mode='a', newline='') as file:
    writer = csv.writer(file)
    for x_value, up_time in zip(x_values, y_values):
        writer.writerow([x_value[0], x_value[1], up_time])
