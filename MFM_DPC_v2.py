# -*- coding: utf-8 -*-
"""
Created on Sun Apr 13 22:45:36 2025

@author: Akhil
"""

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os
from matplotlib.colors import rgb_to_hsv

# Load the image
image_path = "C:/Users/guruj/Downloads/vector_outputs/your_color_field_image3.png"  # Replace with your image path
image = Image.open(image_path)
image = image.convert('RGB')

# Convert the image to numpy array
image_array = np.array(image)

# Convert the RGB image array to normalized values between 0 and 1
image_array_normalized = image_array / 255.0

# Convert to HSV (hue, saturation, value)
image_hsv = rgb_to_hsv(image_array_normalized)

# Extract the hue and value channels
hue_channel = image_hsv[:, :, 0]
value_channel = image_hsv[:, :, 2]  # This is the brightness (value) channel

# Adjust hue so that north-west corresponds to green (0.52)
adjusted_hue_channel_correct = (hue_channel + 0.52) % 1  # Shift to make green (hue=0.75) correspond to South-West.

# Recalculate directions with the corrected hue values
adjusted_directions_correct = np.angle(np.exp(1j * 2 * np.pi * adjusted_hue_channel_correct), deg=True)

# Generate a grid of coordinates for quiver
Y, X = np.mgrid[0:image_array.shape[0]:15, 0:image_array.shape[1]:15]

# Get the U, V components based on the corrected directions
U_adjusted_correct = np.cos(np.radians(adjusted_directions_correct[::15, ::15]))
V_adjusted_correct = np.sin(np.radians(adjusted_directions_correct[::15, ::15]))

# Scale the arrow lengths based on the value (brightness) of the corresponding pixels
arrow_lengths = value_channel[::15, ::15]  # Use the value channel to scale the arrows

# Normalize the arrow lengths to a reasonable range
arrow_lengths_normalized = arrow_lengths / np.max(arrow_lengths)  # Normalize to [0, 1]

# Scale the U and V components by the normalized arrow lengths
U_scaled = U_adjusted_correct * arrow_lengths_normalized
V_scaled = V_adjusted_correct * arrow_lengths_normalized

# Create the "Output" directory if it doesn't exist
output_dir = "Output"
os.makedirs(output_dir, exist_ok=True)

# Plot the overlapped image with quiver arrows
fig, ax = plt.subplots(figsize=(image_array.shape[1] / 100, image_array.shape[0] / 100))  # Adjust figure size to image aspect ratio
ax.imshow(image_array)
ax.quiver(X, Y, U_scaled, V_scaled, angles='xy', scale_units='xy', scale=0.06, color='white', width=0.002)
plt.title("Vector Direction Map with Arrow Lengths Based on Brightness", fontsize=16)

# Save the overlapped image with arrows at 300 DPI
overlapped_image_path = os.path.join(output_dir, "overlapped_image.png")
plt.savefig(overlapped_image_path, dpi=300)
plt.close()

# Plot the arrow map alone (with black background)
fig, ax = plt.subplots(figsize=(image_array.shape[1] / 100, image_array.shape[0] / 100))  # Adjust figure size to image aspect ratio

# Set the figure background color to black
fig.patch.set_facecolor('black')

# Set the axes background color to black as well
ax.set_facecolor('black')

# Invert the y-axis to correct the vertical flip
ax.invert_yaxis()

# Plot the arrows on a black background
ax.quiver(X, Y, U_scaled, V_scaled, angles='xy', scale_units='xy', scale=0.06, color='white', width=0.002)
plt.title("Arrow Map Alone", fontsize=16, color='white')  # Make title text white for visibility

# Save the arrow map alone with black background at 300 DPI
arrow_map_path = os.path.join(output_dir, "arrow_map.png")
plt.savefig(arrow_map_path, dpi=300, bbox_inches='tight', pad_inches=0, facecolor='black')
plt.close()

print(f"Images saved in the '{output_dir}' folder.")
