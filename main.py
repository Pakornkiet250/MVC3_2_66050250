from db import init_db, seed_data


from gui_app import run_gui


def main():
    init_db()
    seed_data()
    run_gui()


if __name__ == "__main__":
    main()
