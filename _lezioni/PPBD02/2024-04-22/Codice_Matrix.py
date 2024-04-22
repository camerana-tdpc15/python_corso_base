from tkinter import Frame, Tk, Canvas
from random import choice
from font_tools import get_font_chars

class Matrix(Frame):
	def __init__(self, master, font_name, font_size):
		super().__init__(master)

		self.canvas = Canvas(master, bg='black')
		self.canvas.place(relx=0, rely=0, relwidth=1, relheight=1)
		self.velocidad = [i for i in range(0,30,5)]
		self.pos = [i for i in range(-200,200,20)]
		self.letters = []
		self.green = 0
		self.font_name = font_name
		self.font_size = font_size
		self.characters = get_font_chars(font_name)
		self.draw()
		self.update()

	def draw(self):
		for x in range(0,1600,20):
			y = choice(self.pos)
			for j in range(0, choice([180,220,280]),20):
				self.obj = self.canvas.create_text(
					20+x, -200+y+j,  # posizione x, y
					text=choice(self.characters),
					fill='green2',
					font=(self.font_name, self.font_size))
				self.letters.append(self.obj)
	
	def update(self):
		for letter in self.letters:
			v = choice(self.velocidad)
			self.green +=5
			color = '#{:02x}{:02x}{:02x}'.format(0,self.green,0)
			self.canvas.itemconfig(letter, fill=color)
			self.canvas.move(letter, 0, v)

			y = self.canvas.coords(self.obj)

			if self.green >=250:
				self.green = 0

		if y[1] >=800:
			self.draw()
			if y[1]>= 1200:
				self.letters.clear()
				self.canvas.delete('all')
		
		self.canvas.after(80, self.update)


if __name__ == '__main__':
	root = Tk()
	root.title('Matrix Animation')
	root.config(bg= 'black')
	#root.attributes('-fullscreen', True)
	app = Matrix(root, 'Arial Unicode', 14)
	app.mainloop()