from tkinter import *
import customtkinter
from PIL import Image,ImageOps, ImageDraw


class App(customtkinter.CTk):
  def __init__(self,title,size):
    super().__init__()
    
    self.init_setup(title,size)
    self.create_layout()
    
    
    self.run()

  def init_setup(self,title,size):
    self._set_appearance_mode("light")
    self.title(title)
    self.geometry(f"{size[0]}x{size[1]}")
    self.minsize(size[0],size[1])
  
  def create_layout(self):
    self.columnconfigure(0,weight=2,uniform="a")
    self.columnconfigure(1,weight=3,uniform="a")
    self.rowconfigure(0,weight=1,uniform="a")

    self.chatlist = ChatList(master=self)
    self.chat     = Chat(master=self)
  
  def run(self):
    self.mainloop()


class ChatList(customtkinter.CTkFrame):
  def __init__(self,master):
    super().__init__(master=master,fg_color="#ffffff",corner_radius = 0)

    self.grid(row=0,column=0,sticky="nsew")
    
class Chat(customtkinter.CTkFrame):
  def __init__(self,master):
    super().__init__(master=master,fg_color="#f4f5f9",corner_radius = 0)
    self.grid(row=0,column=1,sticky="nsew")

    self.create_frames()
    self.configure_frames()
    self.create_widgets()
    self.place_frames()
    self.place_widgets()

    self._iota = 0

  def create_frames(self):
    self.header    = customtkinter.CTkFrame(master=self,corner_radius=0,fg_color="#f4f5f9")
    self.main      = customtkinter.CTkFrame(master=self,corner_radius=0,fg_color="#f4f5f9") 
    self.bottom    = customtkinter.CTkFrame(master=self,corner_radius=0,fg_color="#f4f5f9") 
    self.separator1 = Divider(master=self)
    self.separator2 = Divider(master=self)

  def configure_frames(self):
    self.main .columnconfigure((0,1,2),weight=1)

  def load_imgs(self):
    self.us_persona_img = customtkinter.CTkImage(
                                  light_image=Image.open("imgs/us_persona_img.png"),
                                  dark_image=Image.open("imgs/us_persona_img.png"),
                                  size=(45, 45)
                                  )
    self.mic_img = customtkinter.CTkImage(
                                  light_image=Image.open("imgs/icons/mic_img.png"),
                                  dark_image=Image.open("imgs/icons/mic_img.png"),
                                  size=(20, 20)
                                  )

  
  def create_widgets(self):
    self.load_imgs()

    self.header_label = customtkinter.CTkLabel(master=self.header,
                                       text="    Simon",
                                       font=("Arial",16),
                                       text_color="#212121",
                                       image=self.us_persona_img,
                                       compound="left" 
                                       ) 
    self.audio_button = customtkinter.CTkLabel(master=self.bottom,image=self.mic_img,text="")
    self.audio_button.bind("<Button-1>",command=self.audio_callback)
    self.chat_input    = customtkinter.CTkEntry(master=self.bottom,
                                      border_width=0,
                                      placeholder_text="Type a message here"
                                      )
    self.submit_button = customtkinter.CTkButton(master=self.bottom,
                                        text="Send",
                                        text_color="#212121",
                                        fg_color="#FFD159",
                                        hover_color="#ffec99",
                                        corner_radius=100,
                                        width=80,
                                        height=35,
                                        command=self.chat_callback
                                        )
  def place_frames(self):
    self.header.pack(fill="x")
    self.separator1.pack(fill="x")
    self.main.pack(expand=True,fill="both")
    self.separator2.pack(fill="x")
    self.bottom.pack(fill="x")
  
  def place_widgets(self):
    self.header_label.pack(side="left",padx=15,pady=5)
    self.audio_button.pack(side="left",padx=15,pady=8),
    self.chat_input.pack(side="left",expand=True,fill="x")
    self.submit_button.pack(side="left",padx=15)

  def audio_callback(self,event):
    print("audio clicked")

  
  def chat_callback(self):
    message = self.chat_input.get()
    self._iota += 1
    message_label = customtkinter.CTkLabel(master=self.main,
                                          text=message,
                                          fg_color="#DDE3EF",
                                          text_color="#212121",
                                          font=("Arial",12),
                                          corner_radius=12
                                          
                                          )
    message_label.grid(row=self._iota,column=1,columnspan=2,sticky="e",ipadx=8,ipady=4,padx=15,pady=5)

    self._iota += 1
    answer_label = customtkinter.CTkLabel(master=self.main,
                                          text="answer",
                                          fg_color="#FFFFFF",
                                          text_color="#212121",
                                          font=("Arial",12),
                                          corner_radius=12
                                          
                                          )
    answer_label.grid(row=self._iota,column=0,columnspan=2,sticky="w",ipadx=8,ipady=4,padx=15,pady=5)

    self.chat_input.delete(0,END)

class Divider(customtkinter.CTkFrame):
  def __init__(self,master):
    super().__init__(master=master,fg_color="#e9ecef",corner_radius=0,height=2)

App("wisdom",(800,500))