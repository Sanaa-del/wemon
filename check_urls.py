import os

# Define the input and output file paths
input_file = '/home/sghandi/Téléchargements/wemon-main/urls/urls1000.txt'
output_file = '/home/sghandi/Téléchargements/wemon-main/urls/valid_urls.txt'
base_directory = '/var/www/websites'
base_url = 'http://10.0.0.2'

def is_file_exists(url):
    # Extract the file path from the URL
    file_path = url.replace(base_url, base_directory)
    return os.path.isfile(file_path)

def filter_valid_urls(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            url = line.strip()
            if is_file_exists(url):
                outfile.write(url + '\n')

# Run the script
filter_valid_urls(input_file, output_file)

print(f"Valid URLs have been written to {output_file}")

