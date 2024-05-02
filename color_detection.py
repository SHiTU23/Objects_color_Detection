def color(R, G, B):
    if R > G and R > B:
        return 'Red'
    elif G > R and G > B:
        return 'Green'
    elif B> G and B > R:
        return 'Blue'
    elif ((R==G and G== B and R == B) or
          (R == G or R == B or G == B)):
        return 'Black'
    else:
        return 'White'