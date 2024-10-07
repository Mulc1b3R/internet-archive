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

input_file = "colorized movies.txt"  # File containing the list of URLs
output_file = "hyperlinks.html"  # Output HTML file to store the hyperlinks as a list

generate_hyperlinks(input_file, output_file)