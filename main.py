import tkinter as tk
from view import owners, add_owner, add_payment, find_payment, update_owner
from logiс.scripts import calculation
import dao


class OwnersMenuActions:

    @staticmethod
    def open_add_owner(window, tree):
        add_owner.AddOwner(db, window, tree)

    @staticmethod
    def open_add_payment():
        add_payment.AddPay(db, calculation)

    @staticmethod
    def open_find_payment():
        find_payment.FindPayments(db)

    @staticmethod
    def open_update(owner_id, window, tree):
        update_owner.UpdateOwner(db, owner_id, window, tree)


if __name__ == "__main__":
    root = tk.Tk()
    db = dao.DAO()
    app = owners.Owners(root, OwnersMenuActions(), db)
    app.pack()
    root.title("Clever SNT")
    root.geometry("1050x650+0+0")
    root.mainloop()
