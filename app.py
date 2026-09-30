"""Сараптамалық жүйе «Киберқылмыстардың құқықтық квалификаторы» (Tkinter)."""
import tkinter as tk
from tkinter import ttk

from rules import FLAGS, SCENARIOS, qualify, format_verdict


class CyberLawApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        root.title("Сараптамалық жүйе: киберқылмыстарды квалификациялау (ҚР ҚК)")
        root.geometry("820x900")

        ttk.Label(root, text="Оқиғаны талдау және құқықтық бағалау",
                  font=("Arial", 14, "bold")).pack(pady=8)

        # --- дайын сценарийлер (тестілеу және скриншот үшін ыңғайлы)
        top = ttk.Frame(root)
        top.pack(fill="x", padx=15)
        ttk.Label(top, text="Дайын сценарий:").pack(side="left")
        self.scenario = ttk.Combobox(top, values=list(SCENARIOS), state="readonly", width=40)
        self.scenario.pack(side="left", padx=8)
        ttk.Button(top, text="Жүктеу", command=self.load_scenario).pack(side="left")

        # --- белгілер
        frame = ttk.LabelFrame(root, text="Оқиға параметрлері")
        frame.pack(fill="x", padx=15, pady=10)
        self.vars = {}
        for key, text in FLAGS:
            self.vars[key] = tk.BooleanVar()
            ttk.Checkbutton(frame, text=text, variable=self.vars[key]).pack(anchor="w", padx=8, pady=2)

        # --- батырмалар
        btns = ttk.Frame(root)
        btns.pack(pady=6)
        ttk.Button(btns, text="Оқиғаны квалификациялау", command=self.analyze).pack(side="left", padx=5)
        ttk.Button(btns, text="Тазалау", command=self.reset).pack(side="left", padx=5)

        # --- нәтиже
        out = ttk.LabelFrame(root, text="Қорытынды")
        out.pack(fill="both", expand=True, padx=15, pady=10)
        self.text = tk.Text(out, wrap="word", font=("Consolas", 10), height=18)
        scroll = ttk.Scrollbar(out, command=self.text.yview)
        self.text.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y")
        self.text.pack(fill="both", expand=True)

    def selected(self) -> set:
        """Белгіленген белгілердің жиынын қайтарады."""
        return {k for k, v in self.vars.items() if v.get()}

    def load_scenario(self):
        """Таңдалған дайын сценарийді жүктейді."""
        name = self.scenario.get()
        if not name:
            return
        for k, var in self.vars.items():
            var.set(k in SCENARIOS[name])
        self.analyze()

    def analyze(self):
        """Оқиғаны квалификациялап, нәтижені шығарады."""
        verdict = qualify(self.selected())
        self.text.delete("1.0", "end")
        self.text.insert("end", format_verdict(verdict))

    def reset(self):
        """Барлық белгілерді тазалайды."""
        for var in self.vars.values():
            var.set(False)
        self.scenario.set("")
        self.text.delete("1.0", "end")


if __name__ == "__main__":
    root = tk.Tk()
    CyberLawApp(root)
    root.mainloop()
