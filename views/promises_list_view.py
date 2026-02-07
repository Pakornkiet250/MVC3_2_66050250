class PromisesListView:
    def show(self, promises):
        print("\n=== ALL PROMISES (sorted by announced date) ===")
        if not promises:
            print("No promises found.")
            return
        for row in promises:
            promise_id, detail, announced, status, pol_id, pol_name, party, camp_id, year, district = row
            print(f"[{promise_id}] {announced} | {status} | {pol_name} ({party}) | {detail}")
