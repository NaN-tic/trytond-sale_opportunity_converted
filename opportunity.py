#This file is part sale_opportunity_converted module for Tryton.
#The COPYRIGHT file at the top level of this repository contains
#the full copyright notices and license terms.
from trytond.model import ModelView, Workflow
from trytond.pool import Pool, PoolMeta
from trytond.pyson import Bool, Eval

__all__ = ['SaleOpportunity']
__metaclass__ = PoolMeta


class SaleOpportunity:
    __name__ = "sale.opportunity"

    @classmethod
    def __setup__(cls):
        super(SaleOpportunity, cls).__setup__()
        cls._transitions |= set((
                ('converted', 'lost'),
                ))
        cls._error_messages.update({
                'cancel_sale': ('Sale "%s" must be cancelled before '
                    'lost.'),
                'opportunity_sale': ('You can not create a new sale from opportunity '
                    '"%s" because is related to sale "%s"'),
                })
        cls._buttons.update({
            'convert_without_sale': {
                'invisible': ~Eval('state').in_(['opportunity']),
                },
            'convert_lost': {
                'invisible': ~Eval('state').in_(['converted']),
                },
            'convert_sale': {
                'invisible': ((Eval('state').in_(['converted'])) & (Bool(Eval('sale')))),
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

    @classmethod
    @ModelView.button
    @Workflow.transition('lost')
    def convert_lost(cls, opportunities):
        """Convert a converted opportunity to opportunity"""
        Sale = Pool().get('sale.sale')

        sales = []
        for opportunity in opportunities:
            if opportunity.sale and not opportunity.sale.state == 'cancel':
                cls.raise_user_error('cancel_sale', (opportunity.sale.rec_name,))
                sales.append(opportunity.sale)
        Sale.delete(sales)

    @classmethod
    @ModelView.button
    def convert_sale(cls, opportunities):
        """Create a sale from convert opportunity"""
        for opportunity in opportunities:
            if opportunity.sale:
                cls.raise_user_error('opportunity_sale', (
                    opportunity.rec_name,
                    opportunity.sale.rec_name,
                    ))
            opportunity.create_sale()
