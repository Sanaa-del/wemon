import itertools
import sys

# Define the parameter ranges
server_cpu_range = [1, 0.7, 0.4, 0.1]
fading_range = [1, 2, 4]
delay_range = ['0ms', '10ms', '50ms', '100ms', '400ms']
loss_range = [0, 0.1, 0.5, 1, 5, 10, 20]
bw_range = [100, 50, 10, 5, 2, 1]  # Bandwidth range
client_cpu_range = [1, 0.7, 0.4, 0.1]
medium_availability_range = [100, 70, 30, 15]

# Convert a given scenario line to a list of the correct types
def parse_scenario(line):
    try:
        scenario = line.split()
        parsed_scenario = [float(scenario[0]), int(scenario[1]), str(scenario[2]), float(scenario[3]), int(scenario[4]), float(scenario[5]), int(scenario[6])]
        #print('scenario parsed')
        return parsed_scenario
    except (ValueError, IndexError) as e:
        print(f"Error parsing the scenario: {line}, {e}")
        
        return None

# Generate worse scenarios by iterating over all parameters and their worse ranges
def generate_worse_scenarios(scenario):
    print('generating worse')
    ranges = [server_cpu_range, fading_range, delay_range, loss_range, bw_range, client_cpu_range, medium_availability_range]
    worse_scenarios = []
    parameter_ranges = []


    
    # Get the ranges of worse values for each parameter
    for i in range(len(scenario)):
        current_value = scenario[i]
        param_range = ranges[i]

        # Find the index of the current value in its range
        if current_value in param_range:
            current_index = param_range.index(current_value)
            # Add the worse values for this parameter (including itself)
            parameter_ranges.append(param_range[current_index:])
    
    # Generate all combinations of worse values for all parameters using itertools.product
    for worse_combination in itertools.product(*parameter_ranges):
        worse_scenario = list(worse_combination)
        worse_scenarios.append(worse_scenario)
    
    return worse_scenarios
    
# Search and update the text file
def update_scenarios_in_file(input_file, scenario, worse_scenarios):
    with open(input_file, 'r') as infile:
        lines = infile.readlines()

    with open(input_file, 'w') as outfile:
        for line in lines:
            parts = line.strip().split()

            # Extract the ID, parameters, and label
            if len(parts) < 9:
                continue  # Skip invalid lines
            scenario_id = parts[0]
            parameters = parts[1:8]  # The parameters (7 fields)
            label = parts[-1]  # The label (last field)

            # Convert parameters to the correct types for comparison
            parsed_params = parse_scenario(' '.join(parameters))
            if parsed_params is None:
                outfile.write(line)
                continue

            # Check if the current parameters match the exact scenario -> set it to 'timeout'
            if parsed_params == scenario and label == 'todo':
                print('detected the timeout scenario')
                label = 'timeout'  # Update the label to 'timeout' for the exact scenario

            # Check if the current parameters match any of the worse scenarios
            # AND if the current label is 'todo' -> set it to 'skip'
            elif parsed_params in worse_scenarios and label == 'todo':
                label = 'skip'  # Update the label to 'skip' for worse scenarios

            # Write the updated (or unchanged) line back to the file
            outfile.write(f"{scenario_id} {' '.join(map(str, parameters))} {label}\n")
    print('i finished processing')  


input_file = '/home/sghandi/Téléchargements/wemon-main/scenario_with_labels.txt'

if __name__ == "__main__":
    # Assume that parameters are passed as a single string
    line = sys.argv[1]

    
    scenario = parse_scenario(line)
    if scenario is None:
        print(f"Invalid scenario line: {line}")
        sys.exit(1)

    # Generate worse scenarios based on the provided scenario
    worse_scenarios = generate_worse_scenarios(scenario)

    # Update the file by marking the exact scenario as 'timeout' and the worse ones as 'skip'
    update_scenarios_in_file(input_file, scenario, worse_scenarios)

