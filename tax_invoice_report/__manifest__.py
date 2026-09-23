{
    'name': "Invoice Report",
    'summary': """
        Invoice Report""",
    'description': """
        Invoice Report
    """,
    'license': 'LGPL-3',
    'author': "Ahmed Hussein",
    'category': 'Uncategorized',
    'version': '19.0.1.3.0',
    'depends': ['base','account','l10n_sa'],
    'data': [
        'views/invoice_report.xml',
        'report/invoice_header_footer.xml',
        'report/report.xml',
        'report/nesma_invoice_report.xml'
    ],
}
