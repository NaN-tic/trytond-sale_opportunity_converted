# This file is part sale_opportunity_converted module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.model import ModelView, Workflow
from trytond.pool import Pool, PoolMeta
from trytond.pyson import Bool, Eval

__all__ = ['SaleOpportunity']


class SaleOpportunity:
    __metaclass__ = PoolMeta
    __name__ = "sale.opportunity"

    @classmethod
    def __setup__(cls):
        super(SaleOpportunity, cls).__setup__()
        cls._error_messages.update({
                'opportunity_sale': ('You can not create a new sale from '
                    'opportunity "%s" because it is related to sale "%s".'),
                })
        cls._buttons.update({
            'convert_without_sale': {
                'invisible': ~Eval('state').in_(['opportunity']),
                },
            'create_sales': {
                'invisible': ((~Eval('state').in_(['converted'])) |
                    (Bool(Eval('sales', [])))),
                },
            })

    @classmethod
    @ModelView.button
    @Workflow.transition('converted')
    def convert_without_sale(cls, opportunities):
        """Change a opportunity to converted without generating a sale"""
        Date = Pool().get('ir.date')
        cls.write(opportunities, {
                'end_date': Date.today(),
                })

    @classmethod
    @ModelView.button
    def create_sales(cls, opportunities):
        """Create a sale from converted opportunity"""
        Sale = Pool().get('sale.sale')
        sales = []
        for opportunity in opportunities:
            if opportunity.sales:
                cls.raise_user_error('opportunity_sale', (
                    opportunity.rec_name,
                    opportunity.sales[0].rec_name,
                    ))
            sales.append(opportunity.create_sale())
        Sale.save(sales)
