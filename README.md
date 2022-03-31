# text_generator_py

A naive application that stores data on word frequencies, letter_frequencies and successor words.

text_stats.py contains function to gather the information present in an input .txt file. Optional parameter to store the results in a new .txt file.

foo@bar:~$ python3 text_stats.py <txt_file> <output_file>

generate_text.py uses the information from text_stats.py to generate text using the gathered information. It required a user-supplied starting word and the max number of words the generator should produce.

foo@bar:~$ python3 generate_text.py <txt_file> <starting_word> <max_words>
