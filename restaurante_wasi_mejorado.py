import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import os

class RestauranteWasi:
    def __init__(self, root):
        self.root = root
        self.root.title("Restaurante Wasi de Sabor Peruano")
        self.root.geometry("1000x800")
        self.root.configure(bg="#fff3e6")  # Color hueso
        
        # Centro la ventana en la pantalla
        self.centrar_ventana()

        self.menu = {
            "Ceviche": 25.00,
            "Lomo Saltado": 28.00,
            "Aji de Gallina": 22.00,
            "Anticuchos": 20.00,
            "Papa a la Huancaina": 10.00,
            "Pollo a la Brasa": 24.00,
            "Causa Limeña": 15.00,
            "Rocoto Relleno": 18.00
        }
        self.pedido = {}

        self._crear_estilos()
        self._crear_interfaz()

    def centrar_ventana(self):
        """Centra la ventana en la pantalla"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def _crear_estilos(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TButton", font=("Arial", 14, "bold"), padding=15)
        style.configure("TLabel", background="#fff3e6", font=("Arial", 14))
        style.configure("TCheckbutton", background="#fff3e6", font=("Arial", 13))

    def _crear_interfaz(self):
        # Título principal con mayor tamaño
        titulo = tk.Label(self.root, text="🍽️ RESTAURANTE WASI DE SABOR PERUANO 🍽️",
                          font=("Arial", 26, "bold"), bg="#ff704d", fg="white", pady=20)
        titulo.pack(fill="x")

        # Subtítulo
        subtitulo = tk.Label(self.root, text="Auténtica cocina peruana para tu paladar",
                            font=("Arial", 16, "italic"), bg="#fff3e6", fg="#cc3300", pady=10)
        subtitulo.pack()

        # Marco principal del menú
        marco_menu = tk.LabelFrame(self.root, text="🍽️ NUESTRO MENÚ 🍽️", bg="#ffe6cc", fg="#cc3300",
                                   font=("Arial", 18, "bold"), padx=20, pady=20, bd=6, relief="ridge")
        marco_menu.pack(padx=30, pady=20, fill="both", expand=True)

        self.items_vars = {}
        self.cantidad_vars = {}
        self.precio_labels = {}

        colores = ["#ff9999", "#ffcc66", "#99ffcc", "#66b3ff", "#ffb366", "#ff99cc", "#99ff99", "#ffcc99"]

        # Crear grid para mejor organización
        for idx, (plato, precio) in enumerate(self.menu.items()):
            var = tk.IntVar()
            cant = tk.IntVar(value=1)

            fila = tk.Frame(marco_menu, bg=colores[idx % len(colores)], pady=10, padx=10, relief="raised", bd=3)
            fila.pack(fill="x", pady=8)

            # Nombre del plato y precio base
            info_frame = tk.Frame(fila, bg=colores[idx % len(colores)])
            info_frame.pack(fill="x")
            
            tk.Checkbutton(info_frame, text=f"🍴 {plato}",
                           variable=var, bg=colores[idx % len(colores)],
                           font=("Arial", 16, "bold"), activebackground="#ffdfba").pack(side="left")
            
            precio_base_label = tk.Label(info_frame, text=f"Precio unitario: S/. {precio:.2f}",
                                        bg=colores[idx % len(colores)], font=("Arial", 14))
            precio_base_label.pack(side="right")

            # Controles de cantidad mejorados
            cantidad_frame = tk.Frame(fila, bg=colores[idx % len(colores)])
            cantidad_frame.pack(fill="x", pady=5)
            
            tk.Label(cantidad_frame, text="Cantidad:", bg=colores[idx % len(colores)], 
                    font=("Arial", 14, "bold")).pack(side="left")
            
            # Botones más grandes para cantidad
            btn_menos = tk.Button(cantidad_frame, text="➖", command=lambda p=plato: self.disminuir_cantidad(p),
                                 font=("Arial", 16, "bold"), bg="#ff6666", fg="white", width=3, height=1)
            btn_menos.pack(side="left", padx=5)
            
            entry_cantidad = tk.Entry(cantidad_frame, textvariable=cant, width=6, font=("Arial", 16, "bold"),
                                    justify="center", bd=3, relief="sunken")
            entry_cantidad.pack(side="left", padx=5)
            entry_cantidad.bind('<KeyRelease>', lambda e, p=plato: self.actualizar_precio_total(p))
            
            btn_mas = tk.Button(cantidad_frame, text="➕", command=lambda p=plato: self.aumentar_cantidad(p),
                               font=("Arial", 16, "bold"), bg="#66ff66", fg="white", width=3, height=1)
            btn_mas.pack(side="left", padx=5)

            # Mostrar precio total por plato
            precio_total_label = tk.Label(cantidad_frame, text=f"Total: S/. {precio:.2f}",
                                        bg=colores[idx % len(colores)], font=("Arial", 16, "bold"), fg="#cc3300")
            precio_total_label.pack(side="right")

            self.items_vars[plato] = var
            self.cantidad_vars[plato] = cant
            self.precio_labels[plato] = precio_total_label

        # Botones de acción principales - MÁS GRANDES
        boton_frame = tk.Frame(self.root, bg="#fff3e6")
        boton_frame.pack(pady=20)

        self._boton_grande(boton_frame, "🛒 AGREGAR AL PEDIDO", self.agregar_pedido, "#28a745").pack(side="left", padx=15)
        self._boton_grande(boton_frame, "👁️ VER PEDIDO", self.ver_pedido, "#17a2b8").pack(side="left", padx=15)

        # Área de texto para mostrar el pedido
        self.texto_pedido = tk.Text(self.root, height=12, bg="#ffffe6", fg="#333", 
                                   font=("Courier", 12), state="disabled", bd=5, relief="sunken")
        self.texto_pedido.pack(padx=30, pady=15, fill="both", expand=True)

        # Botones finales - MÁS GRANDES
        botones_finales = tk.Frame(self.root, bg="#fff3e6")
        botones_finales.pack(pady=15)

        self._boton_grande(botones_finales, "✅ FINALIZAR PEDIDO", self.finalizar_pedido, "#007bff").pack(side="left", padx=20)
        self._boton_grande(botones_finales, "🖨️ IMPRIMIR RECIBO", self.imprimir_recibo, "#ffc107").pack(side="left", padx=20)
        self._boton_grande(botones_finales, "❌ CANCELAR TODO", self.cancelar_pedido, "#dc3545").pack(side="left", padx=20)

    def _boton_grande(self, parent, texto, comando, color):
        """Crear botones más grandes y atractivos"""
        boton = tk.Button(parent, text=texto, command=comando, 
                         font=("Arial", 16, "bold"), bg=color, fg="white", 
                         activebackground=self._color_oscuro(color), 
                         width=18, height=2, bd=4, relief="raised",
                         cursor="hand2")
        
        # Efectos hover
        def on_enter(e):
            boton.config(bg=self._color_claro(color), relief="ridge")
        def on_leave(e):
            boton.config(bg=color, relief="raised")
            
        boton.bind("<Enter>", on_enter)
        boton.bind("<Leave>", on_leave)
        return boton

    def _color_claro(self, color):
        """Genera una versión más clara del color para hover"""
        colores = {
            "#28a745": "#34ce57",
            "#17a2b8": "#20c997", 
            "#007bff": "#0d8bff",
            "#ffc107": "#ffcd39",
            "#dc3545": "#e74c3c"
        }
        return colores.get(color, color)

    def _color_oscuro(self, color):
        """Genera una versión más oscura del color para active"""
        colores = {
            "#28a745": "#1e7e34",
            "#17a2b8": "#138496",
            "#007bff": "#0056b3", 
            "#ffc107": "#e0a800",
            "#dc3545": "#bd2130"
        }
        return colores.get(color, color)

    def aumentar_cantidad(self, plato):
        """Aumenta la cantidad de un plato"""
        cantidad_actual = self.cantidad_vars[plato].get()
        if cantidad_actual < 99:
            self.cantidad_vars[plato].set(cantidad_actual + 1)
            self.actualizar_precio_total(plato)

    def disminuir_cantidad(self, plato):
        """Disminuye la cantidad de un plato"""
        cantidad_actual = self.cantidad_vars[plato].get()
        if cantidad_actual > 1:
            self.cantidad_vars[plato].set(cantidad_actual - 1)
            self.actualizar_precio_total(plato)

    def actualizar_precio_total(self, plato):
        """Actualiza el precio total mostrado para un plato específico"""
        try:
            cantidad = self.cantidad_vars[plato].get()
            precio_unitario = self.menu[plato]
            precio_total = precio_unitario * cantidad
            self.precio_labels[plato].config(text=f"Total: S/. {precio_total:.2f}")
        except:
            pass

    def agregar_pedido(self):
        """Agrega los productos seleccionados al pedido"""
        productos_agregados = []
        for plato in self.menu:
            if self.items_vars[plato].get():
                cantidad = self.cantidad_vars[plato].get()
                if cantidad > 0:
                    self.pedido[plato] = self.pedido.get(plato, 0) + cantidad
                    productos_agregados.append(f"{plato} x{cantidad}")
                    # Resetear selección
                    self.items_vars[plato].set(0)
                    self.cantidad_vars[plato].set(1)
                    self.actualizar_precio_total(plato)
        
        if productos_agregados:
            mensaje = "Productos agregados:\n" + "\n".join(productos_agregados)
            messagebox.showinfo("✅ Pedido Actualizado", mensaje)
        else:
            messagebox.showwarning("⚠️ Atención", "Por favor seleccione al menos un producto.")

    def ver_pedido(self):
        """Muestra el pedido actual en el área de texto"""
        self.texto_pedido.config(state="normal")
        self.texto_pedido.delete(1.0, tk.END)

        if not self.pedido:
            self.texto_pedido.insert(tk.END, "🛒 No hay productos en el pedido.\n\n")
            self.texto_pedido.insert(tk.END, "💡 Seleccione productos del menú y haga clic en 'AGREGAR AL PEDIDO'")
        else:
            self.texto_pedido.insert(tk.END, "🧾 RESUMEN DEL PEDIDO\n")
            self.texto_pedido.insert(tk.END, "=" * 50 + "\n\n")
            
            subtotal = 0
            for plato, cantidad in self.pedido.items():
                precio_unitario = self.menu[plato]
                precio_total = precio_unitario * cantidad
                linea = f"🍽️ {plato:<20} x{cantidad:>2} = S/. {precio_total:>7.2f}\n"
                self.texto_pedido.insert(tk.END, linea)
                subtotal += precio_total

            igv = subtotal * 0.18
            total = subtotal + igv

            self.texto_pedido.insert(tk.END, "\n" + "-" * 50 + "\n")
            self.texto_pedido.insert(tk.END, f"💰 Subtotal:     S/. {subtotal:>10.2f}\n")
            self.texto_pedido.insert(tk.END, f"📋 IGV (18%):    S/. {igv:>10.2f}\n")
            self.texto_pedido.insert(tk.END, "=" * 50 + "\n")
            self.texto_pedido.insert(tk.END, f"💵 TOTAL:        S/. {total:>10.2f}\n")
            self.texto_pedido.insert(tk.END, "=" * 50 + "\n")

        self.texto_pedido.config(state="disabled")

    def finalizar_pedido(self):
        """Finaliza el pedido actual"""
        if not self.pedido:
            messagebox.showwarning("⚠️ Atención", "No hay productos en el pedido.")
            return
        
        # Calcular total
        subtotal = sum(self.menu[plato] * cantidad for plato, cantidad in self.pedido.items())
        total = subtotal * 1.18
        
        mensaje = f"🎉 ¡Pedido finalizado exitosamente!\n\n"
        mensaje += f"💵 Total a pagar: S/. {total:.2f}\n\n"
        mensaje += f"📅 Fecha: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}\n"
        mensaje += f"🏪 Restaurante Wasi de Sabor Peruano\n"
        mensaje += f"¡Gracias por su preferencia! 🙏"
        
        messagebox.showinfo("✅ Pedido Finalizado", mensaje)
        self.pedido.clear()
        self.ver_pedido()

    def imprimir_recibo(self):
        """Genera un recibo imprimible"""
        if not self.pedido:
            messagebox.showwarning("⚠️ Atención", "No hay productos en el pedido para imprimir.")
            return
        
        try:
            # Crear archivo de recibo
            fecha_actual = datetime.datetime.now()
            nombre_archivo = f"recibo_wasi_{fecha_actual.strftime('%Y%m%d_%H%M%S')}.txt"
            
            with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
                archivo.write("=" * 50 + "\n")
                archivo.write("    RESTAURANTE WASI DE SABOR PERUANO\n")
                archivo.write("      Auténtica cocina peruana\n")
                archivo.write("=" * 50 + "\n\n")
                
                archivo.write(f"Fecha: {fecha_actual.strftime('%d/%m/%Y %H:%M:%S')}\n")
                archivo.write(f"Pedido #: {fecha_actual.strftime('%Y%m%d%H%M')}\n\n")
                
                archivo.write("DETALLE DEL PEDIDO:\n")
                archivo.write("-" * 50 + "\n")
                
                subtotal = 0
                for plato, cantidad in self.pedido.items():
                    precio_unitario = self.menu[plato]
                    precio_total = precio_unitario * cantidad
                    linea = f"{plato:<25} x{cantidad:>2} S/. {precio_total:>8.2f}\n"
                    archivo.write(linea)
                    subtotal += precio_total
                
                igv = subtotal * 0.18
                total = subtotal + igv
                
                archivo.write("-" * 50 + "\n")
                archivo.write(f"Subtotal:                    S/. {subtotal:>8.2f}\n")
                archivo.write(f"IGV (18%):                   S/. {igv:>8.2f}\n")
                archivo.write("=" * 50 + "\n")
                archivo.write(f"TOTAL:                       S/. {total:>8.2f}\n")
                archivo.write("=" * 50 + "\n\n")
                
                archivo.write("¡Gracias por su preferencia!\n")
                archivo.write("Wasi de Sabor Peruano\n")
                archivo.write("www.wasirestaurante.com\n")
            
            messagebox.showinfo("🖨️ Recibo Generado", 
                              f"Recibo guardado como: {nombre_archivo}\n\n"
                              f"📁 Ubicación: {os.path.abspath(nombre_archivo)}\n\n"
                              f"Puede abrir el archivo e imprimirlo desde cualquier editor de texto.")
            
        except Exception as e:
            messagebox.showerror("❌ Error", f"Error al generar el recibo:\n{str(e)}")

    def cancelar_pedido(self):
        """Cancela todo el pedido"""
        if not self.pedido:
            messagebox.showinfo("ℹ️ Información", "No hay pedido que cancelar.")
            return
            
        respuesta = messagebox.askyesno("❓ Confirmar", 
                                       "¿Está seguro de que desea cancelar todo el pedido?")
        if respuesta:
            self.pedido.clear()
            self.ver_pedido()
            messagebox.showinfo("✅ Pedido Cancelado", "El pedido ha sido cancelado exitosamente.")

def main():
    """Función principal para ejecutar la aplicación"""
    root = tk.Tk()
    
    # Configurar icono si existe
    try:
        root.iconbitmap('icono.ico')  # Opcional: agregar icono
    except:
        pass
    
    app = RestauranteWasi(root)
    
    # Centrar ventana al inicio
    root.after(100, app.centrar_ventana)
    
    # Inicializar mostrando el pedido vacío
    app.ver_pedido()
    
    root.mainloop()

if __name__ == '__main__':
    main()