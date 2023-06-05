# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Czech - Accounting',
    'icon': '/account/static/description/l10n.png',
    'countries': ['cz'],
    'version': '1.0',
    'author': '26HOUSE (http://www.26house.com)',
    'website': 'https://www.odoo.com/documentation/saas-16.3/applications/finance/fiscal_localizations.html',
    'category': 'Accounting/Localizations/Account Charts',
    'description': """
Czech accounting chart and localization.  With Chart of Accounts with taxes and basic fiscal positions.

Tento modul definuje:

- Českou účetní osnovu za rok 2020

- Základní sazby pro DPH z prodeje a nákupu

- Základní fiskální pozice pro českou legislativu
    """,
    'depends': [
        'account',
        'base_iban',
        'base_vat',
    ],
    'demo': [
        'data/demo_company.xml',
    ],
    'license': 'LGPL-3',
}
