# Baseado em https://github.com/jameswylde/openai-chatgpt-terminal

import openai
import sys
import random
import string
import shutil
import argparse
import readline
import os
from types import NoneType
from colorama import Fore, Back, Style
import time
from genie.src.extras import lamp
from genie.src.prompts import opcoes, chains
from llm.llm import chain, chainPiada, chainWithHistory, chainRetriever, chainRetrieverWithHistory
from controllers.DocumentsController import saveDocument, deleteDocumento, listDocumentos

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
        num_columns = 5
        column_width = term_width // num_columns
        formatted_prompts = []

        for i, prompt in enumerate(opcoes):
            formatted_prompt = f"{prompt.split(':')[0]}"
            padded_prompt = formatted_prompt.center(column_width)
            formatted_prompts.append(padded_prompt)

        print(Fore.YELLOW + "=" * term_width)
        for i, formatted_prompt in enumerate(formatted_prompts):
            print(Fore.YELLOW + formatted_prompt, end="")
            if (i + 1) % num_columns == 0 and i != len(formatted_prompts) - 1:
                print()
        print(Fore.YELLOW + "\n" + "=" * term_width + Style.RESET_ALL)
        
    def display_prompt_chain():
        term_width = shutil.get_terminal_size((80, 20)).columns
        num_columns = 5
        column_width = term_width // num_columns
        formatted_prompts = []

        for i, prompt in enumerate(chains):
            formatted_prompt = f"{i + 1} - {prompt.split(':')[0]}"
            padded_prompt = formatted_prompt.center(column_width)
            formatted_prompts.append(padded_prompt)

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

    def parse_commands(menu):
        comando = menu.split(" ")
        if comando[0] == "/chain":
            if len(comando) == 2:
                opcao = int(comando[1]) 
                changeChain(opcao)
            else:
                print(Fore.MAGENTA + "Valor inválido, selecione uma das opções desejada")
                print(Fore.MAGENTA + f"Chain atual: {chains[mainChain - 1]}")
                display_prompt_chain()
        elif comando[0] == "/addDoc":
            comando = menu[8:].split(",")
            if len(comando) == 3:
                print(Fore.MAGENTA + saveDocument(comando[0].strip(), comando[1].strip(), comando[2].strip()))
            else:
                print(Fore.MAGENTA + "Para inserir um documento é preciso passar 3 parâmetros, \"Caminho do arquivo\", \"Título do Arquivo\" e \"Descrição do Arquivo\", os campos devem ser separados por \",\"")
        elif comando[0] == "/delDoc":
            if len(comando) == 2:
                opcao = int(comando[1]) 
                deleteDocumento(opcao)
                print(Fore.MAGENTA + f"Documento {opcao} deletado com sucesso!")
            else:
                print(Fore.MAGENTA + "Para deletar o documento é preciso passar o ID do documento")
        elif comando[0] == "/listDoc":
            documentos = listDocumentos(None)
            print()

            term_width = shutil.get_terminal_size((80, 20)).columns
            num_columns = 6
            column_width = term_width // num_columns
            formatted_prompts = ["| documento_id".ljust(column_width)[:column_width], "| titulo".ljust(column_width)[:column_width], "| descricao".ljust(column_width)[:column_width], "| md5".ljust(column_width)[:column_width], "| url".ljust(column_width)[:column_width], "| chunks".ljust(column_width)[:column_width]]

            print(Fore.MAGENTA + "-" * term_width)
            header = ""
            for formatted_prompt in formatted_prompts:
                header += formatted_prompt

            print(Fore.MAGENTA + header.ljust(term_width)[:term_width])
            print(Fore.MAGENTA + "-" * term_width)
            
            for documento in documentos:
                line = ""
                for doc in documento:
                    if isinstance(doc, str):
                        line += str("| "+doc).ljust(column_width)[:column_width]
                    if isinstance(doc, NoneType):
                        line += str("| ").ljust(column_width)[:column_width]
                    elif isinstance(doc, int):
                        line += str("| "+str(doc)).ljust(column_width)[:column_width]
                    elif isinstance(doc, list):
                        line += str("| Quantidade: "+str(len(doc))).ljust(column_width)[:column_width]
                print(Fore.MAGENTA + line.ljust(term_width)[:term_width])
            print()
        elif comando[0] == "/clearHist":
            print(Fore.MAGENTA + menu)
        elif comando[0] == "/menu":
            display_prompt_menu()
        else:
            print(Fore.MAGENTA + f"Comando \"{menu}\" não encontrado")
            display_prompt_menu()
            
        
    args = parse_args()

    if args.question:
        prompt = " ".join(args.question).rstrip(string.punctuation)
    else:
        print(Fore.YELLOW + center_multiline_string(random.choice(lamp)))

        prompt: str = ""
        
        display_prompt_menu()

    while True:
        prompt = get_user_input(Fore.BLUE + "Você: ")
        
        if prompt.lower() in ["quit", "q", "bye"]:
            print(
                Fore.YELLOW
                + "\nCompliAI: "
                + "Até mais...\n" + Style.RESET_ALL 
            )
            break
        
        if len(prompt) > 0:
            if prompt.lower()[0] == "/":
                parse_commands(prompt)
            else:
                if len(prompt) > 0:
                    response = callChain(prompt)
                
                if len(response) > 0:
                    print(Fore.GREEN + "\nCompliAI: ", end='')
                    for element in response:
                        time.sleep(0.01)
                        print(element, end='', flush=True)
                    print("\n")
                    response = ""

if __name__ == "__main__":
    main()