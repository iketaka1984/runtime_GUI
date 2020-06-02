import multiprocessing as mp
from multiprocessing import Process,Manager
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import font
import os
import sys
from time import sleep
import vm

class MainFrame(tk.Frame):
    def __init__(self,master=None):
        super().__init__(master)
        self.flag = 0
        self.grid()
        self.master.title("virtual machine")
        self.master.geometry("1020x740")

        self.main_frm = ttk.Frame(self.master)
        self.main_frm.grid(column=0,row=0,sticky=tk.NSEW, padx=5,pady=10)

        #self.frame = tk.Toplevel()
        #self.frame.title("subframe1")
        #self.frame.geometry("500x120")
        #self.frame.grid()

        self.file1 = tk.StringVar()
        self.font1 = font.Font(family='Helvetica',size=20,weight='bold')
        self.font2 = font.Font(family='Helvetica',size=10,weight='bold')
        # ウィジェット作成（フォルダパス）
        self.folder_label = ttk.Label(self.main_frm, text="select stack machine code",font=self.font2)
        self.folder_box = ttk.Entry(self.main_frm,textvariable=self.file1)
        self.folder_btn = ttk.Button(self.main_frm,text="1.reference",command=self.button1_clicked)
        # ウィジェット作成（並び順）
        self.order_label = ttk.Label(self.main_frm, text="並び順")
        self.order_comb = ttk.Combobox(self.main_frm, values=["昇順", "降順"], width=10)
        self.order_comb.current(0)
        self.filename=tk.StringVar()
        # ウィジェット作成（実行ボタン)
        self.fapp_box = ttk.Entry(self.main_frm,textvariable=self.filename)
        self.fapp_btn = ttk.Button(self.main_frm, text="2.forward",command=self.button2_clicked)
        self.bapp_box = ttk.Entry(self.main_frm,textvariable=self.filename)
        self.bapp_btn = ttk.Button(self.main_frm, text="5.backward",command=self.button4_clicked)
        self.tapp_box = ttk.Entry(self.main_frm,textvariable=self.filename)
        self.tapp_btn = ttk.Button(self.main_frm, text="3.translate",command=self.button5_clicked)
        # create widget (stdout)
        self.window = []
        self.user = []
        self.std_box = ttk.Entry(self.main_frm)
        self.std_btn = ttk.Button(self.main_frm, text="copy result",command=self.button3_clicked)
        #crate clear wigdet
        self.clear_out = ttk.Entry(self.main_frm)
        self.clear_btn = ttk.Button(self.main_frm, text="4.clear", command=self.button6_clicked)
        # create text window
        #self.scroll = tk.Scrollbar(self.main_frm)
        self.text_label = ttk.Label(self.main_frm, text="result of execution",font=self.font1)
        self.text = tk.Text(self.main_frm,height=40,width=50)
        self.mode_label = ttk.Label(self.main_frm, text="select mode",font=self.font2)
        # create stack text window
        self.fonts = font.Font(family='Helvetica',size=20,weight='bold')
        self.ltext_label = ttk.Label(self.main_frm, text="label stack",font=self.font2)
        self.label_text = tk.Text(self.main_frm,height=30, width=4)
        self.rtext_label = ttk.Label(self.main_frm,text="value stack",font=self.font2)
        self.value_text = tk.Text(self.main_frm,height=30, width=4)


        # ウィジェットの配置
        self.folder_label.grid(column=1, row=0, pady=10)
        self.folder_box.grid(column=2, row=0)#, sticky=tk.EW, padx=5)
        self.folder_btn.grid(column=3, row=0)
        self.fapp_btn.grid(column=2, row=1)
        self.bapp_btn.grid(column=2, row=2)
        self.tapp_btn.grid(column=3, row=1)
        self.std_btn.grid(column=4, row=1)
        self.mode_label.grid(column=1, row=1,pady=10)
        self.text.grid(column=0, row=10)
        self.clear_btn.grid(column=3, row=2)
        self.text_label.grid(column=0,row=2, pady=19)
        self.ltext_label.grid(column=1,row=9)
        self.label_text.grid(column=1,row=10)
        self.rtext_label.grid(column=2,row=9)
        self.value_text.grid(column=2,row=10)


    #    self.MainCounter = 0
    #    self.MainMsg = "main({}):{}".format(\
    #                         os.getpid(),self.MainCounter)
    #    self.SubMsg = "sub:"
    #    self.CreateWidgets()
    #    self.afterId = self.after(1000,self.Update)

    #    self.shareDict = Manager().dict()
    #    self.SubProcess = Process(target=SubProcess\
    #                              , args=(self.shareDict,))
    #    self.SubProcess.start()
    #def __del__(self):
    #    print("killing me")
    #    self.SubProcess.terminate()
    #def CreateWidgets(self):
    #    self.MainLabel = tk.Label(self\
    #            ,text = str(self.MainMsg)\
    #            ,width=32)
    #    self.MainLabel.grid(row=1,column=1)
    #    self.SubLabel = tk.Label(self\
    #            ,text = str(self.SubMsg)\
    #            ,width=32)
    #    self.SubLabel.grid(row=1,column=2)
    #def Update(self):
    #    self.MainCounter += 1
    #    self.MainMsg = "main({}):{}".format(\
    #                         os.getpid(),self.MainCounter)
    #    self.MainLabel.configure(text=self.MainMsg)
    #    self.SubMsg = "sub({}):{}".format(self.shareDict["PID"]\
    #                       ,self.shareDict["val"])
    #    self.SubLabel.configure(text=str(self.SubMsg))
    #    self.afterId = self.after(1000,self.Update)
    def button1_clicked(self):
        if self.flag == 0:
            fTyp = [("","*")]
            iDir = os.path.abspath(os.path.dirname(__file__))
            filepath = filedialog.askopenfilename(filetypes = fTyp,initialdir = iDir)
            self.file1.set(filepath)
            with open(self.file1.get(),'r') as f:
                buf = f.read()
            with open("output_test.txt",'w') as f2:
                f2.write(buf)
            messagebox.showinfo("message","renamed to code.txt and saved this directory")
            self.flag = self.flag + 1
        elif self.flag != 0:
            messagebox.showinfo("message","you've already selected a stack machine code")
        
    def button2_clicked(self):
        #vmprocess = Process(target=vm.main,args=('f',self.frame))
        #vmprocess.start()
        #process_create(self.frame)
        if self.flag == 1:
            vm.main('f',self)
            self.flag = self.flag + 1
        elif self.flag != 1:
            messagebox.showinfo("message","you can't select this mode now")
    def button3_clicked(self):
        if self.flag != 0 or self.flag != 1:
            self.window.append(tk.Toplevel())
            self.user.append(User(self.window[len(self.window)-1],len(self.window)))
        else:
            messagebox.showinfo("message","you can't select this mode")
    def button4_clicked(self):
        if self.flag == 2:
            vm.main('b',self)
            self.flag = self.flag + 1
        elif self.flag != 2:
            messagebox.showinfo("message","you can't select this mode now")
    def button5_clicked(self):
        vm.main('t',self)
        messagebox.showinfo("message","code.txt is translated into inv_code.txt")
    def button6_clicked(self):
        self.text.delete('1.0','end')

    #class IORedirector(object):
    #    def __init__(self, text_area):
    #        self.text_area = text_area

    #class StdoutRedirector(IORedirector):
    def write(self, st):
        self.text.insert(tk.INSERT, st)
    def lwrite(self,st):
        self.label_text.insert(tk.INSERT, st)
    def rwrite(self, st):
        self.value_text.insert(tk.INSERT, st)

class User(tk.Frame):
    def __init__(self,master,num):
        super().__init__(master)
        f = open("stdout.txt",'r')
        buf=f.read()
        self.pack()
        master.geometry("400x1000")
        master.title("stdout")
        scroll = tk.Scrollbar(master)
        text = tk.Text(master,height=4,width=50)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        text.pack(side=tk.LEFT,fill=tk.Y)
        scroll.config(command=text.yview)
        text.config(yscrollcommand=scroll.set)
        text.insert(tk.END, buf)
        f.close()

#def process_create(frame):
#    vmprocess = Process(target=vm.main,args=('f',frame))
#    vmprocess.start()

#def SubProcess(shareDict):
#    i = 0
#    while i<1000:
#        i += 1
#        shareDict["PID"] = os.getpid()
#        shareDict["val"] = i
#    #    print(i)
#        sleep(0.1)

if __name__ == '__main__': 
    root = tk.Tk()
    app = MainFrame(master=root)
    sys.stdout = sys.__stdout__
    app.mainloop()
    #app.__del__()