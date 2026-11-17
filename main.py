from app.config import iniciar_pocketbase
from app.gui import App


def main():
    proc = iniciar_pocketbase()
    try:
        App().mainloop()
    finally:
        if proc:
            proc.terminate()


if __name__ == "__main__":
    main()
