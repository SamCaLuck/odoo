{
    'name': 'real estate',
    'depends': ['base'],
    'author' : "Samuel, \n Diana",
    'version' : '1.0',
    'images' : ['static/description/icon.png'],
    'data': [
            # "'security/security.xml',
            'security/ir.model.access.csv',
            'views/estate.xml',
            'views/estate_type.xml',
            'views/estate_tag.xml',
            'views/estate_offer.xml',
            "views/estate_menu.xml",


    ],
    'application': True,
    'installable': True,
}