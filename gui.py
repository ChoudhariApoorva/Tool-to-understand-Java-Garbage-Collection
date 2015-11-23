from implementation import *
import tkFont

root.configure(background="misty rose")
root.title("Generational Garbage Collection tool")

one = StringVar()
two = StringVar()
three = StringVar()
four = StringVar()
five = StringVar()

customFont = tkFont.Font(family="Helvetica", size=16)

eden = Label(root,textvariable=one,bg="misty rose",font=customFont,relief=FLAT)
one.set("Eden space")
eden.place(x=450,y=50)

surv = Label(root,textvariable=five,bg="misty rose",font=customFont,relief=FLAT)
five.set("Survivor space")
surv.place(x=675,y=50)

S0 = Label(root,textvariable=two,bg="misty rose",font=customFont,relief=FLAT)
two.set("S0")
S0.place(x=875,y=250)

S1 = Label(root,textvariable=three,bg="misty rose",font=customFont,relief=FLAT)
three.set("S1")
S1.place(x=875,y=530)

old = Label(root,textvariable=four,bg="misty rose",font=customFont,relief=FLAT)
four.set("Old Generation")
old.place(x=1020,y=50)

btn1 = Button(root,text="Allocate",command=allocate)
btn2 = Button(root,text="Deallocate",command=deallocate)
btn3 = Button(root,text="Start GC",command=startGC)
btn1.place(x = 50,y = 100)
btn2.place(x = 50,y = 140)
btn3.place(x = 50,y = 180)

root.mainloop()
