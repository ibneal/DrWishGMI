# Function to read a .txt file and convert its lines into a list
def txt_to_list(file_path):
    # Open the file in read mode
    with open(file_path, 'r') as file:
        # Read all lines from the file and strip any extra whitespace
        stockListNYSE = [line.strip() for line in file.readlines()]
    return stockListNYSE

# Function to write the list to a new .txt file in the desired format without new lines after each symbol
def list_to_txt(stockListNYSE, output_file_path):
    with open(output_file_path, 'w') as file:
        file.write('symbols = [')
        for i, symbol in enumerate(stockListNYSE):
            if i == len(stockListNYSE) - 1:
                file.write(f'"{symbol}"')
            else:
                file.write(f'"{symbol}", ')
        file.write(']')

# Path to the input .txt file
input_file_path = 'NYSEStockList.txt'

# Path to the output .txt file
output_file_path = 'output-file.txt'

# Convert the .txt file to a list
stockListNYSE = txt_to_list(input_file_path)

# Write the list to the new .txt file in the desired format
list_to_txt(stockListNYSE, output_file_path)

print(f'The data has been successfully written to {output_file_path}')
