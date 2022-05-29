from datetime import datetime
import re
from tkinter import messagebox
from peewee import *


db = SqliteDatabase("hist.db")


class Fecha():
    def __init__(self,):
        self.fecha = datetime.now()
        self.fecha_actual = datetime.strftime(self.fecha, '%d - %m - %Y')

fecha = Fecha()
fecha_hoy = fecha.fecha_actual


class BaseModel(Model):
    class Meta():
        database = db


class Historia(BaseModel):
    fecha_hoy = CharField()
    apellido = CharField()
    nombre = CharField()
    o_social = CharField()
    dni_h = CharField()
    resumen = TextField()


class Funcion(Historia):

    def __init__(self) -> None:
        pass
    

    def conectar(self, tabla):

        self.reinicio_tree(tabla)
        
        try:
            db.connect()
            db.create_tables([Historia])
            self.inserta_en_tabla(tabla)
        except:
            pass


    def nuevo(self, 
    c_ape, 
    c_nom, 
    c_ob, 
    c_dni, 
    c_res, 
    activa, 
    ape, 
    nom, 
    ob, 
    dni, 
    res
    ):
        
        self.habilitar(c_ape, c_nom, c_ob, c_dni, c_res)
        self.borrar_entradas(ape, nom, ob, dni, res)
        activa(state='normal')

        
    def inserta_en_tabla(self, tabla):
        for p in Historia.select():

            tabla.insert('', 'end',
                            text=p.id,
                            values=(p.fecha_hoy, p.apellido,
                                    p.nombre, p.o_social, p.dni_h)
                            )


    def guardar(self, ape, nom, ob, dni, res, tabla,
                c_ape, c_nom, c_ob, c_dni, c_res, b_guardar):
        b_guardar(state='disabled')
        try:
            if re.findall('[0-9]', str(dni.get())) and \
                re.findall('[\D]', nom.get()) and \
                re.findall('[\D]', ape.get()):
                    
                
                self.reinicio_tree(tabla)
                
                hist = Historia()
                hist.fecha_hoy = fecha_hoy
                hist.apellido = ape.get()
                hist.nombre = nom.get()
                hist.o_social = ob.get()
                hist.dni_h = dni.get()
                hist.resumen = res.get('1.0', 'end')

                hist.save()
                
                self.inserta_en_tabla(tabla)
                
                            
                

                self.borrar_entradas(ape, nom, ob, dni, res)

                messagebox.showinfo("Guardar", "Registro guardado")
            else:
                messagebox.showinfo("Guardar", "Datos no válidos\n\
                                    Revise por favor\n \
                                    DNI: Solo números\n \
                                    Nombre y Apellido: Solo letras")
        except:
            messagebox.showinfo("Guardar", "Datos no válidos\n\
                                    Revise por favor\n \
                                    DNI: Solo números\n \
                                    Nombre y Apellido: print")
        self.borrar_entradas(ape, nom, ob, dni, res)
        self.deshabilitar(c_ape, c_nom, c_ob, c_dni, c_res)
        

    def consulta(self, c_ape, c_nom, c_ob, c_dni, c_res,
                 var_ape, var_nom, var_dni, 
                 var_ob, res_ide, tabla, b_guardar):
        
        self.borrar_entradas(var_ape, var_nom, var_dni, var_ob, res_ide)

        b_guardar(state='disabled')

        item = tabla.item(tabla.selection())
        
        lista = list(item['values'])
        #print(lista)
        ide = item['text']
        #print(ide)
        if ide !='':
        
            self.habilitar(c_ape, c_nom, c_ob, c_dni, c_res)
            var_ape.set(lista[1])
            var_nom.set(lista[2])
            var_dni.set(lista[3])
            var_ob.set(lista[4])
            
            ide = item['text']
                

            for p in Historia.select():
                if p.id == ide:
                    res_ide.insert('1.0', p.resumen)
            
            #b_consulta(state='disabled')

        else:
            messagebox.showinfo('Consulta', 'Seleccione un registro')


    def modificar(self, ape, nom, ob, dni, res, tabla,
                    c_ape, c_nom, c_ob, c_dni, c_res, b_consulta):

        self.reinicio_tree(tabla)

        try:
            if re.findall('[0-9]', str(dni.get())) and \
                re.findall('[\D]', nom.get()) and \
                re.findall('[\D]', ape.get()):

                item = tabla.item(tabla.selection())
                
                lis = (item['text'])
                
                actualizar = Historia.update(apellido=ape.get(), 
                                                nombre=nom.get(), 
                                                o_social=ob.get(), 
                                                dni_h=dni.get(), 
                                                resumen=res.get('1.0', 'end')
                                                ).where(Historia.id == lis)
                
                actualizar.execute()

                

                self.borrar_entradas(ape, nom, ob, dni, res)
                self.deshabilitar(c_ape, c_nom, c_ob, c_dni, c_res)
                
                b_consulta(state='normal')
                self.inserta_en_tabla(tabla)
                messagebox.showinfo('Modificar', 'Se modificó un registro')
            else:
                self.inserta_en_tabla(tabla)
                messagebox.showinfo("Modificar", "Datos no válidos\n\
                                    Revise por favor\n \
                                    DNI: Solo números\n \
                                    Nombre y Apellido: Solo letras")
        except:
            self.inserta_en_tabla(tabla)
            messagebox.showerror("Modificar", \
                                 "Primero debe realizar una consulta")


    def borrar(self, tabla,ape, nom, ob, dni, res,
                    c_ape, c_nom, c_ob, c_dni, c_res):
        
        item = tabla.item(tabla.selection())
        ide = item['text']
        
        if ide !='':
            
            preg_borrar = messagebox.askquestion(
                                                "Borrar",
                                                "Desea borrar este registro?"
                                                )

            if preg_borrar == "yes":
                
                
                    
                borrar = Historia.get(Historia.id == ide)
                borrar.delete_instance()

                self.reinicio_tree(tabla)
                self.inserta_en_tabla(tabla)
                self.borrar_entradas(ape, nom, ob, dni, res)
                self.deshabilitar(c_ape, c_nom, c_ob, c_dni, c_res)

                messagebox.showinfo("Borrar", "Registro borrado")
                

            else:
                messagebox.showinfo("Borrar", "No se borró el registro")
        else:
            messagebox.showinfo('Borrar', 'Seleccione un registro')


    def buscar(self, tabla, v_buscar):

        self.reinicio_tree(tabla)

        
        print(v_buscar.get())
        
        if re.findall('[0-9]', v_buscar.get()):
            print("dentro del if")
            contador = 0
            for p in Historia.select():
                
                if p.dni_h == v_buscar.get():
                    
                    contador += 1
                    tabla.insert('', 'end',
                            text=p.id,
                            values=(p.fecha_hoy, p.apellido,
                                    p.nombre, p.o_social, p.dni_h)
                            )
                
                
            v_buscar.set("")
            
            if contador == 0:
                v_buscar.set("")
                self.conectar(tabla)
                self.inserta_en_tabla(tabla)
                messagebox.showinfo("Buscar","DNI no encontrado")    
        else:
            self.conectar(tabla)
            self.inserta_en_tabla(tabla)
            messagebox.showinfo("Buscar","Datos invalidos")
     

    def refrescar(self, tabla, v_buscar):
        v_buscar.set("")
        self.reinicio_tree(tabla)
        self.conectar(tabla)
        self.inserta_en_tabla(tabla)
        

    def habilitar(self, c_ape, c_nom, c_ob, c_dni, c_res):
        c_ape(state='normal')
        c_nom(state='normal')
        c_ob(state='normal')
        c_dni(state='normal')
        c_res(state='normal')


    def deshabilitar(self, c_ape, c_nom, c_ob, c_dni, c_res):
        c_ape(state='disabled')
        c_nom(state='disabled')
        c_ob(state='disabled')
        c_dni(state='disabled')
        c_res(state='disabled')


    def reinicio_tree(self, tabla):
        borrar = tabla.get_children()
        
        for elemento in borrar:
            tabla.delete(elemento)
    

    def borrar_entradas(self, c_ape, c_nom, c_ob, c_dni, c_res):
        c_ape.set('')
        c_nom.set('')
        c_ob.set('')
        c_dni.set('')
        c_res.delete("1.0", 'end')

