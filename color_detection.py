def color(R, G, B):
    if R > G and R > B:
        return 'Red'
    elif G > R and G > B:
        return 'Green'
    elif B> G and B > R:
        return 'Blue'
    elif (R == 0 and B == 0 and G == 0) or (R==G and G== B and R == B):
        return 'Black'
    else:
        return 'White'