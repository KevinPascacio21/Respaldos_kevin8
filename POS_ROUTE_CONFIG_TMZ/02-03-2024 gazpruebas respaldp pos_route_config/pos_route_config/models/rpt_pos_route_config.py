from odoo import api, fields, models

class RouteConfigReport(models.Model):
    _name = 'report.report_route_config' 
    _inherit = 'report.report_xlsx.abstract' #---------------------------------
    _description = 'Reporte de configuración de rutas'
    
    def generate_xlsx_report(self, workbook, data, route_config):
        for ctrl in route_config:
            report_name = 'Reporte'
            # One sheet by partner

            sheet = workbook.add_worksheet(report_name[:31])
            sheet.write(0, 4, report_name, workbook.add_format({'bold': True, 'align': 'center'}))
            sheet.set_column(1, 1, 20)
            sheet.set_column(2, 2, 25)
            sheet.set_column(3, 3, 25)
            sheet.set_column(4, 4, 25)
            sheet.set_column(5, 5, 20)
            sheet.set_column(6, 6, 25)
            sheet.set_column(7, 7, 20)
            sheet.set_column(8, 8, 25)
            sheet.set_column(9, 9, 25)
            sheet.set_column(10, 10, 25)
            sheet.set_column(11, 11, 20)
            sheet.set_column(12, 12, 25)
            sheet.set_column(13, 13, 20)
            sheet.set_column(14, 14, 25)
            sheet.set_column(15, 15, 25)
            sheet.set_column(16, 16, 25)
            sheet.set_column(17, 17, 20)
            sheet.set_column(18, 18, 25)
            sheet.set_column(19, 19, 20)
            sheet.set_column(20, 20, 25)
            sheet.set_column(21, 21, 25)
            sheet.set_column(22, 22, 25)
            sheet.set_column(23, 23, 20)
            sheet.set_column(24, 24, 25)
            sheet.set_column(25, 25, 20)


            title_cell = workbook.add_format({'bold': True, 'font_color': 'black', 'bg_color': '#F1FADA', 'align': 'center'})
            format_cell = workbook.add_format({'font_color': 'black', 'border': True, 'border_color': '#F1FADA', 'align': 'center'})


            sheet.write(2, 2, 'Fecha de creación', title_cell)
            sheet.write(2, 3, 'Referencia de ruta', title_cell)
            sheet.write(2, 4, 'Punto de venta', title_cell)
            sheet.write(2, 5, 'Litrometro inicial', title_cell)
            sheet.write(2, 6, 'Litrometro final', title_cell)
            sheet.write(2, 7, 'Diferencia Litrometro', title_cell)
            sheet.write(2, 8, 'Peso inicial', title_cell)
            sheet.write(2, 9, 'Peso final', title_cell)
            sheet.write(2, 10, 'Porcentaje inicial', title_cell)
            sheet.write(2, 11, 'Porcentaje final', title_cell)
            sheet.write(2, 12, 'Diferencia Porcentaje', title_cell)
            sheet.write(2, 13, 'Promedio sector', title_cell)
            sheet.write(2, 14, 'Promedio general', title_cell)
            sheet.write(2, 15, 'Carburación inicial', title_cell)
            sheet.write(2, 16, 'Carburación final', title_cell)
            sheet.write(2, 17, 'Diferencia de Carburación', title_cell)
            sheet.write(2, 18, 'Rotogauge inicial', title_cell)
            sheet.write(2, 19, 'Rotogauge final', title_cell)
            sheet.write(2, 20, 'Litros por cobrar', title_cell)
            sheet.write(2, 21, 'Litros para recargar', title_cell)
            sheet.write(2, 22, 'Estatus', title_cell)
            sheet.write(2, 23, 'Empleado', title_cell)
            sheet.write(2, 24, 'Ayudante', title_cell)
            sheet.write(2, 25, 'Justificación', title_cell)


            row = 3
            for line in ctrl.relacion_ids:
                sheet.write(row, 2, line.date, format_cell)
                sheet.write(row, 3, line.name, format_cell)
                sheet.write(row, 4, line.pos_config_id, format_cell)
                sheet.write(row, 5, line.st_volume_meter, format_cell)
                sheet.write(row, 6, line.en_volume_meter, format_cell)
                sheet.write(row, 7, line.dif_volume_meter, format_cell)
                sheet.write(row, 8, line.st_weight, format_cell)
                sheet.write(row, 9, line.en_weight_aux, format_cell)
                sheet.write(row, 10, line.dif_weight, format_cell)
                sheet.write(row, 11, line.st_percent, format_cell)
                sheet.write(row, 12, line.en_percent, format_cell)
                sheet.write(row, 13, line.dif_percent, format_cell)
                sheet.write(row, 14, line.avg_sector , format_cell)
                sheet.write(row, 15, line.hg_avg, format_cell) #promedio general hg_avg
                sheet.write(row, 16, line.st_carburation, format_cell)
                sheet.write(row, 17, line.en_carburation, format_cell)
                sheet.write(row, 18, line.dif_carburation, format_cell)
                sheet.write(row, 19, line.st_gauge, format_cell)
                sheet.write(row, 20, line.en_gauge, format_cell)
                sheet.write(row, 21, line.liters_receivable, format_cell)
                sheet.write(row, 22, line.refuel_liters, format_cell) 
                sheet.write(row, 23, line.state, format_cell)
                sheet.write(row, 24, line.employee_ids, format_cell)
                sheet.write(row, 25, line.x_studio_ayudante_id, format_cell)
                sheet.write(row, 25, line.justification, format_cell)
                row += 1
            

