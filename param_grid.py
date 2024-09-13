import itertools

def generate_parameter_grid():
    """
    Generate a grid of parameter values.

    Returns:
    - A list of tuples, where each tuple contains parameter values for one experiment.
    """
    
    # Define ranges for each parameter
    server_cpu_range = [1, 0.7, 0.4, 0.1]
    fading_range = [1, 2, 4]
    delay_range = ['0ms', '10ms', '50ms', '100ms', '400ms']
    loss_range = [0, 0.1, 0.5, 1, 5, 10, 20]
    bw_range = [1, 2, 5, 10,  50, 100]
    client_cpu_range = [1, 0.7, 0.4, 0.1]
    medium_availability_range = [100, 70, 30, 15]
    
    # Generate combinations of parameter values
    parameter_grid = list(itertools.product(server_cpu_range, fading_range, delay_range, 
                                            loss_range, bw_range, client_cpu_range, medium_availability_range))

    return parameter_grid

if __name__ == '__main__':
    # Generate the parameter grid
    parameter_grid = generate_parameter_grid()

    # Write parameter values to a file with line numbers
    with open('parameter_file.txt', 'w') as file:
        for i, parameters in enumerate(parameter_grid, start=1):
            # Write the line number followed by the parameters, separated by spaces
            file.write(f"{i} " + ' '.join(map(str, parameters)) + '\n')

