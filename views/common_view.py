class CommonView:
    def ask(self, prompt: str) -> str:
        return input(prompt).strip()

    def show_message(self, msg: str):
        print(msg)

    def show_error(self, msg: str):
        print(f"Error: {msg}")

    def show_main_menu(self):
        print("\n=== Promise Tracker (MVC CLI) ===")
        print("1) Login as USER (view only)")
        print("2) Login as ADMIN (can update)")
        print("0) Exit")
