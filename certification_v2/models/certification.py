# Copyright 2019 Eficent
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import timedelta

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Certification(models.Model):
    _name = 'certification'
    _description = 'Certification'

    number = fields.Char()
    owner_id = fields.Many2one('res.partner')
    date = fields.Date(string='Validation Date')
    description = fields.Text(string='Validation Details')
    standard_id = fields.Many2one('certification.standard')
    entity_id = fields.Many2one('res.partner')
    expiry_days = fields.Integer('Expiry Days', readonly=True, compute='_compute_expiry_days')
    expiry_status = fields.Selection([
        ('expired', "Expired"),
        ('available', "Available")
    ], readonly=True, compute='_compute_expiry_days', store=True)

    @api.constrains('entity_id')
    def _check_entity_id(self):
        if self.entity_id and self.entity_id.is_certification_body == False:
            raise ValidationError('It is not a certification entity')

    @api.multi
    def update_date_one_month(self):
        self.ensure_one()
        if self.date:
            self.write({'date': self.date + timedelta(days=30)})

    @api.depends ('date')
    def _compute_expiry_days(self):
        if self.date:
            self.expiry_days = (self.date - fields.Date.today()).days
            if self.expiry_days > 0:
                self.expiry_status = 'available'
            else:
                self.expiry_status = 'expired'