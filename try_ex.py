import numpy as np

# Fitted ex-Gaussian parameters
mu = 313.22     # mean of the Gaussian component
sigma = 164.98  # standard deviation of the Gaussian component
tau = 801.74    # rate parameter (Exponential component)

# Function to generate a random gaze time using the ex-Gaussian distribution
def generate_gaze_time(mu, sigma, tau):
    # Generate a random value from the Gaussian distribution
    gaussian_sample = np.random.normal(mu, sigma)
    
    # Generate a random value from the Exponential distribution
    exponential_sample = np.random.exponential(tau)
    
    # Sum the two values to get the ex-Gaussian sample
    gaze_time = gaussian_sample + exponential_sample
    
    return gaze_time

# Generate a random gaze time for the robot
random_gaze_time = generate_gaze_time(mu, sigma, tau)
print(f"Randomly generated gaze time: {random_gaze_time} ms")