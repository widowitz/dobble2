# Dobble / aka Spot-it
# global variables:
# s: number of symbols on each card
# n: number of symbols that exist overall
# k: number of cards populated
#
# interestingly, maximum k equals n (see below for reasoning)
# n = s * (s-1) + 1
# 
# Rule 1:
# each card with s symbols, each different from each other
#
# Rule 2:
# any pair of two cards share exactly one symbol amongst each other
# (not more, not less)
#
# Rule 3:
# there is not one symbol that shows up on all of the cards
# (as that would be an easy solution, but very uninteresting)
#
# example solution for s = 4:
# (symbols denoted with letters A..M)
# 
#           A B C D E F G H I J K L M
# card 01:  x x x x . . . . . . . . .
# card 02:  x . . . x x x . . . . . .
# card 03:  x . . . . . . x x x . . .
# card 04:  x . . . . . . . . . x x x
# card 05:  . x . . x . . x . . x . .
# card 06:  . x . . . x . . x . . x .
# card 07:  . x . . . . x . . x . . x
# card 08:  . . x . x . . . x . . . x
# card 09:  . . x . . x . . . x x . .
# card 10:  . . x . . . x x . . . x .
# card 11:  . . . x x . . . . x . x . 
# card 12:  . . . x . x . x . . . . x
# card 13:  . . . x . . x . x . x . .
#
# from the above we can deduce that each symbol
# appears only exactly s times!
# why?
# imagine we would start card 5 with an A.
# (which we are about to prove that it is impossible)
# then we would need to continue with N, O and P
# but how can then a card 6, with only 4 symbols, connect
# to 1, 2, 3, 4, AND 5? --> impossible, as it needs to
# connect with one out of BCD, EFG, HIJ, KLM and NOP
# with only four available symbols

# therefore, the symbol A can appear only 4 times (s times)
# 
#
# from all of the above we can model our three constraints:
# constraint 1: the rowsum in each row (card) has to be equal to s
# constraint 2: the colsum in each column (symbol use) has to be
#               equal to s as well
# constraint 3: comparing the vector of any two cards, there must
#               be exactly one match
#               e.g. card 01: 'xxxx.........' and 
#                    card 02: 'x...xxx......'
#               match at the first slot
#
# with all of this, it should be easy to run this through! so let's go!

import constraint, string


def print_solution(solution, n):
    indices = sorted(solution)
    values = [solution[x] for x in indices]
    i = 0
    for x in values:
        xx = 'X' if x==1 else '.'
        print(f"{xx}  ", end="")
        i += 1
        if i == n:
            i = 0
            print('\n', end="")
    return


def two_cards_have_exactly_one_symbol_in_common(*args):
    """
    the args are in a slightly weird format
    [1, 1, 0, 0, 1, 0, 1, 0]
    for example means that the first half is the first card,
    and the second half is the second card

    [1, 1, 0, 0,  <split here>   1, 0, 1, 0]
    the 1 and 0 signify whether the symbol is used on that card or not
    """
    length = len(args)
    middle_index = length//2
    card1 = args[:middle_index]
    card2 = args[middle_index:]
    common = 0
    assert len(card1) == len(card2), 'cards are weird'
    for i in range(len(card1)):
        if card1[i] + card2[i] == 2: common += 1
    return(common == 1) 


def main():
    print("Welcome to the Dobble solver")
    DOBBLE_s = 4                                # the number of symbols per card
    DOBBLE_n = DOBBLE_s * (DOBBLE_s - 1) + 1    # the number of symbols in the universe; 
                                                # 'coincidentally' equal to the number of cards
    problem = constraint.Problem()

    # first we create the variables for our problem:
    # each variable denotes one slot in the matrix shown in the
    # example solution, and will be either 0 or 1
    # 1 meaning that on this particular card (row), this particular
    # symbol (column) is present
    for card_number in range(1, DOBBLE_n + 1):
        for symbol_number in range(1, DOBBLE_n + 1):
            variable_name = f"C{card_number:03}_S{symbol_number:03}"
            problem.addVariable(variable_name, [0,1])

    # now we add constraint 1:
    # each card has exactly s occupied slots
    for card_number in range(1, DOBBLE_n + 1):
        all_variable_names_in_that_row = [f"C{card_number:03}_S{x:03}" for x in range(1, DOBBLE_n + 1)]
        problem.addConstraint(
            constraint.ExactSumConstraint(DOBBLE_s), 
            all_variable_names_in_that_row
        )
    
    # now we add constraint 2:
    # each symbol is used exactly s times
    for symbol_number in range(1, DOBBLE_n + 1):
        all_variable_names_in_that_column = [f"C{x:03}_S{symbol_number:03}" for x in range(1, DOBBLE_n + 1)]
        problem.addConstraint(
            constraint.ExactSumConstraint(DOBBLE_s), 
            all_variable_names_in_that_column
        )

    # now we add constraint 3:
    # iterate each row against all previous ones
    # counting the number of joint symbols between them
    # and returning True if exactly one joint symbol exists
    for r1 in range(1, DOBBLE_n + 1):
        for r2 in range(r1 + 1, DOBBLE_n + 1):
            row1 = [f"C{r1:03}_S{symbol_number:03}" for symbol_number in range(1, DOBBLE_n + 1)]
            row2 = [f"C{r2:03}_S{symbol_number:03}" for symbol_number in range(1, DOBBLE_n + 1)]
            both_rows = row1 + row2
            problem.addConstraint(
                constraint.FunctionConstraint(two_cards_have_exactly_one_symbol_in_common), 
                both_rows
            )
    
    # we solve it and print the result:
    solution = problem.getSolution()
    print_solution(solution, DOBBLE_n)
    return


    

if __name__ == "__main__":
    main()

