import numpy as np

def f_a(S, Xb, l, h):
    if(abs(Xb-l) <= 10**-10):
        return 1./(S[0] + S[2])
    elif(abs(Xb-h) <= 10**-10):
        return 1./(S[0])
    else:
        print("Error!")
        print("Xn=", Xb, "l=", l, "h=", h)
    return

def f_b(S, Xb, l, h):
    if(abs(Xb-l) <= 10**-10):
        return Xb/(S[1])
    elif(abs(Xb-h) <= 10**-10):
        return Xb/(S[1] + S[2])
    else:
        print("Error!")

def f_sab(S, Xb, l, h):
    if(abs(Xb-l) <= 10**-10):
        return 1./(S[0] + S[2])
    elif(abs(Xb-h) <= 10**-10):
        return h/(S[1] + S[2])
    else:
        print("Error!")

def F(S, Xb, l, h, alpha, r, m, d, k):
    A, B, SAB = S
    S2 = np.zeros((3))
    N = np.sum(S)
    S2[0] = r*f_a(S, Xb, l, h)*(1-d*N/k)*A-m*A
    S2[1] = r*f_b(S, Xb, l, h)*(1-d*N/k)*B-m*B
    S2[2] = r*f_sab(S, Xb, l, h)*(1-d*N/k)*SAB-m*SAB
    return S2

def iterations(T, S_init, XXb, l, h, alpha, r, m, d, k):
    dt = T[1] - T[0]
    SS = np.zeros((len(T), 3))
    SS[0] = S_init
    for t in range(len(T)-1):
        SS[t+1] = SS[t] + dt*F(SS[t], XXb[t], l, h, alpha, r, m, d, k)
    return SS

Strat = ["ia (always a)", "ib (always b)", "sab (sensitive)"]
Color = ["red", "green", "blue"]
