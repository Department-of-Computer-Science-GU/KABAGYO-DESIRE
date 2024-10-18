import pywebio.input as p #for handling user input
import pywebio.output as o #displaying the user input on the webpage
import requests #to make http requests to fetch the facts

# Function to fetch a random fun fact from the API
def get_random_fact():
    try:
        # Make a GET request to the API and return the fact
        return requests.get('https://uselessfacts.jsph.pl/api/v2/facts/random').json()['data']['fact']
    except:
        # Return an error message if something goes wrong
        return "Error fetching fact"

# Main application function
def main():
    # Display the app title
    o.put_markdown("# Fun Fact Generator")
    
    # Continuous loop until user exits
    while True:
        # Fetch a random fact
        fact = get_random_fact()
        
        # Display the fact
        o.put_markdown(f"## Random Fun Fact:\n{fact}")
        
        # Ask user what to do next
        action = p.actions(label='Generate New Fact', buttons=['New Fact', 'Exit'])
        
        # Exit condition
        if action == 'Exit':
            break
    
    # Thank user for using the app
    o.toast("Thanks for using the Fun Fact Generator!")

# Run the application
if __name__ == '__main__':
    pywebio.start_server(main, port=80)
