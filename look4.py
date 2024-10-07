import internetarchive

def search_and_write_results(query, output_file):
    search_results = internetarchive.search_items(query)
    
    with open(output_file, 'w') as file:
        for result in search_results:
            item_url = 'https://archive.org/details/' + result['identifier']
            file.write(item_url + '\n')

search_query = input("Enter your search query: ")
output_file = f"{search_query}.txt"

search_and_write_results(search_query, output_file)