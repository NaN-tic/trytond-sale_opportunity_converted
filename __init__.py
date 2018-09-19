# This file is part sale_opportunity_converted module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool
from . import opportunity


def register():
    Pool.register(
        opportunity.SaleOpportunity,
        module='sale_opportunity_converted', type_='model')
