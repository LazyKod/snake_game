from tkinter import * 
from PIL import Image, ImageTk 
from random import randrange
from math import log

#reupdate image
delay = 70
milli=delay

#grid
GRIDSIZE=20
coord_x=30 #ligne
coord_y=30 #colonne

#score et initialisation
score = 0
scoreboard=[] #pour le best score

initialisation=0

#éviter overlapping
move_snake_id = None  

root = Tk()
root.title("Snake")

# Create a container frame to hold all displays
container=Frame(root)
container.pack(expand=True, fill="both")
container.rowconfigure(0, weight=1)
container.columnconfigure(0, weight=1)

# Créer dico pour store Frames
frames={}



# Créer nos frames menu et jeu
for F in ["Menu", "Jeux", "Lost"]:
    fr= Frame(container)
    fr.grid(row=0, column=0, sticky="nsew")
    frames[F]=fr


frames["Jeux"].config(background="#17054B")
# Make Jeux frame expand with screen
frames["Jeux"].grid_propagate(False)  # Prevent it from shrinking

my_score=StringVar(value="Score : 0") #Variable mouvante qui permet de stocker le score et de le changer
best_score=StringVar(value="Best score : ")

top_frame=Frame(frames["Jeux"], bg="#17054B")
top_frame.pack(side="top", fill=X, pady=10)

score_lab=Label(top_frame, textvariable=my_score, foreground="red", background="#17054B", font=("Arial", 10,"bold"))
score_lab.pack(side="left", expand=False, padx=20)

best_sc=Label(top_frame, textvariable=best_score, foreground="white", background="#17054B", font=("Arial", 10,"bold"))
best_sc.pack(side="right",expand=False, padx=20)

canvas = Canvas(frames["Jeux"], width=600, height=600, bg="black")
canvas.pack(side=BOTTOM, expand=True)


#Créer un menu pour commencer le jeu 
frames["Menu"].config(width=600, height=600, background="White")

bg_image = Image.open("ressources\snake.png")  # Replace with your image file
bg_image = bg_image.resize((600, 600))   # Resize to match window
bg_photo = ImageTk.PhotoImage(bg_image)

bg_label = Label(frames["Menu"], image=bg_photo)
bg_label.place(relwidth=1, relheight=1)

but = Button(frames["Menu"], text ="Start", background="#EEEEEE", foreground="black", font=("Arial", 12, "bold"), command=lambda : show_frame("Jeux"))
but.place(relx=0.5, rely=0.5, anchor="center")



# Créer frame si jeu perdu avec le score :
frames["Lost"].config(background="#17054B")

final_score=StringVar(value="")

text_lost= Label (frames["Lost"], text= "Game Over", font=("Game Over", 150, "bold"), background="#17054B",foreground="white")
text_lost.pack(pady=20, anchor="center")

text_score = Label(frames["Lost"], textvariable= final_score, font=("Game Over", 100),foreground="white",background="#17054B")
text_score.pack(pady=50, anchor="center")

text_score = Label(frames["Lost"], textvariable= best_score, font=("Game Over", 80),foreground="white",background="#17054B")
text_score.pack(anchor="center")

button_retry=Button(frames["Lost"], text="Retry",background="#17054B", foreground="White", font=("Arial", 20, "bold"), command=lambda : restart_game())
button_retry.pack(pady=100, anchor="center")



# Commencer à coder le jeu
# il y a un grid de : 30x30 =900 blocs

snake_corps={} #item snake aka son corps
snake_dir={} #direction de chaque item du snake
aliment={}

#initalisation de l'aliment
def init():
    global direction, initialisation
    rand_graille_i = randrange(0,coord_x)
    rand_graille_j= randrange(0,coord_y)
    aliment[0] = canvas.create_rectangle(rand_graille_j*GRIDSIZE, rand_graille_i*GRIDSIZE,(rand_graille_j +1)*GRIDSIZE, (rand_graille_i+1)*GRIDSIZE,  fill="white")
    snake_corps[0]=canvas.create_rectangle(int(coord_x/2)*GRIDSIZE, int(coord_y/2)*GRIDSIZE, (int(coord_x/2)+1)*GRIDSIZE, (int(coord_y/2)+1)*GRIDSIZE, fill="blue")
    direction_ini=["Up","Down","Left","Right"]
    random_num=randrange(0,4)
    direction= direction_ini[random_num]
    my_score.set(f"Score : {score}")
    initialisation=1


#update de l'aliment
def update_alim(nombre):
    global aliment
    canvas.delete(aliment[nombre])
    rand_graille_i = randrange(0,coord_x)
    rand_graille_j= randrange(0,coord_y)
    aliment[int(nombre)+1] = canvas.create_rectangle(rand_graille_j*GRIDSIZE, rand_graille_i*GRIDSIZE,(rand_graille_j +1)*GRIDSIZE, (rand_graille_i+1)*GRIDSIZE,  fill="white") #TO do : l'aliment ne doit pas pop sur le snake

#Récupération de la direction active
def move(event):
    global direction
    if direction =="Up":
        if event.keysym=="Up":
            direction="Up"
        elif event.keysym == "Left":
            direction="Left"
        elif event.keysym == "Right":
            direction="Right"
    
    elif direction =="Down":
        if event.keysym=="Down":
            direction="Down"
        elif event.keysym == "Left":
            direction="Left"
        elif event.keysym == "Right":
            direction="Right"

    elif direction =="Left":
        if event.keysym=="Up":
            direction="Up"
        elif event.keysym=="Down":
            direction="Down"
        elif event.keysym == "Left":
            direction="Left"

    elif direction =="Right":
        if event.keysym=="Up":
            direction="Up"
        elif event.keysym=="Down":
            direction="Down"
        elif event.keysym == "Right":
            direction="Right"
root.bind("<KeyPress>", move)

#permet de bouger le snake en fonction de la direction associée

#game over : si touche bordure ou touche son corps
def game_over():
    global score
    x1, y1, x2, y2 = canvas.coords(snake_corps[score])
    if x1<0 or y1<0 or x2> GRIDSIZE*coord_x or y2> GRIDSIZE*coord_y:
        return reset()
    snake_verif=[snake_corps[i] for i in range(score)]
    for snakes in snake_verif:
        i1,j1,i2,j2 = canvas.coords(snakes)
        if i1 == x1 and j1==y1 and i2 ==x2 and j2 ==y2 :
            return reset()


def reset ():
    global score, initialisation, move_snake, move_snake_id, milli, delay, scoreboard
    final_score.set(f"Final Score : {score}")
    for i in range(score+1):
            canvas.delete(snake_corps[i])
            canvas.delete(snake_dir[i])
            canvas.delete(aliment[i])
    if move_snake_id is not None:
        root.after_cancel(move_snake_id)
        move_snake_id = None
    initialisation=0
    scoreboard.append(score)
    score=0
    milli=delay
    show_frame("Lost")

def scoreboard_update():
    global scoreboard, score
    scoreboard.sort(reverse=True)
    if len(scoreboard)==0 or scoreboard[0]<score:
        best_score.set(f"Best score : {score}")
    else :
        best_score.set(f"Best score : {scoreboard[0]}")


def restart_game():
    global move_snake_id, score, initialisation, milli, delay
    if move_snake_id is not None:
        root.after_cancel(move_snake_id)
        move_snake_id=None
    milli=delay
    show_frame("Jeux")

def difficulté():
    global milli, score
    if score <10 :
        milli -= int(round(0.3*score, 0))
    else :
        milli -= int(round(log(score)/5,0))

def avancer(): # TO do : interdire de bouger vers la auche si il bouge vers la gauche
    for i in range(score): #transmission de la direction à chacun
        snake_dir[i]=snake_dir[i+1]
    snake_dir[score]=direction

    k=0 
    while score>=k: #mouvement de chacune des parties en fonction de sa direction
        if snake_dir[k]=="Up":
            canvas.move(snake_corps[k],0,-GRIDSIZE)
        if snake_dir[k]=="Down":
            canvas.move(snake_corps[k],0,GRIDSIZE)
        if snake_dir[k]=="Left":
            canvas.move(snake_corps[k],-GRIDSIZE,0)
        if snake_dir[k]=="Right":
            canvas.move(snake_corps[k],GRIDSIZE,0)
        k+=1

def grow():
    global score, direction, snake_dir, snake_corps
    #creation d'un rectangle à l'avant en fonction de la direction
    x1, y1, x2, y2 = canvas.coords(snake_corps[score])
    if direction =="Up":
        y1= y1-GRIDSIZE
        y2=y2-GRIDSIZE
    elif direction =="Down":
        y1=y1+GRIDSIZE
        y2=y2+GRIDSIZE
    elif direction =="Left":
        x1=x1-GRIDSIZE
        x2=x2-GRIDSIZE
    elif direction =="Right":
        x1=x1+GRIDSIZE
        x2=x2+GRIDSIZE
    
    #vérifier si le triangle et la graille sont pareils:
    x12, y12, x22, y22 = canvas.coords(aliment[score])
    if x12==x1 and y12==y1 and x22==x2 and y22==y2:
        update_alim(score)
        score+=1
        difficulté()
        my_score.set(f"Score : {score}")
        snake_corps[score]=canvas.create_rectangle(x1,y1,x2,y2, fill="blue")
        snake_dir[score]=direction


#Boucle qui permet de bouger pendant X ms
def move_snake():
    global move_snake_id, milli
    if initialisation == 0:
        init()
    grow()
    avancer()
    game_over()
    scoreboard_update()
    if initialisation == 1 :
        move_snake_id = root.after(milli, move_snake)
        

#Crer une fonction qui permet de mettre en avant une frame
def show_frame(frame_name):
    global move_snake_id, milli
    frames[frame_name].tkraise()
    root.focus_set()
    if frame_name == "Jeux": # le jeux ne se lance que lorsque la frame est active 
        if move_snake_id is not None:
            root.after_cancel(move_snake_id)
            move_snake_id = None
        move_snake()

show_frame("Menu")

root.grid_propagate()
root.mainloop()