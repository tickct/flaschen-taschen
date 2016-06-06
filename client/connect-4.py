import flaschen
import time
import random
import copy

UDP_IP = 'localhost'
UDP_PORT = 1337

ft = flaschen.Flaschen(UDP_IP, UDP_PORT, 45, 35,transparent=True)
piecePattern=[[' ','x','x','x',' '],
              ['x','x','x','x','x'],
              ['x','x','x','x','x'],
              ['x','x','x','x','x'],
              [' ','x','x','x',' ']]

def main():
    board=[[0 for col in range(7)] for row in range(6)]
    winner = False
    player=1
    while(True):
        bPrint(board)
        fPrint(board)
        winLoc=check(board)
        if(winLoc != (0,0,-1)):
            break
        player=opponent(player)
        if player==2:
            board=move(board,player)
        else:
            board=aiMove(board,player)
    won(board,winLoc)

def move(board,player):
    col=input(str(player)+">")-1
    board[height(board,col)][col]=player  
    return board

def height(board, col):
    i = 0
    while(board[i][col] != 0):
        i+=1
    return i
def opponent(player):
    if player == 1:
        return 2
    else:
        return 1

#--- Vitory Checks ---#
def check(board):
    winType=0
    for i in range (6):
        for j in range (7):
            if(board[i][j] != 0):
                if(fourCol(board,board[i][j],i,j)):
                     return (i,j,0)
                elif(fourRow(board,board[i][j],i,j)):
                     return (i,j,1)
                elif(fourDial(board,board[i][j],i,j)):
                     return(i,j,2)
                elif(fourDiar(board,board[i][j],i,j)):
                    return(i,j,3)
    return (0,0,-1)

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
    if(col>3 and row<3):
        for x in range(4):
            if(board[row+x][col-x] != val):
                return False
        return True
    return False

#--- Output ---#
def fPrint(board):
    cDic={}
    for i in range(6):
        for j in range(7):
          cDic['x']=color(board[i][j])
          ft.setSymbol(piecePattern,((5+5*j)),35-(5+5*i),cDic)
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

#--- Game end animation ---#
def won(board,winLoc):
    winA=[]
    #col win
    if(winLoc[2]==0):
        for x in range(4):
            winA.append((winLoc[0]+x,winLoc[1]))
    #row win
    elif(winLoc[2]==1):
        for x in range(4):
            winA.append((winLoc[0],winLoc[1]+x))
    #dial
    elif(winLoc[2]==2):
        for x in range(4):
            winA.append((winLoc[0]-x,winLoc[1]+x))
    #diar
    else:
        for x in range(4):
            winA.append((winLoc[0]+x,winLoc[1]+x))
    print(winA)
    cDic={'x':color(board[winLoc[0]][winLoc[1]])}
    clear={'x':(1,1,1)}
    while(True):
        for x in xrange(4):
              ft.setSymbol(piecePattern,(5+5*winA[x][1]),35-(5+5*winA[x][0]),clear)
        ft.send()
        time.sleep(.5)
        for x in xrange(4):
            ft.setSymbol(piecePattern,(5+5*winA[x][1]),35-(5+5*winA[x][0]),cDic)
        ft.send()
        time.sleep(.5)

#--- AI ---#
def aiMove(board,player):
    cBoards=boardArray(board,player)
    pBoards=boardArray(board,opponent(player))
    costs=[0]*7
    for x in xrange(7):
        if(check(cBoards[x]) != (0,0,-1)):
            costs[x]=2000
        elif(check(pBoards[x]) != (0,0,-1)):
            costs[x]=1000
        else:
            for j in range(-1,1):
                for k in range(-1,2):
                    if (height(board,x)+j)>=0 and (height(board,x)+j) <6 and x+k>=0 and x+k<7:
                        print(str(j)+':'+str(k))
                        if board[height(board,x)+j][x+k]==opponent(player):
                            costs[x] += 1
    print(costs)
    col=costs.index(max(costs))
    board[height(board,col)][col]=player
    return board
           
def boardArray(board,player):
    aBoards=[]
    for x in xrange(7):
       copy=[row[:] for row in board]
       aBoards.append(copy)
       aBoards[x][height(aBoards[x],x)][x]=player
    return aBoards

main()

