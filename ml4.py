
# Gradient Descent to Find Local Minimum

# Define the function and its derivative
def f(x):
    return (x + 3) ** 2

def gradient(x):
    return 2 * (x + 3)

# Initialize parameters
x = 2
learning_rate = 0.1
iterations = 100

# Apply Gradient Descent
for i in range(iterations):
    x = x - learning_rate * gradient(x)

# Display results
print("Local Minimum Point (x):", round(x, 6))
print("Minimum Value (y):", round(f(x), 6))
