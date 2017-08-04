#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Tkinter import *
import os
import sys
import tksimpledialog
import inspect


class MotionpictureSystem(object):

    def __init__(self, knowledge_base, profile=None):
        # Ta emot och spara knowledge_base (archive) i en klassvariabel.
        self.archive = knowledge_base

    def store_motionpicture(self, Motionpicture):
        # sparar en Motionpicture i kunskapsbasen.
        self.archive.add_motionpicture(Motionpicture)

    def delete_motionpicture(self, motionpicture_name):
        # tar bort en Motionpicture i kunskapsbasen.
        self.archive.remove_motionpicture(motionpicture_name)

    def store_descriptive(self, descriptive_name, get_method, set_method):
        # Sag till archive att skapa en ny descriptive. descriptiven
        # haller reda pa vilka funktioner som ska anvandas for att
        # hamta och spara information.
        self.archive.add_descriptive(descriptive_name, get_method, set_method)

    def delete_descriptive(self, descriptive_name):
        # tar bort en descriptive i kunskapsbasen.
        self.archive.remove_descriptive(descriptive_name)

    def tell(self, motionpicture_name, descriptive_name, descriptive_value):
        # Be archive om den funktion
        # som skall anvandas for att spara information
        # (set_method) for en viss descriptive. Anvand funktionen for att spara
        # information om en descriptive for en viss Motionpicture.
        try:
            self.archive.get_descriptive(descriptive_name)
            method = self.archive.get_descriptive_methods(descriptive_name)[1]
            try:
                Motionpicture = self.archive.get_motionpicture(
                    motionpicture_name)
                method(motionpicture_name, descriptive_name, descriptive_value)
            except KeyError:
                return('Error, that Motionpicture does not exist', motionpicture_name)
        except KeyError:
            return('Error, that descriptive does not exist', descriptive_name)

        # Den har funktionen anvander sig av add och replace.
        # Det mesta som ska goras gors dar, i tell valjer man framforallt
        # vilken av dem som ska anvandas, beroende pa descriptivets egenskaper

    def ask(self, motionpicture_name, descriptive_name):
        # Be archive om den funktion som skall 
        # anvandas for att hamta information
        # (get_method) for en viss descriptive. Hamta ratt Motionpicture.
        # Anvand funktionen for att hamta information om ett
        # attribut for en viss Motionpicture.
        # Om en procedural attachment returneras sa kor den med Motionpicturen som
        # argument och returnera resultatet.
        try:
            self.archive.get_descriptive(descriptive_name)
            method = self.archive.get_descriptive_methods(descriptive_name)[0]
            try:
                Motionpicture = self.archive.get_motionpicture(
                    motionpicture_name)
                # if callable(Motionpicture.get_descriptive_value(descriptive_name)):
                    # Calculate_rating(Motionpicture)
                # else:
                    # print(motionpicture_name + "'s descriptive '" + descriptive_name +
                           # "has value:", method(motionpicture_name, descriptive_name))
            except KeyError:
                print(
    'Error, that Motionpicture does not exist',
     motionpicture_name)
        except KeyError:
            print('Error, that descriptive does not exist', descriptive_name)
        # Den har funktionen anvander sig av local och inherit.
        # Det mesta som ska goras gors dar, i ask valjer man framforallt
        # vilken av dem som ska anvandas, beroende pa descriptivets egenskaper
        pass

    def local(self, motionpicture_name, descriptive_name):
        # En get_method. En funktion for att hamta vardet
        # for ett visst attribut for en viss Motionpicture.
        Motionpicture = self.archive.get_motionpicture(motionpicture_name)
        return Motionpicture.get_descriptive_value(descriptive_name)

    def inherit(self, motionpicture_name, descriptive_name):
        # En get_method. En funktion for att hamta vardet for
        # ett visst attribut. Hittas inget varde anvands en Motionpictures genre
        # for att forsoka hitta information pa nasta niva i hierarkin.
        Motionpicture = self.archive.get_motionpicture(motionpicture_name)
        if Motionpicture.get_descriptive_value(descriptive_name):
            return Motionpicture.get_descriptive_value(descriptive_name)
        else:
            Motionpicture = self.archive.get_motionpicture(
                Motionpicture.get_genre())
            return Motionpicture.get_descriptive_value(descriptive_name)

    def add(self, motionpicture_name, descriptive_name, value):
        # En set_method. Lagger till ett varde for ett visst
        # attribut for en viss Motionpicture dvs. flera varden kan
        # sparas for samma attribut.
        Motionpicture = self.archive.get_motionpicture(motionpicture_name)
        Motionpicture.add_descriptive_value(descriptive_name, value)

    def replace(self, motionpicture_name, descriptive_name, value):
        # En set_method. Ersatter vardet for ett visst attribut
        # for en viss Motionpicture.
        Motionpicture = self.archive.get_motionpicture(motionpicture_name)
        Motionpicture.replace_descriptive_value(descriptive_name, value)

    # def calc_global_rating(self, motionpicture_name):
        # Motionpicture = self.archive.get_motionpicture(motionpicture_name)
        # return Motionpicture.calc_global_rating()


class Archive(object):

    def __init__(self):
        self.motionpicture_dictionary = {}
        self.descriptive_dictionary = {}
        self.genre_list = []

    def add_descriptive(self, descriptive_name, get_method, set_method):
        # Spara descriptivet.
        self.descriptive_dictionary[
            descriptive_name] = [get_method, set_method]

    def remove_descriptive(self, descriptive_name):
        # ta bort en descriptive.
        del self.descriptive_dictionary[descriptive_name]

    def add_motionpicture(self, Motionpicture):
        # Spara ratt Motionpicture.
        self.motionpicture_dictionary[
    Motionpicture.motionpicture_name] = Motionpicture

    def remove_motionpicture(self, motionpicture_name):
        # ta bort ratt Motionpicture.
        del self.motionpicture_dictionary[motionpicture_name]

    def get_motionpicture(self, motionpicture_name):
        # Returnera ratt Motionpicture.
        return self.motionpicture_dictionary[motionpicture_name]

    def get_descriptive_methods(self, descriptive_name):
        # Returnera descriptivets metoder for hamta och spara.
        return self.descriptive_dictionary[descriptive_name]

    def get_descriptive(self, descriptive_name):
        # Returnera ratt deskriptiv.
        return self.descriptive_dictionary[descriptive_name]

# class Ratingmethod(object):
    # def __init__(self):
      # pass
    # def subjective_rating_ranked(self):
        # list_comp_ranked = [sum(att*(descriptive_list.index(att)+1)) for att in descriptive_list]
        # self.srating = Motionpicture.add_descriptive_value(self, 'Weighted Average Rating',
        # (list_comp_ranked/len(descriptive_list)))
    # def critic_rating(self, rating_list):
        # sum = sum(rating_list)
        # rating = sum/len(rating_list)
        # self.arating = Motionpicture.add_descriptive_value(self,  'Critics Rating', rating)
    # def audience_rating(self, rating_list):
        # sum = sum(rating_list)
        # rating = sum/len(rating_list)
        # self.crating = Motionpicture.add_descriptive_value(self, 'Audience
        # Rating', rating)


class Motionpicture(object):

    def __init__(self, motionpicture_name, genre):
        # Namn, genre och attributvarden for en Motionpicture ska sparas i sjalva ramen.
        # Varje ram ska innehalla en dictionary for attributvarden.
        self.descriptives = {'Genre': genre}
        self.motionpicture_name = motionpicture_name

    def get_descriptives(self):
        string = ""
        for each in self.descriptives:
          string = string + str(each) + ":" + \
                                str(self.descriptives[each]) + '\n'
        return string

    def get_descriptive_value(self, descriptive_name):
        # Returnera attributvardet fran Motionpicturens dictionary.
        return self.descriptives[descriptive_name]

    def add_descriptive_value(self, descriptive_name, descriptive_value):
        # Lagg till ett varde for descriptivet i Motionpicturens dictionary
        # (flera varden kan sparas for samma attribut).
        if descriptive_name in self.descriptives:
            if type(self.descriptives[descriptive_name]) is type([]):
                self.descriptives[descriptive_name].append(descriptive_value)
            else:
                self.descriptives[descriptive_name] = [self.descriptives[descriptive_name],
                descriptive_value]
        else:
            self.descriptives.update({descriptive_name: descriptive_value})

    def replace_descriptive_value(self, descriptive_name, descriptive_value):
        # Ersatt ett varde med ett annat varde for descriptivet i
        # Motionpictures dictionary.
        self.descriptives[descriptive_name] = descriptive_value

# En klass som arver fran Motionpictureklassen. Den har klassen
# anvands for att skapa instanser och spara filmer i
# databasen.


class Movie(Motionpicture):

    def __init__(self, motionpicture_name, genre):
      super(Movie, self).__init__(motionpicture_name, genre)
      self.descriptives = {'Genre': genre, 'Story': 'No-Rating',
      'Direction': 'No-Rating', 'Acting': 'No-Rating'}


# En klass som arver fran Motionpictureklassen. Den har klassen
# anvands for att skapa instanser och spara serier i
# databasen.
class Series(Motionpicture):

    def __init__(self, motionpicture_name, genre, seasons):
      super(Series, self).__init__(motionpicture_name, genre)
      self.descriptives = {'Genre': genre, 'Story': 'No-Rating',
      'Direction': 'No-Rating', 'Acting': 'No-Rating'}
      self.seasons = seasons

# Window klassen. Instancer skapas i Interfacet.


class Window(tksimpledialog.Dialog):

    def windowfunction1(self, master):
      if self.variable2.get() == 'Series':
        self.menu3.config(state='normal')
        self.variable3.trace("w", lambda x, y, z: self.windowfunction2(master))

      else:
        self.menu3.config(state='disabled')

    def addition(self):
      self.tempdict2[self.variable4.get()] = self.episodes.get()

    def windowfunction2(self, master):
      if self.variable3.get() != 'Nr. of Seasons':
        self.menu3.destroy()
        self.menu2.destroy()
        self.seasonsmenu = apply(OptionMenu, (master, self.variable4) + tuple(
        xrange(1, int(self.variable3.get()) + 1)))
        self.tempdict2 = {}
        self.seasonsmenu.grid(row=self.current_row, column=0)
        self.episodes = StringVar(master)
        self.episodes.set('Nr. of Episodes')
        episodesmenu = apply(OptionMenu, (master, self.episodes) + tuple(
        xrange(1, 31)))
        episodesmenu.grid(row=self.current_row, column=1)
        insert = Button(master, text="Insert", command=self.addition)
        insert.grid(row=self.current_row, column=2)
        insert.config(state='disabled')
        self.episodes.trace("w", lambda x, y, z: self.windowfunction3(master,
        episodesmenu, insert))

    def windowfunction3(self, master, episodesmenu, insert):
      insert.config(state='normal')

    def eventfunction(self, event):
      widget = event.widget
      selection = widget.curselection()
      self.variable3 = widget.get(selection[0])

    def body(self, master, title, settings):
      self.current_row = 0
      self.title = title
      self.e1 = Entry(master)
      self.e2 = Entry(master)
      self.e3 = Entry(master)
      self.e4 = Entry(master)
      self.variable1 = StringVar(master)
      self.variable2 = StringVar(master)
      self.variable3 = StringVar(master)
      self.variable4 = StringVar(master)
      self.variable5 = StringVar(master)
      try:
        self.label1 = Label(master, text=settings['label'][0])
        self.label2 = Label(master, text=settings['label2'][0])
        self.label3 = Label(master, text=settings['label3'][0])
        self.label4 = Label(master, text=settings['label4'][0])
        self.label5 = Label(master, text=settings['label5'][0])
      except KeyError:
        pass
      self.scale1 = Scale(master, from_=0, to=10, orient=HORIZONTAL)
      self.scale2 = Scale(master, from_=0, to=10, orient=HORIZONTAL)
      self.scale3 = Scale(master, from_=0, to=10, orient=HORIZONTAL)
      self.temp_dict = {}

      if 'New Motion-Picture' in self.title:
        self.label1.grid(row=self.current_row)
        self.e1.grid(row=self.current_row, column=settings['e1'][0])
        self.current_row += 1
        self.variable1.set(settings['variable1'])
        self.menu1 = apply(OptionMenu, (master, self.variable1) + tuple(
        settings['menu1'][0]))
        self.menu1.grid(row=self.current_row, column=settings['menu1'][1])
        self.current_row += 1
        self.variable2.set(settings['variable2'])
        for name, obj in inspect.getmembers(sys.modules[__name__]):
          if inspect.isclass(obj):
            if issubclass(obj, Motionpicture) and name != "Motionpicture":
              self.temp_dict[name] = obj
        self.menu2 = apply(OptionMenu, (master, self.variable2) + tuple(
        self.temp_dict.keys()))
        self.menu2.grid(row=self.current_row, column=0)
        self.variable3.set('Nr. of Seasons')
        self.variable4.set("In Season")
        self.menu3 = apply(OptionMenu, (master, self.variable3) + tuple(
        xrange(1, 31)))
        self.menu3.config(state='disabled')
        self.menu3.grid(row=self.current_row, column=1)
        self.variable2.trace("w", lambda x, y, z: self.windowfunction1(master))
      if 'Add Descriptive' in self.title:
        self.label1.grid(row=self.current_row)
        self.e1.grid(row=self.current_row, column=settings['e1'][0])
        self.current_row += 1
        self.label2.grid(row=self.current_row, sticky=settings['label2'][1])
        self.variable1.set('Descriptive Types')
        self.variable2.set('Descriptive')
        self.menu = apply(
    OptionMenu,
    (master,
    self.variable1) +
     tuple('<empty>'))
        if settings['archive'].descriptive_dictionary.keys() == []:
          self.menu.config(state='disabled')
        else:
          self.menu = apply(OptionMenu, (master, self.variable1) + tuple(
          settings['archive'].descriptive_dictionary.keys()))
        self.menu.grid(row=self.current_row, column=1)
        self.current_row += 1
        self.label3.grid(row=self.current_row, sticky=settings['label3'][1])
        self.current_row += 1
        self.textfield = Text(
        master=master,
        wrap=WORD,
        width=20,
        height=10)
        self.textfield.grid(row=self.current_row, column=0)
        self.current_row += 1
        self.label4.grid(row=self.current_row, sticky=settings['label4'][1])
        self.current_row += 1
        self.listbox = Listbox(master)
        for name in settings['archive'].motionpicture_dictionary:
          self.listbox.insert(END, name)
        self.listbox.bind('<ButtonRelease-1>', self.eventfunction)
        self.listbox.grid(row=self.current_row, sticky=N)
      if 'Genre' in self.title:
        self.label1.grid(row=self.current_row)
        self.e1.grid(row=self.current_row, column=settings['e1'][0])
        self.current_row += 1
        self.label1.grid(row=self.current_row, sticky=settings['label'][1])
        self.e1.grid(row=self.current_row, column=settings['e1'][0])
        self.current_row += 1
        self.label2.grid(row=self.current_row, sticky=settings['label2'][1])
        self.listbox = Listbox(master)
        settings['archive'].genre_list.sort()
        for name in settings['archive'].genre_list:
          self.listbox.insert(END, name)
        self.current_row += 1
        self.listbox.grid(row=self.current_row, sticky=S)
      if 'Rating' in self.title:
        self.label1.grid(row=self.current_row, sticky=settings['label'][1])
        self.current_row += 1
        self.listbox = Listbox(master)
        for name in settings['archive'].motionpicture_dictionary:
          self.listbox.insert(END, name)
        self.listbox.bind('<ButtonRelease-1>', self.eventfunction)
        self.listbox.grid(row=self.current_row, sticky=N)
        self.current_row += 1
        self.label2.grid(row=self.current_row, sticky=settings['label2'][1])
        self.current_row += 1
        self.label3.grid(row=self.current_row, sticky=settings['label3'][1])
        self.scale1.grid(row=self.current_row, sticky='E')
        self.current_row += 1
        self.label4.grid(row=self.current_row, sticky=settings['label4'][1])
        self.scale2.grid(row=self.current_row, sticky='E')
        self.current_row += 1
        self.label5.grid(row=self.current_row, sticky=settings['label5'][1])
        self.scale3.grid(row=self.current_row, sticky='E')
      elif 'Remove' in self.title:
        self.current_row += 1
        self.listbox = Listbox(master)
        if 'Motion-Picture' in self.title:
          for name in settings['archive'].motionpicture_dictionary:
            self.listbox.insert(END, name)
        elif 'Descriptive' in self.title:
          for name in settings['archive'].descriptive_dictionary:
            self.listbox.insert(END, name)
        self.listbox.bind('<ButtonRelease-1>', self.eventfunction)
        self.listbox.grid(row=self.current_row, sticky=N)

    def apply(self):
      if self.variable2.get() == "Movie":
        self.result = self.temp_dict[self.variable2.get()](self.e1.get(),
        self.variable1.get())
      elif self.variable2.get() == "Series":
        self.result = self.temp_dict[self.variable2.get()](self.e1.get(),
        self.variable1.get(), self.tempdict2)
      elif 'Genre' in self.title:
        self.result = self.temp_dict = (self.e1.get())
      elif 'Add Descriptive' in self.title:
        self.result = self.temp_dict = (
    self.e1.get(), self.textfield.get(
        "1.0", END), self.variable3)
      elif 'Rating' in self.title:
        self.result = self.temp_dict = (
    self.variable3,
    self.scale1.get(),
    self.scale2.get(),
     self.scale3.get())
      if 'Remove' in self.title:
        self.result = self.temp_dict = (self.variable3)
      return self.result

# En klass som tar hand om den externa vyn av Motionpicturesystemet(MPS).
# tar instanser av archive och MPS och skapar en interface
# i TKinter runt dem. Associerar starkt med window klassen.


class Interface():
    # skapar alla frames och dropdown menyer.

    def __init__(self, master, MotionpictureSystem):
        # self.archive = archive
        self.MPS = MotionpictureSystem
        self.MPS.archive.genre_list = [
        'Action', 'Adventure', 'Animation',
        'Biography', 'Comedy', 'Crime',
        'Documentary', 'Drama', 'Family',
        'Fantasy', 'Film-Noir',
        'History', 'Horror', 'Music', 'Musical',
        'Mystery', 'Romance', 'Sci-Fi', 'Sport',
        'Thriller', 'War', 'Western']
        self.master = master
        mainmenu = Menu(self.master)

        # profilemenu = Menu(mainmenu, tearoff=0)
        # addmenu.add_command(label="New Profile", command=self.addmp_file)
        # editmenu.add_command(label="Edit Current Profile", command=self.editprofile)
        # mainmenu.add_cascade(label="Switch Profile", menu=profilemenumenu)

        addmenu = Menu(mainmenu, tearoff=0)
        mainmenu.add_cascade(label="Add to/Modify Archive", menu=addmenu)
        pmmenu = Menu(addmenu, tearoff=0)
        pmmenu.add_command(label="Create New", command=self.addmp_create)
        # pmmenu.add_command(label="From Webpage", command=self.addmp_web)
        # pmmenu.add_command(label="Browse..", command=self.addmp_file)
        addmenu.add_cascade(label="Motion-Picture", menu=pmmenu)
        addmenu.add_command(label="Add Genre", command=self.add_genre)
        addmenu.add_command(
    label="Add/Modify Descriptive",
     command=self.add_descriptive)
        addmenu.add_command(
    label="Add/Modify MP-Rating",
     command=self.add_rating)

        removemenu = Menu(mainmenu, tearoff=0)
        mainmenu.add_cascade(label="Remove From Archive", menu=removemenu)
        removemenu.add_command(label="Motion-Picture", command=self.removemp)
        removemenu.add_command(label="Descriptive", command=self.removedesc)

        # Lite funktioner som inte anvandes. Tankte implementera dem ngn annan gang.
        # toolsmenu = Menu(mainmenu, tearoff=0)
        # toolsmenu.add_command(label="Compare Motion-Pictures",
        # command=self.compare)

        # pmprmenu = Menu(toolsmenu, tearoff=0)
        # pmprmenu.add_command(label="From Webpage", command=self.addmp_web)
        # pmprmenu.add_command(label="From Archive", command=self.getmp)
        # pmprmenu.add_command(label="Browse..", command=self.addmp_file)

        # toolsmenu.add_cascade(label="Predict Motion-Picture Rating", menu=pmprmenu)
        # toolsmenu.add_cascade(label="Suggest Motion-Picture", menu=pmprmenu)
        # toolsmenu.add_cascade(label="Create your own!(NEW)", menu=pmprmenu)
        # mainmenu.add_cascade(label="Rating Tools", menu=toolsmenu)

        # settingsmenu = Menu(mainmenu, tearoff=0)
        # mainmenu.add_cascade(label="Settings", menu=settingsmenu)

        # datamenu = Menu(mainmenu, tearoff=0)
        # mainmenu.add_cascade(label="Data and Statistics", menu=datamenu)

        # helpmenu = Menu(mainmenu, tearoff=0)
        # helpmenu.add_command(label="How-To", command=self.how_to)
        # helpmenu.add_command(label="About", command=self.about)
        # mainmenu.add_cascade(label="Help", menu=helpmenu)

        self.master.config(menu=mainmenu)

        self.infoframe = Frame(width=375, height=400, bg="black", bd=5,
        colormap="new", relief=RAISED)
        self.infoframe.grid(row=0, column=0, sticky=N)

        self.navigationframe = Frame(
				width=600,
				height=600,
				bg="black",
				bd=10,
				colormap="new",
				relief=RAISED)
        self.navigationframe.grid(row=0, column=1)
        self.coverframe = Frame(bg="black", colormap="new", relief=RAISED)
        self.master.bind('<ButtonRelease-1>', self.clickfunction)
    # klickfunktion till coversen sa att infoframen uppdateras enligt den bild
    # som klickas.
    def clickfunction(self, event):
        widget=event.widget
        selection=widget.cget("text")
        self.updatetxtframes(selection)
    # hamtar och formaterar bilden pa en cover.
    def cover(self, name):
        path="Covers/%s.gif" % (name)
        try:
          cover=PhotoImage(file=path)
        except TclError:
          path="Covers/%s.gif" % ("Default")
          cover=PhotoImage(file=path)
        scale_w=cover.width() / 100
        scale_h=cover.height() / 150
        cover=PhotoImage(file=path).subsample(scale_w, scale_h)
        return cover
    # Uppdaterar framen som visar covers. Fungerar som navigationsframen.
    def updatenavframe(self):
        rowval=0
        colval=0
        self.coverframe.destroy()
        self.coverframe=Frame(bg="black", colormap="new", relief=RAISED)
        self.coverframe.grid(row=0, column=1)
        for mp in self.MPS.archive.motionpicture_dictionary:
          cover=self.cover(mp)
          covericon=Label(self.coverframe, image=cover, text=mp)
          covericon.image=cover
          covericon.grid(row=rowval, column=colval, sticky=W)
          colval += 1
    # Uppdaterar infoframen.
    def updatetxtframes(self, clicked_mp):
      self.infoframe.destroy()
      mp=self.MPS.archive.get_motionpicture(clicked_mp)
      lefttxt=mp.get_descriptives()
      self.infoframe=Frame(width=375, height=400, bg="black", bd=5,
      colormap="new", relief=RAISED)
      self.infoframe.grid(row=0, column=0, sticky=N)
      leftlbl=Label(self.infoframe, text=lefttxt, font=("Helvetica", 20))
      leftlbl.grid(row=0, column=0)
    # dialogrutan som skapar en MP, och lagger till den i arkivet.
    def addmp_create(self):
        mp=Window(self.master, 'Create New Motion-Picture',
        {'label': ['Title', 'W'], 'e1': [1], 'variable1': 'Genre',
        'variable2': 'Category',
        'menu1': [self.MPS.archive.genre_list, 1]})
        self.MPS.store_motionpicture(mp.result)
        self.updatenavframe()
    # dialogrutan som skapar en ny genre och lagger till den i arkivet.
    def add_genre(self):
        genre=Window(self.master, 'Add Genre',
        {'label': ['Enter New Genre', 'W'], 'e1': ['1'],
        'label2': ['These Are the Currently Available Genres', 'N'],
        'archive': self.MPS.archive})
        self.MPS.archive.genre_list.append(genre.result)
    # dialogrutan som skapar en ny deskriptiv, textbeskrivning.
    def add_descriptive(self):
        descriptive=Window(self.master, 'Add Descriptive',
        {'label': ['Enter Descriptive Type', 'W'], 'e1': ['1'],
        'label2': ['Or Choose From Previously Entered Desc. Types', 'N'],
        'label3': ['Descriptive Text', 'N'],
        'label4': ['Select Motion-Picture', 'N'],
        'archive': self.MPS.archive})
        try:
          self.MPS.archive.get_descriptive(descriptive.result[0])
          self.MPS.tell(
    descriptive.result[2],
    descriptive.result[0],
     descriptive.result[1])
        except KeyError:
          self.MPS.store_descriptive(
    descriptive.result[0],
    self.MPS.local,
     self.MPS.replace)
          self.MPS.tell(
    descriptive.result[2],
    descriptive.result[0],
     descriptive.result[1])
    # add_rating ar dialogrutan som anvands for att ranka en film enligt tre kriterier,
		# hur bra storyn var,
    # hur bra den regisserades, och hur bra skadespelet var.
    def add_rating(self):
        rating=Window(self.master, 'Add Rating',
        {'label': ['Select Motion-Picture to Rate', 'N'],
        'label2': ['Rate the MP According to These Metrics', 'N'],
        'label3': ['Story', 'W'],
        'label4': ['Direction', 'W'],
        'label5': ['Acting', 'W'],
        'archive': self.MPS.archive})
        self.MPS.store_descriptive('Story', self.MPS.local, self.MPS.replace)
        self.MPS.store_descriptive(
    'Direction', self.MPS.local, self.MPS.replace)
        self.MPS.store_descriptive('Acting', self.MPS.local, self.MPS.replace)
        story_rating=self.MPS.tell(rating.result[0], 'Story', rating.result[1])
        direction_rating=self.MPS.tell(
    rating.result[0],
    'Direction',
     rating.result[2])
        acting_rating=self.MPS.tell(
    rating.result[0], 'Acting', rating.result[3])
    # dialogrutorna som tar bort en textbeskrivning eller en hel MP. akriv och
    # frames uppdateras enligt.
    def removemp(self):
        rmp=Window(self.master, 'Remove Motion-Picture',
        {'label': ['Choose Which MP to Remove', 'N'],
        'archive': self.MPS.archive})
        self.MPS.delete_motionpicture(rmp.result)
        self.updatenavframe()
    def removedesc(self):
        rdesc=Window(self.master, 'Remove Descriptive',
        {'label': ['Choose Which Descriptive to Remove', 'N'],
        'archive': self.MPS.archive})
        self.MPS.delete_descriptive(rdesc.result)
    # def addmp_file(self):
        # pass
    # def addmp_web(self):
        # pass
    # def getmp(self):
        # pass
    # def rate(self):
        # pass
    # def compare(self):
        # pass
    # def predict(self):
        # pass
    # def suggest(self):
        # pass
    # def textwindow(self):
        # pass
    # def ratingwindow(self):
        # pass
    # def settings(self):
        # pass
    # def sort(self):
        # pass
    # def save(self):
        # pass
    # def help(self):
        # pass
    # def how_to(self):
        # pass
    # def about(self):
        # pass
    # def quitnsavebox(self):
        # pass

def Main():
    root=Tk()
    archive=Archive()
    MPS=MotionpictureSystem(archive)
    interface=Interface(root, MPS)
    root.wm_title("Movie Genie")
    root.mainloop()
if __name__ == "__main__":
    Main()