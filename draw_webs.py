import random

def draw_unique_lines(input_file, output_file, num_lines):
    try:
        # Read all lines from the input file
        with open(input_file, 'r') as file:
            lines = file.readlines()
        
        # Ensure the number of lines requested is not more than the available lines
        if num_lines > len(lines):
            raise ValueError(f"The file contains only {len(lines)} lines, but {num_lines} lines were requested.")
        
        # Shuffle lines to randomize
        random.shuffle(lines)
        
        # Pick the first num_lines lines
        selected_lines = lines[:num_lines]
        
        # Write the selected lines to the output file
        with open(output_file, 'w') as file:
            file.writelines(selected_lines)

        print(f"{num_lines} unique lines written to {output_file}")

    except Exception as e:
        print(f"Error: {e}")

# Usage
input_file_path = '/home/sghandi/Téléchargements/wemon-main/urls/urls.txt'  # Replace with your input file path
output_file_path = '/home/sghandi/Téléchargements/wemon-main/urls/urls1000.txt'  # Replace with your desired output file path
num_lines = 1000  # Number of lines to draw

draw_unique_lines(input_file_path, output_file_path, num_lines)

