from lr import *

if __name__ == "__main__":
    N_cnt, SIGMA_cnt, P_cnt = [int(i) for i in input().split()]
    non_terms = list(input())
    terms = list(input())
    Rules = set()
    for i in range(P_cnt):
        Rules.add(input())
    start = input()
    LR = LR1_Parser()
    LR.fit(start, terms, non_terms, Rules)
    check_cnt = int(input())
    for i in range(check_cnt):
        word = input()
        print("Yes" if LR.predict(word) else "No")
