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
    # self.minsize(size[0],size[1])
  
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
    self.create_widgets()
    self.place_frames()
    self.place_widgets()

    

  def create_frames(self):
    print("create frames")
    self.header    = customtkinter.CTkFrame(master=self,corner_radius=0,fg_color="#f4f5f9")

    text_data = []
    item_height = 60
    self.main       = ListFrame(self,text_data,item_height)
    self.bottom     = customtkinter.CTkFrame(master=self,corner_radius=0,fg_color="#f4f5f9") 
    self.separator1 = Divider(master=self)
    self.separator2 = Divider(master=self)


    

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
    message =  self.chat_input.get()
    self.main.update(message)
    self.chat_input.delete(0,END)


class ListFrame(customtkinter.CTkFrame):
  def __init__(self,master,text_data,item_height):
    super().__init__(master=master)
    self.init(text_data,item_height)
    

  def init(self,text_data,item_height):

    # data 
    self.list_data = text_data
    self.list_number = len(text_data)
    self.list_height = self.list_number * item_height

    # canvas 
    self.canvas = Canvas(master=self,background="#f4f5f9",scrollregion=(0,0,self.winfo_width(),self.list_height),bd=0, highlightthickness=0, relief='ridge')
    self.canvas.pack(expand=True,fill='both')


    # main frame that canvas will draws 
    self.frame = customtkinter.CTkFrame(master=self,fg_color="#f4f5f9",corner_radius=0)
    for index,item in enumerate(self.list_data):
      self.create_item(index,item).pack(expand=True,fill='both')

    self.canvas.create_window(
      (0,0),
      window=self.frame,
      anchor="nw",
      width=self.winfo_width(),
      height=self.list_height
    )

    self.bind("<Configure>",self.update_size)

  def update_size(self,event):
    if self.list_height >= self.winfo_height():
      self.canvas.bind_all('<Button-4>', lambda event: self.canvas.yview_scroll(-int(30),"units"))
      self.canvas.bind_all('<Button-5>', lambda event: self.canvas.yview_scroll(+int(30),"units"))
    else : 
      self.canvas.unbind_all("<Button-4>")
      self.canvas.unbind_all("<Button-5>")

    self.canvas.create_window((0,0),
                              window=self.frame
                              ,anchor="nw",
                              width=self.winfo_width()
                              ,height=self.list_height)

    print(self.list_height)    

  def update(self,message):
    self.canvas.destroy()
    self.list_data.append(message) 
    item_height = 60 
    self.init(self.list_data,item_height)
    if self.list_height >= self.winfo_height():
      self.canvas.bind_all('<Button-4>', lambda event: self.canvas.yview_scroll(-int(30),"units"))
      self.canvas.bind_all('<Button-5>', lambda event: self.canvas.yview_scroll(+int(30),"units"))
    self.canvas.yview_moveto( 1 )
    
  def create_item(self,index,item):
    frame = customtkinter.CTkFrame(master=self.frame,fg_color="#f4f5f9",corner_radius=0)

    frame.rowconfigure(0,weight=1)
    frame.columnconfigure((0,1),weight=1,uniform="a")

    message_label = customtkinter.CTkLabel(master=frame,
                                          text=item,
                                          fg_color="#DDE3EF",
                                          text_color="#212121",
                                          font=("Arial",12),
                                          corner_radius=12
                                          
                                          )
    message_label.grid(row=index,column=1,columnspan=2,sticky="e",ipadx=8,ipady=4,padx=5,pady=5)

    return frame;


class Divider(customtkinter.CTkFrame):
  def __init__(self,master):
    super().__init__(master=master,fg_color="#e9ecef",corner_radius=0,height=2)

App("wisdom",(800,500))