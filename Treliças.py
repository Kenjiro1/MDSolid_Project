import tkinter as tk
from tkinter import messagebox
import numpy as np
import math

class TrussApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Estruturas 2D - Método dos Nós")
        self.root.geometry("1000x700")

        # Dados estruturais
        self.nodes = []    # Lista de tuplas (x, y)
        self.members = []  # Lista de tuplas (node_idx1, node_idx2)
        
        # Controle de desenho
        self.drawing = False
        self.start_point = None
        self.current_mouse = None
        self.snap_radius = 15  # Raio em pixels para unir nós

        # --- Layout da Interface ---
        # Painel Superior (Controles)
        self.control_frame = tk.Frame(root, bg="#f0f0f0", height=50)
        self.control_frame.pack(side=tk.TOP, fill=tk.X)

        self.btn_calc = tk.Button(self.control_frame, text="Calcular Estabilidade", command=self.calculate_stability, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
        self.btn_calc.pack(side=tk.LEFT, padx=10, pady=10)

        self.btn_clear = tk.Button(self.control_frame, text="Limpar Tudo", command=self.clear_all, bg="#f44336", fg="white", font=("Arial", 10))
        self.btn_clear.pack(side=tk.LEFT, padx=10, pady=10)

        self.lbl_info = tk.Label(self.control_frame, text="Clique e arraste para desenhar barras. Nós próximos se conectam automaticamente.", bg="#f0f0f0", font=("Arial", 9))
        self.lbl_info.pack(side=tk.LEFT, padx=20)

        # Canvas para o plano cartesiano
        self.canvas = tk.Canvas(root, bg="white", cursor="cross")
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Painel Inferior (Resultados)
        self.result_frame = tk.Frame(root, bg="#333", height=120)
        self.result_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.txt_results = tk.Text(self.result_frame, bg="#222", fg="#00FF00", font=("Consolas", 10), height=7)
        self.txt_results.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.txt_results.insert(tk.END, "Resultados da análise estrutural aparecerão aqui...\n")
        self.txt_results.config(state=tk.DISABLED)

        # Eventos do Mouse
        self.canvas.bind("<Button-1>", self.on_mouse_down)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_up)
        
        # Desenhar grade inicial
        self.draw_grid()

    def draw_grid(self):
        self.canvas.delete("grid")
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        if w < 10: w = 1000
        if h < 10: h = 550

        # Linhas de grade a cada 50 pixels
        for x in range(0, w, 50):
            self.canvas.create_line(x, 0, x, h, fill="#f0f0f0", tags="grid")
        for y in range(0, h, 50):
            self.canvas.create_line(0, y, w, y, fill="#f0f0f0", tags="grid")

    def get_or_create_node(self, x, y):
        """Verifica se já existe um nó próximo. Se sim, retorna o índice. Senão, cria um novo."""
        for idx, (nx, ny) in enumerate(self.nodes):
            dist = math.hypot(nx - x, ny - y)
            if dist <= self.snap_radius:
                return idx
        # Criar novo nó
        self.nodes.append((x, y))
        return len(self.nodes) - 1

    def on_mouse_down(self, event):
        self.drawing = True
        # Aplicar snap no ponto inicial se houver nó perto
        x, y = event.x, event.y
        for nx, ny in self.nodes:
            if math.hypot(nx - x, ny - y) <= self.snap_radius:
                x, y = nx, ny
                break
        self.start_point = (x, y)
        self.current_mouse = (x, y)

    def on_mouse_drag(self, event):
        if not self.drawing:
            return
        x, y = event.x, event.y
        # Snap preview
        for nx, ny in self.nodes:
            if math.hypot(nx - x, ny - y) <= self.snap_radius:
                x, y = nx, ny
                break
        self.current_mouse = (x, y)
        self.redraw()
        # Desenhar linha temporária de arrasto
        self.canvas.create_line(self.start_point[0], self.start_point[1], x, y, fill="blue", dash=(4, 2), tags="temp")

    def on_mouse_up(self, event):
        if not self.drawing:
            return
        self.drawing = False
        end_x, end_y = event.x, event.y

        # Snap no ponto final
        for nx, ny in self.nodes:
            if math.hypot(nx - end_x, ny - end_y) <= self.snap_radius:
                end_x, end_y = nx, ny
                break

        # Evitar barras de comprimento zero
        if math.hypot(self.start_point[0] - end_x, self.start_point[1] - end_y) > 10:
            n1 = self.get_or_create_node(self.start_point[0], self.start_point[1])
            n2 = self.get_or_create_node(end_x, end_y)
            
            if n1 != n2:
                # Verificar se a barra já existe
                member = tuple(sorted((n1, n2)))
                if member not in self.members:
                    self.members.append(member)

        self.redraw()

    def redraw(self):
        self.canvas.delete("element")
        self.draw_grid()

        # Desenhar membros (barras)
        for n1, n2 in self.members:
            x1, y1 = self.nodes[n1]
            x2, y2 = self.nodes[n2]
            self.canvas.create_line(x1, y1, x2, y2, width=3, fill="#333333", tags="element")

        # Desenhar nós
        for idx, (x, y) in enumerate(self.nodes):
            color = "#FF5722" if idx < 2 else "#2196F3"  # Destacar os dois primeiros nós como apoios
            r = 6
            self.canvas.create_oval(x - r, y - r, x + r, y + r, fill=color, outline="black", width=1, tags="element")
            self.canvas.create_text(x, y - 12, text=f"N{idx}", font=("Arial", 8, "bold"), tags="element")

    def clear_all(self):
        self.nodes.clear()
        self.members.clear()
        self.redraw()
        self.print_result("Estrutura limpa.")

    def print_result(self, text):
        self.txt_results.config(state=tk.NORMAL)
        self.txt_results.delete("1.0", tk.END)
        self.txt_results.insert(tk.END, text)
        self.txt_results.config(state=tk.DISABLED)

    def calculate_stability(self):
        j = len(self.nodes)
        m = len(self.members)
        
        if j == 0 or m == 0:
            messagebox.showwarning("Aviso", "Desenhe pelo menos uma estrutura com nós e barras!")
            return

        # Consideramos 3 reações de apoio padrão para uma treliça planar isostática apoiada nos nós 0 e 1 (se existirem)
        r = 3 

        # Critério de Maxwell para Treliças Planares: m + r >= 2j
        # Condição necessária para estabilidade estática externa e interna
        maxwell_val = m + r
        eq_val = 2 * j

        report = []
        report.append(f"--- ANÁLISE ESTÁTICA E ESTABILIDADE (Método dos Nós) ---")
        report.append(f"Número de Nós (j): {j}")
        report.append(f"Número de Barras (m): {m}")
        report.append(f"Reações de Apoio estimadas (r): {r}")
        report.append(f"Equações de Equilíbrio disponíveis (2j): {eq_val}")
        report.append(f"Graus de liberdade internos/externos (m + r): {maxwell_val}\n")

        if maxwell_val < eq_val:
            report.append("STATUS: HIPOSTÁTICA (Instável!)")
            report.append("-> A estrutura possui menos barras do que o necessário e irá desabar/mecanismo.")
        elif maxwell_val == eq_val:
            report.append("STATUS: ISOSTÁTICA (Estática e Determinada)")
            report.append("-> A estrutura é perfeitamente estável e as forças nas barras podem ser resolvidas exatamente.")
        else:
            report.append("STATUS: HIPERSTÁTICA (Estável e Indeterminada)")
            report.append(f"-> A estrutura possui excesso de {maxwell_val - eq_val} grau(s) de redundância estrutural.")

        # Montagem matricial simplificada para verificação do posto da matriz de incidência (Equilíbrio dos Nós)
        try:
            # Dimensões da matriz de equilíbrio: 2j linhas (equilíbrios Fx, Fy por nó) x (m + r colunas)
            A = np.zeros((2 * j, m + r))
            
            for idx, (n1, n2) in enumerate(self.members):
                x1, y1 = self.nodes[n1]
                x2, y2 = self.nodes[n2]
                L = math.hypot(x2 - x1, y2 - y1)
                if L == 0: continue
                
                cos_theta = (x2 - x1) / L
                sin_theta = (y2 - y1) / L
                
                # Contribuição da barra para o nó n1
                A[2 * n1, idx] = cos_theta
                A[2 * n1 + 1, idx] = sin_theta
                
                # Contribuição da barra para o nó n2 (direção oposta)
                A[2 * n2, idx] = -cos_theta
                A[2 * n2 + 1, idx] = -sin_theta

            # Adicionando reações de apoio fictícias nos nós 0 e 1 para teste de posto
            # Nó 0: fixo (Rx_0, Ry_0) -> colunas m e m+1
            if j > 0:
                A[0, m] = 1.0     # Fx no nó 0
                A[1, m + 1] = 1.0 # Fy no nó 0
            # Nó 1: 1º gênero (Ry_1) -> coluna m+2
            if j > 1:
                A[2 * 1 + 1, m + 2] = 1.0 # Fy no nó 1

            rank = np.linalg.matrix_rank(A)
            report.append(f"\n[Análise de Posto da Matriz do Sistema]")
            report.append(f"Posto da Matriz A: {rank} de {m + r} incógnitas.")
            if rank < m + r:
                report.append("-> Alerta: A matriz é singular ou há mecanismos internos de instabilidade geométrica.")
            else:
                report.append("-> A matriz estrutural possui posto completo.")

        except Exception as e:
            report.append(f"\nErro no cálculo matricial: {str(e)}")

        self.print_result("\n".join(report))

if __name__ == "__main__":
    root = tk.Tk()
    app = TrussApp(root)
    root.mainloop()