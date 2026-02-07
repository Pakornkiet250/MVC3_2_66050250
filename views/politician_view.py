class PoliticianView:
    def show_politicians(self, politicians):
        print("\n=== POLITICIANS ===")
        for pid, name, party in politicians:
            print(f"[{pid}] {name} ({party})")

    def show_promises(self, politician, promises):
        if not politician:
            print("Politician not found.")
            return
        pid, name, party = politician
        print(f"\n=== PROMISES BY {name} ({party}) ===")
        if not promises:
            print("No promises.")
            return
        for promise_id, detail, announced, status in promises:
            print(f"[{promise_id}] {announced} | {status} | {detail}")
