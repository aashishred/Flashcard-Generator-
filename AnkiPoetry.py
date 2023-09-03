# Synopsis: Given a poem, this script generates flashcards where you are given some context (the previous 2 lines) and have to recall the next line.

# Format: The input is plain text. The first line is the title of the poem, the second line is the author, and subsequent lines are the poem.

# Usage:
# Run by typing the following into the terminal: cat poem.txt | python ./AnkiPoetry.py
# This creates a file called "output.csv" in the same folder.
# Go to Anki -> File -> Import -> Navigate to output.csv ...
# ... Choose the relevant deck -> Fields separated by: Comma -> Allow HTML in fields ...
# ... Field 1 of file is mapped to Front; Field 2 of file is mapped to Back -> Import

import argparse
import sys
from collections import deque
import csv # import the csv module

# Define a class for flashcard
class Flashcard:
    def __init__(self, title, author, front, back):
        self.title = title
        self.author = author
        self.front = front
        self.back = back

    def __str__(self):
        return f"<h4 style='margin: 0.25em;'>{self.title}</h4><h5 style='margin: 0.2em 0.2em 1.0em 0.2em;'>{self.author}</h5>{self.front}"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-q", "--qlines", type=int, default=2, 
        help="No. of lines in question")

    args = parser.parse_args()
    qlines = args.qlines

    # Take out blank lines and escape special characters
    poem = []
    previous_line_empty = False  # Flag variable to track empty lines

    for rl in sys.stdin:
        rl = rl.encode('utf-8').decode('utf-8', 'ignore')  # Decode as UTF-8 and ignore invalid characters
        if rl == "\n":
            previous_line_empty = True  # Set the flag to True when encountering a newline
        else:
            if previous_line_empty:
                poem[-1] = poem[-1].strip() + " <br>"  # Append "<br>" to the last line of the previous stanza
                previous_line_empty = False  # Reset the flag to False
            poem.append(rl.strip("\""))



    # The title is the first line.
    title = poem[0]
    # The author is the second line.
    author = poem[1]
    # All subsequent lines are the poem.
    poem = poem[2:]

    # Make a list of flashcards
    flashcards = []
    # Use a deque to store the lines for each flashcard
    lines = deque([""] * qlines)
    
    # Loop through the poem lines
    for i in range(len(poem) - 1):
        # Add the next line to the deque if it exists
        if i < len(poem):
            lines.append(poem[i])
        # Remove the first line from the deque
        lines.popleft()
        # Make a flashcard with the current lines as front and the next line as back if it exists
        if i == 0: # If this is the first card
            front = "Beginning<br>" # Add "Beginning" to the front
            back = poem[i] # Use the first line as back
            flashcard = Flashcard(title, author, front, back)
            # Add the flashcard to the list
            flashcards.append(flashcard)
            # Make another card with "Beginning" and the first line as front and the second line as back
            front = "Beginning<br>" + poem[i] + "<br>" # Add "Beginning" and the first line to the front
            back = poem[i+1] # Use the second line as back
            flashcard = Flashcard(title, author, front, back)
            # Add the flashcard to the list
            flashcards.append(flashcard)
        elif i + 1 < len(poem): # If this is not the last card
            front = "<br>".join(lines) + "<br>" # Add a line break between and after each line in the front
            back = poem[i+1] # Use the next line as back
            flashcard = Flashcard(title, author, front, back)
            # Add the flashcard to the list
            flashcards.append(flashcard)

    # Open the output file with utf-8 encoding
    with open('output.csv', 'w', newline='', encoding='utf-8-sig') as csv_file:
        # Use csv.writer with utf-8 encoding
        writer = csv.writer(csv_file, delimiter=',')
        # Write each flashcard as two columns: front and back
        for flashcard in flashcards:
            writer.writerow([str(flashcard), flashcard.back])

if __name__ == '__main__':
    main()
