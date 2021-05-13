def f_a(S, Xb, l, h):
    if(abs(Xb-l) <= 10**-10):
        return 1./(S[0] + S[2])
    elif(abs(Xb-h) <= 10**-10):
        return 1./(S[0])
    else:
        print("Error!")
        print("Xn=", Xb, "l=", l, "h=", h)
    return
