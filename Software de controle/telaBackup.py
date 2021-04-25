from matplotlib import pyplot as plt
from Guiagem import Guiagem
from WebCamera import WebCamera
from Bluetooth import Bluetooth
from ObjectTracking import ObjectTracking
from PIL import Image
from PIL import ImageTk
import numpy as np
import tkinter.filedialog as tkFileDialog
import tkinter.messagebox as tkMessageBox
import cv2
import sys

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

try:
    import ttk
    py3 = False
except ImportError:
    import tkinter.ttk as ttk
    py3 = True

import tela_support

def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global val, w, root
    root = tk.Tk()
    tela_support.set_Tk_var()
    top = TopLevel (root)
    tela_support.init(root, top)
    root.mainloop()

w = None
def create_TopLevel(root, *args, **kwargs):
    '''Starting point when module is imported by another program.'''
    global w, w_win, rt
    rt = root
    w = tk.Toplevel (root)
    tela_support.set_Tk_var()
    top = TopLevel (w)
    tela_support.init(w, top, *args, **kwargs)
    return (w, top)

def destroy_TopLevel():
    global w
    w.destroy()
    w = None

class TopLevel:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85'
        _ana2color = '#ececec' # Closest X11 color: 'gray92'
        font9 = "-family {Segoe UI} -size 9 -weight normal -slant "  \
            "roman -underline 0 -overstrike 0"
        self.style = ttk.Style()
        if sys.platform == "win32":
            self.style.theme_use('winnative')
        self.style.configure('.',background=_bgcolor)
        self.style.configure('.',foreground=_fgcolor)
        self.style.configure('.',font="TkDefaultFont")
        self.style.map('.',background=
            [('selected', _compcolor), ('active',_ana2color)])

        top.geometry("1262x640+1+1")
        top.minsize(116, 1)
        top.maxsize(1370, 750)
        top.resizable(1, 1)
        top.title("Interface gráfica Ballbot")
        top.configure(background="#d9d9d9")
        top.configure(highlightbackground="#d9d9d9")
        top.configure(highlightcolor="black")

        self.Frame1 = tk.Frame(top)
        self.Frame1.place(relx=0.8, rely=0.016, relheight=0.461, relwidth=0.202)
        self.Frame1.configure(relief='groove')
        self.Frame1.configure(borderwidth="2")
        self.Frame1.configure(relief="groove")
        self.Frame1.configure(background="#d9d9d9")
        self.Frame1.configure(highlightbackground="#d9d9d9")
        self.Frame1.configure(highlightcolor="black")

        self.btnImportar = tk.Button(self.Frame1)
        self.btnImportar.place(relx=0.51, rely=0.034, height=24, width=97)
        self.btnImportar.configure(activebackground="#ececec")
        self.btnImportar.configure(activeforeground="#000000")
        self.btnImportar.configure(background="#d9d9d9")
        self.btnImportar.configure(disabledforeground="#a3a3a3")
        self.btnImportar.configure(foreground="#000000")
        self.btnImportar.configure(highlightbackground="#d9d9d9")
        self.btnImportar.configure(highlightcolor="black")
        self.btnImportar.configure(pady="0")
        self.btnImportar.configure(text='''Importar''')

        self.Label2 = tk.Label(self.Frame1)
        self.Label2.place(relx=0.071, rely=0.041, height=21, width=104)
        self.Label2.configure(activebackground="#f9f9f9")
        self.Label2.configure(activeforeground="black")
        self.Label2.configure(background="#d9d9d9")
        self.Label2.configure(disabledforeground="#a3a3a3")
        self.Label2.configure(font="-family {Segoe UI} -size 11 -weight bold")
        self.Label2.configure(foreground="#000000")
        self.Label2.configure(highlightbackground="#d9d9d9")
        self.Label2.configure(highlightcolor="black")
        self.Label2.configure(text='''Waypoints''')

        self.Listbox1 = tk.Listbox(self.Frame1)
        self.Listbox1.place(relx=0.196, rely=0.271, relheight=0.685
                , relwidth=0.682)
        self.Listbox1.configure(background="white")
        self.Listbox1.configure(disabledforeground="#a3a3a3")
        self.Listbox1.configure(font="TkFixedFont")
        self.Listbox1.configure(foreground="#000000")
        self.Listbox1.configure(highlightbackground="#d9d9d9")
        self.Listbox1.configure(highlightcolor="black")
        self.Listbox1.configure(selectbackground="#c4c4c4")
        self.Listbox1.configure(selectforeground="black")
        self.Listbox1.configure(selectmode='single')

        self.lbNumWaypointAtual = ttk.Label(self.Frame1)
        self.lbNumWaypointAtual.place(relx=0.51, rely=0.169, height=19, width=56)

        self.lbNumWaypointAtual.configure(background="#d9d9d9")
        self.lbNumWaypointAtual.configure(foreground="#000000")
        self.lbNumWaypointAtual.configure(font="-family {Segoe UI} -size 10")
        self.lbNumWaypointAtual.configure(relief="flat")
        self.lbNumWaypointAtual.configure(text='''0''')

        self.TLabel1_14 = ttk.Label(self.Frame1)
        self.TLabel1_14.place(relx=0.235, rely=0.18, height=19, width=66)
        self.TLabel1_14.configure(background="#d9d9d9")
        self.TLabel1_14.configure(foreground="#000000")
        self.TLabel1_14.configure(font="TkDefaultFont")
        self.TLabel1_14.configure(relief="flat")
        self.TLabel1_14.configure(text='''Linha atual''')

        self.lblTitulo = tk.Label(top)
        self.lblTitulo.place(relx=0.095, rely=0.009, height=31, width=484)
        self.lblTitulo.configure(activebackground="#f9f9f9")
        self.lblTitulo.configure(activeforeground="black")
        self.lblTitulo.configure(background="#d9d9d9")
        self.lblTitulo.configure(disabledforeground="#a3a3a3")
        self.lblTitulo.configure(font="-family {Segoe UI} -size 17 -weight bold")
        self.lblTitulo.configure(foreground="#DC143C")
        self.lblTitulo.configure(highlightbackground="#d9d9d9")
        self.lblTitulo.configure(highlightcolor="black")
        self.lblTitulo.configure(text='''LMI - Laboratório de Máquinas Inteligentes''')

        self.Frame3 = tk.Frame(top)
        self.Frame3.place(relx=0.008, rely=0.066, relheight=0.102
                , relwidth=0.574)
        self.Frame3.configure(relief='groove')
        self.Frame3.configure(borderwidth="2")
        self.Frame3.configure(relief="groove")
        self.Frame3.configure(background="#d9d9d9")
        self.Frame3.configure(highlightbackground="#d9d9d9")
        self.Frame3.configure(highlightcolor="black")

        self.btnConectar = tk.Button(self.Frame3)
        self.btnConectar.place(relx=0.883, rely=0.462, height=24, width=77)
        self.btnConectar.configure(activebackground="#ececec")
        self.btnConectar.configure(activeforeground="#000000")
        self.btnConectar.configure(background="#d9d9d9")
        self.btnConectar.configure(disabledforeground="#a3a3a3")
        self.btnConectar.configure(foreground="#000000")
        self.btnConectar.configure(highlightbackground="#d9d9d9")
        self.btnConectar.configure(highlightcolor="black")
        self.btnConectar.configure(pady="0")
        self.btnConectar.configure(text='''Conectar''')

        self.btnOnCam = tk.Button(self.Frame3)
        self.btnOnCam.place(relx=0.028, rely=0.308, height=34, width=107)
        self.btnOnCam.configure(activebackground="#ececec")
        self.btnOnCam.configure(activeforeground="#000000")
        self.btnOnCam.configure(background="#d9d9d9")
        self.btnOnCam.configure(disabledforeground="#a3a3a3")
        self.btnOnCam.configure(foreground="#000000")
        self.btnOnCam.configure(highlightbackground="#d9d9d9")
        self.btnOnCam.configure(highlightcolor="black")
        self.btnOnCam.configure(pady="0")
        self.btnOnCam.configure(text='''Ligar câmera''')

        self.tbDeviceBluetooth = ttk.Combobox(self.Frame3)
        self.tbDeviceBluetooth.place(relx=0.69, rely=0.462, relheight=0.323
                , relwidth=0.17)
        self.tbDeviceBluetooth.configure(textvariable=tela_support.nomesDeviceBluetooth)
        self.tbDeviceBluetooth.configure(takefocus="")

        self.btnAtualizarBluetooth = tk.Button(self.Frame3)
        self.btnAtualizarBluetooth.place(relx=0.593, rely=0.462, height=24
                , width=57)
        self.btnAtualizarBluetooth.configure(activebackground="#ececec")
        self.btnAtualizarBluetooth.configure(activeforeground="#000000")
        self.btnAtualizarBluetooth.configure(background="#d9d9d9")
        self.btnAtualizarBluetooth.configure(disabledforeground="#a3a3a3")
        self.btnAtualizarBluetooth.configure(foreground="#000000")
        self.btnAtualizarBluetooth.configure(highlightbackground="#d9d9d9")
        self.btnAtualizarBluetooth.configure(highlightcolor="black")
        self.btnAtualizarBluetooth.configure(pady="0")
        self.btnAtualizarBluetooth.configure(text='''Atualizar''')

        self.Entry1 = tk.Entry(self.Frame3)
        self.Entry1.place(relx=0.207, rely=0.462,height=20, relwidth=0.337)
        self.Entry1.configure(background="white")
        self.Entry1.configure(disabledforeground="#a3a3a3")
        self.Entry1.configure(font="-family {Courier New} -size 10")
        self.Entry1.configure(foreground="#000000")
        self.Entry1.configure(highlightbackground="#d9d9d9")
        self.Entry1.configure(highlightcolor="black")
        self.Entry1.configure(insertbackground="black")
        self.Entry1.configure(selectbackground="#c4c4c4")
        self.Entry1.configure(selectforeground="black")
        self.Entry1.configure(textvariable=tela_support.enderecoCamera)

        self.TLabel1_8 = ttk.Label(self.Frame3)
        self.TLabel1_8.place(relx=0.207, rely=0.154, height=19, width=126)
        self.TLabel1_8.configure(background="#d9d9d9")
        self.TLabel1_8.configure(foreground="#000000")
        self.TLabel1_8.configure(font="TkDefaultFont")
        self.TLabel1_8.configure(relief="flat")
        self.TLabel1_8.configure(text='''Endereço da câmera:''')

        self.TLabel1_9 = ttk.Label(self.Frame3)
        self.TLabel1_9.place(relx=0.69, rely=0.154, height=19, width=126)
        self.TLabel1_9.configure(background="#d9d9d9")
        self.TLabel1_9.configure(foreground="#000000")
        self.TLabel1_9.configure(font="TkDefaultFont")
        self.TLabel1_9.configure(relief="flat")
        self.TLabel1_9.configure(text='''Dispositivo Bluetooth:''')

        self.Canvas1 = tk.Canvas(top)
        self.Canvas1.place(relx=0.331, rely=0.206, relheight=0.375
                , relwidth=0.254)
        self.Canvas1.configure(background="#d9d9d9")
        self.Canvas1.configure(borderwidth="2")
        self.Canvas1.configure(highlightbackground="#d9d9d9")
        self.Canvas1.configure(highlightcolor="black")
        self.Canvas1.configure(insertbackground="black")
        self.Canvas1.configure(relief="ridge")
        self.Canvas1.configure(selectbackground="#c4c4c4")
        self.Canvas1.configure(selectforeground="black")
        self.Canvas1.bind('<Button-1>',lambda e:tela_support.cliqueCanvas(e))

        self.Frame2 = tk.Frame(top)
        self.Frame2.place(relx=0.8, rely=0.578, relheight=0.477, relwidth=0.202)
        self.Frame2.configure(relief='groove')
        self.Frame2.configure(borderwidth="2")
        self.Frame2.configure(relief="groove")
        self.Frame2.configure(background="#d9d9d9")
        self.Frame2.configure(highlightbackground="#d9d9d9")
        self.Frame2.configure(highlightcolor="black")

        self.Label2_5 = tk.Label(self.Frame2)
        self.Label2_5.place(relx=0.024, rely=0.033, height=21, width=234)
        self.Label2_5.configure(activebackground="#f9f9f9")
        self.Label2_5.configure(activeforeground="black")
        self.Label2_5.configure(background="#d9d9d9")
        self.Label2_5.configure(disabledforeground="#a3a3a3")
        self.Label2_5.configure(font="-family {Segoe UI} -size 11 -weight bold")
        self.Label2_5.configure(foreground="#000000")
        self.Label2_5.configure(highlightbackground="#d9d9d9")
        self.Label2_5.configure(highlightcolor="black")
        self.Label2_5.configure(text='''Config. do ambiente estruturado''')

        self.btnP1 = tk.Button(self.Frame2)
        self.btnP1.place(relx=0.047, rely=0.164, height=24, width=52)
        self.btnP1.configure(activebackground="#ececec")
        self.btnP1.configure(activeforeground="#000000")
        self.btnP1.configure(background="#d9d9d9")
        self.btnP1.configure(disabledforeground="#a3a3a3")
        self.btnP1.configure(foreground="#000000")
        self.btnP1.configure(highlightbackground="#d9d9d9")
        self.btnP1.configure(highlightcolor="black")
        self.btnP1.configure(pady="0")
        self.btnP1.configure(text='''Ponto 1''')

        self.btnP2 = tk.Button(self.Frame2)
        self.btnP2.place(relx=0.275, rely=0.164, height=24, width=52)
        self.btnP2.configure(activebackground="#ececec")
        self.btnP2.configure(activeforeground="#000000")
        self.btnP2.configure(background="#d9d9d9")
        self.btnP2.configure(disabledforeground="#a3a3a3")
        self.btnP2.configure(foreground="#000000")
        self.btnP2.configure(highlightbackground="#d9d9d9")
        self.btnP2.configure(highlightcolor="black")
        self.btnP2.configure(pady="0")
        self.btnP2.configure(text='''Ponto 2''')

        self.btnP3 = tk.Button(self.Frame2)
        self.btnP3.place(relx=0.51, rely=0.164, height=24, width=52)
        self.btnP3.configure(activebackground="#ececec")
        self.btnP3.configure(activeforeground="#000000")
        self.btnP3.configure(background="#d9d9d9")
        self.btnP3.configure(disabledforeground="#a3a3a3")
        self.btnP3.configure(foreground="#000000")
        self.btnP3.configure(highlightbackground="#d9d9d9")
        self.btnP3.configure(highlightcolor="black")
        self.btnP3.configure(pady="0")
        self.btnP3.configure(text='''Ponto 3''')

        self.btnP4 = tk.Button(self.Frame2)
        self.btnP4.place(relx=0.745, rely=0.164, height=24, width=52)
        self.btnP4.configure(activebackground="#ececec")
        self.btnP4.configure(activeforeground="#000000")
        self.btnP4.configure(background="#d9d9d9")
        self.btnP4.configure(disabledforeground="#a3a3a3")
        self.btnP4.configure(foreground="#000000")
        self.btnP4.configure(highlightbackground="#d9d9d9")
        self.btnP4.configure(highlightcolor="black")
        self.btnP4.configure(pady="0")
        self.btnP4.configure(text='''Ponto 4''')

        self.tbDistRealX = tk.Entry(self.Frame2)
        self.tbDistRealX.place(relx=0.647, rely=0.426,height=30, relwidth=0.29)
        self.tbDistRealX.configure(background="white")
        self.tbDistRealX.configure(disabledforeground="#a3a3a3")
        self.tbDistRealX.configure(font="TkFixedFont")
        self.tbDistRealX.configure(foreground="#000000")
        self.tbDistRealX.configure(highlightbackground="#d9d9d9")
        self.tbDistRealX.configure(highlightcolor="black")
        self.tbDistRealX.configure(insertbackground="black")
        self.tbDistRealX.configure(selectbackground="#c4c4c4")
        self.tbDistRealX.configure(selectforeground="black")
        self.tbDistRealX.configure(textvariable=tela_support.distRealX)

        self.TLabel1_10 = ttk.Label(self.Frame2)
        self.TLabel1_10.place(relx=0.071, rely=0.426, height=29, width=136)
        self.TLabel1_10.configure(background="#d9d9d9")
        self.TLabel1_10.configure(foreground="#000000")
        self.TLabel1_10.configure(font="TkDefaultFont")
        self.TLabel1_10.configure(relief="flat")
        self.TLabel1_10.configure(text='''Comprimento em X (cm)''')

        self.TLabel1_2 = ttk.Label(self.Frame2)
        self.TLabel1_2.place(relx=0.078, rely=0.525, height=29, width=126)
        self.TLabel1_2.configure(background="#d9d9d9")
        self.TLabel1_2.configure(foreground="#000000")
        self.TLabel1_2.configure(font="TkDefaultFont")
        self.TLabel1_2.configure(relief="flat")
        self.TLabel1_2.configure(text='''Largura em Y (cm)''')

        self.tbDistRealY = tk.Entry(self.Frame2)
        self.tbDistRealY.place(relx=0.651, rely=0.525,height=30, relwidth=0.29)
        self.tbDistRealY.configure(background="white")
        self.tbDistRealY.configure(disabledforeground="#a3a3a3")
        self.tbDistRealY.configure(font="TkFixedFont")
        self.tbDistRealY.configure(foreground="#000000")
        self.tbDistRealY.configure(highlightbackground="#d9d9d9")
        self.tbDistRealY.configure(highlightcolor="black")
        self.tbDistRealY.configure(insertbackground="black")
        self.tbDistRealY.configure(selectbackground="#c4c4c4")
        self.tbDistRealY.configure(selectforeground="black")
        self.tbDistRealY.configure(textvariable=tela_support.distRealY)

        self.btnAlterarAmbiente = tk.Button(self.Frame2)
        self.btnAlterarAmbiente.place(relx=0.078, rely=0.754, height=34
                , width=222)
        self.btnAlterarAmbiente.configure(activebackground="#ececec")
        self.btnAlterarAmbiente.configure(activeforeground="#000000")
        self.btnAlterarAmbiente.configure(background="#d9d9d9")
        self.btnAlterarAmbiente.configure(disabledforeground="#a3a3a3")
        self.btnAlterarAmbiente.configure(foreground="#000000")
        self.btnAlterarAmbiente.configure(highlightbackground="#d9d9d9")
        self.btnAlterarAmbiente.configure(highlightcolor="black")
        self.btnAlterarAmbiente.configure(pady="0")
        self.btnAlterarAmbiente.configure(text='''Alterar''')

        self.btnVerPontos = tk.Button(self.Frame2)
        self.btnVerPontos.place(relx=0.275, rely=0.295, height=24, width=132)
        self.btnVerPontos.configure(activebackground="#ececec")
        self.btnVerPontos.configure(activeforeground="#000000")
        self.btnVerPontos.configure(background="#d9d9d9")
        self.btnVerPontos.configure(disabledforeground="#a3a3a3")
        self.btnVerPontos.configure(foreground="#000000")
        self.btnVerPontos.configure(highlightbackground="#d9d9d9")
        self.btnVerPontos.configure(highlightcolor="black")
        self.btnVerPontos.configure(pady="0")
        self.btnVerPontos.configure(text='''Ver pontos''')

        self.Frame2_4 = tk.Frame(top)
        self.Frame2_4.place(relx=0.602, rely=0.016, relheight=0.383
                , relwidth=0.194)
        self.Frame2_4.configure(relief='groove')
        self.Frame2_4.configure(borderwidth="2")
        self.Frame2_4.configure(relief="groove")
        self.Frame2_4.configure(background="#d9d9d9")
        self.Frame2_4.configure(highlightbackground="#d9d9d9")
        self.Frame2_4.configure(highlightcolor="black")

        self.Label2_6 = tk.Label(self.Frame2_4)
        self.Label2_6.place(relx=0.041, rely=0.041, height=21, width=224)
        self.Label2_6.configure(activebackground="#f9f9f9")
        self.Label2_6.configure(activeforeground="black")
        self.Label2_6.configure(background="#d9d9d9")
        self.Label2_6.configure(disabledforeground="#a3a3a3")
        self.Label2_6.configure(font="-family {Segoe UI} -size 11 -weight bold")
        self.Label2_6.configure(foreground="#000000")
        self.Label2_6.configure(highlightbackground="#d9d9d9")
        self.Label2_6.configure(highlightcolor="black")
        self.Label2_6.configure(text='''Configuração dos controladores''')

        self.TLabel1_4 = ttk.Label(self.Frame2_4)
        self.TLabel1_4.place(relx=0.041, rely=0.286, height=19, width=26)
        self.TLabel1_4.configure(background="#d9d9d9")
        self.TLabel1_4.configure(foreground="#000000")
        self.TLabel1_4.configure(font="TkDefaultFont")
        self.TLabel1_4.configure(relief="flat")
        self.TLabel1_4.configure(text='''K1''')

        self.TLabel1_1 = ttk.Label(self.Frame2_4)
        self.TLabel1_1.place(relx=0.041, rely=0.367, height=19, width=26)
        self.TLabel1_1.configure(background="#d9d9d9")
        self.TLabel1_1.configure(foreground="#000000")
        self.TLabel1_1.configure(font="TkDefaultFont")
        self.TLabel1_1.configure(relief="flat")
        self.TLabel1_1.configure(text='''K2''')

        self.tbK1 = tk.Entry(self.Frame2_4)
        self.tbK1.place(relx=0.163, rely=0.286,height=20, relwidth=0.302)
        self.tbK1.configure(background="white")
        self.tbK1.configure(disabledforeground="#a3a3a3")
        self.tbK1.configure(font="TkFixedFont")
        self.tbK1.configure(foreground="#000000")
        self.tbK1.configure(highlightbackground="#d9d9d9")
        self.tbK1.configure(highlightcolor="black")
        self.tbK1.configure(insertbackground="black")
        self.tbK1.configure(selectbackground="#c4c4c4")
        self.tbK1.configure(selectforeground="black")
        self.tbK1.configure(textvariable=tela_support.k1)

        self.tbK2 = tk.Entry(self.Frame2_4)
        self.tbK2.place(relx=0.163, rely=0.367,height=20, relwidth=0.302)
        self.tbK2.configure(background="white")
        self.tbK2.configure(disabledforeground="#a3a3a3")
        self.tbK2.configure(font="TkFixedFont")
        self.tbK2.configure(foreground="#000000")
        self.tbK2.configure(highlightbackground="#d9d9d9")
        self.tbK2.configure(highlightcolor="black")
        self.tbK2.configure(insertbackground="black")
        self.tbK2.configure(selectbackground="#c4c4c4")
        self.tbK2.configure(selectforeground="black")
        self.tbK2.configure(textvariable=tela_support.k2)

        self.tbK3 = tk.Entry(self.Frame2_4)
        self.tbK3.place(relx=0.163, rely=0.449,height=20, relwidth=0.302)
        self.tbK3.configure(background="white")
        self.tbK3.configure(disabledforeground="#a3a3a3")
        self.tbK3.configure(font="TkFixedFont")
        self.tbK3.configure(foreground="#000000")
        self.tbK3.configure(highlightbackground="#d9d9d9")
        self.tbK3.configure(highlightcolor="black")
        self.tbK3.configure(insertbackground="black")
        self.tbK3.configure(selectbackground="#c4c4c4")
        self.tbK3.configure(selectforeground="black")
        self.tbK3.configure(textvariable=tela_support.k3)

        self.tbK4 = tk.Entry(self.Frame2_4)
        self.tbK4.place(relx=0.163, rely=0.531,height=20, relwidth=0.302)
        self.tbK4.configure(background="white")
        self.tbK4.configure(disabledforeground="#a3a3a3")
        self.tbK4.configure(font="TkFixedFont")
        self.tbK4.configure(foreground="#000000")
        self.tbK4.configure(highlightbackground="#d9d9d9")
        self.tbK4.configure(highlightcolor="black")
        self.tbK4.configure(insertbackground="black")
        self.tbK4.configure(selectbackground="#c4c4c4")
        self.tbK4.configure(selectforeground="black")
        self.tbK4.configure(textvariable=tela_support.k4)

        self.TLabel1_3 = ttk.Label(self.Frame2_4)
        self.TLabel1_3.place(relx=0.041, rely=0.449, height=19, width=26)
        self.TLabel1_3.configure(background="#d9d9d9")
        self.TLabel1_3.configure(foreground="#000000")
        self.TLabel1_3.configure(font="TkDefaultFont")
        self.TLabel1_3.configure(relief="flat")
        self.TLabel1_3.configure(text='''K3''')

        self.TLabel1_5 = ttk.Label(self.Frame2_4)
        self.TLabel1_5.place(relx=0.041, rely=0.531, height=19, width=26)
        self.TLabel1_5.configure(background="#d9d9d9")
        self.TLabel1_5.configure(foreground="#000000")
        self.TLabel1_5.configure(font="TkDefaultFont")
        self.TLabel1_5.configure(relief="flat")
        self.TLabel1_5.configure(text='''K4''')

        self.TLabel1_6 = ttk.Label(self.Frame2_4)
        self.TLabel1_6.place(relx=0.163, rely=0.163, height=19, width=76)
        self.TLabel1_6.configure(background="#d9d9d9")
        self.TLabel1_6.configure(foreground="#000000")
        self.TLabel1_6.configure(font="TkDefaultFont")
        self.TLabel1_6.configure(relief="flat")
        self.TLabel1_6.configure(text='''Pitch e Roll''')

        self.TLabel1_7 = ttk.Label(self.Frame2_4)
        self.TLabel1_7.place(relx=0.502, rely=0.159, height=19, width=116)
        self.TLabel1_7.configure(background="#d9d9d9")
        self.TLabel1_7.configure(foreground="#000000")
        self.TLabel1_7.configure(font="TkDefaultFont")
        self.TLabel1_7.configure(relief="flat")
        self.TLabel1_7.configure(text='''Controle de Guinada''')

        self.TLabel1_9 = ttk.Label(self.Frame2_4)
        self.TLabel1_9.place(relx=0.494, rely=0.286, height=19, width=36)
        self.TLabel1_9.configure(background="#d9d9d9")
        self.TLabel1_9.configure(foreground="#000000")
        self.TLabel1_9.configure(font="TkDefaultFont")
        self.TLabel1_9.configure(relief="flat")
        self.TLabel1_9.configure(text='''Kp''')

        self.tbKpyaw = tk.Entry(self.Frame2_4)
        self.tbKpyaw.place(relx=0.629, rely=0.286,height=20, relwidth=0.302)
        self.tbKpyaw.configure(background="white")
        self.tbKpyaw.configure(disabledforeground="#a3a3a3")
        self.tbKpyaw.configure(font="TkFixedFont")
        self.tbKpyaw.configure(foreground="#000000")
        self.tbKpyaw.configure(highlightbackground="#d9d9d9")
        self.tbKpyaw.configure(highlightcolor="black")
        self.tbKpyaw.configure(insertbackground="black")
        self.tbKpyaw.configure(selectbackground="#c4c4c4")
        self.tbKpyaw.configure(selectforeground="black")
        self.tbKpyaw.configure(textvariable=tela_support.kpgui)

        self.TLabel1_6 = ttk.Label(self.Frame2_4)
        self.TLabel1_6.place(relx=0.494, rely=0.367, height=19, width=26)
        self.TLabel1_6.configure(background="#d9d9d9")
        self.TLabel1_6.configure(foreground="#000000")
        self.TLabel1_6.configure(font="TkDefaultFont")
        self.TLabel1_6.configure(relief="flat")
        self.TLabel1_6.configure(text='''Ki''')

        self.tbKiyaw = tk.Entry(self.Frame2_4)
        self.tbKiyaw.place(relx=0.629, rely=0.376,height=20, relwidth=0.302)
        self.tbKiyaw.configure(background="white")
        self.tbKiyaw.configure(disabledforeground="#a3a3a3")
        self.tbKiyaw.configure(font="TkFixedFont")
        self.tbKiyaw.configure(foreground="#000000")
        self.tbKiyaw.configure(highlightbackground="#d9d9d9")
        self.tbKiyaw.configure(highlightcolor="black")
        self.tbKiyaw.configure(insertbackground="black")
        self.tbKiyaw.configure(selectbackground="#c4c4c4")
        self.tbKiyaw.configure(selectforeground="black")
        self.tbKiyaw.configure(textvariable=tela_support.kigui)

        self.btnAlterarGanhos = tk.Button(self.Frame2_4)
        self.btnAlterarGanhos.place(relx=0.547, rely=0.853, height=24, width=77)
        self.btnAlterarGanhos.configure(activebackground="#ececec")
        self.btnAlterarGanhos.configure(activeforeground="#000000")
        self.btnAlterarGanhos.configure(background="#d9d9d9")
        self.btnAlterarGanhos.configure(disabledforeground="#a3a3a3")
        self.btnAlterarGanhos.configure(foreground="#000000")
        self.btnAlterarGanhos.configure(highlightbackground="#d9d9d9")
        self.btnAlterarGanhos.configure(highlightcolor="black")
        self.btnAlterarGanhos.configure(pady="0")
        self.btnAlterarGanhos.configure(text='''Alterar''')

        self.cbHabMotores = tk.Checkbutton(self.Frame2_4)
        self.cbHabMotores.place(relx=0.286, rely=0.735, relheight=0.102
                , relwidth=0.453)
        self.cbHabMotores.configure(activebackground="#ececec")
        self.cbHabMotores.configure(activeforeground="#000000")
        self.cbHabMotores.configure(background="#d9d9d9")
        self.cbHabMotores.configure(disabledforeground="#a3a3a3")
        self.cbHabMotores.configure(foreground="#000000")
        self.cbHabMotores.configure(highlightbackground="#d9d9d9")
        self.cbHabMotores.configure(highlightcolor="black")
        self.cbHabMotores.configure(justify='left')
        self.cbHabMotores.configure(text='''Habilitar Motores''')
        self.cbHabMotores.configure(variable=tela_support.cbHabMotoresValue)

        self.btnLerGanhos = tk.Button(self.Frame2_4)
        self.btnLerGanhos.place(relx=0.135, rely=0.853, height=24, width=77)
        self.btnLerGanhos.configure(activebackground="#ececec")
        self.btnLerGanhos.configure(activeforeground="#000000")
        self.btnLerGanhos.configure(background="#d9d9d9")
        self.btnLerGanhos.configure(disabledforeground="#a3a3a3")
        self.btnLerGanhos.configure(foreground="#000000")
        self.btnLerGanhos.configure(highlightbackground="#d9d9d9")
        self.btnLerGanhos.configure(highlightcolor="black")
        self.btnLerGanhos.configure(pady="0")
        self.btnLerGanhos.configure(text='''Ler ganhos''')

        self.cbHabMotores_17 = tk.Checkbutton(self.Frame2_4)
        self.cbHabMotores_17.place(relx=0.065, rely=0.612, relheight=0.102
                , relwidth=0.453)
        self.cbHabMotores_17.configure(activebackground="#ececec")
        self.cbHabMotores_17.configure(activeforeground="#000000")
        self.cbHabMotores_17.configure(background="#d9d9d9")
        self.cbHabMotores_17.configure(disabledforeground="#a3a3a3")
        self.cbHabMotores_17.configure(foreground="#000000")
        self.cbHabMotores_17.configure(highlightbackground="#d9d9d9")
        self.cbHabMotores_17.configure(highlightcolor="black")
        self.cbHabMotores_17.configure(justify='left')
        self.cbHabMotores_17.configure(text='''[0] Pos [1] Vel.''')
        self.cbHabMotores_17.configure(variable=tela_support.cbPosVelLQR)

        self.cbHabMotores_18 = tk.Checkbutton(self.Frame2_4)
        self.cbHabMotores_18.place(relx=0.531, rely=0.612, relheight=0.102
                , relwidth=0.453)
        self.cbHabMotores_18.configure(activebackground="#ececec")
        self.cbHabMotores_18.configure(activeforeground="#000000")
        self.cbHabMotores_18.configure(background="#d9d9d9")
        self.cbHabMotores_18.configure(disabledforeground="#a3a3a3")
        self.cbHabMotores_18.configure(foreground="#000000")
        self.cbHabMotores_18.configure(highlightbackground="#d9d9d9")
        self.cbHabMotores_18.configure(highlightcolor="black")
        self.cbHabMotores_18.configure(justify='left')
        self.cbHabMotores_18.configure(text='''[0] Pos [1] Vel.''')
        self.cbHabMotores_18.configure(variable=tela_support.cbPosVelGuinada)

        self.Frame4 = tk.Frame(top)
        self.Frame4.place(relx=0.602, rely=0.406, relheight=0.289
                , relwidth=0.194)
        self.Frame4.configure(relief='groove')
        self.Frame4.configure(borderwidth="2")
        self.Frame4.configure(relief="groove")
        self.Frame4.configure(background="#d9d9d9")
        self.Frame4.configure(highlightbackground="#d9d9d9")
        self.Frame4.configure(highlightcolor="black")

        self.Label2_7 = tk.Label(self.Frame4)
        self.Label2_7.place(relx=0.033, rely=0.054, height=21, width=74)
        self.Label2_7.configure(activebackground="#f9f9f9")
        self.Label2_7.configure(activeforeground="black")
        self.Label2_7.configure(background="#d9d9d9")
        self.Label2_7.configure(disabledforeground="#a3a3a3")
        self.Label2_7.configure(font="-family {Segoe UI} -size 11 -weight bold")
        self.Label2_7.configure(foreground="#000000")
        self.Label2_7.configure(highlightbackground="#d9d9d9")
        self.Label2_7.configure(highlightcolor="black")
        self.Label2_7.configure(text='''Guinada''')

        self.btnCalibrarBussola = tk.Button(self.Frame4)
        self.btnCalibrarBussola.place(relx=0.531, rely=0.27, height=24, width=97)

        self.btnCalibrarBussola.configure(activebackground="#ececec")
        self.btnCalibrarBussola.configure(activeforeground="#000000")
        self.btnCalibrarBussola.configure(background="#d9d9d9")
        self.btnCalibrarBussola.configure(disabledforeground="#a3a3a3")
        self.btnCalibrarBussola.configure(foreground="#000000")
        self.btnCalibrarBussola.configure(highlightbackground="#d9d9d9")
        self.btnCalibrarBussola.configure(highlightcolor="black")
        self.btnCalibrarBussola.configure(pady="0")
        self.btnCalibrarBussola.configure(text='''Calibrar bússola''')

        self.sliderGuinada = tk.Scale(self.Frame4, from_=0.0, to=360.0)
        self.sliderGuinada.place(relx=0.041, rely=0.162, relwidth=0.433
                , relheight=0.0, height=42, bordermode='ignore')
        self.sliderGuinada.configure(activebackground="#ececec")
        self.sliderGuinada.configure(background="#d9d9d9")
        self.sliderGuinada.configure(foreground="#000000")
        self.sliderGuinada.configure(highlightbackground="#d9d9d9")
        self.sliderGuinada.configure(highlightcolor="black")
        self.sliderGuinada.configure(orient="horizontal")
        self.sliderGuinada.configure(troughcolor="#d9d9d9")

        self.cbControleGuinada = tk.Checkbutton(self.Frame4)
        self.cbControleGuinada.place(relx=0.327, rely=0.054, relheight=0.135
                , relwidth=0.608)
        self.cbControleGuinada.configure(activebackground="#ececec")
        self.cbControleGuinada.configure(activeforeground="#000000")
        self.cbControleGuinada.configure(background="#d9d9d9")
        self.cbControleGuinada.configure(disabledforeground="#a3a3a3")
        self.cbControleGuinada.configure(foreground="#000000")
        self.cbControleGuinada.configure(highlightbackground="#d9d9d9")
        self.cbControleGuinada.configure(highlightcolor="black")
        self.cbControleGuinada.configure(justify='left')
        self.cbControleGuinada.configure(text='''Hab. Controle Guinada''')
        self.cbControleGuinada.configure(variable=tela_support.cbControleGuinadaValue)

        self.btnManualGuiAntiHorario = tk.Button(self.Frame4)
        self.btnManualGuiAntiHorario.place(relx=0.163, rely=0.827, height=24
                , width=47)
        self.btnManualGuiAntiHorario.configure(activebackground="#ececec")
        self.btnManualGuiAntiHorario.configure(activeforeground="#000000")
        self.btnManualGuiAntiHorario.configure(background="#d9d9d9")
        self.btnManualGuiAntiHorario.configure(disabledforeground="#a3a3a3")
        self.btnManualGuiAntiHorario.configure(foreground="#000000")
        self.btnManualGuiAntiHorario.configure(highlightbackground="#d9d9d9")
        self.btnManualGuiAntiHorario.configure(highlightcolor="black")
        self.btnManualGuiAntiHorario.configure(pady="0")
        self.btnManualGuiAntiHorario.configure(text='''<-''')

        self.btnManualGuiParar = tk.Button(self.Frame4)
        self.btnManualGuiParar.place(relx=0.367, rely=0.827, height=24, width=47)

        self.btnManualGuiParar.configure(activebackground="#ececec")
        self.btnManualGuiParar.configure(activeforeground="#000000")
        self.btnManualGuiParar.configure(background="#d9d9d9")
        self.btnManualGuiParar.configure(disabledforeground="#a3a3a3")
        self.btnManualGuiParar.configure(foreground="#000000")
        self.btnManualGuiParar.configure(highlightbackground="#d9d9d9")
        self.btnManualGuiParar.configure(highlightcolor="black")
        self.btnManualGuiParar.configure(pady="0")
        self.btnManualGuiParar.configure(text='''O''')

        self.btnManualGuiHorario = tk.Button(self.Frame4)
        self.btnManualGuiHorario.place(relx=0.571, rely=0.827, height=24
                , width=47)
        self.btnManualGuiHorario.configure(activebackground="#ececec")
        self.btnManualGuiHorario.configure(activeforeground="#000000")
        self.btnManualGuiHorario.configure(background="#d9d9d9")
        self.btnManualGuiHorario.configure(disabledforeground="#a3a3a3")
        self.btnManualGuiHorario.configure(foreground="#000000")
        self.btnManualGuiHorario.configure(highlightbackground="#d9d9d9")
        self.btnManualGuiHorario.configure(highlightcolor="black")
        self.btnManualGuiHorario.configure(pady="0")
        self.btnManualGuiHorario.configure(text='''->''')

        self.btnAlterarNorte = tk.Button(self.Frame4)
        self.btnAlterarNorte.place(relx=0.531, rely=0.551, height=24, width=97)
        self.btnAlterarNorte.configure(activebackground="#ececec")
        self.btnAlterarNorte.configure(activeforeground="#000000")
        self.btnAlterarNorte.configure(background="#d9d9d9")
        self.btnAlterarNorte.configure(disabledforeground="#a3a3a3")
        self.btnAlterarNorte.configure(foreground="#000000")
        self.btnAlterarNorte.configure(highlightbackground="#d9d9d9")
        self.btnAlterarNorte.configure(highlightcolor="black")
        self.btnAlterarNorte.configure(pady="0")
        self.btnAlterarNorte.configure(text='''Alterar''')

        self.TLabel1_7 = ttk.Label(self.Frame4)
        self.TLabel1_7.place(relx=0.082, rely=0.432, height=19, width=116)
        self.TLabel1_7.configure(background="#d9d9d9")
        self.TLabel1_7.configure(foreground="#000000")
        self.TLabel1_7.configure(font="TkDefaultFont")
        self.TLabel1_7.configure(relief="flat")
        self.TLabel1_7.configure(text='''Orientação Norte (º)''')

        self.lbOrientacaoNorte = ttk.Label(self.Frame4)
        self.lbOrientacaoNorte.place(relx=0.204, rely=0.562, height=19, width=56)

        self.lbOrientacaoNorte.configure(background="#d9d9d9")
        self.lbOrientacaoNorte.configure(foreground="#000000")
        self.lbOrientacaoNorte.configure(font="-family {Segoe UI} -size 10")
        self.lbOrientacaoNorte.configure(relief="flat")
        self.lbOrientacaoNorte.configure(text='''0''')

        self.TLabel1_8 = ttk.Label(self.Frame4)
        self.TLabel1_8.place(relx=0.286, rely=0.703, height=19, width=96)
        self.TLabel1_8.configure(background="#d9d9d9")
        self.TLabel1_8.configure(foreground="#000000")
        self.TLabel1_8.configure(font="TkDefaultFont")
        self.TLabel1_8.configure(relief="flat")
        self.TLabel1_8.configure(text='''Guinada manual''')

        self.btnTrajetoria = tk.Button(top)
        self.btnTrajetoria.place(relx=0.032, rely=0.844, height=44, width=147)
        self.btnTrajetoria.configure(activebackground="#ececec")
        self.btnTrajetoria.configure(activeforeground="#000000")
        self.btnTrajetoria.configure(background="#339933")
        self.btnTrajetoria.configure(disabledforeground="#a3a3a3")
        self.btnTrajetoria.configure(font="-family {Segoe UI} -size 10 -weight bold")
        self.btnTrajetoria.configure(foreground="#ffffff")
        self.btnTrajetoria.configure(highlightbackground="#d9d9d9")
        self.btnTrajetoria.configure(highlightcolor="black")
        self.btnTrajetoria.configure(pady="0")
        self.btnTrajetoria.configure(text='''Iniciar trajetória''')

        self.Frame4_9 = tk.Frame(top)
        self.Frame4_9.place(relx=0.602, rely=0.703, relheight=0.336
                , relwidth=0.194)
        self.Frame4_9.configure(relief='groove')
        self.Frame4_9.configure(borderwidth="2")
        self.Frame4_9.configure(relief="groove")
        self.Frame4_9.configure(background="#d9d9d9")
        self.Frame4_9.configure(highlightbackground="#d9d9d9")
        self.Frame4_9.configure(highlightcolor="black")

        self.Label2_8 = tk.Label(self.Frame4_9)
        self.Label2_8.place(relx=0.041, rely=0.047, height=21, width=154)
        self.Label2_8.configure(activebackground="#f9f9f9")
        self.Label2_8.configure(activeforeground="black")
        self.Label2_8.configure(background="#d9d9d9")
        self.Label2_8.configure(disabledforeground="#a3a3a3")
        self.Label2_8.configure(font="-family {Segoe UI} -size 11 -weight bold")
        self.Label2_8.configure(foreground="#000000")
        self.Label2_8.configure(highlightbackground="#d9d9d9")
        self.Label2_8.configure(highlightcolor="black")
        self.Label2_8.configure(text='''Recepção da Serial''')

        self.tbDadosSerial = tk.Text(self.Frame4_9)
        self.tbDadosSerial.place(relx=0.082, rely=0.186, relheight=0.67
                , relwidth=0.833)
        self.tbDadosSerial.configure(background="white")
        self.tbDadosSerial.configure(font="TkTextFont")
        self.tbDadosSerial.configure(foreground="black")
        self.tbDadosSerial.configure(highlightbackground="#d9d9d9")
        self.tbDadosSerial.configure(highlightcolor="black")
        self.tbDadosSerial.configure(insertbackground="black")
        self.tbDadosSerial.configure(selectbackground="#c4c4c4")
        self.tbDadosSerial.configure(selectforeground="black")
        self.tbDadosSerial.configure(wrap="word")

        self.btnLimparSerial = tk.Button(self.Frame4_9)
        self.btnLimparSerial.place(relx=0.694, rely=0.047, height=24, width=57)
        self.btnLimparSerial.configure(activebackground="#ececec")
        self.btnLimparSerial.configure(activeforeground="#000000")
        self.btnLimparSerial.configure(background="#d9d9d9")
        self.btnLimparSerial.configure(disabledforeground="#a3a3a3")
        self.btnLimparSerial.configure(foreground="#000000")
        self.btnLimparSerial.configure(highlightbackground="#d9d9d9")
        self.btnLimparSerial.configure(highlightcolor="black")
        self.btnLimparSerial.configure(pady="0")
        self.btnLimparSerial.configure(text='''Limpar''')

        self.Label2_9 = tk.Label(top)
        self.Label2_9.place(relx=0.396, rely=0.844, height=21, width=204)
        self.Label2_9.configure(activebackground="#f9f9f9")
        self.Label2_9.configure(activeforeground="black")
        self.Label2_9.configure(background="#d9d9d9")
        self.Label2_9.configure(disabledforeground="#a3a3a3")
        self.Label2_9.configure(font="-family {Segoe UI} -size 11 -slant italic")
        self.Label2_9.configure(foreground="#000000")
        self.Label2_9.configure(highlightbackground="#d9d9d9")
        self.Label2_9.configure(highlightcolor="black")
        self.Label2_9.configure(text='''Desenvolvido: Pedro H.Jesus''')

        self.Label2_10 = tk.Label(top)
        self.Label2_10.place(relx=0.349, rely=0.875, height=31, width=304)
        self.Label2_10.configure(activebackground="#f9f9f9")
        self.Label2_10.configure(activeforeground="black")
        self.Label2_10.configure(background="#d9d9d9")
        self.Label2_10.configure(disabledforeground="#a3a3a3")
        self.Label2_10.configure(font="-family {Segoe UI} -size 11 -slant italic")
        self.Label2_10.configure(foreground="#000000")
        self.Label2_10.configure(highlightbackground="#d9d9d9")
        self.Label2_10.configure(highlightcolor="black")
        self.Label2_10.configure(text='''Orientador: Prof. Dr. Cairo L. Nascimento Jr.''')

        self.lbLogoITA = tk.Label(top)
        self.lbLogoITA.place(relx=0.174, rely=0.844, height=61, width=164)
        self.lbLogoITA.configure(activebackground="#f9f9f9")
        self.lbLogoITA.configure(activeforeground="black")
        self.lbLogoITA.configure(background="#d9d9d9")
        self.lbLogoITA.configure(disabledforeground="#a3a3a3")
        self.lbLogoITA.configure(foreground="#000000")
        self.lbLogoITA.configure(highlightbackground="#d9d9d9")
        self.lbLogoITA.configure(highlightcolor="black")
        self.lbLogoITA.configure(text='''logo''')

        self.Canvas2 = tk.Canvas(top)
        self.Canvas2.place(relx=0.192, rely=0.252, relheight=0.313
                , relwidth=0.119)
        self.Canvas2.configure(background="#d9d9d9")
        self.Canvas2.configure(borderwidth="2")
        self.Canvas2.configure(highlightbackground="#d9d9d9")
        self.Canvas2.configure(highlightcolor="black")
        self.Canvas2.configure(insertbackground="black")
        self.Canvas2.configure(relief="ridge")
        self.Canvas2.configure(selectbackground="#c4c4c4")
        self.Canvas2.configure(selectforeground="black")

        self.TLabel1_11 = ttk.Label(top)
        self.TLabel1_11.place(relx=0.42, rely=0.173, height=19, width=126)
        self.TLabel1_11.configure(background="#d9d9d9")
        self.TLabel1_11.configure(foreground="#000000")
        self.TLabel1_11.configure(font="TkDefaultFont")
        self.TLabel1_11.configure(relief="flat")
        self.TLabel1_11.configure(text='''Imagem da Câmera''')

        self.TLabel1_9 = ttk.Label(top)
        self.TLabel1_9.place(relx=0.097, rely=0.197, height=19, width=186)
        self.TLabel1_9.configure(background="#d9d9d9")
        self.TLabel1_9.configure(foreground="#000000")
        self.TLabel1_9.configure(font="TkDefaultFont")
        self.TLabel1_9.configure(relief="flat")
        self.TLabel1_9.configure(text='''Sistema de Localização do Ballbot''')

        self.TSeparator1 = ttk.Separator(top)
        self.TSeparator1.place(relx=0.04, rely=1.03, relwidth=0.531)

        self.Label2_11 = tk.Label(top)
        self.Label2_11.place(relx=0.325, rely=0.922, height=21, width=334)
        self.Label2_11.configure(activebackground="#f9f9f9")
        self.Label2_11.configure(activeforeground="black")
        self.Label2_11.configure(background="#d9d9d9")
        self.Label2_11.configure(disabledforeground="#a3a3a3")
        self.Label2_11.configure(font="-family {Segoe UI} -size 11 -slant italic")
        self.Label2_11.configure(foreground="#000000")
        self.Label2_11.configure(highlightbackground="#d9d9d9")
        self.Label2_11.configure(highlightcolor="black")
        self.Label2_11.configure(text='''Coorientador: Prof. Dr. Douglas Soares dos Santos''')

        self.Frame5_12 = tk.Frame(top)
        self.Frame5_12.place(relx=0.341, rely=0.609, relheight=0.211
                , relwidth=0.25)
        self.Frame5_12.configure(relief='groove')
        self.Frame5_12.configure(borderwidth="2")
        self.Frame5_12.configure(relief="groove")
        self.Frame5_12.configure(background="#d9d9d9")
        self.Frame5_12.configure(highlightbackground="#d9d9d9")
        self.Frame5_12.configure(highlightcolor="black")

        self.btnManualParar = tk.Button(self.Frame5_12)
        self.btnManualParar.place(relx=0.238, rely=0.519, height=24, width=47)
        self.btnManualParar.configure(activebackground="#ececec")
        self.btnManualParar.configure(activeforeground="#000000")
        self.btnManualParar.configure(background="#d9d9d9")
        self.btnManualParar.configure(disabledforeground="#a3a3a3")
        self.btnManualParar.configure(foreground="#000000")
        self.btnManualParar.configure(highlightbackground="#d9d9d9")
        self.btnManualParar.configure(highlightcolor="black")
        self.btnManualParar.configure(pady="0")
        self.btnManualParar.configure(text='''O''')

        self.btnManualDir = tk.Button(self.Frame5_12)
        self.btnManualDir.place(relx=0.387, rely=0.519, height=24, width=47)
        self.btnManualDir.configure(activebackground="#ececec")
        self.btnManualDir.configure(activeforeground="#000000")
        self.btnManualDir.configure(background="#d9d9d9")
        self.btnManualDir.configure(disabledforeground="#a3a3a3")
        self.btnManualDir.configure(font="-family {Segoe UI} -size 9")
        self.btnManualDir.configure(foreground="#000000")
        self.btnManualDir.configure(highlightbackground="#d9d9d9")
        self.btnManualDir.configure(highlightcolor="black")
        self.btnManualDir.configure(pady="0")
        self.btnManualDir.configure(text='''>''')

        self.btnManualEsq = tk.Button(self.Frame5_12)
        self.btnManualEsq.place(relx=0.089, rely=0.519, height=24, width=47)
        self.btnManualEsq.configure(activebackground="#ececec")
        self.btnManualEsq.configure(activeforeground="#000000")
        self.btnManualEsq.configure(background="#d9d9d9")
        self.btnManualEsq.configure(disabledforeground="#a3a3a3")
        self.btnManualEsq.configure(foreground="#000000")
        self.btnManualEsq.configure(highlightbackground="#d9d9d9")
        self.btnManualEsq.configure(highlightcolor="black")
        self.btnManualEsq.configure(pady="0")
        self.btnManualEsq.configure(text='''<''')

        self.btnManualCima = tk.Button(self.Frame5_12)
        self.btnManualCima.place(relx=0.238, rely=0.341, height=24, width=47)
        self.btnManualCima.configure(activebackground="#ececec")
        self.btnManualCima.configure(activeforeground="#000000")
        self.btnManualCima.configure(background="#d9d9d9")
        self.btnManualCima.configure(disabledforeground="#a3a3a3")
        self.btnManualCima.configure(font="-family {Segoe UI} -size 9")
        self.btnManualCima.configure(foreground="#000000")
        self.btnManualCima.configure(highlightbackground="#d9d9d9")
        self.btnManualCima.configure(highlightcolor="black")
        self.btnManualCima.configure(pady="0")
        self.btnManualCima.configure(text='''△''')

        self.btnManualBaixo = tk.Button(self.Frame5_12)
        self.btnManualBaixo.place(relx=0.238, rely=0.689, height=24, width=47)
        self.btnManualBaixo.configure(activebackground="#ececec")
        self.btnManualBaixo.configure(activeforeground="#000000")
        self.btnManualBaixo.configure(background="#d9d9d9")
        self.btnManualBaixo.configure(disabledforeground="#a3a3a3")
        self.btnManualBaixo.configure(foreground="#000000")
        self.btnManualBaixo.configure(highlightbackground="#d9d9d9")
        self.btnManualBaixo.configure(highlightcolor="black")
        self.btnManualBaixo.configure(pady="0")
        self.btnManualBaixo.configure(text='''▽''')

        self.sliderVelocidade = tk.Scale(self.Frame5_12, from_=0.0, to=360.0)
        self.sliderVelocidade.place(relx=0.603, rely=0.444, relwidth=0.337
                , relheight=0.0, height=42, bordermode='ignore')
        self.sliderVelocidade.configure(activebackground="#ececec")
        self.sliderVelocidade.configure(background="#d9d9d9")
        self.sliderVelocidade.configure(foreground="#000000")
        self.sliderVelocidade.configure(highlightbackground="#d9d9d9")
        self.sliderVelocidade.configure(highlightcolor="black")
        self.sliderVelocidade.configure(orient="horizontal")
        self.sliderVelocidade.configure(troughcolor="#d9d9d9")

        self.TLabel1_10 = ttk.Label(self.Frame5_12)
        self.TLabel1_10.place(relx=0.508, rely=0.296, height=19, width=136)
        self.TLabel1_10.configure(background="#d9d9d9")
        self.TLabel1_10.configure(foreground="#000000")
        self.TLabel1_10.configure(font="TkDefaultFont")
        self.TLabel1_10.configure(relief="flat")
        self.TLabel1_10.configure(text='''Velocidade de translação''')

        self.Label2_17 = tk.Label(self.Frame5_12)
        self.Label2_17.place(relx=0.032, rely=0.015, height=21, width=134)
        self.Label2_17.configure(activebackground="#f9f9f9")
        self.Label2_17.configure(activeforeground="black")
        self.Label2_17.configure(background="#d9d9d9")
        self.Label2_17.configure(disabledforeground="#a3a3a3")
        self.Label2_17.configure(font="-family {Segoe UI} -size 11 -weight bold")
        self.Label2_17.configure(foreground="#000000")
        self.Label2_17.configure(highlightbackground="#d9d9d9")
        self.Label2_17.configure(highlightcolor="black")
        self.Label2_17.configure(text='''Controle Manual''')

        self.Frame5_10 = tk.Frame(top)
        self.Frame5_10.place(relx=0.8, rely=0.484, relheight=0.086
                , relwidth=0.202)
        self.Frame5_10.configure(relief='groove')
        self.Frame5_10.configure(borderwidth="2")
        self.Frame5_10.configure(relief="groove")
        self.Frame5_10.configure(background="#d9d9d9")
        self.Frame5_10.configure(highlightbackground="#d9d9d9")
        self.Frame5_10.configure(highlightcolor="black")

        self.Label2_12 = tk.Label(self.Frame5_10)
        self.Label2_12.place(relx=0.039, rely=0.364, height=21, width=124)
        self.Label2_12.configure(activebackground="#f9f9f9")
        self.Label2_12.configure(activeforeground="black")
        self.Label2_12.configure(background="#d9d9d9")
        self.Label2_12.configure(disabledforeground="#a3a3a3")
        self.Label2_12.configure(font="-family {Segoe UI} -size 11 -weight bold")
        self.Label2_12.configure(foreground="#000000")
        self.Label2_12.configure(highlightbackground="#d9d9d9")
        self.Label2_12.configure(highlightcolor="black")
        self.Label2_12.configure(text='''Telemetria''')

        self.btnIniciarTelemetria = tk.Button(self.Frame5_10)
        self.btnIniciarTelemetria.place(relx=0.549, rely=0.364, height=24
                , width=87)
        self.btnIniciarTelemetria.configure(activebackground="#ececec")
        self.btnIniciarTelemetria.configure(activeforeground="#000000")
        self.btnIniciarTelemetria.configure(background="#d9d9d9")
        self.btnIniciarTelemetria.configure(disabledforeground="#a3a3a3")
        self.btnIniciarTelemetria.configure(foreground="#000000")
        self.btnIniciarTelemetria.configure(highlightbackground="#d9d9d9")
        self.btnIniciarTelemetria.configure(highlightcolor="black")
        self.btnIniciarTelemetria.configure(pady="0")
        self.btnIniciarTelemetria.configure(text='''Iniciar''')

        self.menubar = tk.Menu(top,font=font9,bg=_bgcolor,fg=_fgcolor)
        top.configure(menu = self.menubar)

        self.Frame5 = tk.Frame(top)
        self.Frame5.place(relx=0.024, rely=0.259, relheight=0.305
                , relwidth=0.147)
        self.Frame5.configure(relief='groove')
        self.Frame5.configure(borderwidth="2")
        self.Frame5.configure(relief="groove")
        self.Frame5.configure(background="#d9d9d9")
        self.Frame5.configure(highlightbackground="#d9d9d9")
        self.Frame5.configure(highlightcolor="black")

        self.TLabel1_10 = ttk.Label(self.Frame5)
        self.TLabel1_10.place(relx=0.059, rely=0.031, height=19, width=106)
        self.TLabel1_10.configure(background="#d9d9d9")
        self.TLabel1_10.configure(foreground="#000000")
        self.TLabel1_10.configure(font="-family {Segoe UI} -size 10 -weight bold")
        self.TLabel1_10.configure(relief="flat")
        self.TLabel1_10.configure(text='''Posição X,Y [cm]''')

        self.lbPosicaoBallbot2 = tk.Label(self.Frame5)
        self.lbPosicaoBallbot2.place(relx=0.378, rely=0.205, height=21
                , width=104)
        self.lbPosicaoBallbot2.configure(activebackground="#f9f9f9")
        self.lbPosicaoBallbot2.configure(activeforeground="black")
        self.lbPosicaoBallbot2.configure(background="#d9d9d9")
        self.lbPosicaoBallbot2.configure(disabledforeground="#a3a3a3")
        self.lbPosicaoBallbot2.configure(font="-family {Segoe UI} -size 11 -slant italic")
        self.lbPosicaoBallbot2.configure(foreground="#000000")
        self.lbPosicaoBallbot2.configure(highlightbackground="#d9d9d9")
        self.lbPosicaoBallbot2.configure(highlightcolor="black")
        self.lbPosicaoBallbot2.configure(text='''0,0''')

        self.TLabel1_12 = ttk.Label(self.Frame5)
        self.TLabel1_12.place(relx=0.054, rely=0.154, height=19, width=36)
        self.TLabel1_12.configure(background="#d9d9d9")
        self.TLabel1_12.configure(foreground="#000000")
        self.TLabel1_12.configure(font="TkDefaultFont")
        self.TLabel1_12.configure(relief="flat")
        self.TLabel1_12.configure(text='''Atual''')

        self.TLabel1_11 = ttk.Label(self.Frame5)
        self.TLabel1_11.place(relx=0.076, rely=0.292, height=19, width=36)
        self.TLabel1_11.configure(background="#d9d9d9")
        self.TLabel1_11.configure(foreground="#000000")
        self.TLabel1_11.configure(font="TkDefaultFont")
        self.TLabel1_11.configure(relief="flat")
        self.TLabel1_11.configure(text='''Erro''')

        self.lbErroPosicaoBallbot2 = tk.Label(self.Frame5)
        self.lbErroPosicaoBallbot2.place(relx=0.378, rely=0.308, height=21
                , width=104)
        self.lbErroPosicaoBallbot2.configure(activebackground="#f9f9f9")
        self.lbErroPosicaoBallbot2.configure(activeforeground="black")
        self.lbErroPosicaoBallbot2.configure(background="#d9d9d9")
        self.lbErroPosicaoBallbot2.configure(disabledforeground="#a3a3a3")
        self.lbErroPosicaoBallbot2.configure(font="-family {Segoe UI} -size 11 -slant italic")
        self.lbErroPosicaoBallbot2.configure(foreground="#000000")
        self.lbErroPosicaoBallbot2.configure(highlightbackground="#d9d9d9")
        self.lbErroPosicaoBallbot2.configure(highlightcolor="black")
        self.lbErroPosicaoBallbot2.configure(text='''0,0''')

        self.TLabel1_12 = ttk.Label(self.Frame5)
        self.TLabel1_12.place(relx=0.108, rely=0.718, height=19, width=66)
        self.TLabel1_12.configure(background="#d9d9d9")
        self.TLabel1_12.configure(foreground="#000000")
        self.TLabel1_12.configure(font="-family {Segoe UI} -size 10 -weight bold")
        self.TLabel1_12.configure(relief="flat")
        self.TLabel1_12.configure(text='''Ref.Vel.''')

        self.lbRefVel2 = tk.Label(self.Frame5)
        self.lbRefVel2.place(relx=0.432, rely=0.718, height=21, width=84)
        self.lbRefVel2.configure(activebackground="#f9f9f9")
        self.lbRefVel2.configure(activeforeground="black")
        self.lbRefVel2.configure(background="#d9d9d9")
        self.lbRefVel2.configure(disabledforeground="#a3a3a3")
        self.lbRefVel2.configure(font="-family {Segoe UI} -size 11 -slant italic")
        self.lbRefVel2.configure(foreground="#000000")
        self.lbRefVel2.configure(highlightbackground="#d9d9d9")
        self.lbRefVel2.configure(highlightcolor="black")
        self.lbRefVel2.configure(text='''0,0''')

        self.TSeparator1_13 = ttk.Separator(self.Frame5)
        self.TSeparator1_13.place(relx=0.086, rely=0.59, relwidth=0.811)

        self.Frame5_11 = tk.Frame(top)
        self.Frame5_11.place(relx=0.024, rely=0.609, relheight=0.211
                , relwidth=0.131)
        self.Frame5_11.configure(relief='groove')
        self.Frame5_11.configure(borderwidth="2")
        self.Frame5_11.configure(relief="groove")
        self.Frame5_11.configure(background="#d9d9d9")
        self.Frame5_11.configure(highlightbackground="#d9d9d9")
        self.Frame5_11.configure(highlightcolor="black")

        self.TLabel1_13 = ttk.Label(self.Frame5_11)
        self.TLabel1_13.place(relx=0.073, rely=0.022, height=19, width=106)
        self.TLabel1_13.configure(background="#d9d9d9")
        self.TLabel1_13.configure(foreground="#000000")
        self.TLabel1_13.configure(font="-family {Segoe UI} -size 10 -weight bold")
        self.TLabel1_13.configure(relief="flat")
        self.TLabel1_13.configure(text='''Orientação [º]''')

        self.lbOrientacao2 = tk.Label(self.Frame5_11)
        self.lbOrientacao2.place(relx=0.57, rely=0.23, height=21, width=64)
        self.lbOrientacao2.configure(activebackground="#f9f9f9")
        self.lbOrientacao2.configure(activeforeground="black")
        self.lbOrientacao2.configure(background="#d9d9d9")
        self.lbOrientacao2.configure(disabledforeground="#a3a3a3")
        self.lbOrientacao2.configure(font="-family {Segoe UI} -size 11 -slant italic")
        self.lbOrientacao2.configure(foreground="#000000")
        self.lbOrientacao2.configure(highlightbackground="#d9d9d9")
        self.lbOrientacao2.configure(highlightcolor="black")
        self.lbOrientacao2.configure(text='''0''')

        self.TLabel1_17 = ttk.Label(self.Frame5_11)
        self.TLabel1_17.place(relx=0.055, rely=0.252, height=19, width=36)
        self.TLabel1_17.configure(background="#d9d9d9")
        self.TLabel1_17.configure(foreground="#000000")
        self.TLabel1_17.configure(font="TkDefaultFont")
        self.TLabel1_17.configure(relief="flat")
        self.TLabel1_17.configure(text='''Atual''')

        self.TLabel1_18 = ttk.Label(self.Frame5_11)
        self.TLabel1_18.place(relx=0.061, rely=0.422, height=19, width=36)
        self.TLabel1_18.configure(background="#d9d9d9")
        self.TLabel1_18.configure(foreground="#000000")
        self.TLabel1_18.configure(font="TkDefaultFont")
        self.TLabel1_18.configure(relief="flat")
        self.TLabel1_18.configure(text='''Erro''')

        self.lbErroOrientacao2 = tk.Label(self.Frame5_11)
        self.lbErroOrientacao2.place(relx=0.558, rely=0.393, height=21, width=64)

        self.lbErroOrientacao2.configure(activebackground="#f9f9f9")
        self.lbErroOrientacao2.configure(activeforeground="black")
        self.lbErroOrientacao2.configure(background="#d9d9d9")
        self.lbErroOrientacao2.configure(disabledforeground="#a3a3a3")
        self.lbErroOrientacao2.configure(font="-family {Segoe UI} -size 11 -slant italic")
        self.lbErroOrientacao2.configure(foreground="#000000")
        self.lbErroOrientacao2.configure(highlightbackground="#d9d9d9")
        self.lbErroOrientacao2.configure(highlightcolor="black")
        self.lbErroOrientacao2.configure(text='''0''')

        self.TLabel1_13 = ttk.Label(self.Frame5_11)
        self.TLabel1_13.place(relx=0.061, rely=0.556, height=29, width=76)
        self.TLabel1_13.configure(background="#d9d9d9")
        self.TLabel1_13.configure(foreground="#000000")
        self.TLabel1_13.configure(font="TkDefaultFont")
        self.TLabel1_13.configure(relief="flat")
        self.TLabel1_13.configure(text='''Ref. Guinada''')

        self.lbRefGuinada2 = tk.Label(self.Frame5_11)
        self.lbRefGuinada2.place(relx=0.552, rely=0.556, height=21, width=64)
        self.lbRefGuinada2.configure(activebackground="#f9f9f9")
        self.lbRefGuinada2.configure(activeforeground="black")
        self.lbRefGuinada2.configure(background="#d9d9d9")
        self.lbRefGuinada2.configure(disabledforeground="#a3a3a3")
        self.lbRefGuinada2.configure(font="-family {Segoe UI} -size 11 -slant italic")
        self.lbRefGuinada2.configure(foreground="#000000")
        self.lbRefGuinada2.configure(highlightbackground="#d9d9d9")
        self.lbRefGuinada2.configure(highlightcolor="black")
        self.lbRefGuinada2.configure(text='''0''')

        self.Frame5_13 = tk.Frame(top)
        self.Frame5_13.place(relx=0.158, rely=0.609, relheight=0.211
                , relwidth=0.178)
        self.Frame5_13.configure(relief='groove')
        self.Frame5_13.configure(borderwidth="2")
        self.Frame5_13.configure(relief="groove")
        self.Frame5_13.configure(background="#d9d9d9")
        self.Frame5_13.configure(highlightbackground="#d9d9d9")
        self.Frame5_13.configure(highlightcolor="black")

        self.Label2_13 = tk.Label(self.Frame5_13)
        self.Label2_13.place(relx=0.031, rely=0.022, height=21, width=114)
        self.Label2_13.configure(activebackground="#f9f9f9")
        self.Label2_13.configure(activeforeground="black")
        self.Label2_13.configure(background="#d9d9d9")
        self.Label2_13.configure(disabledforeground="#a3a3a3")
        self.Label2_13.configure(font="-family {Segoe UI} -size 11 -weight bold")
        self.Label2_13.configure(foreground="#000000")
        self.Label2_13.configure(highlightbackground="#d9d9d9")
        self.Label2_13.configure(highlightcolor="black")
        self.Label2_13.configure(text='''Rastrear objeto''')

        self.TLabel1_15 = ttk.Label(self.Frame5_13)
        self.TLabel1_15.place(relx=0.044, rely=0.63, height=19, width=56)
        self.TLabel1_15.configure(background="#d9d9d9")
        self.TLabel1_15.configure(foreground="#000000")
        self.TLabel1_15.configure(font="TkDefaultFont")
        self.TLabel1_15.configure(relief="flat")
        self.TLabel1_15.configure(text='''Dist. max.''')

        self.lbObjectTrackiingDist = tk.Entry(self.Frame5_13)
        self.lbObjectTrackiingDist.place(relx=0.311, rely=0.615, height=20
                , relwidth=0.284)
        self.lbObjectTrackiingDist.configure(background="white")
        self.lbObjectTrackiingDist.configure(disabledforeground="#a3a3a3")
        self.lbObjectTrackiingDist.configure(font="TkFixedFont")
        self.lbObjectTrackiingDist.configure(foreground="#000000")
        self.lbObjectTrackiingDist.configure(highlightbackground="#d9d9d9")
        self.lbObjectTrackiingDist.configure(highlightcolor="black")
        self.lbObjectTrackiingDist.configure(insertbackground="black")
        self.lbObjectTrackiingDist.configure(selectbackground="#c4c4c4")
        self.lbObjectTrackiingDist.configure(selectforeground="black")
        self.lbObjectTrackiingDist.configure(textvariable=tela_support.varRefDist)

        self.cbObjectT_SistLocalizacao = tk.Checkbutton(self.Frame5_13)
        self.cbObjectT_SistLocalizacao.place(relx=0.622, rely=0.052
                , relheight=0.185, relwidth=0.307)
        self.cbObjectT_SistLocalizacao.configure(activebackground="#ececec")
        self.cbObjectT_SistLocalizacao.configure(activeforeground="#000000")
        self.cbObjectT_SistLocalizacao.configure(background="#d9d9d9")
        self.cbObjectT_SistLocalizacao.configure(disabledforeground="#a3a3a3")
        self.cbObjectT_SistLocalizacao.configure(foreground="#000000")
        self.cbObjectT_SistLocalizacao.configure(highlightbackground="#d9d9d9")
        self.cbObjectT_SistLocalizacao.configure(highlightcolor="black")
        self.cbObjectT_SistLocalizacao.configure(justify='left')
        self.cbObjectT_SistLocalizacao.configure(text='''Rastrear''')
        self.cbObjectT_SistLocalizacao.configure(variable=tela_support.cbHabilitaRastrear)

        self.cbObjectT_Dist = tk.Checkbutton(self.Frame5_13)
        self.cbObjectT_Dist.place(relx=0.644, rely=0.593, relheight=0.185
                , relwidth=0.262)
        self.cbObjectT_Dist.configure(activebackground="#ececec")
        self.cbObjectT_Dist.configure(activeforeground="#000000")
        self.cbObjectT_Dist.configure(background="#d9d9d9")
        self.cbObjectT_Dist.configure(disabledforeground="#a3a3a3")
        self.cbObjectT_Dist.configure(foreground="#000000")
        self.cbObjectT_Dist.configure(highlightbackground="#d9d9d9")
        self.cbObjectT_Dist.configure(highlightcolor="black")
        self.cbObjectT_Dist.configure(justify='left')
        self.cbObjectT_Dist.configure(text='''Hab.''')
        self.cbObjectT_Dist.configure(variable=tela_support.cbObjectT_Dist)

        self.TLabel1_16 = ttk.Label(self.Frame5_13)
        self.TLabel1_16.place(relx=0.089, rely=0.785, height=19, width=56)
        self.TLabel1_16.configure(background="#d9d9d9")
        self.TLabel1_16.configure(foreground="#000000")
        self.TLabel1_16.configure(font="TkDefaultFont")
        self.TLabel1_16.configure(relief="flat")
        self.TLabel1_16.configure(text='''Kg''')

        self.tbK4_15 = tk.Entry(self.Frame5_13)
        self.tbK4_15.place(relx=0.311, rely=0.785,height=20, relwidth=0.284)
        self.tbK4_15.configure(background="white")
        self.tbK4_15.configure(disabledforeground="#a3a3a3")
        self.tbK4_15.configure(font="TkFixedFont")
        self.tbK4_15.configure(foreground="#000000")
        self.tbK4_15.configure(highlightbackground="#d9d9d9")
        self.tbK4_15.configure(highlightcolor="black")
        self.tbK4_15.configure(insertbackground="black")
        self.tbK4_15.configure(selectbackground="#c4c4c4")
        self.tbK4_15.configure(selectforeground="black")
        self.tbK4_15.configure(textvariable=tela_support.varKg)

        self.labposXPixels = ttk.Label(self.Frame5_13)
        self.labposXPixels.place(relx=0.044, rely=0.244, height=19, width=76)
        self.labposXPixels.configure(background="#d9d9d9")
        self.labposXPixels.configure(foreground="#000000")
        self.labposXPixels.configure(font="TkDefaultFont")
        self.labposXPixels.configure(relief="flat")
        self.labposXPixels.configure(text='''Pos. X [Pixels]''')

        self.lbObjectTrackingX = ttk.Label(self.Frame5_13)
        self.lbObjectTrackingX.place(relx=0.467, rely=0.252, height=19, width=46)

        self.lbObjectTrackingX.configure(background="#d9d9d9")
        self.lbObjectTrackingX.configure(foreground="#000000")
        self.lbObjectTrackingX.configure(font="TkDefaultFont")
        self.lbObjectTrackingX.configure(relief="flat")
        self.lbObjectTrackingX.configure(text='''0''')

        self.lbObjectTrackiingDist2 = ttk.Label(self.Frame5_13)
        self.lbObjectTrackiingDist2.place(relx=0.467, rely=0.437, height=19
                , width=46)
        self.lbObjectTrackiingDist2.configure(background="#d9d9d9")
        self.lbObjectTrackiingDist2.configure(foreground="#000000")
        self.lbObjectTrackiingDist2.configure(font="TkDefaultFont")
        self.lbObjectTrackiingDist2.configure(relief="flat")
        self.lbObjectTrackiingDist2.configure(text='''0''')

        self.labposXPixels_16 = ttk.Label(self.Frame5_13)
        self.labposXPixels_16.place(relx=0.062, rely=0.43, height=19, width=76)
        self.labposXPixels_16.configure(background="#d9d9d9")
        self.labposXPixels_16.configure(foreground="#000000")
        self.labposXPixels_16.configure(font="TkDefaultFont")
        self.labposXPixels_16.configure(relief="flat")
        self.labposXPixels_16.configure(text='''Dist. [cm]''')
        self.iniciarConfig()

    def iniciarConfig(self):


        self.bluetooth = Bluetooth()
        self.guiagem = Guiagem()
        self.webcam = WebCamera()
        self.objecttracking = ObjectTracking()

        self.bluetooth.setDaemon(True)  # Força a thread WebCam fechar juntamente com a main thread
        self.bluetooth.registrarParaNotificacao(self.lbOrientacao2, self.tbDadosSerial,
                                                self.guiagem)  # Registra o canvas para receber notificações (novas imagens)
        #self.bluetooth.start()

        self.objecttracking.setDaemon(True)  # Força a thread WebCam fechar juntamente com a main thread
        self.objecttracking.registrarParaNotificacao(self.bluetooth, self.webcam, self.lbObjectTrackiingDist2, self.lbObjectTrackingX, self.lbOrientacao2)
        self.objecttracking.start()

        self.guiagem.setDaemon(True)  # Força a thread WebCam fechar juntamente com a main thread
        self.guiagem.registrarParaNotificacao(self.bluetooth, self.lbErroPosicaoBallbot2, self.lbErroOrientacao2,
                                              self.lbRefGuinada2, self.lbNumWaypointAtual, self.lbRefVel2,
                                              self.btnTrajetoria, self.webcam)
        self.guiagem.start()

        self.webcam.setDaemon(True)  # Força a thread WebCam fechar juntamente com a main thread
        self.webcam.registrarParaNotificacao(self.Canvas1, self.Canvas2, self.lbPosicaoBallbot2,
                                             self.guiagem)  # Registra o canvas para receber notificações (novas imagens)
        self.webcam.start()

        self.webcam.pararGravacao()
        ##########################################################
        ############### Atributos da Tela ########################
        ##########################################################

        # Pontos para calibrar o sistema de posição, dist é a distância em pixels dos pontos
        self.pto1 = [24, 217]
        self.pto2 = [289, 208]
        self.pto3 = [83, 13]
        self.pto4 = [236, 11]
        # pontoAtual é para selecionar o clique no Canvas.
        self.pontoAtual = 0  # #Se for 0 nada acontece. Se 1 sera ponto1, 2 será ponto2...etc

        # Eventos dos componentes (botão, slider, canvas)
        self.btnImportar.configure(command=self.carregarTXT)
        self.btnOnCam.configure(command=self.ligarCAM)
        self.btnP1.configure(command=self.P1)
        self.btnP2.configure(command=self.P2)
        self.btnP3.configure(command=self.P3)
        self.btnP4.configure(command=self.P4)
        self.Canvas1.bind("<Button-1>", self.cliqueCanvas)
        self.sliderGuinada.bind("<ButtonRelease-1>", self.setGuinada)
        self.cbHabMotores.configure(command=self.habMotores)
        self.cbControleGuinada.configure(command=self.habGuinada)
        self.btnVerPontos.configure(command=self.imprimePontos)
        self.btnAlterarAmbiente.configure(command=self.alterarAmbiente)
        self.btnConectar.configure(command=self.abrirSerial)
        self.btnLimparSerial.configure(command=self.limparSerial)
        self.btnAlterarGanhos.configure(command=self.alterarGanhos)
        self.btnCalibrarBussola.configure(command=self.calibrarBussola)
        self.btnLerGanhos.configure(command=self.lerGanhos)
        self.btnAtualizarBluetooth.configure(command=self.atualizarBluetooth)
        self.btnIniciarTelemetria.configure(command=self.iniciarTelemetria)
        self.btnAlterarNorte.configure(command=self.alterarNorte)
        self.btnTrajetoria.configure(command=self.iniciarTrajetoria)

        # Botões de controle manual de Guinada
        self.btnManualGuiParar.configure(command=self.manualGuiParar)
        self.btnManualGuiHorario.configure(command=self.manualGuiHorario)
        self.btnManualGuiAntiHorario.configure(command=self.manualGuiAntiHorario)
        self.cbObjectT_SistLocalizacao.configure(command=self.habObjectTracking)

        # Botões de controle manual de Translação
        self.btnManualDir.configure(command=self.manualDir)
        self.btnManualEsq.configure(command=self.manualEsq)
        self.btnManualParar.configure(command=self.manualParar)
        self.btnManualCima.configure(command=self.manualCima)
        self.btnManualBaixo.configure(command=self.manualBaixo)

        # Associando os métodos da classe para ler as teclas
        root.bind_all('<Up>', self.teclaUp)
        root.bind_all('<Down>', self.teclaDown)
        root.bind_all('<Left>', self.teclaLeft)
        root.bind_all('<Right>', self.teclaRight)
        root.bind_all('<Key>', self.lerTeclas)

        # Valores para calibração do sistema de localização
        # Inicializar os valores dos campos de textos

        # Carregar logo do ITA
        logo = Image.open('ita.png')
        self.tkimage = ImageTk.PhotoImage(logo)
        self.lbLogoITA.configure(image=self.tkimage)

        # Carregar o dispostivo padrão para evitar ter que atualizar (demorando alguns seg)
        self.tbDeviceBluetooth.configure(values=["0","1","2","3"])

        # Carregar os valores dos texbox / combobox
        tela_support.distRealX.set("150")
        tela_support.distRealY.set("200")
        # Valores do controlador de Pitch e Roll
        tela_support.k1.set("90")
        tela_support.k2.set("30")
        tela_support.k3.set("3")
        tela_support.k4.set("0")

        # Valores do controle de guinada
        tela_support.kpgui.set("0")
        tela_support.kigui.set("0")
        # Valores booleanos do combobox
        tela_support.cbControleGuinadaValue.set("0")
        tela_support.cbHabMotoresValue.set("1")
        # Carregar o IP para a câmera
        tela_support.enderecoCamera.set("http://192.168.1.105:4747/") #
        # tela_support.enderecoCamera.set("0")

        # Parametros do object tracker
        tela_support.varRefDist.set("50")
        tela_support.varKg.set("0.002")
    # Teclas do teclado para controle manual
    def teclaUp(self, event):
        self.manualCima()
    def teclaDown(self, event):
        self.manualBaixo()
    def teclaLeft(self, event):
        self.manualEsq()
    def teclaRight(self, event):
        self.manualDir()
    def lerTeclas(self, event):
        if (event.char == "f"):
            self.manualParar()
        if (event.char == "a"):
            self.manualGuiHorario()
        if (event.char == "s"):
            self.manualGuiParar()
        if (event.char == "d"):
            self.manualGuiAntiHorario()

    # Métodos para o controle manual de translação (usando botões)
    def manualParar(self):
        try:
            self.bluetooth.sock.send("x0\n")
            self.bluetooth.sock.send("y0\n")
        except:
            tkMessageBox.showinfo('Mensagem', "Verifique a comunicação")
    def manualDir(self):
        try:
            # self.bluetooth.sock.send("y85\n")
            self.bluetooth.sock.send("y-" + str(self.sliderVelocidade.get() * 1.1) + "\n")
        except:
            tkMessageBox.showinfo('Mensagem', "Verifique a comunicação")
    def manualEsq(self):
        try:
            self.bluetooth.sock.send("y" + str(self.sliderVelocidade.get() * 1.1) + "\n")
        except:
            tkMessageBox.showinfo('Mensagem', "Verifique a comunicação")
    def manualCima(self):
        try:
            self.bluetooth.sock.send("x" + str(self.sliderVelocidade.get()) + "\n")
        except:
            tkMessageBox.showinfo('Mensagem', "Verifique a comunicação")
    def manualBaixo(self):
        try:
            self.bluetooth.sock.send("x-" + str(self.sliderVelocidade.get()) + "\n")
        except:
            tkMessageBox.showinfo('Mensagem', "Verifique a comunicação")

    # Métodos referentes a conexão bluetooth / telemetria
    def abrirSerial(self):
        #self.bluetooth.sock.close()
        #self.bluetooth.sock = self.bluetooth.device

        self.bluetooth.conectar(self.tbDeviceBluetooth.current())
        if self.bluetooth.conectado == True:
            self.btnConectar.configure(text="Desconectar")
            self.bluetooth.start()
        else:
            self.btnConectar.configure(text="Conectar")



    def atualizarBluetooth(self):
        self.bluetooth.atualizarLista()
        self.tbDeviceBluetooth.configure(values=self.bluetooth.listaDevices)

    def iniciarTelemetria(self):
        try:
            if self.bluetooth.telemetria == True:
                self.bluetooth.telemetria = False
                self.btnIniciarTelemetria.configure(text='''Iniciar''')
                self.bluetooth.sock.send("p\n")

                file = open("dadost.txt", "w")
                for x in self.bluetooth.dados:
                    file.write(x)
                file.close()

                # Criar uma array do tempo com multiples de 6 ms (tempo do loop de controle)
                tempo = []
                for i in range(len(self.bluetooth.pitch)):
                    tempo.append(i * 6)

                fig, axs = plt.subplots(3)
                axs[0].plot(tempo, self.bluetooth.pitch)
                axs[0].set_title('Ângulo Pitch')
                axs[1].plot(tempo, self.bluetooth.roll)
                axs[1].set_title('Ângulo Roll')
                axs[2].plot(tempo, self.bluetooth.yaw)
                axs[2].set_title('Ângulo Yaw')


                """
                fig, axs = plt.subplots(2, 3)
                axs[0, 0].plot(tempo, self.bluetooth.pitch)
                axs[0, 0].plot(tempo, self.bluetooth.setpointX)
                axs[0, 0].set_title('Ângulo Pitch')

                axs[0, 1].plot(tempo, self.bluetooth.roll)
                axs[0, 1].plot(tempo, self.bluetooth.setpointY)
                axs[0, 1].set_title('Ângulo Roll')

                axs[0, 2].plot(tempo, self.bluetooth.yaw)
                axs[0, 2].plot(tempo, self.bluetooth.setpointZ)
                axs[0, 2].set_title('Ângulo Yaw')

                axs[1, 0].plot(tempo, self.bluetooth.velX)
                axs[1, 0].set_title('Velocidade X')

                axs[1, 1].plot(tempo, self.bluetooth.velY)
                axs[1, 1].set_title('Velocidade Y')

                axs[1, 2].plot(tempo, self.bluetooth.velZ)
                axs[1, 2].set_title('Velocidade Z')
                """
                plt.show()

            else:
                # Ao parar a telemetria apagar todos os dados.
                self.bluetooth.pitch = []
                self.bluetooth.roll = []
                self.bluetooth.yaw = []

                self.bluetooth.velX = []
                self.bluetooth.velY = []
                self.bluetooth.velZ = []

                self.bluetooth.setpointX = []
                self.bluetooth.setpointY = []
                self.bluetooth.setpointZ = []

                # Apagar dados da telemetria
                self.dados = []

                self.bluetooth.telemetria = True
                self.btnIniciarTelemetria.configure(text='''Parar''')
                self.bluetooth.sock.send("t\n")

        except:
            tkMessageBox.showinfo('Mensagem', "Verifique a comunicação")
    def lerGanhos(self):
        try:
            self.bluetooth.sock.send("l\n")
        except:
            tkMessageBox.showinfo('Mensagem', "Verifique a comunicação")
    def calibrarBussola(self):
        try:
            self.bluetooth.sock.send("c\n")
        except:
            tkMessageBox.showinfo('Mensagem', "Verifique a comunicação ")
    def alterarGanhos(self):
        try:
            self.bluetooth.sock.send("q" + self.tbK1.get() + "\n")
            self.bluetooth.sock.send("w" + self.tbK2.get() + "\n")
            self.bluetooth.sock.send("a" + self.tbK3.get() + "\n")
            self.bluetooth.sock.send("s" + self.tbK4.get() + "\n")
            self.bluetooth.sock.send("l" + "\n")

        except:
            tkMessageBox.showinfo('Mensagem', "Verifique a comunicação")
    def limparSerial(self):
        self.tbDadosSerial.delete('1.0', tk.END)

    # Métodos referentes a Guinada, para controle manual ou automático
    def setGuinada(self, event):
        # print(self.sliderGuinada.get()*3.14/180)
        try:
            self.bluetooth.sock.send("z" + str(self.sliderGuinada.get()) + "\n")
        except:
            tkMessageBox.showinfo('Mensagem', "Verifique a comunicação")

    def manualGuiParar(self):
        try:
            self.bluetooth.sock.send("r0\n")
        except:
            tkMessageBox.showinfo('Mensagem', "Verifique a comunicação")
    def manualGuiAntiHorario(self):
        try:
            self.bluetooth.sock.send("r0.4\n")
        except:
            tkMessageBox.showinfo('Mensagem', "Verifique a comunicação")
    def manualGuiHorario(self):
        try:
            self.bluetooth.sock.send("r-0.4\n")
        except:
            tkMessageBox.showinfo('Mensagem', "Verifique a comunicação")
    def habGuinada(self):

        val = tela_support.cbControleGuinadaValue.get()
        print(val)
        try:
            if (val == "1"):
                self.bluetooth.sock.send("g\n")
            else:
                self.bluetooth.sock.send("f\n")
        except:
            tkMessageBox.showinfo('Mensagem', "Verifique a comunicação ")
        # print("Alterado")
        #
    def habMotores(self):

        val = tela_support.cbHabMotoresValue.get()
        # print(val)
        try:
            if (val == 1):
                self.bluetooth.sock.send("h\n")
            else:
                self.bluetooth.sock.send("j\n")
        except:
            tkMessageBox.showinfo('Mensagem', "Verifique a comunicação")
        # print("Alterado")
        #

    def habObjectTracking(self):




        val = tela_support.cbHabilitaRastrear.get()
        if (val == 1):
            self.objecttracking.refD = tela_support.varRefDist.get()
            self.objecttracking.ligado = True
            self.btnTrajetoria["state"] = "disabled"
            self.objecttracking.dados=[]

            file = open("DadosGerados/dadosoObjTrack2.txt", "w")
            file.write(" ")
            file.close()


            try:
                self.bluetooth.sock.send("r0\n")
                #self.bluetooth.sock.send("x0" + str(self.objecttracking.refD)  +"\n")
                print(self.objecttracking.refD)
            except:
                print("Erro no desligar OBJTRack")
                pass
        else:
            self.objecttracking.ligado = False
            self.btnTrajetoria["state"] = "normal"

            file = open("DadosGerados/dadosRastreamentoObjeto.txt", "w")
            for x in range(len(self.objecttracking.dados)):
                file.write(self.objecttracking.dados[x] +'\n')
            file.close()


    def alterarNorte(self):
        self.guiagem.orientacaoNorte = float(self.lbOrientacao2['text'])
        self.lbOrientacaoNorte.configure(text=self.guiagem.orientacaoNorte)
        try:
            self.bluetooth.sock.send("z" + str(self.guiagem.orientacaoNorte) + "\n")
        except:
            tkMessageBox.showinfo('Mensagem', "Verifique a comunicação")
        # print(self.orientacaoNorte)

    # Métodos referentes ao ambiente estruturado / waypoints
    def ligarCAM(self):
        # Ajusta a nova URL
        if self.webcam.ligado == False:
            self.webcam.ligado = True
            self.btnOnCam.configure(text='''Pausar câmera''')
            #self.webcam.gravarVideo = True
        else:
            self.btnOnCam.configure(text='''Ligar câmera''')
            self.webcam.ligado = False
            #self.webcam.gravarVideo = False

        try:
            if tela_support.enderecoCamera.get() == "0":
                self.webcam.camera.release()
                self.webcam.camera = cv2.VideoCapture(0)
                self.webcam.camera.set(cv2.CAP_PROP_BUFFERSIZE, 1);
            else:
                self.webcam.camera = cv2.VideoCapture(tela_support.enderecoCamera.get() + "/video")
                self.webcam.camera.set(cv2.CAP_PROP_BUFFERSIZE, 1);
        except:
            pass





    def pararCam(self):
        self.webcam.ligado = False
        self.btnOnCam.configure(text='''Ligar câmera''')
    def alterarAmbiente(self):
        try:
            self.Canvas1.delete('all')
            self.Canvas2.delete('all')
            self.webcam.tamX = int(self.tbDistRealX.get())
            self.webcam.tamY = int(self.tbDistRealY.get())

            pts1 = np.float32([self.pto1, self.pto2, self.pto3, self.pto4])
            pts2 = np.float32(
                [[0, 0], [self.webcam.tamX, 0], [0, self.webcam.tamY], [self.webcam.tamX, self.webcam.tamY]])

            self.webcam.matrix = cv2.getPerspectiveTransform(pts1, pts2)
            self.webcam.ambienteAlterado = True
            print(self.pto1)
            print(self.pto2)
            print(self.pto3)
            print(self.pto4)
        except:
            self.webcam.ambienteAlterado = False
            pass
    def imprimePontos(self):
        if self.webcam.ligado == False:
            self.Canvas1.create_text(self.pto1[0] + 10, self.pto1[1] + 10, fill="darkblue", font="Times 20 italic bold",
                                     text="1")
            self.Canvas1.create_text(self.pto1[0], self.pto1[1], fill="red", font="Times 20 italic bold", text="x")

            self.Canvas1.create_text(self.pto2[0] + 10, self.pto2[1] + 10, fill="darkblue", font="Times 20 italic bold",
                                     text="2")
            self.Canvas1.create_text(self.pto2[0], self.pto2[1], fill="red", font="Times 20 italic bold", text="x")

            self.Canvas1.create_text(self.pto3[0] + 10, self.pto3[1] + 10, fill="darkblue", font="Times 20 italic bold",
                                     text="3")
            self.Canvas1.create_text(self.pto3[0], self.pto3[1], fill="red", font="Times 20 italic bold", text="x")

            self.Canvas1.create_text(self.pto4[0] + 10, self.pto4[1] + 10, fill="darkblue", font="Times 20 italic bold",
                                     text="4")
            self.Canvas1.create_text(self.pto4[0], self.pto4[1], fill="red", font="Times 20 italic bold", text="x")
        else:
            tkMessageBox.showinfo('Mensagem', "Primeiro clique em parar a câmera, depois clique em ver pontos")
    def P1(self):
        self.pararCam()
        self.pontoAtual = 1
    def P2(self):
        self.pararCam()
        self.pontoAtual = 2
    def P3(self):
        self.pararCam()
        self.pontoAtual = 3
    def P4(self):
        self.pararCam()
        self.pontoAtual = 4
    def cliqueCanvas(self, event):

        if self.pontoAtual != 0:
            self.Canvas1.create_text(event.x + 10, event.y + 10, fill="darkblue", font="Times 20 italic bold",
                                     text=str(self.pontoAtual))
            self.Canvas1.create_text(event.x, event.y, fill="red", font="Times 20 italic bold", text="x")
            # Salvar o ponto selecionado
            if self.pontoAtual == 1:
                self.pto1 = [event.x, event.y]
            if self.pontoAtual == 2:
                self.pto2 = [event.x, event.y]
            if self.pontoAtual == 3:
                self.pto3 = [event.x, event.y]
            if self.pontoAtual == 4:
                self.pto4 = [event.x, event.y]
        self.pontoAtual = 0
    def carregarTXT(self):  # O botão irá ler o TXT
        # Apagar os pontos para recarregar novamente
        self.Canvas1.delete('all')
        self.Canvas2.delete('all')

        file_path = tkFileDialog.askopenfilename()  # Diretório e arquivo
        # f.close()
        self.webcam.caminhoTXT = file_path

        f = open(file_path, "r")

        i = 0
        self.Listbox1.delete(0, tk.END)
        # self.webcam.waypoints = []
        self.guiagem.waypoints = []
        for x in f:
            self.Listbox1.insert(i, str(i + 1) + ") " + x)
            i = i + 1
            pos = x.split(',')
            self.guiagem.waypoints.append([float(pos[0]), float(pos[1])])  # pos[0] é o X e pos[1] é o Y do waypoint

        f.close()

        self.webcam.imprimeWaypoints()

    # Métodos Guiagem
    def iniciarTrajetoria(self):
        if self.guiagem.ligado == True:
            self.webcam.ligado = False
            self.bluetooth.ligado = False
            self.guiagem.ligado = False
            self.btnTrajetoria.configure(text='''Iniciar trajetória''')
            self.btnTrajetoria.configure(background="#339933")
            self.lbNumWaypointAtual['text'] = 0
            self.webcam.gravarVideo = False
            self.webcam.pararGravacao()
            file = open("dadosa.txt", "w")
            for x in self.webcam.dados:
                file.write(x)
            file.close()
            self.webcam.ligado = True  # Voltar com a thread webcam
            self.bluetooth.ligado = True

        else:
            self.guiagem.ligado = True
            self.btnTrajetoria.configure(text='''Parar trajetória''')
            self.btnTrajetoria.configure(background="#FF6347")
            self.guiagem.contWaypoint = 0
            self.webcam.gravarVideo = True
            self.webcam.recomecarGravacao()
            self.Canvas1.delete('all')
            self.Canvas2.delete('all')
            self.webcam.dados = []


if __name__ == '__main__':
    vp_start_gui()





