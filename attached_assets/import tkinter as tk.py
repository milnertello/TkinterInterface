import tkinter as tk
from tkinter import ttk, messagebox

class RestauranteWasi:
    def __init__(self, root):
        self.root = root
        self.root.title("Restaurante Wasi de Sabor Peruano")
        self.root.geometry("800x700")
        self.root.configure(bg="#fff3e6")  # Color hueso

        self.menu = {
            "Ceviche": 25.00,
            "Lomo Saltado": 28.00,
            "Aji de Gallina": 22.00,
            "Anticuchos": 20.00,
            "Papa a la Huancaina": 10.00
        }
        self.pedido = {}

        self._crear_estilos()
        self._crear_interfaz()

    def _crear_estilos(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TButton", font=("Arial", 12, "bold"), padding=10)
        style.configure("TLabel", background="#fff3e6", font=("Arial", 12))
        style.configure("TCheckbutton", background="#fff3e6", font=("Arial", 11))

    def _crear_interfaz(self):
        titulo = tk.Label(self.root, text="Restaurante Wasi de Sabor Peruano",
                          font=("Arial", 22, "bold"), bg="#ff704d", fg="white", pady=15)
        titulo.pack(fill="x")

        marco_menu = tk.LabelFrame(self.root, text=".", bg="#ffe6cc", fg="#cc3300",
                                   font=("Arial", 14, "bold"), padx=15, pady=15, bd=5, relief="ridge")
        marco_menu.pack(padx=20, pady=20, fill="both", expand=True)

        self.items_vars = {}
        self.cantidad_vars = {}

        colores = ["#ff9999", "#ffcc66", "#99ffcc", "#66b3ff", "#ffb366"]

        for idx, (plato, precio) in enumerate(self.menu.items()):
            var = tk.IntVar()
            cant = tk.IntVar(value=1)

            fila = tk.Frame(marco_menu, bg=colores[idx % len(colores)], pady=5)
            fila.pack(fill="x", pady=5)

            tk.Checkbutton(fila, text=f"{plato} - S/. {precio:.2f}",
                           variable=var, bg=colores[idx % len(colores)],
                           font=("Arial", 12, "bold"), activebackground="#ffdfba").pack(side="left", padx=10)
            tk.Label(fila, text="Cantidad:", bg=colores[idx % len(colores)], font=("Arial", 11)).pack(side="left")
            tk.Entry(fila, textvariable=cant, width=4).pack(side="left", padx=5)

            self.items_vars[plato] = var
            self.cantidad_vars[plato] = cant

        boton_frame = tk.Frame(self.root, bg="#fff3e6")
        boton_frame.pack(pady=10)

        self._boton_colorido(boton_frame, "Agregar al Pedido", self.agregar_pedido).pack(side="left", padx=10)
        self._boton_colorido(boton_frame, "Ver Pedido", self.ver_pedido).pack(side="left", padx=10)

        self.texto_pedido = tk.Text(self.root, height=10, bg="#ffffe6", fg="#333", font=("Courier", 11), state="disabled", bd=4)
        self.texto_pedido.pack(padx=20, pady=10, fill="both", expand=True)

        botones_finales = tk.Frame(self.root, bg="#fff3e6")
        botones_finales.pack(pady=10)

        self._boton_colorido(botones_finales, "Finalizar Pedido", self.finalizar_pedido).pack(side="left", padx=20)
        self._boton_colorido(botones_finales, "Cancelar Todo", self.cancelar_pedido).pack(side="left", padx=20)

    def _boton_colorido(self, parent, texto, comando):
        boton = tk.Button(parent, text=texto, command=comando, font=("Arial", 12, "bold"),
                          bg="#ff8533", fg="white", activebackground="#cc5200", width=16, bd=3)
        boton.bind("<Enter>", lambda e: boton.config(bg="#ffa366"))
        boton.bind("<Leave>", lambda e: boton.config(bg="#ff8533"))
        return boton

    def agregar_pedido(self):
        for plato in self.menu:
            if self.items_vars[plato].get():
                cantidad = self.cantidad_vars[plato].get()
                if cantidad > 0:
                    self.pedido[plato] = self.pedido.get(plato, 0) + cantidad
        messagebox.showinfo("Pedido", "Producto(s) agregado(s) al pedido.")

    def ver_pedido(self):
        self.texto_pedido.config(state="normal")
        self.texto_pedido.delete(1.0, tk.END)

        if not self.pedido:
            self.texto_pedido.insert(tk.END, "No hay productos en el pedido.")
        else:
            subtotal = 0
            for plato, cantidad in self.pedido.items():
                precio = self.menu[plato] * cantidad
                self.texto_pedido.insert(tk.END, f"{plato} x{cantidad} - S/. {precio:.2f}\n")
                subtotal += precio

            igv = subtotal * 0.18
            total = subtotal + igv

            self.texto_pedido.insert(tk.END, f"\nSubtotal: S/. {subtotal:.2f}\n")
            self.texto_pedido.insert(tk.END, f"IGV (18%): S/. {igv:.2f}\n")
            self.texto_pedido.insert(tk.END, f"TOTAL: S/. {total:.2f}\n")

        self.texto_pedido.config(state="disabled")

    def finalizar_pedido(self):
        if not self.pedido:
            messagebox.showwarning("Aviso", "No hay productos en el pedido.")
            return
        messagebox.showinfo("Pedido Finalizado", "Gracias por su compra en Wasi de Sabor Peruano!")
        self.pedido.clear()
        self.ver_pedido()

    def cancelar_pedido(self):
        self.pedido.clear()
        self.ver_pedido()

if __name__ == '__main__':
    root = tk.Tk()
    app = RestauranteWasi(root)
    root.mainloop()
