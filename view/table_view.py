def view_owners(self, tree):
    self.tree = tree
    [self.tree.delete(i) for i in self.tree.get_children()]
    [self.tree.insert('', 'end', values=owner) for owner in self.db.owner.list()]


def view_payments(self, tree, find_v):
    self.tree = tree
    for i in self.tree.get_children():
        self.tree.delete(i)
    i = 0
    for debt in self.db.debt.get_by_number(find_v):
        i += 1
        debt_list = list(debt)
        del debt_list[1]
        debt_list.insert(2, '')
        debt_list.insert(6, '')
        debt_list.insert(7, '')
        debt_list.insert(9, '')
        debt_list.insert(10, 'Долг')
        self.tree.insert('', 'end', values=debt_list)
        if i == 1:
            for payment in self.db.payment.get_by_number(find_v):
                payment_list = list(payment)
                del payment_list[1]
                self.tree.insert('', 'end', values=payment_list)
