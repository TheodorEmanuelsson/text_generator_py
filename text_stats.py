import sys
import time

startTime = time.time()

### HELP FUNCTIONS ###
def text_to_words(input_text):
    """Function that splits an input string into a list of strings separated by a blank space """
    words = input_text.split()
    return words

def count_alphahetical_and_remove_nonalphabetical(word_list):
    """Function that removes all non-alphabetical characters from a list of words
    and counts the occurances of alphabetical letters"""
    # Dictionary with the count of the alphabetic characters
    count_char = {}
    for index in range(len(word_list)): # For each word
        for char in word_list[index]: # For each character
            if not char.isalpha(): # Check if alphabetic
                word_list[index] = word_list[index].replace(char,"") # Replace non alphahetric with empty
            else: # If alphabetic count it in the dictionary
                char = char.lower()
                count_char = increment_dictionary(count_char, char)
        word_list[index] = word_list[index].lower() # Make word lower case
    word_list = list(filter(None, word_list)) # Filter out the empty replacements
    count_char = dict(sorted(count_char.items(), reverse=True, key = lambda x: x[1])) # Sort the letter counts
    return word_list, count_char

# combines the two functions above
def filter_text(input_text):
    """Simple function that takes a text and returns the alphabetical words in a list
    and the counts of the alphabetical characters
    """
    words = text_to_words(input_text)
    words, count_letters = count_alphahetical_and_remove_nonalphabetical(words)
    return words, count_letters

def increment_dictionary(dictionary, key):
    """Simple function that increments the value of a key in a dictionary given the dictionary and the key"""
    if not key in dictionary.keys():
        dictionary[key] = 1
    else:
        dictionary[key] += 1
    return dictionary

def add_word_to_dictionary(dictionary, key):
    """Simple function to initialize a new key in a nested dictionary"""
    dictionary[key] = {}
    return dictionary

def find_five_most_common_words(dict_freq):
    """A function that sorts and then returns the five most common words in a dictionary."""
    dict_frequencies = dict(sorted(dict_freq.items(), reverse=True, key = lambda x: x[1]))
    top_five_words = list(dict_frequencies)[0:5]
    top_five_count = list(dict_frequencies.values())[0:5]
    five_most_common = dict(zip(top_five_words,top_five_count))
    return five_most_common

def find_three_most_common_successors(most_common_dict, word_successor_dictionary):
    """A function that find the three most common successors to a dictionary of most common words """
    five_most_common_keys = dict.fromkeys(most_common_dict)
    three_common_successors = {}
    for word in five_most_common_keys:
        three_common_successors[word] = word_successor_dictionary[word]
    return three_common_successors

def multi_dict_sort(dictionary, sort_type=1):
    """A function that sorts a nested dictionary in descending order"""
    items_list = [key for (key, value) in dictionary.items() if type(value) is dict]
    for item_key in items_list:
        dictionary[item_key] = dict(sorted(dictionary[item_key].items(), key=lambda x:x[sort_type], reverse = True))
    return dictionary


### MAIN FUNCTION ###
def dictionaries_of_words(input_text):
    """A function that counts the frequencies of words in a text, their successors and their frequencies as successors to a word
    and the five most common words in a text

    Input:
        - A string

    Output
        - frequencies_dictionary (A dictionary containing the word frequencies in the string and)
        - word_successor_dictionary (A nested dictionary containing the word and its successors)
        - five_most_common (A dictionary of the five most common words and their count)
        - top_with_successors (A dictionary of the three most common successors to the five most common words)
        - count_letters (A dictionary of the counts of alphabetical letters in the input text file)
    """

    # Filter and split text
    words, count_letters = filter_text(input_text)

    # Initalize dictionaries
    frequencies_dictionary = {}
    word_successor_dictionary = {} # Dictionary to store words, their count and their successors
    successor_dictionary = {} # Dictionary to store current successors

    for index in range(len(words)):
        current_word = words[index]
        # Count the instance of current word in the frequencies dictionary
        frequencies_dictionary = increment_dictionary(frequencies_dictionary, current_word)

        # Add the word as key to the outer successors dictionary
        if not current_word in word_successor_dictionary:
            word_successor_dictionary = add_word_to_dictionary(word_successor_dictionary, current_word)

        successor = index + 1 # Successor is the next word in the list

        if successor != len(words): # Last word cannot have a successor
            # Count the instance of succesor words in the successor_dictionary
            if current_word in word_successor_dictionary.keys(): # Check if the successor is a previous successor
                successor_dictionary = word_successor_dictionary[current_word] # If so copy the nested dictonary
                successor_dictionary = increment_dictionary(successor_dictionary, words[successor]) # And increment it
            else:
                successor_dictionary = increment_dictionary(successor_dictionary, words[successor]) # If not there, make new entry

            # Put the successors into the dictionary handling
            word_successor_dictionary[current_word] = dict(successor_dictionary)

        # Reset successor_dictionary
        successor_dictionary = {}

    # Sort the frequencies_dictionary
    #frequencies_dictionary = dict(sorted(frequencies_dictionary.items(), reverse=True, key = lambda x: x[1]))
    # Sort the nested dictionary of successors
    word_successor_dictionary = multi_dict_sort(word_successor_dictionary)

    # Get the three most common words and their counts
    five_most_common = find_five_most_common_words(frequencies_dictionary)
    # Get successors to the five most common
    top_with_successors = find_three_most_common_successors(five_most_common, word_successor_dictionary)

    return frequencies_dictionary, word_successor_dictionary, five_most_common, top_with_successors, count_letters

### PRESENT FUNCTION ###
def user_inference(input_text):
    """Function that handles printing to the text file"""

    text_name = sys.argv[1]

    frequencies, successors, top_five_words, top_successors, letter_count  = dictionaries_of_words(input_text)

    if len(sys.argv) == 2:
        print("No results file was provided. results.txt has been created for you.")
        results_file_name = "results.txt"
        results_mode = "w"
    elif len(sys.argv) == 3:
        results_file_name = sys.argv[2]
        results_mode = "a"
        print(f"A results file was provided. {results_file_name} will be used to return results.")

    with open(results_file_name, results_mode) as results_file:
        results_file.write("------------------------------------------------------\n")
        results_file.write(f"Frequency table of alphabetic letters in {text_name}\n")
        results_file.write("------------------------------------------------------\n")
        for letter, count in letter_count.items():
            results_file.write(f"{letter.ljust(10)}({count} occurances)\n")
        results_file.write("------------------------------------------------------\n")

        results_file.write("------------------------------------------------------\n")
        results_file.write(f"Information about {text_name}\n")
        results_file.write("------------------------------------------------------\n")
        # Second, print number of words
        results_file.write(f"{text_name} contains {sum(frequencies.values())} words\n")
        # Third, print unique words
        results_file.write(f"{text_name} contains {len(frequencies)} unique words\n")
        results_file.write("------------------------------------------------------\n")

        # Fourth, print five most common words along with three most common successors
        results_file.write("------------------------------------------------------\n")
        results_file.write(f"Five most common words and their successors in {text_name}\n")
        results_file.write("------------------------------------------------------\n")

        for word, count in top_five_words.items():
            results_file.write(f"{word} ({count} occurances)\n")
            for successor, succ_count in list(top_successors[word].items())[0:3]:
                results_file.write(f"-- {successor} ({succ_count} occurances)\n")
            results_file.write("------------------------------------------------------\n")
        results_file.write("\n\nEND RESULTS")

        print(f"Results have been generated. See {results_file_name}")

        executionTime = (time.time() - startTime)
        print('Execution time in seconds: ' + str(executionTime))

    return None

### CHECKS FOR ARGUMENTS AND OPENS TARGET FILE ###
if __name__ == "__main__":
    # Check if the user inputed a text file to read
    if len(sys.argv) <= 1: # If length is one then only script was called
        print("Error: No argument for .txt file found. Please enter a valid .txt file to proceed.")
    elif len(sys.argv) > 3: # If length is more than three; too many arguments
        print("Error: Too many arguments passed. Please enter a valid .txt file as the first argument and an optional .txt file to print the results.")
    else:
        try: # Try to open the .txt file
            with open(sys.argv[1], "r", encoding="utf-8") as txt_file:
                      input_text = txt_file.read()
                      user_inference(input_text)
        except FileNotFoundError: # If doesnt work throw an error
            print("Error: The provided .txt file was not found. Please enter a valid .txt file as the first argument.")
