from tkinter import *
from tkinter import messagebox
import sqlite3 as sql
from tkinter.ttk import Combobox

win=Tk()
win.state('zoomed')
win.configure(bg='pink')
win.resizable(width=False,height=False)
title=Label(win,text='Library Management System',font=('',35,'bold'),bg='pink')
title.pack()

db='library.db'

unq_authors=set()

def db_return(win,frm,title_combo,author_combo,student_name_entry,student_roll_entry):
      title=title_combo.get()
      author=author_combo.get()
      sturoll=student_roll_entry.get()
      stuname=student_name_entry.get()
      con=sql.connect(database=db)
      cur=con.cursor()
      cur.execute("select left_copies from book where title=? and author=?",(title,author))
      tup=cur.fetchone()
      left_copies=tup[0]
      if(left_copies>0):
            cur.execute("update book set left_copies=left_copies+1 where title=? and author=?",(title,author))
            con.commit()
            messagebox.showinfo("Return","book is returned ")
      else:
            messagebox.showerror("Return","book is already returned")
            con.close()


def db_allot(win,frm,title_combo,author_combo,student_name_entry,student_roll_entry):
    title=title_combo.get()
    author=author_combo.get()
    stuname=student_name_entry.get()
    sturoll=student_roll_entry.get()
    con=sql.connect(database=db)
    cur=con.cursor()
    cur.execute("select left_copies from book where title=? and author=?",(title,author))
    tup=cur.fetchone()
    left_copies=tup[0]
    if(stuname>3):
              messagebox.warning("Book cannot be alloted,return 1 book")
    else:
          messagebox.showinfo("Proceed for allotment")
          if(left_copies>0):
                cur.execute("insert into allotment values(?,?,?,?)",(title,author,stuname,sturoll))
                cur.execute("update book set left_copies=left_copies-1 where title=? and author=?",(title,author))

                con.commit()
                messagebox.showinfo("allot","book is alloted ")
          else:
                messagebox.showerror("allot","book is not available")
    con.close()


def getAuthor(event):
    unq_authors.clear()
    title=event.widget.get()
    con=sql.connect(database=db)
    cur=con.cursor()
    cur.execute("select author from book where title=?",(title,))
    allauthors=cur.fetchall()
    for tup in allauthors:
        unq_authors.add(tup[0])
    author_combo.configure(values=list(unq_authors))
    author_combo.current(0)
    
def db_search(win,frm,title_combo,result_label):
    result_label.configure(text='')
    
    title=title_combo.get()
    con=sql.connect(database=db)
    cur=con.cursor()
    cur.execute("select * from book where title=?",(title,))
    rows=cur.fetchall()
    msg="\tTitle Id\tTitle\tAuthor\tCopies\tLeft Copies\n"
    for row in rows:
        msg=msg+str(row[0])+"\t"+str(row[1])+"\t"+str(row[2])+"\t"+str(row[3])+"\t"+str(row[4])+"\n"
    result_label.configure(text=msg)
    con.close()
    
def db_book(win,frm,title_entry,author_entry,copies_entry):
    t=title_entry.get()
    a=author_entry.get()
    c=copies_entry.get()
    if(len(t)==0 or len(a)==0 or len(c)==0):
        messagebox.showwarning('book mgmt','Fields can not be empty')
    else:
        con=sql.connect(database=db)        
        cur=con.cursor()
        cur.execute("select max(titlle_id) from book")
        tup=cur.fetchone()
        if(tup[0]==None):
            tid=1
        else:
            tid=tup[0]+1

        cur.execute("insert into book(titlle_id,title,author,copies,left_copies) values(?,?,?,?,?)",(tid,t,a,c,c))
        con.commit()
        con.close()
        messagebox.showinfo('book mgmt','Entry done..')
        title_entry.delete(0,END)
        author_entry.delete(0,END)
        copies_entry.delete(0,END)
        title_entry.focus()
        
        
def back(win,pfrm):
    welcome_screen(win,pfrm)

def reset(user_entry,pass_entry):
    user_entry.delete(0,END)
    pass_entry.delete(0,END)
    user_entry.focus()

def login(user_entry,pass_entry,pfrm):
    u=user_entry.get()
    p=pass_entry.get()
    if(len(u)==0 or len(p)==0):
        messagebox.showwarning('login','username/password can not be empty')
    else:    
        if(u=='admin' and p=='admin'):
            messagebox.showinfo('login','Welcome,Admin')
            welcome_screen(win,pfrm)
        else:
            messagebox.showerror('login','Invalid Username or Password')

def logout(win,prfm):
    option=messagebox.askyesno('logout','Do you want to logout?')
    if(option==True):
        prfm.destroy()
        home_screen(win)
def home_screen(win):
    frm=Frame(win)
    frm.configure(bg='powder blue')
    frm.place(x=0,y=100,relwidth=1,relheight=1)
    user_lbl=Label(frm,text='Username',font=('',20,'bold'),bg='powder blue')
    user_lbl.place(relx=.3,rely=.2)
    
    pass_lbl=Label(frm,text='Password',font=('',20,'bold'),bg='powder blue')
    pass_lbl.place(relx=.3,rely=.3)

    user_entry=Entry(frm,font=('',20,'bold'),bd=5)
    user_entry.focus()
    user_entry.place(relx=.42,rely=.2)

    pass_entry=Entry(frm,font=('',20,'bold'),bd=5,show='*')
    pass_entry.place(relx=.42,rely=.3)

    login_btn=Button(frm,command=lambda:login(user_entry,pass_entry,frm),text='login',font=('',20,'bold'),bd=5)
    login_btn.place(relx=.45,rely=.4)

    reset_btn=Button(frm,command=lambda:reset(user_entry,pass_entry),text='reset',font=('',20,'bold'),bd=5)
    reset_btn.place(relx=.55,rely=.4)
    

def search(win,pfrm):
    pfrm.destroy()
    frm=Frame(win)
    frm.configure(bg='powder blue')
    frm.place(x=0,y=100,relwidth=1,relheight=1)

    wel_lbl=Label(frm,text="Welcome,Admin",font=('',20),bg='powder blue')
    wel_lbl.place(relx=0,rely=0)

    logout_btn=Button(frm,command=lambda:logout(win,frm),text='logout',font=('',20,'bold'),bd=5)
    logout_btn.place(relx=.9,rely=0)
    
    back_btn=Button(frm,text='back',command=lambda:back(win,frm),font=('',20,'bold'),bd=5)
    back_btn.place(relx=0,rely=.1)


    title_lbl=Label(frm,text='Title',font=('',20,'bold'),bg='powder blue')
    title_lbl.place(relx=.3,rely=.1)

    con=sql.connect(database=db)
    cur=con.cursor()
    cur.execute('select title from book')
    alltitles=cur.fetchall()
    unq_titles=set()
    for tup in alltitles:
        unq_titles.add(tup[0])
    
    title_combo=Combobox(frm,font=('',15,'bold'),values=list(unq_titles))
    title_combo.current(0)
    
    title_combo.place(relx=.4,rely=.1)

    result_label=Label(frm,font=('',15,'bold'),bg='powder blue')
    result_label.place(relx=.3,rely=.2)
    
    sub_btn=Button(frm,command=lambda:db_search(win,frm,title_combo,result_label),text='search',font=('',15,'bold'),bd=5)
    sub_btn.place(relx=.6,rely=.1)
    
    
def book_mgt_screen(win,pfrm):
    pfrm.destroy()
    frm=Frame(win)
    frm.configure(bg='powder blue')
    frm.place(x=0,y=100,relwidth=1,relheight=1)

    wel_lbl=Label(frm,text="Welcome,Admin",font=('',20),bg='powder blue')
    wel_lbl.place(relx=0,rely=0)

    logout_btn=Button(frm,command=lambda:logout(win,frm),text='logout',font=('',20,'bold'),bd=5)
    logout_btn.place(relx=.9,rely=0)
    
    back_btn=Button(frm,text='back',command=lambda:back(win,frm),font=('',20,'bold'),bd=5)
    back_btn.place(relx=0,rely=.1)

    title_lbl=Label(frm,text='Title',font=('',20,'bold'),bg='powder blue')
    title_lbl.place(relx=.3,rely=.2)
    
    author_lbl=Label(frm,text='Author',font=('',20,'bold'),bg='powder blue')
    author_lbl.place(relx=.3,rely=.3)

    copies_lbl=Label(frm,text='Copies',font=('',20,'bold'),bg='powder blue')
    copies_lbl.place(relx=.3,rely=.4)

    title_entry=Entry(frm,font=('',20,'bold'),bd=5)
    title_entry.focus()
    title_entry.place(relx=.42,rely=.2)

    author_entry=Entry(frm,font=('',20,'bold'),bd=5)
    author_entry.place(relx=.42,rely=.3)

    copies_entry=Entry(frm,font=('',20,'bold'),bd=5)
    copies_entry.place(relx=.42,rely=.4)

    sub_btn=Button(frm,command=lambda:db_book(win,frm,title_entry,author_entry,copies_entry),text='submit',font=('',20,'bold'),bd=5)
    sub_btn.place(relx=.5,rely=.5)


def book_allot_screen(win,pfrm):
    pfrm.destroy()
    frm=Frame(win)
    frm.configure(bg='powder blue')
    frm.place(x=0,y=100,relwidth=1,relheight=1)

    wel_lbl=Label(frm,text="Welcome,Admin",font=('',20),bg='powder blue')
    wel_lbl.place(relx=0,rely=0)

    logout_btn=Button(frm,command=lambda:logout(win,frm),text='logout',font=('',20,'bold'),bd=5)
    logout_btn.place(relx=.9,rely=0)
    
    back_btn=Button(frm,text='back',command=lambda:back(win,frm),font=('',20,'bold'),bd=5)
    back_btn.place(relx=0,rely=.1)

    
    title_lbl=Label(frm,text='Title',font=('',20,'bold'),bg='powder blue')
    title_lbl.place(relx=.25,rely=.2)
    
    author_lbl=Label(frm,text='Author',font=('',20,'bold'),bg='powder blue')
    author_lbl.place(relx=.25,rely=.3)

    student_name_lbl=Label(frm,text='Student Name',font=('',20,'bold'),bg='powder blue')
    student_name_lbl.place(relx=.25,rely=.4)

    student_roll_lbl=Label(frm,text='Student Roll',font=('',20,'bold'),bg='powder blue')
    student_roll_lbl.place(relx=.25,rely=.5)

    con=sql.connect(database=db)
    cur=con.cursor()
    cur.execute('select title from book')
    alltitles=cur.fetchall()
    unq_titles=set()
    for tup in alltitles:
        unq_titles.add(tup[0])
    
    title_combo=Combobox(frm,font=('',15,'bold'),values=list(unq_titles))
    title_combo.current(0)
    title_combo.bind("<<ComboboxSelected>>",getAuthor)
    
    title_combo.place(relx=.42,rely=.2)

    global author_combo
    
    author_combo=Combobox(frm,font=('',15,'bold'),value=list(unq_authors))
    author_combo.place(relx=.42,rely=.3)

    student_name_entry=Entry(frm,font=('',20,'bold'),bd=5)
    student_name_entry.place(relx=.42,rely=.4)

    student_roll_entry=Entry(frm,font=('',20,'bold'),bd=5)
    student_roll_entry.place(relx=.42,rely=.5)

    sub_btn=Button(frm,command=lambda:db_allot(win,frm,title_combo,author_combo,student_name_entry,student_roll_entry),text='Allot',font=('',20,'bold'),bd=5)
    sub_btn.place(relx=.5,rely=.6)

def book_return_screen(win,pfrm):
      pfrm.destroy()
      frm=Frame(win)
      frm.configure(bg='powder blue')
      frm.place(x=0,y=100,relwidth=1,relheight=1)
      wel_lbl=Label(frm,text="Welcome,Admin",font=('',20),bg='powder blue')
      wel_lbl.place(relx=0,rely=0)

      logout_btn=Button(frm,command=lambda:logout(win,frm),text='logout',font=('',20,'bold'),bd=5)
      logout_btn.place(relx=.9,rely=0)

      back_btn=Button(frm,text='back',command=lambda:back(win,frm),font=('',20,'bold'),bd=5)
      back_btn.place(relx=0,rely=.1)

      title_lbl=Label(frm,text='Title',font=('',20,'bold'),bg='powder blue')
      title_lbl.place(relx=.25,rely=.2)

      author_lbl=Label(frm,text='Author',font=('',20,'bold'),bg='powder blue')
      author_lbl.place(relx=.25,rely=.3)

      student_name_lbl=Label(frm,text='Student Name',font=('',20,'bold'),bg='powder blue')
      student_name_lbl.place(relx=.25,rely=.4)

      student_roll_lbl=Label(frm,text='Student Roll',font=('',20,'bold'),bg='powder blue')
      student_roll_lbl.place(relx=.25,rely=.5)

      con=sql.connect(database=db)
      cur=con.cursor()
      cur.execute('select title from book')
      alltitles=cur.fetchall()
      unq_titles=set()
      for tup in alltitles:
            unq_titles.add(tup[0])

            title_combo=Combobox(frm,font=('',15,'bold'),values=list(unq_titles))
            title_combo.current(0)
            title_combo.bind("<<ComboboxSelected>>",getAuthor)

            title_combo.place(relx=.42,rely=.2)

            global author_combo

            author_combo=Combobox(frm,font=('',15,'bold'),value=list(unq_authors))
            author_combo.place(relx=.42,rely=.3)

            student_name_entry=Entry(frm,font=('',20,'bold'),bd=5)
            student_name_entry.place(relx=.42,rely=.4)

            student_roll_entry=Entry(frm,font=('',20,'bold'),bd=5)
            student_roll_entry.place(relx=.42,rely=.5)

            sub_btn=Button(frm,command=lambda:db_return(win,frm,title_combo,author_combo,student_name_entry,student_roll_entry),text='Return',font=('',20,'bold'),bd=5)
            sub_btn.place(relx=.5,rely=.6)


def welcome_screen(win,pfrm):
    pfrm.destroy()
    frm=Frame(win)
    frm.configure(bg='powder blue')
    frm.place(x=0,y=100,relwidth=1,relheight=1)

    wel_lbl=Label(frm,text="Welcome,Admin",font=('',20),bg='powder blue')
    wel_lbl.place(relx=0,rely=0)

    logout_btn=Button(frm,command=lambda:logout(win,frm),text='logout',font=('',20,'bold'),bd=5)
    logout_btn.place(relx=.9,rely=0)
    
    search_btn=Button(frm,command=lambda:search(win,frm),text='search',width=20,font=('',20,'bold'),bd=5)
    search_btn.place(relx=.35,rely=.1)

    book_btn=Button(frm,text='book mgmt',command=lambda:book_mgt_screen(win,frm),width=20,font=('',20,'bold'),bd=5)
    book_btn.place(relx=.35,rely=.2)

    allot_btn=Button(frm,command=lambda:book_allot_screen(win,frm),text='book allotment',width=20,font=('',20,'bold'),bd=5)
    allot_btn.place(relx=.35,rely=.3)

    return_btn=Button(frm,command=lambda:book_return_screen(win,frm),text='book return',width=20,font=('',20,'bold'),bd=5)
    return_btn.place(relx=.35,rely=.4)

home_screen(win)
win.mainloop()









