import numpy as np

def simulate_solid_angle(radius_source, radius_detector, distance, num_samples):
    count_inside = 0
    
    for _ in range(num_samples):
        # Generate random point on the source disc
        theta_source = 2 * np.pi * np.random.rand()
        r_source = radius_source * np.sqrt(np.random.rand())
        x_source = r_source * np.cos(theta_source)
        y_source = r_source * np.sin(theta_source)
        
        # Generate random direction
        phi = 2 * np.pi * np.random.rand()
        theta = np.arccos(2 * np.random.rand() - 1)
        direction = np.array([
            np.sin(theta) * np.cos(phi),
            np.sin(theta) * np.sin(phi),
            np.cos(theta)
        ])
        
        # Find intersection with the plane of the detector (z = distance)
        t = distance / direction[2]
        x_intercept = x_source + t * direction[0]
        y_intercept = y_source + t * direction[1]
        
        # Check if the intercept point is within the detector disc
        if x_intercept**2 + y_intercept**2 <= radius_detector**2:
            count_inside += 1
    
    # Solid angle
    solid_angle = (count_inside / num_samples) * 2 * np.pi
    return solid_angle

def propagate_uncertainty(radius_source_mean, radius_source_uncertainty, radius_detector, distance, num_samples, num_iterations):
    solid_angles = []
    
    for _ in range(num_iterations):
        # Sample the source radius from a normal distribution
        radius_source_sampled = np.random.normal(radius_source_mean, radius_source_uncertainty)
        
        # Ensure the sampled radius is positive
        if radius_source_sampled <= 0:
            continue
        
        # Calculate the solid angle for this sampled radius
        solid_angle = simulate_solid_angle(radius_source_sampled, radius_detector, distance, num_samples)
        solid_angles.append(solid_angle)
    
    # Calculate the mean and standard deviation of the solid angles
    mean_solid_angle = np.mean(solid_angles)
    std_solid_angle = np.std(solid_angles)
    
    return mean_solid_angle, std_solid_angle

def theoretical_solid_angle_point_source(radius_detector, distance):
    return 2 * np.pi * (1 - distance / np.sqrt(distance**2 + radius_detector**2))

# Parameters
radius_source_mean = 2.5
radius_source_uncertainty = 0.5
radius_detector = 4
distances = np.array([5, 13, 21, 29, 37])
num_samples = 10000
num_iterations = 100

for distance in distances:
    
    mean_solid_angle, std_solid_angle = propagate_uncertainty(radius_source_mean, radius_source_uncertainty, radius_detector, distance, num_samples, num_iterations)

    print(f"Estimated solid angle: {mean_solid_angle:.6f} steradians")
    print(f"Uncertainty in solid angle: {std_solid_angle:.6f} steradians")

    solid_angle_theoretical = theoretical_solid_angle_point_source(radius_detector, distance)
    print(f"Theoretical solid angle for {distance} (Point Source): {solid_angle_theoretical} steradians \n")
