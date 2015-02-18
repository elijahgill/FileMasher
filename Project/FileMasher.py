from tkinter import *
from tkinter.ttk import Frame, Button, Style
import tkinter.messagebox
import tkinter.filedialog
import shutil
import os


class FileMasher(Frame):
	def __init__(self, parent):
		Frame.__init__(self, parent)
		self.parent = parent
		self.initUI()
	
	def initUI(self):
		self.parent.title("FileMasher")
		self.style = Style()
		self.style.theme_use("default")
		
		self.pack(fill=BOTH, expand=1)
		
		# Configure certain columns
		self.columnconfigure(1,weight=1)
		self.columnconfigure(3, pad=10)
		self.rowconfigure(5, weight=1)
		self.rowconfigure(6, weight=1)
		self.rowconfigure(8,pad=7)
		
		scrollbar = Scrollbar(self, orient=HORIZONTAL)
		scrollbar.grid(row=7, column=0, columnspan=2, sticky=E+W)
		
		self.lstFileList = Listbox(self, xscrollcommand=scrollbar.set, selectmode=EXTENDED)
		self.lstFileList.grid(row=1,column=0,columnspan=2, rowspan=6, sticky=E+W+S+N)
		scrollbar.config(command=self.lstFileList.xview)
		
		# Button to select files in the listbox
		btnSelectFiles = Button(self, text="Add Files",command=self.selectFiles)
		btnSelectFiles.grid(row=1, column=3, sticky=E+W)
		
		# Button to remove item from the listbox
		btnRemoveItem = Button(self, text="Remove",
			command=self.deleteSelectedListItems )
		btnRemoveItem.grid(row=2, column=3, sticky=E+W)
		
		# Button to move item up in the listbox
		btnMoveUp = Button(self, text="Move Up",
			command=self.moveListItemUp )
		btnMoveUp.grid(row=3, column=3, sticky=E+W)
		
		# Button to move item down in the listbox
		btnMoveUp = Button(self, text="Move Down",
			command=self.moveListItemDown )
		btnMoveUp.grid(row=4, column=3, sticky=E+W)
		
		# Button to create a file and combine selected files into it
		btnGo = Button(self, text="Mash Files!",command=self.joinFiles)
		btnGo.grid(row=6, column=3, sticky=E+W+N+S, rowspan=2)
		
		#btnQuit = Button(self, text="Quit",command=self.quit)
		#btnQuit.grid(row=8, column=0)
		
		self.centerWindow()
		
	def centerWindow(self):
		w = 350
		h = 350
		
		sw = self.parent.winfo_screenwidth()
		sh = self.parent.winfo_screenheight()
		
		x = (sw-w)/2 
		y = (sh-h)/2
		
		self.parent.geometry('%dx%d+%d+%d' % (w,h,x,y))
		
	def selectFiles(self):
		# Get files to combine
		filez = tkinter.filedialog.askopenfilenames(title="Choose files to combine")
		for f in filez:
			self.lstFileList.insert(END, f)
		self.fileList = filez
		
	def joinFiles(self):
		# set destination
		destination = tkinter.filedialog.asksaveasfile(mode='w+b', defaultextension=".mp3")
		if destination is None: #exit if cancelled
			return
		
		for filename in self.lstFileList.get(0,END):
			# Files are opened in binary mode for byte level processing
			sFile = open(filename, 'r+b')
			# write to the console to track progress
			print("Adding file " + filename)
			# Copy the current file to the end of the destination file
			shutil.copyfileobj(sFile, destination)
			sFile.close()
		destination.close()
		print("\n\nFinished")
		self.alertBox(msgText="Finished mashing files!", msgTitle="Mashing Completed")
		
	def quit(self):
		self.parent.destroy()
		
	# Simple alert message. Destroyed when done.
	def alertBox(self, msgText, msgTitle="Alert!"):
		window = Tk()
		window.wm_withdraw()
		tkinter.messagebox.showinfo(title=msgTitle, message=msgText)
		window.destroy()
		
	"""
	Listbox functions
	"""
	
	def deleteSelectedListItems(self):
		l = self.lstFileList
		# reverse to avoid deleting a wrong index after the list reindexes
		for li in reversed( l.curselection() ): 
			l.delete( li )
		
	def moveListItemUp(self):
		l = self.lstFileList
		posList = l.curselection()
		if not posList:
			return
		
		for pos in posList:
			if pos == 0:
				continue
			text = l.get(pos)
			l.delete(pos)
			l.insert(pos-1, text)
			l.selection_set(pos-1)
	
	def moveListItemDown(self):
		l = self.lstFileList
		posList = l.curselection()
		if not posList:
			return
		
		for pos in reversed(posList):
			if pos == l.index(END):
				continue
			text = l.get(pos)
			l.delete(pos)
			l.insert(pos+1, text)
			l.selection_set(pos+1)
		
def main():
	root = Tk()
	root.geometry("250x150+300+300")
	app = FileMasher(root)
	root.mainloop()

# Main program
if __name__ == '__main__':
	main()