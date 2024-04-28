# Baseado em https://github.com/jameswylde/openai-chatgpt-terminal

import openai
import sys
import random
import string
import colorama
import shutil
import argparse
import readline
import os
from colorama import Fore, Back, Style
import time
from genie.src.extras import greeting, lamp
from genie.src.prompts import chains
from llm.llm import chain, chainPiada, chainWithHistory, chainRetriever, chainRetrieverWithHistory

"""
Genie: A Python implementation of OpenAI's ChatGPT integrated into your shell.
Interact with the model interactively or pass questions to it from the terminal.
Supports custom prompts for honed interaction and switching of API model.
"""

mainChain:int = 2

def changeChain(chainNumber: int):
    global mainChain
    mainChain=chainNumber
    print(Fore.MAGENTA + "Alterdo Chain para " + chains[chainNumber-1].split(":")[0])
    
def callChain(input: str)-> str:
    global mainChain
    if mainChain==1:
        return chainPiada(input)
    elif mainChain==2:
        return chain(input)
    elif mainChain==3:
        return chainRetriever(input)
    elif mainChain==4:
        return chainRetrieverWithHistory(input, 123)
    else:
        return chainWithHistory(input, 123)

    

def main():
    openai.api_key = os.environ['OPENAI_API_KEY']

    def parse_args():
        parser = argparse.ArgumentParser(description="Genie: Chat with ChatGPT")
        parser.add_argument(
            "--model",
            default="gpt-3.5-turbo",
            choices=["gpt-4", "gpt-3.5-turbo", "code-davinci-002", "text-davinci-003"],
            help="Choose the API model to use",
        )
        parser.add_argument(
            "--temperature",
            default=0.7,
            type=float,
            help="Control the randomness of the response (default: 0.7)",
        )
        parser.add_argument(
            "question", nargs="*", help="Optional question for non-interactive mode"
        )
        return parser.parse_args()

    def display_prompt_menu():
        term_width = shutil.get_terminal_size((80, 20)).columns
        num_columns = 3
        column_width = term_width // num_columns
        formatted_prompts = []

        for i, prompt in enumerate(chains):
            formatted_prompt = f"{i + 1} - {prompt.split(':')[0]}"
            padded_prompt = formatted_prompt.center(column_width)
            formatted_prompts.append(padded_prompt)

        print(
            Fore.YELLOW
            + "Escolha a Chain desejada, 'q' para sair ou '/menu' para mostrar as opções:".center(term_width)
            + "\n"
        )
        print(Fore.YELLOW + "=" * term_width)
        for i, formatted_prompt in enumerate(formatted_prompts):
            print(Fore.YELLOW + formatted_prompt, end="")
            if (i + 1) % num_columns == 0 and i != len(formatted_prompts) - 1:
                print()
        print(Fore.YELLOW + "\n" + "=" * term_width + Style.RESET_ALL)

    def center_multiline_string(s):
        term_width = shutil.get_terminal_size((80, 20)).columns
        centered_lines = []

        for line in s.split("\n"):
            padding_left = (term_width - len(line)) // 2
            centered_line = " " * padding_left + line
            centered_lines.append(centered_line)

        return "\n".join(centered_lines)

    def get_user_input(prompt):
        try:
            return input(prompt)
        except (EOFError, KeyboardInterrupt):
            return "q"

    def print_centered_no_newline(text):
        term_width = shutil.get_terminal_size((80, 20)).columns
        padding_left = (term_width - len(text)) // 2
        print(" " * padding_left + text, end="")

    args = parse_args()

    messages = []

    randomgreeting = random.choice(greeting)

    if args.question:
        prompt = " ".join(args.question).rstrip(string.punctuation)
    else:
        print(Fore.YELLOW + center_multiline_string(random.choice(lamp)))

        reply: str = ""
        prompt: str = ""
        
        display_prompt_menu()
        print(Fore.BLUE + "Você: ", end="")
        user_input = get_user_input(Fore.BLUE + "")
        if user_input.strip().isdigit() and 1 <= int(user_input.strip()) <= len(chains):
            changeChain(int(user_input.strip()))
        else:
            prompt = user_input.strip()

    while True:
        if prompt.lower() in ["quit", "q", "bye"]:
            print(
                Fore.YELLOW
                + "\nCompliAI: "
                + "Farewell, master. Until you drag me out of bed again...\n"
            )
            break
        
        if len(prompt) > 0:
            response = callChain(prompt)
            reply = response
        
        if len(reply) > 0:
            print(Fore.GREEN + "\nCompliAI: ", end='')
            for element in reply:
                time.sleep(0.01)
                print(element, end='', flush=True)
            print("\n")

        if args.question:
            break
        else:
            prompt = get_user_input(Fore.BLUE + "Você: ")
            
            if len(prompt) > 0 and prompt.lower()[0] == "/":
                comando = prompt.lower().split(" ")
                if comando[0] == "/chain":
                    if int(comando[1]) > 0:
                        changeChain(int(comando[1]))
                    else:
                        print(Fore.MAGENTA + "Valor inválido, selecione uma das opções desejada")
                        display_prompt_menu()
                elif comando[0] == "/menu":
                    display_prompt_menu()
                    user_input = get_user_input(Fore.BLUE + "Escolha a Chain desejada ou 'q' para sair: ".center(shutil.get_terminal_size((80, 20)).columns)).strip()
                    if user_input.isdigit() and 1 <= int(user_input) <= len(chains):
                        changeChain(int(user_input))
                        prompt = ""
                        reply = ""
                    else:
                        prompt = ""
                        reply = ""
                prompt = ""
                reply = ""

if __name__ == "__main__":
    main()