# Do I even have to mention when I use ChatGPT anymore?

import json, pygame, cv2

with open("locs.json") as f:
    locs = json.load(f)

print(locs)

WINDOW_WIDTH = 800*2
WINDOW_HEIGHT = 600*2
IMAGE_WIDTH = 768*2
IMAGE_HEIGHT = 576*2

# Initialize pygame
pygame.init()

# Load images and locs
images = [pygame.image.load(f"plans/{i}.jpg") for i in range(4)]
names = list(locs)
image_index = 0
loc_index = 0

# Scale the images
scaled_images = []
for i, image in enumerate(images):
    aspect_ratio = image.get_width() / image.get_height()
    scaled_width = min(IMAGE_WIDTH, int(IMAGE_HEIGHT * aspect_ratio))
    scaled_height = min(IMAGE_HEIGHT, int(IMAGE_WIDTH / aspect_ratio))
    scaled_image = pygame.transform.scale(image, (scaled_width, scaled_height))
    scaled_images.append(scaled_image)

# Set up the window
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption(f"Floor {image_index} - {names[loc_index]}")

# Start the game loop
running = True
new_location = False
prev_image_index = 0
while running:

    # Handle events
    for event in pygame.event.get():

        # Handle mouse clicks
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:
                loc_index -= 1
                loc_index = max(0, loc_index)
                # image_index = prev_image_index
                pygame.display.set_caption(f"Floor {image_index} - {names[loc_index]}")
            elif event.button == 1:
                x, y = event.pos
                x_scale_factor = images[image_index].get_width() / IMAGE_WIDTH
                y_scale_factor = images[image_index].get_height() / IMAGE_HEIGHT
                scale_factor = max(x_scale_factor, y_scale_factor)
                x_scaled = int((x - (WINDOW_WIDTH - scaled_images[image_index].get_width()) // 2) * scale_factor)
                y_scaled = int((y - (WINDOW_HEIGHT - scaled_images[image_index].get_height()) // 2) * scale_factor)
                
                locs[names[loc_index]] = (x_scaled, y_scaled, image_index)

                # Move to the next string
                loc_index = loc_index + 1
                loc_index = loc_index % len(names)
                # if loc_index == len(names):
                #     running = False
                #     break
                
                # prev_image_index = image_index
                # image_index = 0

                # Update the window title
                pygame.display.set_caption(f"Floor {image_index} - {names[loc_index]}")

        # Handle key presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                image_index = (image_index + 1) % len(images)
                pygame.display.set_caption(f"Floor {image_index} - {names[loc_index]}")
            elif event.key == pygame.K_n:
                new_location = True
                names = names[:loc_index] + [input()] + names[loc_index:]
                pygame.display.set_caption(f"Floor {image_index} - {names[loc_index]}")
            elif event.key == pygame.K_s:
                loc_index += 1
                loc_index = loc_index % len(names)
                pygame.display.set_caption(f"Floor {image_index} - {names[loc_index]}")
            elif event.key == pygame.K_ESCAPE:
                running = False
                

        # Handle window close button
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    window.fill((255, 255, 255))

    # Blit the current image onto the screen
    scaled_image = scaled_images[image_index]
    x_offset = (WINDOW_WIDTH - scaled_image.get_width()) // 2
    y_offset = (WINDOW_HEIGHT - scaled_image.get_height()) // 2

    x_scale_factor = images[image_index].get_width() / IMAGE_WIDTH
    y_scale_factor = images[image_index].get_height() / IMAGE_HEIGHT
    scale_factor = max(x_scale_factor, y_scale_factor)
    
    window.blit(scaled_image, (x_offset, y_offset))
    for name, v in locs.items():
        if v is None: continue
        x, y, floor = v
        if floor == image_index:
            x_scaled = x / scale_factor + x_offset
            y_scaled = y / scale_factor + y_offset
            c = (255, 0, 0)
            r = 5
            if name == names[loc_index]:
                c = (0, 0, 255)
                r *= 2
            pygame.draw.circle(window, c, (x_scaled, y_scaled), r)

    # Update the display
    pygame.display.flip()

# Quit pygame
pygame.quit()

with open("locs.json", "w") as f:
    json.dump(locs, f)