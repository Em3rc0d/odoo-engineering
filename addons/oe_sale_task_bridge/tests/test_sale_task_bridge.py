from odoo.tests import TransactionCase
from odoo.exceptions import UserError


class TestSaleTaskBridge(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        partner = cls.env["res.partner"].create({"name": "OE Test Customer"})
        cls.order = cls.env["sale.order"].create({"partner_id": partner.id})
        cls.project = cls.env["project.project"].create({"name": "OE Test Project"})

    def test_count_is_zero_for_empty_order(self):
        self.assertEqual(self.order.oe_task_count, 0)

    def test_reject_creation_from_unconfirmed_order(self):
        with self.assertRaises(UserError):
            self.order.action_oe_new_task()

    def test_group_counts_are_order_specific(self):
        another = self.env["sale.order"].create({"partner_id": self.order.partner_id.id})
        Task = self.env["project.task"]
        Task.create({"name": "A", "project_id": self.project.id, "oe_sale_order_id": self.order.id})
        Task.create({"name": "B", "project_id": self.project.id, "oe_sale_order_id": self.order.id})
        Task.create({"name": "C", "project_id": self.project.id, "oe_sale_order_id": another.id})
        orders = self.order | another
        orders.invalidate_recordset(["oe_task_count"])
        self.assertEqual(self.order.oe_task_count, 2)
        self.assertEqual(another.oe_task_count, 1)

    def test_task_wizard_refuses_unconfirmed_order(self):
        wizard = self.env["oe.sale.task.wizard"].create({
            "sale_order_id": self.order.id,
            "project_id": self.project.id,
            "name": "Prepare delivery",
        })
        with self.assertRaises(UserError):
            wizard.action_create_task()

    def test_task_wizard_creates_link_to_project_and_order(self):
        self.order.action_confirm()
        wizard = self.env["oe.sale.task.wizard"].create({
            "sale_order_id": self.order.id,
            "project_id": self.project.id,
            "name": "Prepare delivery",
        })
        action = wizard.action_create_task()
        task = self.env["project.task"].browse(action["res_id"])
        self.assertEqual(task.project_id, self.project)
        self.assertEqual(task.oe_sale_order_id, self.order)
        self.assertEqual(task.name, "Prepare delivery")
