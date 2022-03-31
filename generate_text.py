import sys
import time
import text_stats
from random import choices

startTime = time.time()

def text_generation(input_text, initial_word, number_of_words):

    initial_word = initial_word.lower()

    _, text_dictionary, _, _, _ = text_stats.dictionaries_of_words(input_text)

    # Check if inital word exists in the text
    if not initial_word in list(text_dictionary.keys()):
        print(f"{initial_word} does not exist in the supplied .txt file. Will return None")
        return None

    output_text = list()
    output_text.append(initial_word)

    counter = 0
    end_successor = False

    curr_word = initial_word

    while counter <= number_of_words or end_successor == True:
        curr_successors = text_dictionary[curr_word]
        # Randomly choose the successor with set weights to the counts of the word as successor
        curr_word = choices(population = list(curr_successors.keys()), weights = list(curr_successors.values()))[0]
        output_text.append(curr_word)
        # Check if the next words successors is empty
        if len(text_dictionary[curr_word]) == 0:
            end_successor == True
            print("Terminated the text because of no new successor")
        counter += 1

    output_text = " ".join(output_text)

    with open("generated.txt", "w") as generated_txt:
        generated_txt.write(output_text)

    print("The text has been generated")
    executionTime = (time.time() - startTime)
    print('Execution time in seconds: ' + str(executionTime))

    return None

if __name__ == "__main__":
    if len(sys.argv) <= 3: # If length is one then only script was called
        print("Error: Not all arguments specified.")
    elif len(sys.argv) > 4: # If length is more than four; too many arguments
        print("Error: Too many arguments passed. Please enter a valid .txt file as the first argument, an inital word as the second argument and the maximum number of words as the third argument.")
    else:
        try: # Try to open the .txt file
            with open(sys.argv[1], "r", encoding="utf-8") as txt_file:
                input_text = txt_file.read()
                init_word = str(sys.argv[2])
                n_words = int(sys.argv[3])
                text_generation(input_text, init_word, n_words)
        except FileNotFoundError: # If doesnt work throw an error
            print("Error: The provided .txt file was not found. Please enter a valid .txt file as the first argument.")
