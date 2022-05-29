import sqlite3
import webbrowser
from tkinter import messagebox



class MenuCascada:

        def print_tabla(self):

                self.doc = open('baseDeDatos.txt', 'w')
                self.doc.write("Planilla de pacientes\n\n")
                self.doc.close()  

                self.datos = []
                self.nombre_db = 'hist.db'
                self.conexion = sqlite3.connect(self.nombre_db)
                self.cursor = self.conexion.cursor()
                        
                self.most = "SELECT id, fecha, apellido, nombre, \
                        obra_social, dni FROM historia"
                self.cursor.execute(self.most)
                self.datos = self.cursor.fetchall()

                for p in self.datos:
                        
                        f = open('baseDeDatos.txt', "a")
                        f.write(f"Fecha:{p[1]}\nApellido:{p[2]}\nNombre:{p[3]}\
                                \nObra Social:{p[4]}\nDNI:{p[5]}\n--------\n")
                        f.close()
                                
                self.conexion.commit()
                self.conexion.close()

        def link_obras(self):
                self.path = 'https://www.ineba.net/obras-sociales-y-prepagas'
                webbrowser.open_new(self.path)

        def version(self):
                messagebox.showinfo('Version 2.2.0', "Versión aplicando POO\nY nuevas funciones\nConsulte el Manual para\nmás información")

        def manual(self):
                self.path = 'docs/build/html/index.html'
                webbrowser.open_new(self.path)
                