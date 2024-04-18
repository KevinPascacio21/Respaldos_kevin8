from odoo import api, fields, models
from datetime import datetime, timedelta #

class DescuentoInegrReport(models.Model):
    _name = 'report.report_descuen_integrado' 
    _inherit = 'report.report_xlsx.abstract' 
    _description = 'Reporte de descuento integrado'


    def generate_xlsx_report(self, workbook, data, descuento_integrado):
        for ctrl in descuento_integrado:
            report_name = 'Reporte de descuento integrado'
            # One sheet by partner

            #Celdas
            sheet = workbook.add_worksheet(report_name[:31])
            sheet.write(0, 3, report_name, workbook.add_format({'bold': True, 'align': 'center'}))
            sheet.set_column(1, 1, 20)
            sheet.set_column(2, 2, 25)
            sheet.set_column(3, 3, 25)
            # sheet.set_column(4, 4, 25)


            title_cell = workbook.add_format({'bold': True, 'font_color': 'black', 'bg_color': '#F1FADA', 'align': 'center'})
            format_cell = workbook.add_format({'font_color': 'black', 'border': True, 'border_color': '#F1FADA', 'align': 'center'})
            format_cell_Date = workbook.add_format({'font_color': 'black', 'border': True, 'border_color': '#F1FADA', 'num_format': 'dd/mm/yy', 'align': 'center'})
            # format_cell_Date = workbook.add_format({'font_color': 'black', 'border': True, 'border_color': '#F1FADA', 'bg_color': '#F1FADA', 'num_format': 'dd/mm/yy', 'align': 'center'}) 


            sheet.write(2, 2, 'Nombre', title_cell)
            sheet.write(2, 3, 'Cliente', title_cell)
            sheet.write(2, 4, 'Fecha de la factura', title_cell)
            # sheet.write(2, 5, 'Descuento', title_cell)

            row = 3
            for line in ctrl.relacion_ids:

                sheet.write(row, 2, line.name, format_cell)
                sheet.write(row, 3, line.partner_id, format_cell)
                sheet.write(row, 4, line.invoice_date, format_cell_Date)
                # sheet.write(row, 5, line.total_cash_discount, format_cell)
                row += 1