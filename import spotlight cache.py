# import file from spotlight cache to this folder

import os
import shutil
import hashlib
import tkinter as tk
from tkinter import Variable, ttk
from tkinter import filedialog as fd
from tkinter.constants import X 
from PIL import Image, ImageTk,ImageFilter
import io

spotlight_dir = "%USERPROFILE%\\AppData\\Local\\Packages\\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy\\LocalState\\Assets"
spotlight_dir = "C:\\Users\\User\\AppData\\Local\\Packages\\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy\\LocalState\\Assets"
export_dir = '.'

def main2():
    root = tk.Tk()
    app = App(root)
    app.mainloop()
    

def get_new_images():
    # making a list of all saved jpg files in
    # export director
    saved_files = []
    for filename in os.listdir(export_dir):
        if filename.endswith('.jpg'):
            saved_files.append(filename)
    
    # 
    new_images = []
    for filename in os.listdir(spotlight_dir):
        file = os.path.join(spotlight_dir,filename)
        if os.path.getsize(file) > (100 * 1024) and isJPEG(file):
            # check if this file already saved
            if filename+'.jpg' not in saved_files:
                #copy this file to export dir
                new_images.append(filename)
    return new_images

def main():
    
    # making a list of all saved jpg files in
    # export director
    saved_files = []
    for filename in os.listdir(export_dir):
        if filename.endswith('.jpg'):
            saved_files.append(filename)
    
    # 
    for filename in os.listdir(spotlight_dir):
        file = os.path.join(spotlight_dir,filename)
        if os.path.getsize(file) > (100 * 1024) and isJPEG(file):
            # check if this file already saved
            if filename+'.jpg' not in saved_files:
                #copy this file to export dir
                shutil.copyfile(file,export_dir+filename+".jpg")
            else:
                print('same file',filename)
                

def hashfile(file):
    BUFFER_SIZE = 1*1024*1024   # 1 MB
    hash_obj = hashlib.md5() 
    
    with open(file,'r') as f:
        while True:
            data = f.read(BUFFER_SIZE)
            if not data : break
            hash_obj.update(data)
    return hash_obj.hexdigest()
    

def isJPEG(file):
    with open(file,'rb') as f:
        magic = f.read(3)
    return magic == b'\xff\xd8\xff'
    

#------------------------------------------------------

class App(tk.Frame):
    def __init__(self,root):
        super().__init__(root)
        root.title("Spotlight Cache Import")
        self.pack(fill="both",expand=True)

        self.export_dir = tk.StringVar(value=os.path.abspath(export_dir))
        self.image_list = get_new_images()
        self.image_select_list = [tk.IntVar(value=1) for i in range(len(self.image_list))]

        btnFrame = tk.Frame(self,padx=15,pady=10,bg="#ffffff")
        btnFrame.pack(side="top",fill="x")

        tk.Label(btnFrame,text="Location: ",bg="#ffffff",padx=5,font="-size 10 -weight bold").pack(side="left")
        tk.Label(btnFrame,textvariable=self.export_dir,bg="#e8e8e8",padx=5,pady=3).pack(side="left")
        tk.Button(btnFrame,text="browse",padx=7,pady=2,fg="black",bg="#d1d1d1",activebackground="#b1b1b1",highlightcolor="red",
                relief="flat",bd=0,command=self.change_location).pack(side="left")

        tk.Button(btnFrame,text="Save Selected",padx=20,pady=7,fg="white",bg="#007bff",activebackground="#0069d9",activeforeground="white",
                relief="flat",bd=0,font="-size 10 -weight bold",command=self.save_selected).pack(side="right")
        tk.Label(btnFrame,width=1,bg="#ffffff").pack(side="right")
        self.select_btn_text = tk.StringVar(value="Deselect All")
        tk.Button(btnFrame,textvariable=self.select_btn_text,padx=7,pady=2,fg="black",bg="#d1d1d1",activebackground="#b0b0b0",
                relief="flat",bd=0,command=self.toggle_selection).pack(side="right")

        self.list_new_images()
        #btn = tk.Button(self,text="save",fg="red")
        #btn.pack(side="left")
        

    def list_new_images(self):
        mainFrame = tk.Frame(self,bg="#ffffff")
        mainFrame.pack(side="top",fill="y",expand=True)
        #create canvas
        canvas = tk.Canvas(mainFrame,width=877,height=452,bg="#ffffff",highlightcolor="#f1f1f1",)
        canvas.pack(side=tk.LEFT,fill="both",expand=True)
        #create scrollbar
        scrollbar = tk.Scrollbar(mainFrame, command=canvas.yview)
        scrollbar.pack(side=tk.LEFT, fill='y',expand=True)
        
        canvas.configure(yscrollcommand = scrollbar.set)
        canvas.bind('<Configure>', lambda e:e.widget.configure(scrollregion=e.widget.bbox('all')) )
        
        # put fram to canvas
        frame = tk.Frame(canvas,padx=10,pady=10,bg="#ffffff")
        canvas.create_window((0,0), window=frame, anchor='nw')

        col_count = 4 
        for i,img in enumerate(self.image_list):
            checkVar = self.image_select_list[i]
            ImageFrame(frame,os.path.join(spotlight_dir,img),checkVar).grid(row=i//col_count,column=i%col_count)

    def toggle_selection(self):
        if self.select_btn_text.get() == 'Select All':
            setvalue = 1
            self.select_btn_text.set('Deselect All')
        else:
            setvalue = 0
            self.select_btn_text.set('Select All')

        for img in self.image_select_list:
            img.set(setvalue)

    def save_selected(self):
        export_dir = self.export_dir.get()
        for img,select in zip(self.image_list,self.image_select_list):
            if select.get() == 1:
                orgfile = os.path.join(spotlight_dir,img)
                newfile = os.path.join(export_dir,img)+".jpg"
                shutil.copyfile(orgfile,newfile)
    
    def change_location(self):
        global export_dir
        dir = fd.askdirectory()
        if len(dir) > 0:
            self.export_dir.set(dir)

class ImageFrame(tk.Frame):
    def __init__(self,parent,image,checkVar):
        super().__init__(parent,pady=5,padx=5,bg="#ffffff")
        # frame = tk.Frame(self,pady=2,padx=2,bg="#e1e1e1")
        # frame.pack()

        img = Image.open(image)
        img.thumbnail((200,200))
        # img_tk = ImageTk.PhotoImage(img)

        img_bg = img.resize((200,200)).filter(ImageFilter.GaussianBlur(15))
        img_bg.putalpha(100)
        img_w, img_h = img.size
        img_bg_w, img_bg_h = img_bg.size
        offset = ((img_bg_w - img_w) // 2, (img_bg_h - img_h) // 2)
        img_bg.paste(img,offset)

        img_bg_tk = ImageTk.PhotoImage(img_bg)

        hist = img_bg.histogram()
        domcolor = '#'+(('00'+hex(hist[0:256].index(max(hist[0:256])))[2:])[-2:] + 
                        ('00'+hex(hist[256:512].index(max(hist[256:512])))[2:])[-2:] + 
                        ('00'+hex(hist[512:768].index(max(hist[512:768])))[2:])[-2:] )

        img_bg_l = tk.Label(self,image=img_bg_tk,width=200,height=200,padx=0,pady=0,bd=0,bg=domcolor)
        img_bg_l.image = img_bg_tk
        img_bg_l.pack()
        
        select_img = ImageTk.PhotoImage(check_selected_image)
        unselect_img = ImageTk.PhotoImage(check_unselected_image)
        ckk = tk.Checkbutton(self,variable=checkVar,image=unselect_img,selectimage=select_img,indicatoron=0,compound='left',
                offrelief='flat',relief='flat',overrelief='flat',bd=0,highlightthickness=0,selectcolor="#ffffff",bg="#ffffff")
        ckk.place(x=0,y=0) 
        ckk.image = unselect_img
        ckk.reief = "flat"
        ckk.selectimage = select_img
        
        


#------------------------------------------------------

check_selected = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x14\x00\x00\x00\x14\x08\x06\x00\x00\x01\xfa\x8e-\x9b\x00\x00\x00\tpHYs\x00\x00\x0fa\x00\x00\x0fa\x01\xa8?\xa7i\x00\x00\x01\x86IDAT8\xcb\xad\x94\xcd+\x04a\x1c\xc7?\xfbbI\x92rP\xb4Q\x94\xe2\xa0\xf6$\xca[^\xdaVR\xdc\x1c$qrAmj\x8b\x0b\x07\x07\x7f\x00\x91\xdc8\xb8\x10\xe6\xe0\xaa\x1c\x94=\x89\x1bm\x1c%\xc9nkw\xc7\xb3fgvfv\xec\x8e\xb5\x9f\xc3\xf4<\xf3{~\xaf\xdfy\xc6\xe1\r%e2\xb8\xd3\x8f\xb6F\xe7\xcf\xc6\x89\x0e\x87vldG\x96\xe3\tYv\xa4\x17\x9aIuR\xd1v\xd2\x9cU\x10\x1dn\xb3\xeb\xddS\xca\x98;\xd8\xaf\xab\xce[\x03\x8b=\xb0t\xa2K\x14y\xcb\xbe\xf8\xb5$39y\xcc\x1cO\xc3\x94O\x97;MG=l\x06 t\x01\xeb~\xb8\x89\xc0\xc4A\x9e\xd4e.\xf8J\xe6\xa6v\xab\x8bBXN\xcd\n\x83zEwm\xa9\xa2\x99\xf6:\xa3\xb2\x96\x07\xbb\x9a`k\x0c\xfc\xbb\xa6\x1a\xd3\x9c\xcd\xc2k\x14\x8e\xc2\xb0\xd0\r\xa3{ \xcb\x16\x11\x03\xc2\x90H)\x87\xc6\xf7\x95uN\xd7*3\x87P\xe5\x81X\xc2F3\x1f\xf1<s,\xa92v\xd1z)\xa4b!\xd4\xea\x8b\x8e\xd2\\\x0b\xf3\x9dP\xe9\xc93m;\xf8\x1a`m\x18\xca\x85\xa7t\x0f\xd1x\x81\x80.Qs\xb0O\x91p\xfb\x1a>3\x0e\x03-\xb0\xdc\xab\xd8\xaf\x1ea\xe3\x12Rr\x9e\x19\xaa$\xc5(\xa4\x07qc\x07\xc5\xcf\xab\xd5h\x0b\xbf\xc0\xaa\x04\xf1\xa4\rQ\xf4\xdc>\xc3\xa4\xb8\xf6\xd5\x15\xa2\xbd!\xe5\x96\xaf\x9cg\xab\xb5\xa5\xb2\x15\xef1\xd1\xe6\xe9\xdff\xec\xa4\xc4\xb8\xcd\xdf\xd1\x7f\xf9\x06>\xda\x82O\x8eh\x96+\x00\x00\x00\x00IEND\xaeB`\x82'
check_unselected = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x14\x00\x00\x00\x14\x08\x06\x00\x00\x01\xfa\x8e-\x9b\x00\x00\x00\tpHYs\x00\x00\x0fa\x00\x00\x0fa\x01\xa8?\xa7i\x00\x00\x00pIDAT8\xcbc\x94\xad\xfe\xfb\x9f\x01\nX@D\xb97\x13\x98\xc3\xc4\x80\x04\x18a\xca\x18\xa7\x1c\xfb\xff\x1fE\x1a,\x05\xd3\x04\x03\xa8<tCP\x04a\x06\xc2@\xe7\xd6\x7f\xd8\xb5\x13/\x88\xd5I\xe8\x00\xa7=D[C\x91B\xac\x81A\x91B\x94\xd8\x1b\xa4\xbe\x1e\n\n\xa9\x1f3\xc4\x02\x16\x18\x83P,\x12\x02\xa0X&\xc9\xcfT\x0f\xc4Q\x03\x87\xb0\x81TO\xd8\x00Ca-\x83w\x8f\xc6\x9a\x00\x00\x00\x00IEND\xaeB`\x82'

check_selected_image = Image.open(io.BytesIO(check_selected))
check_unselected_image = Image.open(io.BytesIO(check_unselected))
#------------------------------------------------------
    
    

if __name__=='__main__':
    #main()
    main2()