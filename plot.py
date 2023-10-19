import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

FIT_SETS = True;

# Lists to store X and Y values
x_values = []
y_values = []

# Read data from the "results.txt" file
with open("results.txt", "r") as file:
    # Skip header
    next(file);

    # For each entr
    for line in file:
        # Split the line by comma and convert to float for later use
        parts = line.strip().split(",")

        # Check for invalid data
        if len(parts) == 2:
            x_values.append(float(parts[0]))
            y_values.append(float(parts[1]))

# Convert lists to numpy arrays for higher effiency and easier manipulation
x_values = np.array(x_values)
y_values = np.array(y_values)

# Fit a polynomial to the data
# a low-end degree is chosen to try and prevent overfitting
degree = 5
coefficients = np.polyfit(x_values, y_values, degree)

# Create a function that represents the polynomial
poly_function = np.poly1d(coefficients)

# Generate x values for the curve
x_curve = np.linspace(min(x_values), max(x_values), 100)

# Calculate the corresponding y values for the curve
y_curve = poly_function(x_curve)

# Create a scatter plot of the data points above and below the curve
plt.scatter(x_values, y_values, label='Data Points')

# Plot the polynomial curve
plt.plot(x_curve, y_curve, color='red', label=f'Fitted Polynomial (Degree {degree}) - All points')

# Define colors for points above and below the curve
above_color = 'green'
below_color = 'blue'

# Highlight and list points above and below the curve
above_points = []
below_points = []

for x, y in zip(x_values, y_values):
    if y > poly_function(x):
        plt.scatter(x, y, color=above_color)
        above_points.append((x, y))
    else:
        plt.scatter(x, y, color=below_color)
        below_points.append((x, y))

# Add labels and a title
plt.xlabel('Size of the square board NxN')
plt.ylabel('Number of iterations')
plt.title('Correlation between size and number of iterations')

# Show the legend
plt.legend()

if (FIT_SETS):
    # Create DataFrames for above and below points
    above_df = pd.DataFrame(above_points, columns=['X', 'Y'])
    below_df = pd.DataFrame(below_points, columns=['X', 'Y'])

    # Fit a polynomial to the above_points and below_points
    degree_above = 5  
    degree_below = 5  

    coefficients_above = np.polyfit(above_df['X'], above_df['Y'], degree_above)
    coefficients_below = np.polyfit(below_df['X'], below_df['Y'], degree_below)

    # Create functions for the fitted polynomials
    poly_function_above = np.poly1d(coefficients_above)
    poly_function_below = np.poly1d(coefficients_below)

    # Calculate y values for the fitted polynomials
    y_curve_above = poly_function_above(x_curve)
    y_curve_below = poly_function_below(x_curve)

    # Plot the fitted polynomials for above_points and below_points
    plt.plot(x_curve, y_curve_above, color='orange', label=f'Fitted Polynomial Above (Degree {degree_above}) - Points above')
    plt.plot(x_curve, y_curve_below, color='purple', label=f'Fitted Polynomial Below (Degree {degree_below}) - Points below')

    # Show the legend with the updated labels
    plt.legend()

    # Display the plot
    plt.show()

    # Print tables for points above and below the curve
    print("Points Above the Curve:")
    print(above_df.to_string(index=False))

    print("\nPoints Below the Curve:")
    print(below_df.to_string(index=False))
