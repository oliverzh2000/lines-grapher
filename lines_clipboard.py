import pyperclip
import sys

for line in open(sys.argv[1]).readlines():
    pyperclip.copy(line)
    user_prompt = input(line.strip("\n"))
    if user_prompt in ("exit", "quit"):
        break
