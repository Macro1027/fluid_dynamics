def create_cow_side_view(width, height):
    # Initialize the 2D array with False
    array = [[False for _ in range(width)] for _ in range(height)]

    # Define the cow silhouette (side view) pattern
    cow_silhouette = [
        (1, 3), (1, 4), (1, 5), 
        (2, 2), (2, 6),
        (3, 1), (3, 2), (3, 6), (3, 7),
        (4, 1), (4, 7),
        (5, 1), (5, 7),
        (6, 1), (6, 7),
        (7, 1), (7, 7),
        (8, 2), (8, 6),
        (9, 3), (9, 4), (9, 5)
    ]

    for i in range(height):
        for j in range(width):
            if (i, j) in cow_silhouette:
                array[i][j] = True

    return array

# Dimensions for a detailed shape
width, height = 10, 10

# Create the cow array
cow_array = create_cow_side_view(width, height)

# Print the array
for row in cow_array:
    print(' '.join(['🐄' if cell else '🌿' for cell in row]))
