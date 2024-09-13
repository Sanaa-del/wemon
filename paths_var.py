import os

# Define the directory to search
directory_to_search = "/var/www/websites"

# Define the output file
output_file = "html_paths.txt"

# Open the output file in binary mode for writing
with open(output_file, "wb") as file_out:
    # Walk through the directory
    for root, _, files in os.walk(directory_to_search):
        for filename in files:
            # Check if the file is an HTML file
            if filename.endswith(".html"):
                # Write the full path to the output file in binary mode
                full_path = os.path.join(root, filename)
                file_out.write((full_path + "\n").encode('utf-8', errors='replace'))

print(f"Paths of all HTML files have been written to {output_file}.")

