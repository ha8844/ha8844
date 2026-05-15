import tkinter as tk
from tkinter import messagebox, ttk
import random
import json
import os
from datetime import datetime

class RPGTodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("RPG QUEST CHRONICLES - PIXEL TRAIL FIXED")
        self.root.geometry("1200x950") 
        
        # 스타일 및 색상 설정
        self.bg_color = "#000033"
        self.card_bg = "#111144"
        self.exp_bar_color = "#00FF7F" 
        self.font_main = ("Courier", 10, "bold")
        self.font_stat = ("Courier", 12, "bold")
        self.font_btn = ("Courier", 8, "bold")
        self.font_title = ("Courier", 18, "bold")
        self.save_file = "quest_chronicles.json"
        self.root.configure(bg=self.bg_color)

        # 1. 배경 캔버스 생성 (가장 먼저 생성하여 레이어 최하단에 배치)
        self.trail_canvas = tk.Canvas(self.root, bg=self.bg_color, highlightthickness=0, bd=0)
        self.trail_canvas.place(x=0, y=0, relwidth=1, relheight=1)

        # 2. 메인 UI 컨테이너 (캔버스 위에 배치됨)
        self.main_container = tk.Frame(self.root, bg="") # 투명 효과를 위해 bg 생략 시도 시 시스템 기본색이 나올 수 있어 처리
        self.main_container.place(relx=0.5, rely=0.5, anchor="center", relwidth=1, relheight=1)
        self.main_container.configure(bg=self.bg_color)

        # 스타일 설정
        self.style = ttk.Style()
        self.style.theme_use("default")
        self.style.configure("Exp.Horizontal.TProgressbar", troughcolor="#000066", background=self.exp_bar_color, thickness=20)
        self.style.configure("Treeview", background="#111144", foreground="white", fieldbackground="#111144", rowheight=25, font=("Courier", 9))
        self.style.configure("Treeview.Heading", background="#222266", foreground="white", font=("Courier", 10, "bold"))
        
        # 기본 데이터 초기화
        self.tasks = []
        self.completed_tasks = []
        self.current_exp = 0
        self.current_level = 1
        self.stat_points = 0
        self.stats = {"STR (힘)": 0, "DEX (민첩)": 0, "INT (지능)": 0}
        self.quest_types = ["일일퀘스트", "주간퀘스트", "월간퀘스트"]
        self.quest_config = {"일일퀘스트": {"exp": 20, "color": "#FFFFFF"}, "주간퀘스트": {"exp": 50, "color": "#FFCC00"}, "월간퀘스트": {"exp": 100, "color": "#FF00FF"}}
        
        self.current_sort_mode = "date"
        self.sort_date_desc = True 
        self.sort_content_asc = True
        self.honor_win = None 
        self.stat_timer = None 

        self.load_data() 
        self.setup_ui()
        self.spawn_static_objects()
        self.animate_monsters_loop()
        
        # 전역 마우스 움직임 감지
        self.root.bind("<Motion>", self.create_pixel_trail)

    def create_pixel_trail(self, event):
        """마우스 위치에 도트 파티클 생성"""
        colors = ["#FF00FF", "#00FFFF", "#FFFF00", "#FF0000", "#00FF00", "#FFFFFF"]
        color = random.choice(colors)
        size = random.randint(3, 6)
        
        # 절대 좌표 계산 (이벤트 발생 위젯 기준이 아닌 전체 창 기준)
        x = self.root.winfo_pointerx() - self.root.winfo_rootx()
        y = self.root.winfo_pointery() - self.root.winfo_rooty()
        
        pixel = self.trail_canvas.create_rectangle(x, y, x + size, y + size, fill=color, outline="")
        self.animate_pixel(pixel, 1.0)

    def animate_pixel(self, pixel, opacity):
        """도트 물리 효과"""
        if opacity <= 0:
            self.trail_canvas.delete(pixel)
            return
        self.trail_canvas.move(pixel, random.uniform(-1.5, 1.5), random.uniform(1, 4))
        self.root.after(30, lambda: self.animate_pixel(pixel, opacity - 0.1))

    def setup_ui(self):
        header = tk.Frame(self.main_container, bg=self.bg_color); header.pack(pady=10)
        self.title_label = tk.Label(header, text=f"<{self.get_title()}>", font=self.font_main, bg=self.bg_color, fg="#00FFFF"); self.title_label.pack()
        tk.Label(header, text="⚔️ HERO'S QUEST BOARD ⚔️", font=self.font_title, bg=self.bg_color, fg="#FFFF00").pack()

        sb_frame = tk.Frame(self.main_container, bg=self.bg_color); sb_frame.pack(pady=5)
        self.lvl_label = tk.Label(sb_frame, text=f"LV.{self.current_level}", font=("Courier", 14, "bold"), bg=self.bg_color, fg="#00FF00"); self.lvl_label.pack(side=tk.LEFT, padx=10)
        self.progress = ttk.Progressbar(sb_frame, length=600, mode='determinate', style="Exp.Horizontal.TProgressbar"); self.progress.pack(side=tk.LEFT); self.progress['value'] = self.current_exp

        input_frame = tk.Frame(self.main_container, bg=self.bg_color); input_frame.pack(pady=15)
        self.type_var = tk.StringVar(self.root); self.type_var.set("일일퀘스트")
        tk.OptionMenu(input_frame, self.type_var, *self.quest_types).config(font=("Courier", 10), width=12, bg="#111144", fg="white"); input_frame.winfo_children()[-1].pack(side=tk.LEFT, padx=5)
        self.task_entry = tk.Entry(input_frame, font=self.font_main, width=30); self.task_entry.pack(side=tk.LEFT, padx=5)
        self.task_entry.bind("<Return>", lambda event: self.add_quest())
        tk.Button(input_frame, text="퀘스트 수락!", font=self.font_main, bg="#00FF00", command=self.add_quest).pack(side=tk.LEFT, padx=2)
        tk.Button(input_frame, text="환생하기!", font=self.font_main, bg="#FF3333", fg="white", command=self.rebirth_game).pack(side=tk.LEFT, padx=2)

        self.board_frame = tk.Frame(self.main_container, bg=self.bg_color); self.board_frame.pack(fill="both", expand=True, padx=20, pady=10)
        self.sections = {}
        for idx, q_type in enumerate(self.quest_types):
            sec_outer = tk.Frame(self.board_frame, bg=self.bg_color, highlightthickness=1, highlightbackground="#333388")
            sec_outer.grid(row=0, column=idx, sticky="nsew", padx=5); self.board_frame.grid_columnconfigure(idx, weight=1)
            tk.Label(sec_outer, text=f"[{q_type}]", font=("Courier", 12, "bold"), bg="#222266", fg=self.quest_config[q_type]["color"]).pack(fill="x")
            container = tk.Frame(sec_outer, bg=self.bg_color); container.pack(fill="both", expand=True)
            canvas = tk.Canvas(container, bg=self.bg_color, highlightthickness=0); scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
            scroll_frame = tk.Frame(canvas, bg=self.bg_color); canvas.configure(yscrollcommand=scrollbar.set)
            scrollbar.pack(side="right", fill="y"); canvas.pack(side="left", fill="both", expand=True)
            win_id = canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
            scroll_frame.bind("<Configure>", lambda e, c=canvas: c.configure(scrollregion=c.bbox("all")))
            canvas.bind("<Configure>", lambda e, c=canvas, w=win_id: c.itemconfig(w, width=e.width))
            self.sections[q_type] = scroll_frame

        self.setup_status_window()
        self.render_tasks()

    def get_title(self):
        lvl = self.current_level
        if lvl < 20:
            return "[ 풋내기 모험가 ]"
        elif lvl < 40:
            return "[ 베테랑 용병 ]"
        elif lvl < 60:
            return "[ 왕실 수호기사 ]"
        elif lvl < 80:
            return "[ 대륙의 영웅 ]"
        elif lvl < 100:
            return "[ 신의 대리인 ]"
        else:
            return "[ 태초의 초월신 ]"

    def setup_status_window(self):
        self.stat_frame = tk.Frame(self.main_container, bg="#111133", highlightthickness=2, highlightbackground="#FFFF00")
        self.stat_frame.place(relx=0.5, y=580, width=450, height=160, anchor="n") 
        tk.Label(self.stat_frame, text="[ CHARACTER STATUS ]", font=self.font_stat, bg="#111133", fg="#FFFF00").pack(pady=2)
        self.point_label = tk.Label(self.stat_frame, text=f"사용 가능 포인트: {self.stat_points}", font=self.font_main, bg="#111133", fg="#00FF00"); self.point_label.pack()
        btn_container = tk.Frame(self.stat_frame, bg="#111133"); btn_container.pack(pady=5)
        self.stat_buttons = {}
        for s_name in self.stats:
            btn = tk.Button(btn_container, text=f"{s_name}: {self.stats[s_name]}", font=self.font_btn, bg="#222266", fg="white", width=12)
            btn.pack(side=tk.LEFT, padx=5)
            btn.bind("<ButtonPress-1>", lambda e, n=s_name: self.start_stat_upgrade(n))
            btn.bind("<ButtonRelease-1>", lambda e: self.stop_stat_upgrade())
            self.stat_buttons[s_name] = btn
        tk.Button(self.stat_frame, text="📜 명예의 전당 (연대기)", font=self.font_btn, bg="#8B4513", fg="white", command=self.show_honor_roll).pack(pady=5)

    def start_stat_upgrade(self, stat_name):
        self.upgrade_stat(stat_name)
        self.stat_timer = self.root.after(400, lambda: self._repeat_upgrade(stat_name))

    def _repeat_upgrade(self, stat_name):
        if self.stat_points > 0:
            self.upgrade_stat(stat_name)
            self.stat_timer = self.root.after(100, lambda: self._repeat_upgrade(stat_name))
        else:
            self.stop_stat_upgrade()

    def stop_stat_upgrade(self):
        if self.stat_timer:
            self.root.after_cancel(self.stat_timer)
            self.stat_timer = None

    def upgrade_stat(self, n):
        if self.stat_points > 0:
            self.stat_points -= 1
            self.stats[n] += 1
            self.update_status_ui()
            self.save_data()

    def update_status_ui(self):
        self.point_label.config(text=f"사용 가능 포인트: {self.stat_points}")
        for s, b in self.stat_buttons.items():
            b.config(text=f"{s}: {self.stats[s]}")

    def show_honor_roll(self):
        if self.honor_win and self.honor_win.winfo_exists(): self.honor_win.lift(); return
        self.honor_win = tk.Toplevel(self.root); self.honor_win.title("📜 HONOR ROLL"); self.honor_win.geometry("1000x650"); self.honor_win.configure(bg="#000022")
        ctrl_frame = tk.Frame(self.honor_win, bg="#000044"); ctrl_frame.pack(fill="x", padx=10, pady=10)
        self.filter_status_var = tk.StringVar(value="전체상태")
        tk.OptionMenu(ctrl_frame, self.filter_status_var, "전체상태", "퀘스트 진행중", "퀘스트 완료", command=lambda _: self.refresh_honor_list()).config(bg="#111166", fg="#00FF00", width=12); ctrl_frame.winfo_children()[-1].pack(side="left", padx=5)
        self.filter_type_var = tk.StringVar(value="전체분류")
        tk.OptionMenu(ctrl_frame, self.filter_type_var, "전체분류", *self.quest_types, command=lambda _: self.refresh_honor_list()).config(bg="#111166", fg="white", width=10); ctrl_frame.winfo_children()[-1].pack(side="left", padx=5)
        self.sort_content_btn = tk.Button(ctrl_frame, text="내용 정렬: ㄱㄴㄷ▼", bg="#222266", fg="white", command=self.toggle_content_sort); self.sort_content_btn.pack(side="left", padx=5)
        self.sort_date_btn = tk.Button(ctrl_frame, text="날짜 정렬: 최신순▼", bg="#333399", fg="white", command=self.toggle_date_sort); self.sort_date_btn.pack(side="right", padx=10)
        self.tree = ttk.Treeview(self.honor_win, columns=("상태", "분류", "내용", "수락일", "완료일"), show="headings", style="Treeview")
        for col in ("상태", "분류", "내용", "수락일", "완료일"): self.tree.heading(col, text=col); self.tree.column(col, width=120 if col=="상태" else 250 if col=="내용" else 150)
        self.tree.pack(fill="both", expand=True, padx=10, pady=5); self.refresh_honor_list()

    def refresh_honor_list(self):
        if not self.honor_win or not self.honor_win.winfo_exists(): return
        for item in self.tree.get_children(): self.tree.delete(item)
        all_data = []
        for t in self.tasks: d = dict(t); d["status"] = "퀘스트 진행중"; d["completed_at"] = "-"; all_data.append(d)
        for t in self.completed_tasks: d = dict(t); d["status"] = "퀘스트 완료"; all_data.append(d)
        s_filter = self.filter_status_var.get()
        if s_filter != "전체상태": all_data = [d for d in all_data if d["status"] == s_filter]
        t_filter = self.filter_type_var.get()
        if t_filter != "전체분류": all_data = [d for d in all_data if d["type"] == t_filter]
        if self.current_sort_mode == "content": all_data.sort(key=lambda x: x["content"], reverse=not self.sort_content_asc)
        else: all_data.sort(key=lambda x: x.get("completed_at") if x.get("completed_at") != "-" else x.get("accepted_at", ""), reverse=self.sort_date_desc)
        for d in all_data: self.tree.insert("", tk.END, values=(d["status"], d["type"], d["content"], d.get("accepted_at", "-"), d.get("completed_at", "-")))

    def toggle_date_sort(self):
        self.current_sort_mode = "date"; self.sort_date_desc = not self.sort_date_desc
        self.sort_date_btn.config(text="날짜 정렬: 최신순▼" if self.sort_date_desc else "날짜 정렬: 과거순▲"); self.refresh_honor_list()

    def toggle_content_sort(self):
        self.current_sort_mode = "content"; self.sort_content_asc = not self.sort_content_asc
        self.sort_content_btn.config(text="내용 정렬: ㄱㄴㄷ▼" if self.sort_content_asc else "내용 정렬: ㅎㅍㅌ▲"); self.refresh_honor_list()

    def complete_quest(self, i):
        q = self.tasks[i]; now = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.completed_tasks.append({"content": q["content"], "type": q["type"], "accepted_at": q.get("accepted_at", "-"), "completed_at": now})
        self.current_exp += self.quest_config[q["type"]]["exp"]
        while self.current_exp >= 100:
            self.current_level += 1; self.current_exp -= 100; self.stat_points += 3
            messagebox.showinfo("LEVEL UP!", f"🎉LV.{self.current_level} 달성!🎉")
            self.title_label.config(text=f"<{self.get_title()}>")
        del self.tasks[i]; self.update_stats_display(); self.render_tasks(); self.save_data(); self.refresh_honor_list()

    def add_quest(self):
        c = self.task_entry.get()
        if c.strip():
            now = datetime.now().strftime("%Y-%m-%d %H:%M")
            self.tasks.append({"content": c, "type": self.type_var.get(), "accepted_at": now})
            self.task_entry.delete(0, tk.END); self.render_tasks(); self.save_data(); self.refresh_honor_list()

    def render_tasks(self):
        for frame in self.sections.values():
            for widget in frame.winfo_children(): widget.destroy()
        for i, q in enumerate(self.tasks):
            f = tk.Frame(self.sections[q["type"]], bg=self.card_bg, highlightthickness=1, highlightbackground="white"); f.pack(fill="x", pady=4, padx=5)
            tk.Label(f, text=f"⚔️ {q['content']}", fg=self.quest_config[q["type"]]["color"], bg=self.card_bg, font=self.font_main, wraplength=220, justify="left").pack(anchor="w", padx=5, pady=5)
            tk.Label(f, text=f"EXP: +{self.quest_config[q['type']]['exp']}", fg="#FFD700", bg=self.card_bg, font=("Courier", 9, "bold")).pack(anchor="w", padx=5)
            btn_row = tk.Frame(f, bg=self.card_bg); btn_row.pack(fill="x", padx=5, pady=2)
            tk.Button(btn_row, text="퀘스트 완료", command=lambda idx=i: self.complete_quest(idx), font=self.font_btn, bg="#228B22", fg="white").pack(side="left", padx=2)
            tk.Button(btn_row, text="퀘스트 포기", command=lambda idx=i: self.delete_quest(idx), font=self.font_btn, bg="#FF3333", fg="white").pack(side="left", padx=2)
            tk.Label(f, text=f"수락: {q.get('accepted_at', '-')}", fg="#777777", bg=self.card_bg, font=("Courier", 7)).pack(anchor="e", padx=5)

    def rebirth_game(self):
        if messagebox.askyesno("환생", "환생(초기화) 하시겠습니까?"):
            self.current_level, self.current_exp, self.stat_points = 1, 0, 0
            self.stats = {k: 0 for k in self.stats}; self.completed_tasks = []; self.tasks = []
            self.update_stats_display(); self.render_tasks(); self.save_data(); self.refresh_honor_list()

    def update_stats_display(self):
        self.lvl_label.config(text=f"LV.{self.current_level}"); self.progress['value'] = self.current_exp; self.update_status_ui()

    def delete_quest(self, i): del self.tasks[i]; self.render_tasks(); self.save_data(); self.refresh_honor_list()

    def spawn_static_objects(self):
        tk.Label(self.main_container, text="🤴", font=("Courier", 35), bg=self.bg_color, fg="#87CEEB").place(x=20, y=810)
        tk.Label(self.main_container, text="👸", font=("Courier", 35), bg=self.bg_color, fg="#FF69B4").place(x=1100, y=810)
        tk.Label(self.main_container, text="🎁", font=("Courier", 60), bg=self.bg_color, fg="#FFD700").place(x=1085, y=855)

    def animate_monsters_loop(self):
        self.monster_labels = []
        self.monsters_data = [{"icon": "👾", "color": "#FF3333", "x": 400, "y": 810, "speed": 3, "dir": 1, "jump": 0}, {"icon": "🦖", "color": "#FFFF00", "x": 450, "y": 830, "speed": 5, "dir": 1, "jump": 0}, {"icon": "👻", "color": "#00FF00", "x": 750, "y": 810, "speed": 2, "dir": -1, "jump": 0}, {"icon": "🐍", "color": "#FF00FF", "x": 550, "y": 820, "speed": 4, "dir": -1, "jump": 0}, {"icon": "🕷️", "color": "#808080", "x": 500, "y": 825, "speed": 6, "dir": 1, "jump": 0}, {"icon": "🧙‍♂️", "color": "#0000FF", "x": 600, "y": 815, "speed": 2, "dir": -1, "jump": 0}, {"icon": "🧛‍♂️", "color": "#800000", "x": 700, "y": 835, "speed": 4, "dir": -1, "jump": 0}, {"icon": "🤖", "color": "#C0C0C0", "x": 650, "y": 820, "speed": 3, "dir": 1, "jump": 0}]
        def update():
            for i, m in enumerate(self.monsters_data):
                m["x"] += (m["speed"] * m["dir"]); m["y"] += m["jump"]; m["jump"] += 1.5
                if m["x"] > 1020 or m["x"] < 150: m["dir"] *= -1
                base_y = 810 if i % 2 == 0 else 830
                if m["y"] >= base_y: m["y"] = base_y; m["jump"] = 0
                if m["y"] == base_y and random.random() < 0.03: m["jump"] = -12
                if len(self.monster_labels) <= i:
                    lbl = tk.Label(self.main_container, text=m["icon"], font=("Courier", 20), bg=self.bg_color, fg=m["color"]); lbl.place(x=m["x"], y=m["y"]); self.monster_labels.append(lbl)
                else: self.monster_labels[i].place(x=m["x"], y=m["y"])
            self.root.after(30, update)
        update()

    def save_data(self):
        d = {"level": self.current_level, "exp": self.current_exp, "tasks": self.tasks, "stat_points": self.stat_points, "stats": self.stats, "completed": self.completed_tasks}
        with open(self.save_file, "w", encoding="utf-8") as f: json.dump(d, f, ensure_ascii=False, indent=4)

    def load_data(self):
        if os.path.exists(self.save_file):
            try:
                with open(self.save_file, "r", encoding="utf-8") as f:
                    d = json.load(f); self.current_level = d.get("level", 1); self.current_exp = d.get("exp", 0)
                    self.tasks = d.get("tasks", []); self.stat_points = d.get("stat_points", 0)
                    self.stats = d.get("stats", {"STR (힘)": 0, "DEX (민첩)": 0, "INT (지능)": 0}); self.completed_tasks = d.get("completed", [])
            except: pass

if __name__ == "__main__":
    root = tk.Tk(); app = RPGTodoApp(root); root.mainloop()
