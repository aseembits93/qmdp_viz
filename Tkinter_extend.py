
'''TODO put start button to start simulation
check boxes for different maps goal map is static so dont redraw '''

from Tkinter import *
import numpy as np
from PIL import Image, ImageTk
#draw square grid of size N 0 red 1 blue from binary numpy array
class qmdp_viz():
	"""docstring for qmdp_viz"""
	def __init__(self,root):
		self.root = root
		#define canvas object
		self.canvas = Canvas(self.root, width=800, height=800)
		self.canvas.pack()
		#window title
		self.root.title('QMDPNet')
		#variables for tracking map,belief statuses
		self.rect_status = np.asarray([[None for _ in range(10)] for _ in range(10)])
		self.map_status = np.asarray([[None for _ in range(10)] for _ in range(10)])
		self.photo = np.asarray([[None for _ in range(10)] for _ in range(10)])
		#color map for drawing grids 
		self.col_map = {0.0:'gray', 1.0:'silver'}
		self.col_map_for_map = {0.0:'green', 1.0:'orange'}
		#grid parameters 
		self.random_belief=np.random.rand(10,10)
		self.square_size = 50 #in pixels the length of each grid element
		self.arr1 = np.eye(10,10)
		#Radio Button Variable
		self.rad_var = IntVar()
		#True Belief Button
		self.b_t = Radiobutton(
		self.root, text="Belief(True)", variable=self.rad_var,value=0, command=self.cb)
		self.b_t.pack(side=RIGHT)
		#Reward Button
		self.reward_button = Radiobutton(
		self.root, text="Reward", variable=self.rad_var, value=1, command=self.cb)
		self.reward_button.pack(side=RIGHT)
		#Belief Predicted Button
		self.b_p = Radiobutton(
		self.root, text="Belief(Predicted)", variable=self.rad_var, value=2, command=self.cb)
		self.b_p.pack(side=RIGHT)
		#Start Button
		self.start_b = Button(self.root, text="Start", command=self.cb)
		self.start_b.pack(side=LEFT)
		#Step Button
		self.step_b = Button(self.root, text="Step", command=self.cb)
		self.step_b.pack(side=LEFT)
		#Pause/Continue Button
		self.p_b = Button(self.root, text="Pause/Continue", command=self.cb)
		self.p_b.pack(side=LEFT)
		#Reset Button
		self.reset_b = Button(self.root, text="Reset", command=self.cb)
		self.reset_b.pack(side=LEFT)
		#Network Options
		self.options = ["QMDPNet","QMDPNet-LSTM","QMDP-Untied","CNN-LSTM"]
		#Variable for choosing options from menu
		self.opt_var = StringVar(self.root)
		self.opt_var.set(self.options[0]) # default value
		#draw Option menu
		opt_menu = OptionMenu(self.root, self.opt_var, *self.options, command=self.cb2)
		opt_menu.pack()
		#draw map
		self.draw_map()
		#visualize belief
		#self.visualize_belief([0,255,0])
		
		
		
	def cb2(self,value):
		print value	
	def cb(self):
		print "yes"	
	def cb1(self):
		print "nothing"		
	def draw_grid(self):
		for i in range(self.random_belief.shape[0]):
			for j in range(self.random_belief.shape[1]):
				self.rect_status[i][j] = self.draw_rect_at(i,j,self.random_belief[i][j])
	def draw_rect_at(self,i,j,col):
		x1 = i*self.square_size
		y1 = j*self.square_size
		x2 = x1 + self.square_size
		y2 = y1 + self.square_size
		id1 = self.canvas.create_rectangle(x1,y1,x2,y2,fill=self.col_map[col], tags=(str(int(i))+','+str(int(j))))
		return id1
	def redraw_grid(self):
		for i in range(self.arr1.shape[0]):
			for j in range(self.arr1.shape[1]):
				col = self.col_map[self.arr1[i][j]]
				self.canvas.itemconfig(self.rect_status[i][j],fill=col)
	def draw_map(self):
		for i in range(self.arr1.shape[0]):
			for j in range(self.arr1.shape[1]):
				self.map_status[i][j] = self.draw_rect_at(i,j,self.arr1[i][j])
	def draw_circle_at(self,i,j,col):
		x1 = i*self.square_size
		y1 = j*self.square_size
		x2 = x1 + self.square_size
		y2 = y1 + self.square_size
		x1+= (self.square_size/4) #reduce size of square to fit inside 
		y1+= (self.square_size/4)
		x2-= (self.square_size/4)
		y2-= (self.square_size/4)
		id1 = self.canvas.create_oval(x1,y1,x2,y2,fill=self.col_map_for_map[col], tags=(str(int(i))+','+str(int(j))))
		return id1				
	def visualize_belief(self,color):
		
		#pim = Image.new('RGBA', (50,50), (0,255,0,100))
		#photo = ImageTk.PhotoImage(pim)
		#self.canvas.create_image(200,200, image=photo, anchor='nw')
		max_num = np.max(self.random_belief)
		min_num = np.min(self.random_belief)
		scalex1 = 0
		scalex2 = 100
		for i in range(self.random_belief.shape[0]):
			for j in range(self.random_belief.shape[1]):
				s_factor = ((scalex2-scalex1)*(self.random_belief[i][j]-min_num))/(max_num-min_num) + (scalex1)
				newcol = tuple(color+list([int(s_factor)]))
				pim = Image.new('RGBA', (50,50), newcol)
				self.photo[i][j] = ImageTk.PhotoImage(pim)
				self.canvas.create_image(i*self.square_size,j*self.square_size, image=self.photo[i][j], anchor='nw')		
	# #def callback(self):
	# 	if self.first_time:
	# 		self.first_time = False
	# 		self.draw_grid()
	# 	else:	
	# 		if np.array_equal(self.arr1,np.eye(5,5)):
	# 			self.arr1 = np.ones((5,5)) - self.arr1
	# 		else:
	# 			self.arr1 = np.eye(5,5)
	# 		self.redraw_grid()	
	# 	self.root.after(300,self.callback)
#root Tk window
root = Tk()		
#instantiate class
qmdp_win = qmdp_viz(root)
#start mainloop
qmdp_win.root.mainloop()


