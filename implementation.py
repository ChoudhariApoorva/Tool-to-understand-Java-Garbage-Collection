from Tkinter import *
from collections import defaultdict
import tkMessageBox
import random
import copy
import tkFont

root = Tk() 			#constructor call
var1 = StringVar()
var2 = StringVar()
text = Entry(root)  		#global so that it can be accessed in the function draw_rect
blocks_text = Entry(root)
x = 0
y = 0
val = 0
new_y = 0
rect_obj_list = []		#create a list to hold the rectangle blocks which are allocated
gc_list = []			#create a list to hold the rectangle blocks which have to be collected during GC
list_of_sizes = []		#create a list to hold the sizes of the blocks allocated. This is required during compaction
temp_list = []
survivor_list = []			#create a list to hold survivor space objects
#s1_list = []				#create a list to hold 'to' survivor space objects
survivor_space_num = 0
block_count = 1			#for printing the blocks
temp_y = 0			#for clearing the blocks

age_dict = defaultdict(list)	# create a defualt dictionary to hold the ages

customFont = tkFont.Font(family="Helvetica", size=16)

#create eden space
mycan = 0
mycan = Canvas(root,bg="white",height=600,width=200)
mycan.place(x = 400, y = 100)
line=mycan.create_line(1,1,1,600,200,600,200,1,1,1)

#create 'from' survivor space
s0 = 0
s0 = Canvas(root, bg = "white", height = 300, width = 200)
s0.place(x = 650, y = 100)
line_s0 = s0.create_line(1,1,1,300,200,300,200,1,1,1)

#create 'to' survivor space
s1 = 0
s1 = Canvas(root, bg = "white", height = 300, width = 200)
s1.place(x=650, y=410)
line_s1 = s1.create_line(1,1,1,300,200,300,200,1,1,1)

#create old generation
old_can = 0
old_can = Canvas(root,bg="white",height=600,width=200)
old_can.place(x = 1000, y = 100)
line=old_can.create_line(1,1,1,600,200,600,200,1,1,1)


def allocate():			#called when the chosen option is allocate
	global mycan
	global block_count
	global temp_y
	global age_dict
	temp_y = 0
	
	if (tkMessageBox.askyesno("Allocation","Do you want manual allocation?") == True):
		label = Label(root,textvariable=var1,relief=RAISED)
		var1.set("Enter number of bytes")
		label.place(x = 50,y = 300)          #place the elements at specific positions using elem.place(x coordinate,y coordinate)

		text.place(x = 200,y = 300,width=50)
		
		submitbtn = Button(root,text="OK",command=draw_rect)
		submitbtn.place(x = 120,y = 350)
		
	else:
		rand_num = 0
		global y
		global list_of_sizes
		
		y_val = 0

		while(y_val < 600):
			rand_num = random.randrange(1,200,1)		#params for randrange(start,end,step)

			if(y_val >= 600 or rand_num > (600-y_val)):
				tkMessageBox.showinfo("Error","Not enough space")
				break
				#swap(foo)
			
			else:
				y_val += rand_num
				msg = "Allocated %d bytes" % rand_num
				tkMessageBox.showinfo("Value",msg)
				rect=mycan.create_rectangle(0,y,200,y_val,fill="SkyBlue")
				list_of_sizes.append(y_val-y)
				age_dict[y_val-y].append(0)	#copy the size and initialize the age to zero in age_dict
				#print age_dict
				rect_obj_list.append(rect)
				print "age_dict[y_val-y]"
				print age_dict[y_val-y]
				disp_block_num(y_val,y_val-y,age_dict[y_val-y])
				
				y = y_val

def disp_block_num(y_val,size,age):
	global block_count	
	global y
	global temp_y
	global mycan

	block_var = StringVar()
	block_label = Label(root,textvariable=block_var,bg="misty rose",relief=FLAT)
	block_var.set(block_count)
	temp_y += (y_val-y)/2 + 100
	block_label.place(x=380,y=temp_y)
	#print temp_y
	print_age = mycan.create_text(50,temp_y-100,text=age)
	print_block_size = mycan.create_text(150,temp_y-100,text=size)  #to display block size, Y value is w.r.t canvas.. so subtract 100
	temp_y = y_val
	block_count += 1
	
def draw_rect():		#called after the user specifies the number of bytes to be allocated
	global y
	global mycan
	global block_count
	global age_dict
	num_of_bytes = int(text.get())
	val = num_of_bytes+y
	
	if(val > 600 or num_of_bytes > (600-y)):
		tkMessageBox.showinfo("Error","Not enough space")
		#swap(foo)	
	
	else:
		rect=mycan.create_rectangle(0,y,200,val,fill="SkyBlue")
		rect_obj_list.append(rect)
		list_of_sizes.append(val-y)
		age_dict[val-y].append(0)			#copy the size and initialize the age to zero in age_dict
		print age_dict
		disp_block_num(val,val-y,age_dict[val-y][-1])	#pass the latest value of the list
		y = val
	
def deallocate():			#called when the chosen option is deallocate
	global mycan
	global list_of_sizes
	global age_dict
	if (tkMessageBox.askyesno("Deallocation","Do you want manual deallocation?") == True):
		get_block_number()
	else:
		num_of_blocks = len(rect_obj_list)
		rand_num = random.randrange(1,num_of_blocks,1)

		while rand_num:
			rand_block = random.randrange(1,num_of_blocks,1)
			temp_key = list_of_sizes[rand_block-1]
			#print list_of_sizes
			list_of_sizes[rand_block-1] = -1
			msg = "Deallocated %d th block" % rand_block
			tkMessageBox.showinfo("Deallocated block",msg)
			rect_obj = rect_obj_list[rand_block-1]
			#print temp_key
			
			if(temp_key != -1):			# if the same random block is deallocated again
				age_dict[temp_key][0] = -1
			print "age dict"
			print age_dict
			#del age_dict[list_of_sizes[rand_block-1]][0]
			gc_list.append(rect_obj)				#add the object to gc list
			mycan.itemconfigure(rect_obj,fill="dark salmon")
			rand_num -= 1
			
def get_block_number():			#called after the user specifies the block to be deallocated		
	label = Label(root,textvariable=var2,relief=RAISED)
	var2.set("Enter block number")
	label.place(x = 50,y = 400)

	blocks_text.place(x = 200,y = 400,width=50)
		
	submitbtn = Button(root,text="OK",command=deallocate_block)
	submitbtn.place(x = 120,y = 450)
	
def deallocate_block():
	global mycan
	global age_dict
	global list_of_sizes

	block_num = int(blocks_text.get())-1			#list index starts from 0
	
	if(block_num >= len(rect_obj_list)):	
		tkMessageBox.showinfo("Error","Cannot deallocate the block")
	
	else:
		temp = list_of_sizes[block_num]
		print "temp"
		print temp
		print age_dict[temp][block_num]
		if(temp != -1):
			age_dict[temp][block_num] = -1
			
		list_of_sizes[block_num] = -1
		rect_obj = rect_obj_list[block_num]
		gc_list.append(rect_obj)			#add the object to gc list
		mycan.itemconfigure(rect_obj,fill="dark salmon")

def startGC():
	global mycan
	for i in range(len(gc_list)):
		obj = gc_list[i]
		mycan.itemconfigure(obj,fill="white")
	tkMessageBox.showinfo("GC message","Garbage collection complete")
	#tkMessageBox.showinfo("GC message","Compacting the area")
	#compact()
	swap()
	clear_block_numbers()

def clear_block_numbers():
	global block_count
	global temp_y
	clear_block_num_can = 0
	clear_block_num_can = Canvas(root,bg="misty rose",bd=-1,height=600,width=10)
	clear_block_num_can.place(x = 380, y = 100)
	block_count = 1	
	temp_y = 0
	
def reset_values():
	global list_of_sizes
	global temp_list
	global y_val
	global y
	global rect_obj_list
  	del rect_obj_list[:]
	y_val = 0
	y = 0
	del list_of_sizes[:]
	
def swap():
	global mycan
	global temp_list
	global new_y
	global s0
	global s1
	global survivor_space_num 
	global age_dict
	#print survivor_space_num
	
	#have the updated list of sizes
	for i in range(len(list_of_sizes)):
		if(list_of_sizes[i] != -1):
			temp_list.append(list_of_sizes[i])
	
	#clear the eden space
	mycan = Canvas(root,bg="white",height=600,width=200)
	mycan.place(x = 400, y = 100)
	line=mycan.create_line(1,1,1,600,200,600,200,1,1,1)
			
	#fill the survivor space
	if(survivor_space_num == 0):
		#clear s1
		s1 = 0
		s1 = Canvas(root, bg = "white", height = 300, width = 200)
		s1.place(x=650, y=410)
		line_s1 = s1.create_line(1,1,1,300,200,300,200,1,1,1)
		
		length = len(set(temp_list))			# to take the unique values of temp_list
		
		for i in range(length):
			if(len(age_dict[temp_list[i]]) > 1):		#if same block has more than one age
				for j in range(len(age_dict[temp_list[i]])):
					if (age_dict[temp_list[i]][j] != -1): 
						age_dict[temp_list[i]][j] += 1
						
			else:
				age_dict[temp_list[i]][0] += 1

		#fill s0
		for i in range(len(temp_list)):
			blk = s0.create_rectangle(0,new_y,200,new_y+20,fill="SkyBlue")
			temp = new_y
			new_y = new_y + 20
			survivor_list.append(blk)
			
			val = (new_y - temp) / 2
			val = val + temp
			text_size = s0.create_text(100,val,text=temp_list[i])  		#to display block size
		survivor_space_num = 1
		new_y = 0
	
	else:
		#clear s0
		s0 = 0
		s0 = Canvas(root, bg = "white", height = 300, width = 200)
		s0.place(x = 650, y = 100)
		line_s0 = s0.create_line(1,1,1,300,200,300,200,1,1,1)
		
		length = len(set(temp_list))			# to take the unique values of temp_list
		
		for i in range(length):
			if(len(age_dict[temp_list[i]]) > 1):		#if same block has more than one age
				for j in range(len(age_dict[temp_list[i]])):
					if (age_dict[temp_list[i]][j] != -1):
						age_dict[temp_list[i]][j] += 1
			
			else:
				age_dict[temp_list[i]][0] += 1

		#fill s1
		for i in range(len(temp_list)):
			blk = s1.create_rectangle(0,new_y,200,new_y+20,fill="SkyBlue")
			temp = new_y
			new_y = new_y + 20
			survivor_list.append(blk)
			
			val = (new_y - temp) / 2
			val = val + temp
			text_size = s1.create_text(100,val,text=temp_list[i])
		survivor_space_num = 0
		new_y = 0
	
	print "age_dict survivor space"
	print age_dict
	reset_values()
