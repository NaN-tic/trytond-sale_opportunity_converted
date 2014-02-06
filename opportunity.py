#This file is part sale_opportunity_converted module for Tryton.
#The COPYRIGHT file at the top level of this repository contains
#the full copyright notices and license terms.
from trytond.model import ModelView, Workflow
from trytond.pool import Pool, PoolMeta
from trytond.pyson import Eval

__all__ = ['SaleOpportunity']
__metaclass__ = PoolMeta


class SaleOpportunity:
    __name__ = "sale.opportunity"

    @classmethod
    def __setup__(cls):
        super(SaleOpportunity, cls).__setup__()
        cls._buttons.update({
            'convert_without_sale': {
                'invisible': ~Eval('state').in_(['opportunity']),
                },
            })

    @classmethod
    @ModelView.button
    @Workflow.transition('converted')
    def convert_without_sale(cls, opportunities):
        """Convert a opportunity to converted withou generate a sale"""
        Date = Pool().get('ir.date')
        cls.write(opportunities, {
                'end_date': Date.today(),
                })
