# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Lorenzo Battistini <lorenzo.battistini@agilebg.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import fields, orm
from openerp.tools.translate import _


def send_notification(self, cr, uid, ids, esito, context):
    if context is None:
        context = {}
    if 'active_id' not in context:
        raise orm.except_orm(
            _("Error"), _("Missing active ID"))
    invoice_pool = self.pool['account.invoice']
    notification_pool = self.pool['fatturapa.notification']
    wizard = self.browse(cr, uid, ids[0], context=context)
    invoice = invoice_pool.browse(
        cr, uid, context['active_id'], context=context)
    notification_pool.create_notifica_esito_committente(
        cr, uid, ids, invoice, esito='EC01',
        description=wizard.name, context=context)


class SendAcceptNotification(orm.TransientModel):
    _name = 'wizard.fatturapa.in.accept'
    _columns = {
        'name': fields.text("Message"),
        }

    def send(self, cr, uid, ids, context=None):
        send_notification(self, cr, uid, ids, 'EC01', context)
        return {'type': 'ir.actions.act_window_close'}


class SendRejectNotification(orm.TransientModel):
    _name = 'wizard.fatturapa.in.reject'
    _columns = {
        'name': fields.text("Message"),
        }

    def send(self, cr, uid, ids, context=None):
        send_notification(self, cr, uid, ids, 'EC02', context)
        return {'type': 'ir.actions.act_window_close'}
