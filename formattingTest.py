
import pyperclip

with open('points.txt', 'r') as file:
    text = file.readlines()
text = text[:1802]

newText = []
for line in text:
    myLine = (line.replace('\n', '').split())
    newText.append([num for num in myLine])

finalText = []
for line in newText:
    finalText.append(line[:34])

final = ''
for arr in finalText:
    final += (' '.join(arr)) + '\n'


with open('points.txt', 'w') as file:
    print(final)
    file.write(final)

