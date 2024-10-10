def initialize_labels(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            # Read the line, add 'todo' as the initial label
            scenario_with_label = line.strip() + " todo\n"
            outfile.write(scenario_with_label)

input_file = "/home/sghandi/Téléchargements/wemon-main/parameter_file.txt"  # The file with scenario IDs and parameters
output_file = "/home/sghandi/Téléchargements/wemon-main/scenario_with_labels.txt"  # New file with labels

initialize_labels(input_file, output_file)
