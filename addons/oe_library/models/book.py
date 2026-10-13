# Original redesign of the book/copy pattern inspired by the LGPL-3
# JoseCarlosLuque/odoo_practices cd_library_practices exercises.
from odoo import fields, models


class LibraryBook(models.Model):
    _name = "oe.library.book"
    _description = "Library Title"
    _order = "name, id"

    name = fields.Char(required=True, index=True)
    author = fields.Char()
    isbn = fields.Char(copy=False, index=True)
    active = fields.Boolean(default=True)
    copy_ids = fields.One2many("oe.library.copy", "book_id", string="Copies")
