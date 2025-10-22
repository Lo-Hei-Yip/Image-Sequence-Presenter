import pygame
import os
import random
import csv
from datetime import datetime

# Variables for customization
folder = 'intermediate'  # Folder containing the PNG images
show_time = 2  # Time to show each image (in seconds)
imagine_time = 2  # Time for imagine phase (black screen, in seconds)
rest_total = 2  # Total rest time (in seconds)
rest_text_time = 1  # Time to show "REST" text (in seconds, if 0, no text shown)

# Cropping variables to remove black background
crop_top = 1230  # Pixels to crop from top
crop_bottom = 1230  # Pixels to crop from bottom  
crop_left = 3000  # Pixels to crop from left
crop_right = 3000  # Pixels to crop from right

# Initial black screen time
initial_black_screen_time = 3  # Seconds of black screen at start (in seconds)

# Get list of PNG images in the folder
images = [f for f in os.listdir(folder) if f.endswith('.png')]
if not images:
    raise ValueError("No PNG images found in the folder.")

# Randomize the order
random.shuffle(images)

# Initialize Pygame
pygame.init()

# Set up full screen display
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_width, screen_height = screen.get_size()
pygame.display.set_caption('Image Sequence Video')

# Colors
black = (0, 0, 0)
white = (255, 255, 255)

# Dictionary to store imagine start and end times for each image
times = {}

# Font for "REST" text, scaled based on screen height
font_size = screen_height // 10
font = pygame.font.Font(None, font_size)

# Create output folder if it doesn't exist
output_folder = 'output'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Generate CSV filename with folder name and current timestamp
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
csv_filename = os.path.join(output_folder, f'{folder}_output_{timestamp}.csv')

# Show initial black screen
print("Starting in...")
for i in range(initial_black_screen_time, 0, -1):
    print(f"{i}...")
    screen.fill(black)
    pygame.display.flip()
    pygame.time.wait(1000)
print("Starting sequence!")

# Process each image in the randomized order
for img_file in images:
    title = os.path.splitext(img_file)[0]
    
    # Load image
    img_path = os.path.join(folder, img_file)
    img = pygame.image.load(img_path)
    
    # Crop the image to remove black background
    img_width, img_height = img.get_size()
    cropped_width = img_width - crop_left - crop_right
    cropped_height = img_height - crop_top - crop_bottom
    
    # Create a new surface for the cropped image
    cropped_img = pygame.Surface((cropped_width, cropped_height))
    cropped_img.blit(img, (0, 0), (crop_left, crop_top, cropped_width, cropped_height))
    
    # Calculate scaling to fit screen while maintaining aspect ratio
    scale_x = screen_width / cropped_width
    scale_y = screen_height / cropped_height
    scale = min(scale_x, scale_y)  # Use min to ensure entire image fits
    
    # Scale the cropped image
    scaled_width = int(cropped_width * scale)
    scaled_height = int(cropped_height * scale)
    scaled_img = pygame.transform.smoothscale(cropped_img, (scaled_width, scaled_height))
    
    # Center the image on screen
    x_pos = (screen_width - scaled_width) // 2
    y_pos = (screen_height - scaled_height) // 2
    
    # Show the image
    screen.fill(black)  # Clear with black background
    screen.blit(scaled_img, (x_pos, y_pos))
    pygame.display.flip()
    
    # Record the actual display time for the image
    image_start = datetime.now()
    pygame.time.wait(show_time * 1000)  # Wait in milliseconds
    
    # Imagine phase: black screen
    screen.fill(black)
    pygame.display.flip()
    start = datetime.now()
    pygame.time.wait(imagine_time * 1000)
    end = datetime.now()
    
    # Store times (format to milliseconds)
    start_str = start.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    end_str = end.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    times[title] = (start_str, end_str)
    
    # Rest phase: Show "REST" text for rest_text_time, then black for remaining time
    # Both within the total rest_total time
    if rest_text_time > 0:
        # Show "REST" text for rest_text_time seconds
        screen.fill(black)
        text = font.render("REST", True, white)
        text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.wait(rest_text_time * 1000)
    
    # Remaining rest time as plain black screen (within the total rest_total)
    remaining_rest = rest_total - rest_text_time
    if remaining_rest > 0:
        screen.fill(black)
        pygame.display.flip()
        pygame.time.wait(remaining_rest * 1000)

# Quit Pygame
pygame.quit()

# Prepare CSV data with proper column structure
headers = []
data = []

# Add each start and end time as separate columns
for img_file in images:  # Use the shuffled order
    title = os.path.splitext(img_file)[0]
    headers.append(f'imagine_{title}_start_time')
    headers.append(f'imagine_{title}_end_time')
    data.append(times[title][0])
    data.append(times[title][1])

# Write to CSV with comma delimiter (standard CSV format)
with open(csv_filename, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)  # Remove delimiter parameter to use default comma
    writer.writerow(headers)
    writer.writerow(data)

print(f"CSV file '{csv_filename}' has been generated in the '{output_folder}' folder.")
print(f"Processed {len(images)} images in random order.")

# Display the CSV structure for verification
print("\nCSV Structure Preview:")
print("Number of columns:", len(headers))
print("First few columns:", headers[:4])
print("First few data points:", data[:4])