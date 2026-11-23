import tkinter as tk
from tkinter import messagebox
import random
import time

#συνοπτικά οι αριθμοί στα payouts όπως και οι ονομασίες των strings και των class που δημιούργησα πήρα την πηγή και τα ονόματα τους από εργαλείο τεχνητής νοημοσύνης, ενώ η έρευνα για τη δημιουργία του κώδικα έγινε στο ίντερνετ. 
PAYOUTS = {
    1: {1: 2.5},
    2: {1: 1, 2: 5},
    3: {2: 2.5, 3: 25},
    4: {2: 1, 3: 4, 4: 100},
    5: {3: 2, 4: 20, 5: 450},
    6: {3: 1, 4: 7, 5: 50, 6: 1600},
    7: {3: 1, 4: 3, 5: 20, 6: 100, 7: 5000},
    8: {4: 2, 5: 10, 6: 50, 7: 1000, 8: 15000},
    9: {4: 1, 5: 5, 6: 25, 7: 200, 8: 4000, 9: 40000},
    10: {0: 2, 5: 2, 6: 20, 7: 80, 8: 500, 9: 10000, 10: 100000},
    11: {0: 2, 5: 1, 6: 10, 7: 50, 8: 250, 9: 1500, 10: 15000, 11: 500000},
    12: {0: 4, 6: 5, 7: 25, 8: 150, 9: 1000, 10: 2500, 11: 25000, 12: 1000000}
}

MONTHS_GR = ["ΙΑΝ", "ΦΕΒ", "ΜΑΡ", "ΑΠΡ", "ΜΑΙ", "ΙΟΥΝ", "ΙΟΥΛ", "ΑΥΓ", "ΣΕΠ", "ΟΚΤ", "ΝΟΕ", "ΔΕΚ"]

def generate_kino_numbers():
    return random.sample(range(1, 81), 20)

#Οποιοδήποτε νούμερο επιλέχθηκε ήταν τυχαίο με βάση μια εικόνα jpg από το google για να μοιάζει με live εκείνη την ώρα σαν αληθινή ροή
#Τα χρώματα και το γραφικό περιβάλλον τα βρήκε ένα εργαλείο τεχνητής νοημοσύνης με βάση την εικόνα jpeg για να μπορέσω να είμαι πιο ακριβής. Πιο συγκεκριμένα το https://tailwindcss.com/
class KinoAuthenticApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ΚΙΝΟ")
        self.root.geometry("960x620")
        self.root.configure(bg="#f59e0b")

        self.selected_numbers = []
        self.is_drawing = False
        self.draw_id = 599281
        self.cells = {}
        self.bet_var = tk.StringVar(value="0.50")

        self.canvas = tk.Canvas(self.root, width=960, height=620, bg="#f59e0b", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.draw_gold_backdrop()
        self.draw_kino_screen()
        self.build_controls()
        self.update_live_clock()

    def draw_gold_backdrop(self):
        self.canvas.create_rectangle(0, 0, 960, 620, fill="#e69500", outline="")
        self.canvas.create_oval(-80, -80, 420, 420, fill="#fbbf24", outline="")
        self.canvas.create_oval(580, 220, 1080, 720, fill="#fbbf24", outline="")
        self.canvas.create_oval(220, 80, 740, 540, fill="#fcd34d", outline="")

    def draw_kino_screen(self):
        self.canvas.create_rectangle(42, 25, 918, 538, fill="#06101a", outline="#03080e", width=3)
        self.canvas.create_rectangle(48, 31, 912, 532, fill="#0c2033", outline="#1e3a5f", width=2)

        self.canvas.create_text(115, 50, text="ΩΡΑ ΚΛΗΡΩΣΗΣ", fill="#8faec9", font=("Arial", 8, "bold"))
        now_str = time.strftime("%H:%M")
        self.draw_time_id = self.canvas.create_text(115, 73, text=now_str, fill="#ffffff", font=("Arial", 22, "bold"))

        self.canvas.create_text(255, 50, text="ΚΛΗΡΩΣΗ", fill="#8faec9", font=("Arial", 8, "bold"))
        self.draw_num_id = self.canvas.create_text(255, 73, text=str(self.draw_id), fill="#ffffff", font=("Arial", 22, "bold"))

	#Η εικόνα επιλέχθηκε από το google όπου και κατέβηκε στα αρχεία
        self.kino_logo = tk.PhotoImage(file="Kino.png")
        self.kino_logo = self.kino_logo.subsample(3, 3)
        self.canvas.create_image(480, 68, image=self.kino_logo)

        self.canvas.create_rectangle(685, 48, 725, 92, fill="#0b1b2b", outline="#8faec9", width=2)
        self.canvas.create_rectangle(685, 48, 725, 62, fill="#8faec9", outline="")
        month_txt = MONTHS_GR[int(time.strftime("%m")) - 1]
        day_txt = str(int(time.strftime("%d")))
        self.canvas.create_text(705, 55, text=month_txt, fill="#0b1b2b", font=("Arial", 7, "bold"))
        self.canvas.create_text(705, 77, text=day_txt, fill="#ffffff", font=("Arial", 14, "bold"))

        self.clock_id = self.canvas.create_text(815, 71, text=time.strftime("%H:%M:%S"), fill="#ffffff", font=("Arial", 24, "bold"))

        self.canvas.create_rectangle(70, 106, 890, 114, fill="#06101a", outline="#1e3a5f", width=1)
        self.progress_bar = self.canvas.create_rectangle(71, 107, 71, 113, fill="#38bdf8", outline="")

        start_x = 110
        start_y = 148
        step_x = 82
        step_y = 48

        for num in range(1, 81):
            row = (num - 1) // 10
            col = (num - 1) % 10
            cx = start_x + col * step_x
            cy = start_y + row * step_y

            oval_outer = self.canvas.create_oval(
                cx - 30, cy - 18, cx + 30, cy + 18,
                fill="", outline="", width=2,
                tags=("cell_" + str(num),)
            )
            oval_inner = self.canvas.create_oval(
                cx - 27, cy - 15, cx + 27, cy + 15,
                fill="", outline="", width=0,
                tags=("cell_" + str(num),)
            )
            txt = self.canvas.create_text(
                cx, cy, text=str(num), fill="#6b8cae",
                font=("Arial", 18, "bold"),
                tags=("cell_" + str(num),)
            )
            self.cells[num] = (oval_outer, oval_inner, txt)
            self.canvas.tag_bind("cell_" + str(num), "<Button-1>", lambda e, n=num: self.toggle_number(n))

    def build_controls(self):
        bar = tk.Frame(self.root, bg="#0b1b2b", highlightbackground="#03080e", highlightthickness=2)
        self.canvas.create_window(45, 550, window=bar, anchor="nw", width=870, height=54)

        self.lbl_count = tk.Label(bar, text="Επιλογές: 0/12", bg="#0b1b2b", fg="#38bdf8", font=("Arial", 11, "bold"))
        self.lbl_count.pack(side="left", padx=12)

        tk.Label(bar, text="Ποσό (€):", bg="#0b1b2b", fg="white", font=("Arial", 10)).pack(side="left")
        bet_menu = tk.OptionMenu(bar, self.bet_var, "0.50", "1.00", "2.00", "5.00", "10.00")
        bet_menu.config(bg="#1e293b", fg="#facc15", font=("Arial", 10, "bold"), highlightthickness=0, bd=1)
        bet_menu["menu"].config(bg="#1e293b", fg="white")
        bet_menu.pack(side="left", padx=6)

        self.btn_quick = tk.Button(
            bar, text="Τυχαία", bg="#1e3a5f", fg="white", font=("Arial", 10, "bold"),
            relief="flat", cursor="hand2", command=self.quick_pick
        )
        self.btn_quick.pack(side="left", padx=5, ipady=3, ipadx=8)

        self.btn_clear = tk.Button(
            bar, text="Καθαρισμός", bg="#1e3a5f", fg="white", font=("Arial", 10, "bold"),
            relief="flat", cursor="hand2", command=self.clear_board
        )
        self.btn_clear.pack(side="left", padx=5, ipady=3, ipadx=8)

        self.btn_draw = tk.Button(
            bar, text="ΚΛΗΡΩΣΗ", bg="#dc2626", fg="white", font=("Arial", 12, "bold"),
            relief="flat", cursor="hand2", state="disabled", command=self.start_draw
        )
        self.btn_draw.pack(side="right", padx=12, ipady=4, ipadx=14)

        self.lbl_status = tk.Label(
            bar, text="Επιλέξτε 1-12 αριθμούς", bg="#0b1b2b", fg="#facc15", font=("Arial", 11, "bold")
        )
        self.lbl_status.pack(side="right", padx=12)

    def update_live_clock(self):
        self.canvas.itemconfig(self.clock_id, text=time.strftime("%H:%M:%S"))
        self.root.after(1000, self.update_live_clock)

    def set_cell_style(self, num, style):
        oval_outer, oval_inner, txt = self.cells[num]
        if style == "default":
            self.canvas.itemconfig(oval_outer, fill="", outline="")
            self.canvas.itemconfig(oval_inner, fill="", outline="")
            self.canvas.itemconfig(txt, fill="#6b8cae")
        elif style == "selected":
            self.canvas.itemconfig(oval_outer, fill="#133250", outline="#38bdf8", width=2)
            self.canvas.itemconfig(oval_inner, fill="", outline="")
            self.canvas.itemconfig(txt, fill="#e0f2fe")
        elif style == "gold":
            # Χρυσό οβάλ (όπως τα 2, 6, 7, 10, 15 κλπ στην εικόνα)
            self.canvas.itemconfig(oval_outer, fill="#ca8a04", outline="#fef08a", width=2)
            self.canvas.itemconfig(oval_inner, fill="#facc15", outline="")
            self.canvas.itemconfig(txt, fill="#111827")
        elif style == "red":
            # Κόκκινο οβάλ (όπως το 73 στην εικόνα)
            self.canvas.itemconfig(oval_outer, fill="#991b1b", outline="#fca5a5", width=2)
            self.canvas.itemconfig(oval_inner, fill="#dc2626", outline="")
            self.canvas.itemconfig(txt, fill="#ffffff")

    def reset_visuals(self):
        self.canvas.coords(self.progress_bar, 71, 107, 71, 113)
        for num in range(1, 81):
            if num in self.selected_numbers:
                self.set_cell_style(num, "selected")
            else:
                self.set_cell_style(num, "default")

    def toggle_number(self, num):
        if self.is_drawing:
            return
        self.reset_visuals()
        if num in self.selected_numbers:
            self.selected_numbers.remove(num)
            self.set_cell_style(num, "default")
        else:
            if len(self.selected_numbers) >= 12:
                messagebox.showwarning("Όριο", "Μπορείτε να επιλέξετε έως 12 αριθμούς.")
                return
            self.selected_numbers.append(num)
            self.set_cell_style(num, "selected")
        self.update_controls()

    def update_controls(self):
        c = len(self.selected_numbers)
        self.lbl_count.config(text="Επιλογές: " + str(c) + "/12")
        if c > 0:
            self.btn_draw.config(state="normal", bg="#dc2626")
            self.lbl_status.config(text="Παιχνίδι " + str(c) + " αριθμών")
        else:
            self.btn_draw.config(state="disabled", bg="#475569")
            self.lbl_status.config(text="Επιλέξτε 1-12 αριθμούς")

    def clear_board(self):
        if self.is_drawing:
            return
        self.selected_numbers = []
        self.reset_visuals()
        self.update_controls()

    def quick_pick(self):
        if self.is_drawing:
            return
        count = len(self.selected_numbers) if len(self.selected_numbers) > 0 else 5
        self.clear_board()
        self.selected_numbers = random.sample(range(1, 81), count)
        for num in self.selected_numbers:
            self.set_cell_style(num, "selected")
        self.update_controls()

    def start_draw(self):
        if self.is_drawing or not self.selected_numbers:
            return
        self.is_drawing = True
        self.btn_draw.config(state="disabled", bg="#475569")
        self.btn_quick.config(state="disabled")
        self.btn_clear.config(state="disabled")
        self.reset_visuals()

        self.draw_id += 1
        self.canvas.itemconfig(self.draw_num_id, text=str(self.draw_id))
        self.canvas.itemconfig(self.draw_time_id, text=time.strftime("%H:%M"))
        self.lbl_status.config(text="Κλήρωση σε εξέλιξη...")

        kino_numbers = generate_kino_numbers()
        self.animate_step(kino_numbers, 0, None)

    def animate_step(self, kino_numbers, idx, prev_num):
        if idx < len(kino_numbers):
            if prev_num is not None and prev_num not in self.selected_numbers:
                self.set_cell_style(prev_num, "gold")

            num = kino_numbers[idx]
            self.set_cell_style(num, "red")

            bar_width = 71 + int(((idx + 1) / 20.0) * (889 - 71))
            self.canvas.coords(self.progress_bar, 71, 107, bar_width, 113)

            self.root.after(400, lambda: self.animate_step(kino_numbers, idx + 1, num))
        else:
            winning = set(kino_numbers).intersection(set(self.selected_numbers))
            hits = len(winning)
            game_type = len(self.selected_numbers)
            bet = float(self.bet_var.get())
            multiplier = PAYOUTS.get(game_type, {}).get(hits, 0)
            winnings = round(bet * multiplier, 2)

            self.lbl_status.config(text="Επιτυχίες: " + str(hits) + "/" + str(game_type) + " | Κέρδη: " + ("%.2f" % winnings) + " €")
            self.is_drawing = False
            self.btn_draw.config(state="normal", bg="#dc2626")
            self.btn_quick.config(state="normal")
            self.btn_clear.config(state="normal")

if __name__ == "__main__":
    root = tk.Tk()
    app = KinoAuthenticApp(root)
    root.mainloop()