from distutils import command
from email import message
from fileinput import filename
from importlib.metadata import files
from msilib.schema import RadioButton
from multiprocessing.sharedctypes import Value
from random import choice
from tkinter import *
from tkinter import font
from tkinter import messagebox
from tkinter import filedialog
from turtle import bgcolor, width
from typing import final
from unittest import result
from matplotlib import image
from PIL import Image, ImageTk
import speech_recognition as sr
import pyttsx3
import smtplib
import os
from email.message import EmailMessage
import imghdr
import pandas

from matplotlib.pyplot import text
from numpy import pad



#function to exit the application
def iexit():
    result = messagebox.askyesno('Notification', 'Do you want to exit?')
    if result == True:
        root.destroy()
    else:
        pass    
    
#function to clear all field after clicking the button
def clear():
    toEntryField.delete(0, END)
    subjectEntryField.delete(0, END)
    textarea.delete(1.0, END)
   
    
#function for speech to text conversion
def speak():
    r = sr.Recognizer() 
    with sr.Microphone() as source2:
           try:
                  
            # wait for a second to let the recognizer
            # adjust the energy threshold based on 
            # the surrounding noise level 
            r.adjust_for_ambient_noise(source2, duration=0.2)
              
            #listens for the user's input 
            audio2 = r.listen(source2)
              
            # Using ggogle to recognize audio
            MyText = r.recognize_google(audio2)
            MyText = MyText.lower()
            textarea.insert(END, text+'.')
       
           except print(0):
               pass
    
        # use the microphone as source for input.

#taking credentials of user for sending mail
def settings():
    #for clearing inputs on button click
    def clear1():
        fromEntryField.delete(0, END)    
        passwordEntryField.delete(0, END) 
    
    def save():
        if fromEntryField.get() == '' or passwordEntryField.get()=='':
            messagebox.showerror('Error', 'Please fill up both fields', parent=root1)
        else:
            f=open('credentials.txt', 'w')
            f.write(fromEntryField.get()+','+passwordEntryField.get())
            f.close()
            messagebox.showinfo('Information', 'CREDENTIALS SAVED SUCCESFULLY', parent=root1)    
       
    root1=Toplevel()
    root1.title('Setting')
    root1.geometry('650x340+350+90')
    
    root1.config(bg='#111')
    
    img1 = Image.open('browse.png')
    resized=img1.resize((45, 45), Image.ANTIALIAS)
    browseImage1 = ImageTk.PhotoImage(resized)
    Label(root1, text="Credential Settings ", image=browseImage1, compound=RIGHT, font=('Tahoma', 30, 'bold'), fg='white', bg='#111').grid(padx=95)
    
    fromLabelFrame = LabelFrame(root1, text='From [Email Address]', font=('Tahoma', 16, 'bold'), bd=5, fg='white', bg='#111')
    fromLabelFrame.grid(row=1, column=0, pady=20)
    
    fromEntryField = Entry(fromLabelFrame, font=('Tahoma', 18, 'bold'), width=30)
    fromEntryField.grid(row=0, column=0)
    
    passwordLabelFrame = LabelFrame(root1, text='password', font=('Tahoma', 16, 'bold'), bd=5, fg='white', bg='#111')
    passwordLabelFrame.grid(row=2, column=0, pady=10)
    
    passwordEntryField = Entry(passwordLabelFrame, font=('Tahoma', 18, 'bold'), show='*', width=30)
    passwordEntryField.grid(row=0, column=0)
    
    Button(root1, text='Save', font=('Tahoma', 18, 'bold'), cursor='hand2', bg='gold2', fg='#111', command=save).place(x=210, y=260)
    Button(root1, text='Clear', font=('Tahoma', 18, 'bold'), cursor='hand2', bg='gold2', fg='#111', command=clear1).place(x=340, y=260)
    
    f=open('credentials.txt','r')
    for i in f:
        credentials=i.split(',')
    
    fromEntryField.insert(0, credentials[0])
    passwordEntryField.insert(0, credentials[1])
    root1.mainloop() 
    
#sending email waala function
def sendingEmail(toAddress, subject, body):
    f=open('credentials.txt','r')
    for i in f:
        credentials=i.split(',')
        
    message=EmailMessage()
    message['subject']=subject
    message['to']=toAddress
    message['from']=credentials[0]
    message.set_content(body)
    if check:
        if filetype=='png' or filetype=='jpg' or filetype=='jpeg':
            f=open(filepath,'rb')
            file_data=f.read()
            subtype=imghdr.what(filepath)
            
            message.add_attachment(file_data,maintype='image',subtype=subtype,filename=filename)
        else:
            f = open(filepath, 'rb')
            file_data = f.read()
            message.add_attachment(file_data,maintype='application',subtype='octet-stream',filename=filename)

    s=smtplib.SMTP('smtp.gmail.com',587)
    s.starttls()
    s.login(credentials[0],credentials[1])
    s.send_message(message)
    x=s.ehlo()
    if x[0]==250:
        return 'sent'
    else:
        return 'failed'
    
    
def send_email():
        if toEntryField.get()=='' or subjectEntryField.get()=='' or textarea.get(1.0,END)=='\n':
            messagebox.showerror('Error','All Fields Are Required',parent=root)

        else:
            if choice.get()=='single':
                result=sendingEmail(toEntryField.get(),subjectEntryField.get(),textarea.get(1.0,END))
                if result=='sent':
                    messagebox.showinfo('Success','Email is sent successfulyy')

                if result=='failed':
                    messagebox.showerror('Error','Email is not sent.')

            if choice.get()=='multiple':
                sent=0
                failed=0
                for x in final_emails:
                    result=sendingEmail(x,subjectEntryField.get(),textarea.get(1.0,END))
                    if result=='sent':
                        sent+=1
                    if result=='failed':
                        failed+=1

                    totalLabel.config(text='')
                    sentLabel.config(text='Sent:' + str(sent))
                    leftLabel.config(text='Left:' + str(len(final_emails) - (sent + failed)))
                    failedLabel.config(text='Failed:' + str(failed))

                    totalLabel.update()
                    sentLabel.update()
                    leftLabel.update()
                    failedLabel.update()

                messagebox.showinfo('Success','Emails are sent successfully')
                       
# attachment button accepting attachment to insert
check=False
def attachment():
       global filename,filetype,filepath,check
       check=True
       filepath=filedialog.askopenfilename(initialdir='c:/', title='Select File')
       filetype = filepath.split('.')
       filetype=filetype[1]
       filename = os.path.basename(filepath)
       textarea.insert(END, f'\n{filename}\n')
       
#checking if the sending type of mail is multiple or not to disable or enable the browse button
def button_check():
    if choice.get() == 'multiple':
            browseButton.config(state=NORMAL)
            toEntryField.config(state='readonly')
    if choice.get() == 'single':
            browseButton.config(state=DISABLED)
            toEntryField.config(state=NORMAL)
# sending multiple emails
def browse():
    global final_emails
    path=filedialog.askopenfilename(initialdir='c:/',title='Select Excel File')
    if path=='':
        messagebox.showerror('Error','Please select an Excel File')

    else:
        data=pandas.read_excel(path)
        if 'Email' in data.columns:
            emails=list(data['Email'])
            final_emails=[]
            for i in emails:
                if pandas.isnull(i)==False:
                    final_emails.append(i)

            if len(final_emails)==0:
                messagebox.showerror('Error','File does not contain any email addresses')

            else:
                toEntryField.config(state=NORMAL)
                toEntryField.insert(0,os.path.basename(path))
                toEntryField.config(state='readonly')
                totalLabel.config(text='Total: '+str(len(final_emails)))
                sentLabel.config(text='Sent:')
                leftLabel.config(text='Left:')
                failedLabel.config(text='Failed:')
                
#---------------------------------------FrontEnd-------------------------------#
#initializing a object
root = Tk()

#title
root.title('Email Sender')

#setting width and height of the screen
root.geometry('900x750+100+50')

#window cannot be resized i.e cannot be made smaller or bigger
root.resizable(0,0)

#setting background window color
root.config(bg="#111")

#Title
titleFrame=Frame(root, bg='#111', bd='0')
titleFrame.grid(row=0,column=0)
titleLabel = Label(titleFrame, text=" Email Sender", font=('Tahoma', 38, 'bold'), bg='#111', fg='white') 
titleLabel.grid(row=0, column=0)
img = Image.open('email.png')
resized=img.resize((60, 60), Image.ANTIALIAS)
settingImage = ImageTk.PhotoImage(resized)
Button(titleFrame, bg="#111",command=settings , bd=0, image=settingImage, cursor='hand2',activebackground='#111').grid(row=0, column=1, padx=20)

#chooseing between multiple or single email(radio buttons)
chooseFrame = Frame(root, bg='#111')
chooseFrame.grid(row=1, column=0, pady=10)
choice=StringVar()
singleRadioButton = Radiobutton(chooseFrame,command=button_check, text='Single', cursor='hand2', activebackground='#111', font=('Tahoma', 25, 'bold'), bg = '#111', variable=choice,value='single', fg='white')
singleRadioButton.grid(row=0, column=0)

multipleRadioButton = Radiobutton(chooseFrame,command=button_check, text='Multiple', cursor='hand2', activebackground='#111', font=('Tahoma', 25, 'bold'), bg = '#111', variable=choice, value='multiple', fg='white')
multipleRadioButton.grid(row=0, column=1,padx=20)

choice.set('single')
#labelframe for Sender
toLabelFrame = LabelFrame(root, text='To [Email Address]', font=('Tahoma', 16, 'bold'), bd=5, fg='white', bg='#111')
toLabelFrame.grid(row=2, column=0, padx=150, pady=10)

browseImage=PhotoImage(file='browse.png')
browseButton=Button(toLabelFrame,command=browse,text='   Browse', state=DISABLED, image=browseImage,compound=LEFT, fg="white", font=('Tahoma', 12, "bold"),bg="#111", bd=0, padx=2, cursor='hand2')
browseButton.grid(row=0, column=1, padx=20)

toEntryField = Entry(toLabelFrame, font=('Tahoma', 18, 'bold'), width=30)
toEntryField.grid(row=0, column=0)

#subject label frame
subjectLabelFrame = LabelFrame(root, text='Subject', font=('Tahoma', 16, 'bold'), bd=5, fg='white', bg='#111')
subjectLabelFrame.grid(row=3, column=0, pady=10)

subjectEntryField = Entry(subjectLabelFrame, font=('Tahoma', 18, 'bold'), width=30)
subjectEntryField.grid(row=0, column=0)

#text area (Compose Email)
emailLabelFrame = LabelFrame(root, text='Compose Email', font=('Tahoma', 16, 'bold'), bd=5, fg='white', bg='#111')
emailLabelFrame.grid(row=4, column=0, pady=10)

micImage=PhotoImage(file='mic.png')
Button(emailLabelFrame, command=speak, text='  Speak', image=micImage,compound=LEFT, fg="white", font=('Tahoma', 12, "bold"),bg="#111", bd=0, padx=2, cursor='hand2').grid(row=0, column=0)

attachImage=PhotoImage(file='attach.png')
Button(emailLabelFrame, text='  Attachment',command=attachment, image=attachImage,compound=LEFT, fg="white", font=('Tahoma', 12, "bold"),bg="#111", bd=0, padx=2, cursor='hand2').grid(row=0, column=1)

textarea=Text(emailLabelFrame, font=('Tahoma', 14, 'bold'), height=12, width=55)
textarea.grid(row=1, column=0, columnspan=2)

#exit clear and mail button
sendImage=PhotoImage(file='mail.png')
clearImage=PhotoImage(file='clear.png')
exitImage=PhotoImage(file='exit.png')
Button(root, bg="#111", bd=0, image=sendImage, cursor='hand2',activebackground='#111', command=send_email).place(x=620,y=695)
Button(root, bg="#111", bd=0, image=clearImage, cursor='hand2',activebackground='#111', command=clear).place(x=720,y=690)
Button(root, bg="#111", bd=0, image=exitImage, cursor='hand2',activebackground='#111',command=iexit).place(x=790,y=690)


totalLabel=Label(root, font=("Tahoma", 18, "bold"), fg="white", bg="#111")
totalLabel.place(x=10, y=690)
sentLabel=Label(root, font=("Tahoma", 18, "bold"), fg="white", bg="#111")
sentLabel.place(x=120, y=690)
leftLabel=Label(root, font=("Tahoma", 18, "bold"), fg="white", bg="#111")
leftLabel.place(x=210, y=690)
failedLabel=Label(root, font=("Tahoma", 18, "bold"), fg="white", bg="#111")
failedLabel.place(x=300, y=690)



#running the frame
root.mainloop()
