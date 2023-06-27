# Synopsis: 
# Given a sequence, this script generates flashcards to remember that sequence. The cards are:
# - A test card that asks you to recall the entire sequence.
# - For each element of the sequence:
#   - A forward card that asks you to recall the element from its position.
#   - A backward card that asks you to recall the position of a given element.
#   - A successor card that asks you what comes after a specific element.
#   - A predecessor card that asks you what comes before a specific element.

# Format: The input is plain text. The first line is the title of the sequence, and subsequent lines are the sequence.

# Usage:
# Run by typing the following into the terminal: cat sequence.txt | python ./AnkiSequence.py
# This creates a file called "output.csv" in the same folder.
# Go to Anki -> File -> Import -> Navigate to output.csv ...
# ... Choose the relevant deck -> Fields separated by: Comma -> Allow HTML in fields ...
# ... Field 1 of file is mapped to Front; Field 2 of file is mapped to Back -> Import

# Disclaimers: 
# See disclaimers in AnkiPoetry.py: this program was put together by using Bing AI to adapt that script to the synopsis above.

import sys
import csv # import the csv module
import html # import the html module

# Define a class for flashcard
class Flashcard:
    def __init__(self, title, front, back):
        self.title = title
        self.front = front
        self.back = back

    def __str__(self):
        return f"<h4 style='margin: 0.25em;'>{self.title}</h4>{self.front}"

# Define a function to escape special characters in HTML
def escape_html(text):
    return html.escape(text)

def main():
    # Take out blank lines and escape special characters
    sequence = [escape_html(rl.strip("\"")) for rl in sys.stdin.readlines() 
                    if len(rl.strip("\"")) > 0]

    # The title is the first line.
    title = sequence[0]
    # All subsequent lines are the elements of the sequence.
    sequence = sequence[1:]

    # Make a list of flashcards
    flashcards = []
    
    # Make a test card that asks to recall the entire sequence
    front = f"Recall all elements of the sequence:"
    back = ", ".join(sequence)
    flashcard = Flashcard(title, front, back)
    # Add the flashcard to the list
    flashcards.append(flashcard)

    # Loop through the elements of the sequence
    for i, element in enumerate(sequence):
        # Make a forward card that asks to recall the element from its position
        front = f"What element has position {i+1}?"
        back = element
        flashcard = Flashcard(title, front, back)
        # Add the flashcard to the list
        flashcards.append(flashcard)

        # Make a backward card that asks to recall the position of a given element
        front = f"What is the position of {element}?"
        back = str(i+1)
        flashcard = Flashcard(title, front, back)
        # Add the flashcard to the list
        flashcards.append(flashcard)

        # Make a successor card that asks what comes after a specific element if it exists
        if i < len(sequence) - 1: # If this is not the last element
            front = f"What comes after {element}?"
            back = sequence[i+1]
            flashcard = Flashcard(title, front, back)
            # Add the flashcard to the list
            flashcards.append(flashcard)

        # Make a predecessor card that asks what comes before a specific element if it exists
        if i > 0: # If this is not the first element
            front = f"What comes before {element}?"
            back = sequence[i-1]
            flashcard = Flashcard(title, front, back)
            # Add the flashcard to the list
            flashcards.append(flashcard)

    # Open the output file with utf-8 encoding
    with open('output.csv', 'w', newline='', encoding='utf-8') as csv_file:
        # Use csv.writer with utf-8 encoding
        writer = csv.writer(csv_file, delimiter=',')
        # Write each flashcard as two columns: front and back
        for flashcard in flashcards:
            writer.writerow([str(flashcard), flashcard.back])

if __name__ == '__main__':
    main()
