class PromiseDetailView:
    def show(self, promise_row, updates):
        if not promise_row:
            print("\n=== PROMISE DETAIL ===")
            print("Promise not found.")
            return

        promise_id, detail, announced, status, pol_id, pol_name, party, camp_id, year, district = promise_row

        print("\n=== PROMISE DETAIL ===")
        print(f"Promise ID: {promise_id}")
        print(f"Announced: {announced}")
        print(f"Status: {status}")
        print(f"Politician: {pol_name} ({party}) [{pol_id}]")
        print(f"Campaign: {camp_id} | {year} | {district}")
        print(f"Detail: {detail}")

        print("\n--- UPDATES ---")
        if not updates:
            print("No updates yet.")
        else:
            for uid, udate, udetail in updates:
                print(f"- ({udate}) {udetail}  [update_id={uid}]")
