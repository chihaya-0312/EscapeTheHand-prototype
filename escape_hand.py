import tkinter
import random

hx = 0#手のx座標
hy = 0#手のy座標
mx = 0#マウスのx座標
my = 0#マウスのy座標
proc = 0

hand_open = True#手の開閉
can_click = True

time = 30
items = []
ITEM_R = 8
score = 0

def draw_hand():
    if mx < hx:
        if hand_open:
            cvs.create_image(hx, hy, image=open_handL, anchor="center", tag="hand")
        else:
            cvs.create_image(hx, hy, image=close_handL, anchor="center", tag="hand")
    else:
        if hand_open:
            cvs.create_image(hx, hy, image=open_handR, anchor="center", tag="hand")
        else:
            cvs.create_image(hx, hy, image=close_handR, anchor="center", tag="hand")

def switch_hand():
    global hand_open
    hand_open = not hand_open
    root.after(500, switch_hand)

def check_hit():
    global proc, can_click
    dx = hx - mx
    dy = hy - my
    if dx*dx + dy*dy < 60*60:
        proc = 2
        can_click = False
        root.after(3000, click_saikai)

def add_item():
    if proc != 1:
        return

    x = random.randint(ITEM_R, 640 - ITEM_R)
    y = random.randint(80, 480 - ITEM_R)
    item = cvs.create_oval(
        x - ITEM_R, y - ITEM_R, 
        x + ITEM_R, y + ITEM_R, 
        fill="white", outline="gray", width="3", tag="item"
    )
    items.append(item)

    root.after(1500, add_item)

def click_item(e):
    global score

    if proc != 1:
        return

    for item in items[:]:
        x1, y1, x2, y2 = cvs.coords(item)
        cx = (x1 + x2) / 2
        cy = (y1 + y2) / 2

        if (cx - e.x)**2 + (cy - e.y)**2 < ITEM_R**2:
            cvs.delete(item)
            items.remove(item)
            score += 1
            break

def move(e):
    global mx, my
    mx = e.x
    my = e.y

def click(e):
    global proc

    if not can_click:
        return

    # ゲームオーバー or クリアからタイトル
    if proc == 2 or proc == 3:
        proc = 0

def game_start():
    global hx, hy, proc, hand_open, time, score, can_click

    hx = -100
    hy = -100
    hand_open = True

    score = 0
    time = 30
    root.after(1000, countdown)

    can_click = True

    items.clear()
    root.after(1500, add_item)

    proc = 1
    btn.place_forget()  

def countdown():
    global time, proc, can_click

    if proc != 1:
        return

    time -= 1

    if time <= 0:
        proc = 3
        can_click = False
        root.after(3000, click_saikai)
        return

    root.after(1000, countdown)

def click_saikai():
    global can_click
    can_click = True

def main():
    global hx, hy, proc

    cvs.delete("hand")
    cvs.delete("ui")

    #タイトル画面
    if proc == 0:
        cvs.create_text(320, 180, text="Escape the hand", fill="white", font=("Times New Roman", 40), tag="ui")
        cvs.create_text(320, 260, text="追いかけてくる手から逃げながら\n次々と現れる●をクリックして集めてください。", fill="white", font=("Arial", 15), justify="center", tag="ui")

        btn.place(x=320, y=360, anchor="center")
    #プレイ中
    elif proc == 1:
        cvs.create_text(540, 30, text=f"残り時間: {time}", fill="white", font=("Times New Roman", 19), anchor="center", tag="ui")
        cvs.create_text(100, 30, text=f"集めた数: {score}", fill="white", font=("Times New Roman", 19), anchor="center", tag="ui")
        
        if hx < mx: hx += 4
        if mx < hx: hx -= 4
        if hy < my: hy += 4
        if my < hy: hy -= 4

        draw_hand()
        check_hit()

    #ゲームオーバー
    elif proc == 2:
        cvs.delete("item")
        cvs.create_text(320, 180, text="Caught!", fill="red", font=("Times New Roman", 40), tag="ui")
        cvs.create_text(320, 260, text="あなたは捕まってしまいました…", fill="white", font=("Times New Roman", 20), tag="ui")
        cvs.create_text(320, 360, text="click to title", fill="white", font=("Times New Roman", 16), tag="ui")

    #クリア
    elif proc == 3:
        cvs.delete("item")
        cvs.create_text(320, 180, text="Great!", fill="gold", font=("Times New Roman", 40), tag="ui")
        cvs.create_text(320, 260, text=f"あなたは●を{score}個集めました。\nもう一度集めてくれますよね？", fill="white", font=("Times New Roman", 15), justify="center", tag="ui")
        cvs.create_text(320, 360, text="click to title", fill="white", font=("Times New Roman", 16), tag="ui")

    root.after(50, main)

root = tkinter.Tk()
root.title("Escape the hand")
root.resizable(False, False)
root.bind("<Motion>",move)
root.bind("<Button-1>", click)
root.bind("<Button-1>", click_item, add="+")
cvs = tkinter.Canvas(width=640, height=480, bg="black")
open_handR = tkinter.PhotoImage(file="image/open_handR.png")
open_handL = tkinter.PhotoImage(file="image/open_handL.png")
close_handR = tkinter.PhotoImage(file="image/close_handR.png")
close_handL = tkinter.PhotoImage(file="image/close_handL.png")
cvs.pack()
btn = tkinter.Button(root, text="START", font= ("Times New Roman", 18), width=8, command=game_start, relief="raised", bd=3)

switch_hand()
main()
root.mainloop()
