import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from skimage.draw import line


def process_image(image_path, start_point, end_point, num_lines_to_average=5):
    """
    Process a single image to extract and average the intensity profile along the specified lines.
    """
    # Load the BMP image and convert to grayscale
    img = Image.open(image_path).convert('L')

    # Convert to NumPy array
    img_array = np.array(img)

    # Define the range of offsets for parallel lines
    offset_range = range(-num_lines_to_average // 2, num_lines_to_average // 2 + 1)

    # Initialize an empty list to store intensities of all lines
    all_intensities = []

    # Loop over all offset lines to gather pixel intensities
    for offset in offset_range:
        # Offset the start and end points horizontally (x-direction)
        start_offset = (start_point[0], start_point[1] + offset)  # Adding offset to the column (x-axis)
        end_offset = (end_point[0], end_point[1] + offset)  # Adding offset to the column (x-axis)

        # Ensure points are within bounds
        if (0 <= start_offset[1] < img_array.shape[1]) and (0 <= end_offset[1] < img_array.shape[1]):
            # Extract the line coordinates
            rr, cc = line(start_offset[0], start_offset[1], end_offset[0], end_offset[1])

            # Clip the coordinates to stay within the image boundaries
            rr = np.clip(rr, 0, img_array.shape[0] - 1)
            cc = np.clip(cc, 0, img_array.shape[1] - 1)

            # Extract the intensities along the line
            intensities = img_array[rr, cc]
            all_intensities.append(intensities)

    # Convert the list of intensities to a NumPy array for easier manipulation
    all_intensities = np.array(all_intensities)

    # Calculate the average intensity profile by averaging across all lines
    average_intensity = np.mean(all_intensities, axis=0)

    return img_array, average_intensity, start_point, end_point, offset_range


def plot_image_with_lines(ax, img_array, start_point, end_point, offset_range, num_lines_to_average, image_name):
    """
    Plot an image with the original line and the averaged region marked.
    """
    # Get the start and end coordinates for the region of interest (leftmost and rightmost lines)
    left_start = (start_point[0], start_point[1] + min(offset_range))
    left_end = (end_point[0], end_point[1] + min(offset_range))
    right_start = (start_point[0], start_point[1] + max(offset_range))
    right_end = (end_point[0], end_point[1] + max(offset_range))

    # Display the image
    ax.imshow(img_array, cmap='gray')

    # Mark the left and right lines that define the averaged region
    ax.plot([left_start[1], left_end[1]], [left_start[0], left_end[0]], 'g--', label="Left boundary")
    ax.plot([right_start[1], right_end[1]], [right_start[0], right_end[0]], 'g--', label="Right boundary")

    # Fill the area between the left and right lines to mark the region
    ax.fill_betweenx([start_point[0], end_point[0]], left_start[1], right_start[1], color='green', alpha=0.2,
                     label="Averaged Area")

    # Plot the original middle line
    ax.plot([start_point[1], end_point[1]], [start_point[0], end_point[0]], 'r-', label="Original line")

    # Add legend and title
    # ax.legend()
    ax.set_title(image_name)
    plt.tight_layout()


# Define start and end points for each image, scaling factors, and intensity offsets

image_line_definitions = [
    {
        'image_name': r'Plasma dicing channel - 400nm PR focus on top slot 2.bmp',
        'start_point': (210, 800),  # (row, col) -> y, x
        'end_point': (320, 800),  # (row, col) -> y, x
        'pixel_to_mm_ratio': 0.8,  # Example: 0.1 mm per pixel for this image
        'intensity_offset': 0  # Add intensity offset for image 1
    },
    {
        'image_name': r'Plasma dicing channel - 400nm PR focus on top Slot 3.bmp',
        'start_point': (134, 500),
        'end_point': (244, 500),
        'pixel_to_mm_ratio': 0.8,  # Example: 0.1 mm per pixel for this image
        'intensity_offset': -14  # Add intensity offset for image 1
    },
    {
        'image_name': r'Plasma dicing channel - 400nm PR focus on top Slot 4.bmp',
        'start_point': (191, 500),
        'end_point': (301, 500),
        'pixel_to_mm_ratio': 0.8,  # Example: 0.1 mm per pixel for this image
        'intensity_offset': -6  # Add intensity offset for image 1
    },
    {
        'image_name': r'Plasma dicing channel - Navitar focus on top slot 2.bmp',
        'start_point': (538, 800),
        'end_point': (740, 800),
        'pixel_to_mm_ratio': 0.4,  # Example: 0.1 mm per pixel for this image
        'intensity_offset': 49  # Add intensity offset for image 1
    }
]

# Number of lines to average over
num_lines_to_average = 51

# Initialize a figure for the image plots with a 2x2 grid
fig, axes = plt.subplots(2, 2, figsize=(10, 10))

# Initialize a figure for the intensity profile comparison
plt.figure(figsize=(8, 6))

# Loop through each image, process it, and plot the image and average intensity profile
for idx, line_def in enumerate(image_line_definitions):
    image_name = line_def['image_name']
    folder_path = r"C:\Users\omry-b\OneDrive - Nova\Desktop\Omry-B\\"
    image_path = folder_path + image_name
    start_point = line_def['start_point']
    end_point = line_def['end_point']
    pixel_to_mm_ratio = line_def['pixel_to_mm_ratio']
    intensity_offset = line_def['intensity_offset']  # Intensity offset for each image

    # Process the image to get the average intensity profile
    img_array, avg_intensity, start_point, end_point, offset_range = process_image(image_path, start_point, end_point,
                                                                                   num_lines_to_average)

    # Plot the image with the lines and averaged area on the respective axis in the 2x2 grid
    row, col = divmod(idx, 2)  # Determine the row and column index for the grid
    plot_image_with_lines(axes[row, col], img_array, start_point, end_point, offset_range, num_lines_to_average, image_name)

    # Convert pixel distances to millimeters for the x-axis
    pixel_distances = np.arange(len(avg_intensity))
    mm_distances = pixel_distances * pixel_to_mm_ratio

    # Apply the intensity offset to the average intensity profile
    avg_intensity_with_offset = avg_intensity + intensity_offset

    # Plot the average intensity profile in millimeters on a separate figure for comparison
    plt.plot(mm_distances, avg_intensity_with_offset,
             label=f"{image_name} ({pixel_to_mm_ratio} nm/pixel, offset: {intensity_offset})")

# Hide the empty subplot (if any)
if len(image_line_definitions) < 4:
    axes[1, 1].axis('off')

# Customize the intensity profile comparison plot
plt.title('Comparison of Averaged Intensity Profiles with Offsets')
plt.xlabel('Distance along the line (um)')  # Now in millimeters
plt.ylabel('Average Intensity')
plt.legend()  # Add legend to distinguish between the images
plt.grid(True)
plt.tight_layout()

# Show both the 2x2 grid of images and the comparison plot
plt.show()