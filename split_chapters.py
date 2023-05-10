import re
import os

full_text_file = "/Users/psin/Desktop/cos401/cos401_final_proj/modern_books/modern_books_full/joyluckclub.txt"
directory = "/Users/psin/Desktop/cos401/cos401_final_proj/modern_books/modern_book_chapters/joyluckclub/"
book_name = "rpo"

if not os.path.exists(directory):
    os.mkdir(directory)

f = open(full_text_file, "r")
raw = f.read()
# raw = re.sub(r'\d+\s+GABRIEL GARCIA MARQUES x ONE HUNDRED YEARS OF SOLITUDE', '', raw)

# chapter_list = re.split(r"Chapter \d+", raw)
chapter_list = re.split(r"CHAPTER_[a-zA-Z]+", raw)
print("length:", len(chapter_list))
for i in range(0, len(chapter_list)):
    file_name = directory + f"section_{i}_part_0.txt"
    f = open(file_name, "w")
    f.write(chapter_list[i].strip())
    f.close()
