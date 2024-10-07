import internetarchive

def search_and_write_results(query, output_file):
    search_results = internetarchive.search_items(query)
    
    with open(output_file, 'w') as file:
        for result in search_results:
            item_url = 'https://archive.org/details/' + result['identifier']
            file.write(item_url + '\n')

# Get user's search query
search_query = input("Enter your search query: ")
output_file = f"{search_query}.txt"

search_and_write_results(search_query, output_file)

def generate_hyperlinks(input_file, output_file):
    with open(input_file, 'r') as file_in, open(output_file, 'w') as file_out:
        file_out.write('<ul>\n')  # Start the unordered list in HTML
        for line in file_in:
            url = line.strip()
            identifier = url.split('/details/')[-1]
            hyperlink = f'<a href="{url}">{identifier}</a>'
            list_item = f'<li>{hyperlink}</li>'
            file_out.write(list_item + '\n')
        file_out.write('</ul>')  # End the unordered list in HTML

input_file = f"{search_query}.txt"  # Input file matching search query output
output_file = f"html/{search_query}.html"  # Output HTML file for hyperlinks

generate_hyperlinks(input_file, output_file)