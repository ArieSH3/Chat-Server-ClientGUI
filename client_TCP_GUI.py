import socket
import threading
import tkinter as tk




class Client_Start:
	def __init__(self):
		self.PORT = 2210
		self.SERVER_IP = '127.0.0.1'

		# Adding socket(IPv4, TCP) to client_socket var
		self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		self.separator = '<SEP>'
		self.username = None

		try:
			print('[CLIENT] connecting to server: {}:{}'.format(self.SERVER_IP, self.PORT))
			self.client_socket.connect((self.SERVER_IP, self.PORT))
			print('[CLIENT] you have connected!')
		except ConnectionRefusedError:
			print('[CLIENT] failed to connect to the server!')




class Client_App(Client_Start):
	def __init__(self, root):
		# ================= CLIENT START ===========================================================
		# Starts Client class which tries to connect to the server
		self.CS = Client_Start()


		# ================= RESOURCES ==============================================================
		
		self.background = '#333333'
		self.font = 'Helvetica 10 bold'
		self.font_colour = '#FFFFFF'

		#self.username = None
		self.input_text = None

		
		# ================= ROOT ===================================================================
		
		self.root = root
		self.root.geometry('700x500+300+250')
		self.root.title('Text test')
		self.root.config(bg=self.background)
		self.root.resizable(False, False)

		
		

		# ***===========*** MAIN WINDOW ***===========***===============================================
		
		# ==== FRAMEs ====
		self.frame_main = tk.Frame(self.root)
		self.frame_main.config(bg=self.background)
		#frame_main.place(relx=0.5, rely=0.66, anchor='center')
		self.frame_main.pack(pady=20)

		# ==== TEXT ====
		#	Display field
		self.display_field = tk.Text(self.frame_main)
		self.display_field.config(height=23, borderwidth=0, font=self.font)
		self.display_field.pack()

		#	Input field
		self.chat_input_field = tk.Text(self.frame_main)
		self.chat_input_field.config(height=5, borderwidth=0, width=71, font=self.font)
		# Sets focus on widget so we dont have to click on it when starting a program
		#	yet the cursor will already be blinking on it and we can start typing
		self.chat_input_field.focus_set()
		self.chat_input_field.pack(pady=(20,0), side='left')

		# ==== BUTTON ====
		#	Send button
		self.button_send_message = tk.Button(self.frame_main, command=self.add_text)
		self.button_send_message.config(text='Send', width=10, justify='center', borderwidth=1, font=self.font)
		self.button_send_message.pack(pady=(20,0), side='left', fill='both', expand=True)

		# ==== BIND KEY ====
		# Function needs to have an event argument since bind sends an event
		self.root.bind('<Return>', self.add_text)


		

		# ***===========*** USERNAME PROMPT WINDOW ***===========***=====================================

		# ==== TOP LEVEL ====
		self.user_window = tk.Toplevel()
		self.user_window.resizable(False, False)
		self.user_window.geometry('300x70')
		self.user_window.config(bg=self.background)
		# Sets the focus on the new window and until it is closed the other windows widgets
		#	in the App cannot be interacted with
		self.user_window.grab_set()

		# ==== FRAMEs ====
		self.frame_username = tk.Frame(self.user_window)
		self.frame_username.config(bg=self.background)
		self.frame_username.place(relx=0.5, rely=0.5, anchor='center')

		# ==== LABEL ====
		self.username_label = tk.Label(self.frame_username, text='Username:')
		self.username_label.config(font=self.font, bg=self.background, fg=self.font_colour)
		self.username_label.pack(side='left')

		# ==== TEXT ====
		self.username_input_field = tk.Text(self.frame_username)
		self.username_input_field.config(height=1, borderwidth=4, width=20, font=self.font, wrap='none')
		self.username_input_field.pack(side='left')

		# ==== BUTTON ====
		self.username_button = tk.Button(self.frame_username, command=self.add_username)
		self.username_button.config(borderwidth=1, font=self.font, text='Confirm')
		self.username_button.pack(fill='both', expand=True)

		# Have to find a way to bind while toplevel open, otherwise
		#	it messes up the other bind on (enter) for chatting
		# root.bind('<Return>', add_username)



	# ============== METHODS ============================================================

	def add_username(self):
		# Var username in class Client_Start given a value from the window prompt
		self.CS.username = self.username_input_field.get('1.0', 'end').strip()

		# Clears the text input area
		self.username_input_field.delete('1.0','end')

		# Closes window with username prompt
		self.user_window.destroy()

	#
	def add_text(self, event=None):
		# Gets text from input field and strips it to clean it up
		self.input_text = self.chat_input_field.get('1.0','end').strip()
		if len(self.input_text)>0:
			try:
				# Checks if username added
				if len(self.CS.username)>0:
					self.input_text = '{}: {}'.format(self.CS.username, self.input_text)
			# If no username is entered it reminds the user and allows no further access
			#	to chat functions
			except NameError:
				# Switched 'end' with tk.INSERT and it seems to do the same thing
				self.display_field.insert(tk.INSERT, 'Error: no username detected!' + '\n')
				self.chat_input_field.detelete('1.0','end')
				return

			# Enables edit of display field
			self.display_field['state'] = 'normal'
			# Insert text from input field to display field and remove
			#	any trailing spaces and add new line at the end
			# Switched 'end' with tk.INSERT and it seems to do the same thing
			#	Its an index and just adds text below the existing one
			self.display_field.insert(tk.INSERT, self.input_text + '\n')
			
			# Disables the editing of display_field
			self.display_field['state'] = 'disabled'

			# Will always go to the last line so the newest input will always be shown
			#	and there is no need to manually scroll
			self.display_field.see(tk.END)

			# **SEND MESSAGE TO THE SERVER**
			self.CS.client_socket.send(self.input_text.encode('utf-8'))
			# Checks if message sent is /exit and if so it closes the socket
			if self.input_text.split(':')[1] == '/exit':
				self.client_socket.close()

		# Clears the text input area
		self.chat_input_field.delete('1.0','end')


	def listen_for_server(self):
		while True:
			try:
				print('Gonna receive msg')
				server_message = self.CS.client_socket.recv(1024)
				print('Msg received')
				server_message = server_message.decode('utf-8')
				# Add message to the text display field
				print(server_message)
				# PROGRAM REFUSES TO INSERT TEXT WHEN TWO USERS TALKING EVEN
				# 	THOUGH IT RECEIVES MESSAGE AND PRINTS IT OUT JUST BEFORE THIS LINE OF CODE
				self.display_field['state'] ='normal'
				self.display_field.insert(tk.INSERT, server_message+'\n')
				self.display_field['state'] = 'disabled'


			except ConnectionAbortedError:
				print('[CLIENT] disconnected...')
				break

	# Threads listen_for_server method
	def thread_lfs(self):
		print('threading...')
		thread = threading.Thread(target=self.listen_for_server)
		thread.daemon = True
		thread.start()





if __name__ == '__main__':
	root = tk.Tk()
	window = Client_App(root)
	window.thread_lfs()


	root.mainloop()