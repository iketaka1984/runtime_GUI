import multiprocessing as mp
from multiprocessing import Process,Manager,Value
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import font
import os
import sys
import re
from time import sleep
import vm

class MainFrame(tk.Frame):
    def __init__(self,master=None):
        super().__init__(master)
        self.flag = 0
        self.vm_value = Value('i',0)
        self.mode_select = '0'
        self.grid()
        self.master.title("virtual machine")
        self.master.geometry("1120x740")

        self.main_frm = ttk.Frame(self.master)
        self.main_frm.grid(column=0,row=0,sticky=tk.NSEW, padx=5,pady=10)

        #self.frame = tk.Toplevel()
        #self.frame.title("subframe1")
        #self.frame.geometry("500x120")
        #self.frame.grid()

        self.file1 = tk.StringVar()
        self.font1 = font.Font(family='Helvetica',size=20,weight='bold')
        self.font2 = font.Font(family='Helvetica',size=10,weight='bold')
        # create widget（folder path）
        self.folder_label = ttk.Label(self.main_frm, text="select stack machine code",font=self.font2)
        self.folder_box = ttk.Entry(self.main_frm,textvariable=self.file1)
        self.folder_btn = ttk.Button(self.main_frm,text="1.reference",command=self.button1_clicked)
        self.filename=tk.StringVar()
        # create widget（execute button)
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
        self.text = tk.Text(self.main_frm,height=30,width=50)
        self.mode_label = ttk.Label(self.main_frm, text="select mode",font=self.font2)
        # create stack text window
        self.fonts = font.Font(family='Helvetica',size=20,weight='bold')
        self.ltext_label = ttk.Label(self.main_frm, text="label stack\n(program counter, process number)",font=self.font2)
        self.label_text = tk.Text(self.main_frm,height=30, width=4)
        self.rtext_label = ttk.Label(self.main_frm,text="value stack\n(variable's value, process number)",font=self.font2)
        self.value_text = tk.Text(self.main_frm,height=30, width=4)
        #create code.txt and inv_code.txt window
        self.window2 = []
        self.user2 = []
        self.code_box = ttk.Entry(self.main_frm)
        self.code_btn = ttk.Button(self.main_frm, text="code.txt",command=self.button7_clicked)
        self.window3 = []
        self.user3 = []
        self.icode_box = ttk.Entry(self.main_frm)
        self.icode_btn = ttk.Button(self.main_frm, text="inv_code.txt",command=self.button8_clicked)
        #create again btn
        self.again_box = ttk.Entry(self.main_frm)
        self.again_btn = ttk.Button(self.main_frm, text="execute again",command=self.button9_clicked)
        #create exec btn
        self.exec_box = ttk.Entry(self.main_frm)
        self.exec_btn = ttk.Button(self.main_frm, text="exec process 1", command=self.button10_clicked)
        self.exec2_box = ttk.Entry(self.main_frm)
        self.exec2_btn = ttk.Button(self.main_frm, text="exec process 2", command=self.button11_clicked)
        self.exec3_box = ttk.Entry(self.main_frm)
        self.exec3_btn = ttk.Button(self.main_frm, text="exec esc", command=self.button12_clicked)
        #create auto and select mode btn
        self.auto_mode_box = ttk.Entry(self.main_frm)
        self.auto_mode_btn = ttk.Button(self.main_frm, text="auto mode", command=self.button13_clicked)
        self.select_mode_box = ttk.Entry(self.main_frm)
        self.select_mode_btn = ttk.Button(self.main_frm, text="step mode", command=self.button14_clicked)
        self.asmode_label = ttk.Label(self.main_frm, text="select auto or step mode",font=self.font2)
        #create explain part
        self.exp_label = ttk.Label(self.main_frm, text="(program counter, process number)")
        self.exp2_label = ttk.Label(self.main_frm, text="(variable's value, process number")
        
        # array widget
        self.asmode_label.grid(column=1,row=0,pady=10)
        self.auto_mode_btn.grid(column=2,row=0)
        self.select_mode_btn.grid(column=3,row=0)
        self.folder_label.grid(column=1, row=1, pady=10)
        self.folder_box.grid(column=2, row=1)#, sticky=tk.EW, padx=5)
        self.folder_btn.grid(column=3, row=1)
        self.fapp_btn.grid(column=2, row=2)
        self.bapp_btn.grid(column=2, row=3)
        self.tapp_btn.grid(column=3, row=2)
        self.std_btn.grid(column=4, row=2)
        self.code_btn.grid(column=5,row=2)
        self.mode_label.grid(column=1, row=2,pady=10)
        self.text.grid(column=0, row=10)
        self.clear_btn.grid(column=3, row=3)
        self.again_btn.grid(column=4,row=3)
        self.icode_btn.grid(column=5,row=3)
        self.exec_btn.grid(column=3,row=4)
        self.exec2_btn.grid(column=4,row=4)
        self.exec3_btn.grid(column=5,row=4)
        self.text_label.grid(column=0,row=9, pady=19)
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
    def delete(self):
        print("killing me")
        self.vmprocess.terminate()
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
            with open("code.txt",'w') as f2:
                f2.write(buf)
            messagebox.showinfo("message","renamed to code.txt and saved this directory")
            self.flag = self.flag + 1
        elif self.flag != 0:
            messagebox.showinfo("message","you've already selected a stack machine code")
        
    def button2_clicked(self):
        if self.mode_select == '2':
            self.vmprocess = Process(target=vm.main,args=('f',self.vm_value,self.mode_select,0))
            self.vmprocess.start()
            sleep(0.3)
            with open("stdout.txt",'r') as f:
                self.buf = f.read() 
            sys.stdout = self.write(self.buf)
            with open("valuecash.txt",'r') as f:
                self.buf = f.read()
            sys.stdout = self.rwrite(self.buf)
        elif self.mode_select == '1':
        #process_create(self.frame)
            if self.flag == 1:
                vm.main('f',self.vm_value,self.mode_select,self)
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
        #if self.mode_select == '1':
        #if self.flag == 2:
        if self.mode_select == '1':
            vm.main('b',self.vm_value,self.mode_select,self)
        elif self.mode_select == '2':
            self.vmprocess = Process(target=vm.main,args=('b',self.vm_value,self.mode_select,0))
            self.vmprocess.start()
            sleep(0.3)
            with open("stdout.txt",'r') as f:
                self.buf = f.read() 
            sys.stdout = self.write(self.buf)
        #    self.flag = self.flag + 1
        #elif self.flag != 2:
        #    messagebox.showinfo("message","you can't select this mode now")
        #elif self.mode_select == '2':
        #    self.vmbprocess = Process(target=vm.main,args=('b',self.vm_value,self.mode_select,0))
        #    self.vmbprocess.start()
    def button5_clicked(self):
        vm.main('t',self.vm_value,self.mode_select,self)
        messagebox.showinfo("message","code.txt is translated into inv_code.txt")
    def button6_clicked(self):
        self.text.delete('1.0','end')
    def button7_clicked(self):
        if self.flag != 0 or self.flag != 1:
            self.window2.append(tk.Toplevel())
            self.user2.append(User2(self.window2[len(self.window2)-1],len(self.window2)))
        else:
            messagebox.showinfo("message","you can't select this mode")
    def button8_clicked(self):
        if self.flag != 0 or self.flag != 1:
            self.window3.append(tk.Toplevel())
            self.user3.append(User3(self.window3[len(self.window3)-1],len(self.window3)))
        else:
            messagebox.showinfo("message","you can't select this mode")
    def button9_clicked(self):
        #if self.flag > 2:
        self.flag = 1
        self.label_text.delete('1.0','end')
        self.value_text.delete('1.0','end')
        self.text.delete('1.0','end')
        #else:
        #    messagebox.showinfo("message","you can't select this mode now")
    def button10_clicked(self):
        self.vm_value.value = 1
        sleep(0.1)
        with open("stdcash.txt",'r') as f:
            self.buf = f.read()
        sys.stdout = self.write(self.buf)
        with open("labelcash.txt",'r') as f:
            self.buf = f.read()
        sys.stdout = self.lwrite(self.buf)
        with open("valuecash.txt",'r') as f:
            self.buf = f.read()
        sys.stdout = self.rwrite(self.buf)
    def button11_clicked(self):
        self.vm_value.value = 2
        sleep(0.1)
        with open("stdcash.txt",'r') as f:
            self.buf = f.read()
        sys.stdout = self.write(self.buf)
        with open("labelcash.txt",'r') as f:
            self.buf = f.read()
        sys.stdout = self.lwrite(self.buf)
        with open("valuecash.txt",'r') as f:
            self.buf = f.read()
        sys.stdout = self.rwrite(self.buf)
    def button12_clicked(self):
        self.vm_value.value = 3
        sleep(0.1)
        with open("stdcash.txt",'r') as f:
            self.buf = f.read()
        sys.stdout = self.write(self.buf)
    def button13_clicked(self):
        self.mode_select = '1'
        messagebox.showinfo("message","set up auto mode")
    def button14_clicked(self):
        self.mode_select = '2'
        messagebox.showinfo("messagebox","set up step mode")
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

class User2(tk.Frame):
    def __init__(self,master,num):
        super().__init__(master)
        f = open("code.txt",'r')
        buf=f.read()
        self.com = []
        self.opr = []
        self.renamed_com = {}
        count_pc=0
        for i in range(0,len(buf),9):
            t1=buf[i:i+2]
            s1=re.search(r'\d+',t1)
            t2=buf[i+2:i+8]
            s2=re.search(r'\d+',t2)
            self.com.append((int)(s1.group()))
            self.opr.append((int)(s2.group()))
            count_pc= count_pc+1
        for i in range(0,count_pc,1):
            if self.com[i]==1:
                self.renamed_com[i]="ipush"
            elif self.com[i]==2:
                self.renamed_com[i]=" load"
            elif self.com[i]==3:
                self.renamed_com[i]="store"
            elif self.com[i]==4:
                self.renamed_com[i]="  jpc"
            elif self.com[i]==5:
                self.renamed_com[i]="  jmp"
            elif self.com[i]==6:
                self.renamed_com[i]="   op"
            elif self.com[i]==7:
                self.renamed_com[i]="label"
            elif self.com[i]==10:
                self.renamed_com[i]="  par"
            elif self.com[i]==11:
                self.renamed_com[i]="alloc"
            elif self.com[i]==12:
                self.renamed_com[i]=" free"
        self.pack()
        master.geometry("200x800")
        master.title("code.txt")
        scroll = tk.Scrollbar(master)
        text = tk.Text(master,height=4,width=50)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        text.pack(side=tk.LEFT,fill=tk.Y)
        scroll.config(command=text.yview)
        text.config(yscrollcommand=scroll.set)
        for i in range(0,count_pc,1):
            text.insert(tk.INSERT, "<"+str(i+1).rjust(3)+">")
            text.insert(tk.INSERT, "  "+self.renamed_com[i]+" ")
            text.insert(tk.INSERT, " "+str(self.opr[i]).rjust(3)+"\n")
        f.close()

class User3(tk.Frame):
    def __init__(self,master,num):
        super().__init__(master)
        f = open("inv_code.txt",'r')
        buf=f.read()
        self.com2 = []
        self.opr2 = []
        self.renamed_com2 = {}
        count_pc=0
        for i in range(0,len(buf),9):
            t1=buf[i:i+2]
            s1=re.search(r'\d+',t1)
            t2=buf[i+2:i+8]
            s2=re.search(r'\d+',t2)
            self.com2.append((int)(s1.group()))
            self.opr2.append((int)(s2.group()))
            count_pc= count_pc+1
        for i in range(0,count_pc,1):
            if self.com2[i]==0:
                self.renamed_com2[i]="    nop"
            elif self.com2[i]==7:
                self.renamed_com2[i]="  label"
            elif self.com2[i]==8:
                self.renamed_com2[i]="   rjmp"
            elif self.com2[i]==9:
                self.renamed_com2[i]="restore"
            elif self.com2[i]==10:
                self.renamed_com2[i]="    par"
            elif self.com2[i]==11:
                self.renamed_com2[i]="  alloc"
            elif self.com2[i]==12:
                self.renamed_com2[i]="   free"
        self.pack()
        master.geometry("200x800")
        master.title("inv_code.txt")
        scroll = tk.Scrollbar(master)
        text = tk.Text(master,height=4,width=50)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        text.pack(side=tk.LEFT,fill=tk.Y)
        scroll.config(command=text.yview)
        text.config(yscrollcommand=scroll.set)
        for i in range(0,count_pc,1):
            text.insert(tk.INSERT, "<"+str(i+1).rjust(3)+">")
            text.insert(tk.INSERT, "  "+self.renamed_com2[i]+"")
            text.insert(tk.INSERT, "  "+str(self.opr2[i]).rjust(3)+"\n")
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
    if app.mode_select == '2':
        app.delete()