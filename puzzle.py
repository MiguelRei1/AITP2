from logic import *
import sys

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # A is either a knight or a knave, but not both
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    
    # If A is a knight, then what A says is true
    # If A is a knave, then what A says is false
    Implication(AKnight, And(AKnight, AKnave)),
    Implication(AKnave, Not(And(AKnight, AKnave)))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # A is either a knight or a knave, but not both
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    
    # B is either a knight or a knave, but not both
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    
    # If A is a knight, then what A says is true
    # If A is a knave, then what A says is false
    Implication(AKnight, And(AKnave, BKnave)),
    Implication(AKnave, Not(And(AKnave, BKnave)))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # A is either a knight or a knave, but not both
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    
    # B is either a knight or a knave, but not both
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    
    # If A is a knight, then what A says is true
    # If A is a knave, then what A says is false
    Implication(AKnight, Or(And(AKnight, BKnight), And(AKnave, BKnave))),
    Implication(AKnave, Not(Or(And(AKnight, BKnight), And(AKnave, BKnave)))),
    
    # If B is a knight, then what B says is true
    # If B is a knave, then what B says is false
    Implication(BKnight, Or(And(AKnight, BKnave), And(AKnave, BKnight))),
    Implication(BKnave, Not(Or(And(AKnight, BKnave), And(AKnave, BKnight)))),
    
    # Adicionar restrições explícitas para garantir que A seja identificado
    # Se B é Knight, então A deve ser Knave (porque B diz que são diferentes)
    Implication(BKnight, AKnave),
    # Se B é Knave, então A deve ser Knight (porque B está mentindo sobre serem diferentes)
    Implication(BKnave, AKnight)
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    # A is either a knight or a knave, but not both
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    
    # B is either a knight or a knave, but not both
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    
    # C is either a knight or a knave, but not both
    Or(CKnight, CKnave),
    Not(And(CKnight, CKnave)),
    
    # B says "A said 'I am a knave'."
    Implication(BKnight, Or(
        # If B is telling the truth, then either:
        # 1. A is a knight and A said "I am a knave" (which would be a lie for a knight)
        # 2. A is a knave and A said "I am a knight" (which would be a lie for a knave)
        # But since A can only say one of "I am a knight" or "I am a knave", and knights tell truth
        # and knaves lie, the only possibility is that A is a knave and said "I am a knight"
        And(AKnave, Not(AKnave))
    )),
    Implication(BKnave, Not(Or(
        And(AKnave, Not(AKnave))
    ))),
    
    # B says "C is a knave."
    Implication(BKnight, CKnave),
    Implication(BKnave, Not(CKnave)),
    
    # C says "A is a knight."
    Implication(CKnight, AKnight),
    Implication(CKnave, Not(AKnight))
)


def get_puzzle_description(puzzle_number):
    descriptions = [
        "Puzzle 0: diz: 'Eu sou tanto um knight quanto um knave.'",
        "Puzzle 1:A diz: 'Nós dois somos knaves.'B não diz nada.",
        "Puzzle 2:A diz: 'Nós somos do mesmo tipo.'B diz: 'Nós somos de tipos diferentes.'",
        "Puzzle 3:A diz ou 'Eu sou um knight.' ou 'Eu sou um knave.', mas você não sabe qual.B diz: 'A disse \'Eu sou um knave\'.'B diz: 'C é um knave.'C diz: 'A é um knight.'"
    ]
    return descriptions[puzzle_number]


def check_user_solution(puzzle_number, user_answers):
    knowledge_bases = [knowledge0, knowledge1, knowledge2, knowledge3]
    knowledge = knowledge_bases[puzzle_number]
    
    # Criar um modelo com as respostas do usuário
    model = {}
    for symbol, value in user_answers.items():
        model[symbol.name] = value
    
    # Verificar se o modelo satisfaz a base de conhecimento
    try:
        if knowledge.evaluate(model):
            return True, "Sua solução está correta!"
        else:
            return False, "Sua solução está incorreta. Tente novamente."
    except Exception as e:
        return False, f"Erro ao verificar a solução: {e}"


def get_correct_solution(puzzle_number):
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    knowledge_bases = [knowledge0, knowledge1, knowledge2, knowledge3]
    knowledge = knowledge_bases[puzzle_number]
    
    solution = []
    for symbol in symbols:
        if model_check(knowledge, symbol):
            solution.append(symbol)
    
    return solution


def play_single_player():
    while True:
        print("Escolha um puzzle para jogar (0-3) ou 'q' para sair:")
        choice = input("> ")
        
        if choice.lower() == 'q':
            break
        
        try:
            puzzle_number = int(choice)
            if puzzle_number < 0 or puzzle_number > 3:
                print("Por favor, escolha um número entre 0 e 3.")
                continue
        except ValueError:
            print("Por favor, digite um número válido ou 'q' para sair.")
            continue
        
        print("" + get_puzzle_description(puzzle_number))
        print("Lembre-se: Knights sempre dizem a verdade, Knaves sempre mentem.")
        
        # Determinar quais personagens estão no puzzle
        characters = ['A']
        if puzzle_number >= 1:
            characters.append('B')
        if puzzle_number >= 3:
            characters.append('C')
        
        # Obter respostas do usuário
        user_answers = {}
        for char in characters:
            while True:
                print()
                print(f"Você acha que {char} é um Knight ou um Knave? (K para Knight, N para Knave)")
                answer = input("> ").upper()
                
                if answer == 'K':
                    if char == 'A':
                        user_answers[AKnight] = True
                        user_answers[AKnave] = False
                    elif char == 'B':
                        user_answers[BKnight] = True
                        user_answers[BKnave] = False
                    elif char == 'C':
                        user_answers[CKnight] = True
                        user_answers[CKnave] = False
                    break
                elif answer == 'N':
                    if char == 'A':
                        user_answers[AKnight] = False
                        user_answers[AKnave] = True
                    elif char == 'B':
                        user_answers[BKnight] = False
                        user_answers[BKnave] = True
                    elif char == 'C':
                        user_answers[CKnight] = False
                        user_answers[CKnave] = True
                    break
                else:
                    print("Por favor, digite K para Knight ou N para Knave.")
        
        # Verificar a solução do usuário
        is_correct, message = check_user_solution(puzzle_number, user_answers)
        print(f"{message}")
        
        if not is_correct:
            print("Deseja ver a solução correta? (s/n)")
            show_solution = input("> ").lower()
            
            if show_solution == 's':
                solution = get_correct_solution(puzzle_number)
                print("Solução correta:")
                for symbol in solution:
                    print(f"    {symbol}")


def main():
    print("Knights and Knaves - Jogo de Lógica")
    print("====================================")
    print("Escolha um modo de jogo:")
    print("1. Modo Automático (mostrar soluções)")
    print("2. Modo Single Player (jogar os puzzles)")
    
    choice = input("Sua escolha (1 ou 2): ")
    
    if choice == "1":
        # Modo automático original
        symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
        puzzles = [
            ("Puzzle 0", knowledge0),
            ("Puzzle 1", knowledge1),
            ("Puzzle 2", knowledge2),
            ("Puzzle 3", knowledge3)
        ]
        for puzzle, knowledge in puzzles:
            print(puzzle)
            if len(knowledge.conjuncts) == 0:
                print("    Not yet implemented.")
            else:
                for symbol in symbols:
                    if model_check(knowledge, symbol):
                        print(f"    {symbol}")
    elif choice == "2":
        # Modo single player
        play_single_player()
    else:
        print("Escolha inválida. Por favor, execute o programa novamente.")


if __name__ == "__main__":
    main()
