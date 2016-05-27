import flaschen

UDP_IP = 'ft.noise'
UDP_PORT = 1337

ft = flaschen.Flaschen(UDP_IP, UDP_PORT, 45, 35,transparent=True)
piecePattern=[['','x','x','x',''],
              ['x','x','x','x','x'],
              ['x','x','x','x','x','x'],
              ['x','x','x','x','x'],
              ['','x','x','x','']]
def main():
    board=[[0 for col in range(7)] for row in range(6)]
    winner = False
    player=1
    while(True):
        bPrint(board)
        fPrint(board)
        if(check(board)):
            break
        player=opponent(player)
        board=move(board,player)
    print("player"+str(player)+" has won")
def move(board,player):
    col = input(str(player)+">")-1
    i = 0
    while(board[i][col] != 0):
        i+=1
    board[i][col]=player
    return board
def opponent(player):
    if player == 1:
        return 2
    else:
        return 1


def check(board):
    for i in range (6):
        for j in range (7):
            if(board[i][j] != 0):
                if(fourCol(board,board[i][j],i,j) or fourRow(board,board[i][j],i,j) or fourDial(board,board[i][j],i,j) or fourDiar(board,board[i][j],i,j) ):
                    return True
    return False

def fourCol(board,val,row,col):
    if(row<3):
        for x in range(4):
            if(board[row+x][col] != val):
                return False
        return True
    return False

def fourRow(board,val,row,col):
    if(col<4):
        for x in range(4):
            if(board[row][col+x] != val):
                return False
        return True
    return False

def fourDiar(board,val,row,col):
    if(col<4 and row<3):
        for x in range(4):
            if(board[row+x][col+x] != val):
                return False
        return True
    return False

def fourDial(board,val,row,col):
    if(col<3 and row<3):
        for x in range(4):
            if(board[row+x][col-x] != val):
                return False
        return True
    return False

def fPrint(board):
    cDic={}
    for i in range(6):
        for j in range(7):
          cDic['x']=color(board[i][j])
          ft.setSymbol(piecePattern,(5+5*i),(5+5*j),cDic)
    ft.send()

def color(val):
    if val == 0:
        return (0,0,0)
    elif val == 1:
        return (255,0,0)
    else:
        return (0,0,255)
            
def bPrint(board):
    for i in range(6):
        line=""
        for j in range(7):
          line=line+str(board[5-i][j])+"|"
        print(line)
    print("1 2 3 4 5 6 7")
    
main()
