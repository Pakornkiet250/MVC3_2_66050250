import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

from db import init_db, seed_data
from models.auth_model import AuthModel
from models.promise_model import PromiseModel
from models.update_model import PromiseUpdateModel
from models.politician_model import PoliticianModel


class GuiApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Promise Tracker")
        self.geometry("800x500")
        self.username = None
        self.role = None
        self._build_login()

    def _build_login(self):
        for w in self.winfo_children():
            w.destroy()

        frm = ttk.Frame(self, padding=20)
        frm.pack(expand=True)

        ttk.Label(frm, text="Role:").grid(row=0, column=0, sticky="w")
        self.role_var = tk.StringVar(value="USER")
        role_cb = ttk.Combobox(frm, textvariable=self.role_var, values=["USER", "ADMIN"], state="readonly")
        role_cb.grid(row=0, column=1, sticky="w")

        ttk.Label(frm, text="Username:").grid(row=1, column=0, sticky="w")
        self.user_entry = ttk.Entry(frm)
        self.user_entry.grid(row=1, column=1, sticky="w")

        ttk.Label(frm, text="Password:").grid(row=2, column=0, sticky="w")
        self.pw_entry = ttk.Entry(frm, show="*")
        self.pw_entry.grid(row=2, column=1, sticky="w")

        login_btn = ttk.Button(frm, text="Login", command=self._do_login)
        login_btn.grid(row=3, column=0, columnspan=2, pady=10)

    def _do_login(self):
        username = self.user_entry.get().strip()
        password = self.pw_entry.get().strip()
        role = self.role_var.get()

        user = AuthModel.login(username, password)
        if not user or user[1] != role:
            messagebox.showerror("Login failed", f"Login failed for role {role}.")
            return

        self.username = username
        self.role = role
        self._build_main_menu()

    def _build_main_menu(self):
        for w in self.winfo_children():
            w.destroy()

        toolbar = ttk.Frame(self, padding=10)
        toolbar.pack(fill="x")

        ttk.Label(toolbar, text=f"Logged in: {self.username} ({self.role})").pack(side="left")
        ttk.Button(toolbar, text="All Promises", command=self.show_all_promises).pack(side="left", padx=6)
        ttk.Button(toolbar, text="Promise by ID", command=self._ask_promise_id).pack(side="left", padx=6)
        ttk.Button(toolbar, text="Politicians", command=self.show_politicians).pack(side="left", padx=6)
        if self.role == "ADMIN":
            ttk.Button(toolbar, text="Add Update (by ID)", command=self._ask_add_update).pack(side="left", padx=6)
        ttk.Button(toolbar, text="Logout", command=self._logout).pack(side="right")

        self.content = ttk.Frame(self, padding=10)
        self.content.pack(fill="both", expand=True)

        ttk.Label(self.content, text="Welcome to Promise Tracker GUI", font=(None, 14)).pack(pady=20)

    def _clear_content(self):
        for w in self.content.winfo_children():
            w.destroy()

    def _logout(self):
        self.username = None
        self.role = None
        self._build_login()

    def show_all_promises(self):
        promises = PromiseModel.list_all_promises()
        self._clear_content()
        ttk.Label(self.content, text="All Promises", font=(None, 12)).pack(anchor="w")
        tv = ttk.Treeview(self.content, columns=("id","politician","date","status","detail"), show="headings")
        tv.heading("id", text="ID")
        tv.heading("politician", text="Politician")
        tv.heading("date", text="Announced")
        tv.heading("status", text="Status")
        tv.heading("detail", text="Detail")
        tv.pack(fill="both", expand=True)

        for p in promises:
            pid = p[0]
            detail = p[1]
            announced = p[2]
            status = p[3]
            pol_name = p[5]
            tv.insert("", "end", values=(pid, pol_name, announced, status, detail))

        def on_double(event):
            item = tv.selection()
            if item:
                pid = tv.item(item[0])['values'][0]
                self.show_promise_detail(pid)

        tv.bind("<Double-1>", on_double)

    def _ask_promise_id(self):
        pid = simpledialog.askstring("Promise ID", "Enter Promise ID:")
        if pid:
            self.show_promise_detail(pid.strip())

    def show_promise_detail(self, promise_id):
        p = PromiseModel.get_promise(promise_id)
        if not p:
            messagebox.showerror("Not found", "Promise not found")
            return

        updates = PromiseUpdateModel.list_updates(promise_id)
        self._clear_content()
        ttk.Label(self.content, text=f"Promise {promise_id}", font=(None, 12)).pack(anchor="w")

        info = f"ID: {p[0]}\nDetail: {p[1]}\nAnnounced: {p[2]}\nStatus: {p[3]}\nPolitician: {p[5]} ({p[6]})\nCampaign: {p[7]} {p[8]} {p[9]}"
        ttk.Label(self.content, text=info, justify="left").pack(anchor="w", padx=10, pady=10)

        ttk.Label(self.content, text="Updates:").pack(anchor="w", padx=10)
        updates_box = tk.Listbox(self.content, height=8)
        updates_box.pack(fill="both", expand=True, padx=10, pady=6)
        for u in updates:
            updates_box.insert("end", f"{u[1]} - {u[2]}")

        btn_frame = ttk.Frame(self.content)
        btn_frame.pack(fill="x", padx=10, pady=6)
        if self.role == "ADMIN":
            ttk.Button(btn_frame, text="Add Update", command=lambda: self._open_add_update(promise_id, None)).pack(side="left")
        ttk.Button(btn_frame, text="Back", command=self._build_main_menu).pack(side="right")

    def _open_add_update(self, promise_id, parent=None):
        if self.role != "ADMIN":
            messagebox.showerror("Forbidden", "Only ADMIN can add updates")
            return

        txt = simpledialog.askstring("Add Update", "Enter progress detail:")
        if txt is None:
            return
        try:
            from datetime import date

            PromiseUpdateModel.add_update(promise_id, date.today().isoformat(), txt)
            messagebox.showinfo("OK", "Update added")
            # รีเฟรชหน้ารายละเอียดคำสัญญาอัตโนมัติ
            self.show_promise_detail(promise_id)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _ask_add_update(self):
        pid = simpledialog.askstring("Promise ID", "Enter Promise ID to update:")
        if pid:
            self._open_add_update(pid.strip())

    def show_politicians(self):
        pols = PoliticianModel.list_politicians()
        self._clear_content()
        ttk.Label(self.content, text="Politicians", font=(None, 12)).pack(anchor="w")
        lb = tk.Listbox(self.content)
        lb.pack(fill="both", expand=True)
        for p in pols:
            lb.insert("end", f"{p[0]} - {p[1]} ({p[2]})")

        def on_sel(evt):
            if not lb.curselection():
                return
            idx = lb.curselection()[0]
            text = lb.get(idx)
            pid = text.split(" - ")[0]
            promises = PromiseModel.list_promises_by_politician(pid)
            self._show_promises_of_politician(pid, promises)

        lb.bind("<<ListboxSelect>>", on_sel)

    def _show_promises_of_politician(self, pid, promises):
        self._clear_content()
        ttk.Label(self.content, text=f"Promises of {pid}", font=(None, 12)).pack(anchor="w")
        tv = ttk.Treeview(self.content, columns=("id","date","status","detail"), show="headings")
        tv.heading("id", text="ID")
        tv.heading("date", text="Announced")
        tv.heading("status", text="Status")
        tv.heading("detail", text="Detail")
        tv.pack(fill="both", expand=True)
        for p in promises:
            tv.insert("", "end", values=(p[0], p[2], p[3], p[1]))

        def on_double(event):
            item = tv.selection()
            if item:
                pid = tv.item(item[0])['values'][0]
                self.show_promise_detail(pid)

        tv.bind("<Double-1>", on_double)


def run_gui():
    init_db()
    seed_data()
    app = GuiApp()
    app.mainloop()


if __name__ == "__main__":
    run_gui()
