from datetime import timedelta

from odoo import fields
from odoo.exceptions import UserError, ValidationError
from odoo.tests import TransactionCase


class TestLibrary(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.book = cls.env["oe.library.book"].create({"name": "OE Testing Book"})
        cls.copy = cls.env["oe.library.copy"].create({
            "code": "OE-T-TEST-1", "book_id": cls.book.id,
        })
        cls.borrower = cls.env["res.partner"].create({"name": "OE Test Borrower"})

    def _loan(self, **kw):
        data = {"copy_id": self.copy.id, "borrower_id": self.borrower.id}
        data.update(kw)
        return self.env["oe.library.loan"].create(data)

    def test_checkout_return_and_reuse(self):
        first = self._loan()
        first.action_start()
        self.assertEqual(first.state, "active")
        first.action_return()
        self.assertEqual(first.state, "returned")
        self.assertTrue(first.return_date)
        second = self._loan()
        second.action_start()
        self.assertEqual(second.state, "active")

    def test_second_active_loan_is_rejected(self):
        first = self._loan()
        first.action_start()
        second = self._loan()
        with self.assertRaises(UserError):
            second.action_start()
        self.assertEqual(second.state, "draft")

    def test_maintenance_copy_is_not_loanable(self):
        self.copy.condition = "repair"
        with self.assertRaises(UserError):
            self._loan().action_start()

    def test_due_date_must_follow_borrow_date(self):
        today = fields.Date.context_today(self.env["oe.library.loan"])
        with self.assertRaises(ValidationError):
            self._loan(loan_date=today, due_date=today - timedelta(days=1))

    def test_overdue_is_calculated_from_current_day(self):
        today = fields.Date.context_today(self.env["oe.library.loan"])
        loan = self._loan(loan_date=today - timedelta(days=5), due_date=today - timedelta(days=2))
        self.assertFalse(loan.is_overdue)
        loan.action_start()
        self.assertTrue(loan.is_overdue)
        loan.action_return()
        self.assertFalse(loan.is_overdue)

    def test_cannot_return_draft(self):
        with self.assertRaises(UserError):
            self._loan().action_return()
