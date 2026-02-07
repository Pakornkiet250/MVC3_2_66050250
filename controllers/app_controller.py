from datetime import date

from models.auth_model import AuthModel
from models.politician_model import PoliticianModel
from models.promise_model import PromiseModel
from models.update_model import PromiseUpdateModel

class AppController:
    def __init__(self, common_view, list_view, detail_view, update_view, politician_view):
        self.v = common_view
        self.list_view = list_view
        self.detail_view = detail_view
        self.update_view = update_view
        self.politician_view = politician_view

    def run(self):
        while True:
            self.v.show_main_menu()
            choice = self.v.ask("Choose: ")

            if choice == "0":
                self.v.show_message("Bye!")
                break

            if choice == "1":
                self.session_flow(role="USER")
            elif choice == "2":
                self.session_flow(role="ADMIN")
            else:
                self.v.show_message("Invalid choice.")

    def session_flow(self, role: str):
        username = self.v.ask("Username: ")
        password = self.v.ask("Password: ")
        user = AuthModel.login(username, password)

        if not user or user[1] != role:
            self.v.show_error(f"Login failed ({role}).")
            return

        while True:
            print("\n--- MENU ---")
            print("1) All promises")
            print("2) Promise detail")
            print("3) Politicians")
            if role == "ADMIN":
                print("4) Add update to a promise")
            print("0) Logout")

            cmd = self.v.ask("Choose: ")

            if cmd == "0":
                return
            elif cmd == "1":
                self.show_all_promises()
            elif cmd == "2":
                self.show_promise_detail_flow(role)
            elif cmd == "3":
                self.politician_flow()
            elif cmd == "4" and role == "ADMIN":
                self.add_update_flow_then_back_to_detail()
            else:
                self.v.show_message("Invalid option.")

    
    def show_all_promises(self):
        promises = PromiseModel.list_all_promises()
        self.list_view.show(promises)

    
    def show_promise_detail_flow(self, role: str):
        promise_id = self.v.ask("Promise ID: ")
        self.render_detail(promise_id)
        if role == "ADMIN":
            print("\nA) Add update")
        print("B) Back")
        cmd = self.v.ask("Choose: ").upper()
        if cmd == "A" and role == "ADMIN":
            self.add_update_for_specific_promise(promise_id) 
       

    def render_detail(self, promise_id: str):
        promise = PromiseModel.get_promise(promise_id)
        updates = PromiseUpdateModel.list_updates(promise_id)
        self.detail_view.show(promise, updates)

    
    def politician_flow(self):
        politicians = PoliticianModel.list_politicians()
        self.politician_view.show_politicians(politicians)
        pid = self.v.ask("Enter politician_id to view promises (or B to back): ").upper()
        if pid == "B":
            return
        pol = PoliticianModel.get(pid)
        promises = PromiseModel.list_promises_by_politician(pid)
        self.politician_view.show_promises(pol, promises)

   
    def add_update_flow_then_back_to_detail(self):
        promise_id = self.v.ask("Promise ID to update: ")
        self.add_update_for_specific_promise(promise_id)

    def add_update_for_specific_promise(self, promise_id: str):
        self.update_view.show_form(promise_id)
        update_date = date.today().isoformat()
        progress = self.v.ask("Progress detail: ")

        try:
            PromiseUpdateModel.add_update(promise_id, update_date, progress)
            self.v.show_message("Update added.")
        except Exception as e:
            self.v.show_error(str(e))

        # BU rule
        self.render_detail(promise_id)
