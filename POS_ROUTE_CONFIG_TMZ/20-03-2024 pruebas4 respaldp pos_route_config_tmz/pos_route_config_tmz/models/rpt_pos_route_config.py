from odoo import api, fields, models

class RouteConfigReport(models.Model):
    _name = 'report.report_route_conf' 
    _inherit = 'report.report_xlsx.abstract' 
    _description = 'Reporte de configuración de rutas'
    
    def generate_xlsx_report(self, workbook, data, route_config):
        for ctrl in route_config:
            report_name = 'Reporte de configuración de rutas'
            # One sheet by partner

            #Celdas
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
            sheet.set_column(26, 26, 25)
            sheet.set_column(27, 27, 20)


            title_cell = workbook.add_format({'bold': True, 'font_color': 'black', 'bg_color': '#F1FADA', 'align': 'center'})
            format_cell = workbook.add_format({'font_color': 'black', 'border': True, 'border_color': '#F1FADA', 'align': 'center'})
            format_cell_Date = workbook.add_format({'font_color': 'black', 'border': True, 'border_color': '#F1FADA', 'num_format': 'dd/mm/yy', 'align': 'center'})                                                    #HH:MM:SS', 'align': 'center'})
            
            #Dar formato y color a las celdas
            format_cell_white = workbook.add_format({'font_color': 'black', 'bg_color': '#ffffff', 'border': True, 'border_color': '#F1FADA', 'align': 'center'})
            format_cell_orange = workbook.add_format({'font_color': 'black', 'bg_color': '#fadb62', 'border': True, 'border_color': '#F1FADA', 'align': 'center'})
            format_cell_grey = workbook.add_format({'font_color': 'black', 'bg_color': '#c4c4c4', 'border': True, 'border_color': '#F1FADA', 'align': 'center'})
            format_cell_blue = workbook.add_format({'font_color': 'black', 'bg_color': '#81c8ef', 'border': True, 'border_color': '#F1FADA', 'align': 'center'})
            format_cell_yellow = workbook.add_format({'font_color': 'black', 'bg_color': '#e7f177', 'border': True, 'border_color': '#F1FADA', 'align': 'center'})
            format_cell_green = workbook.add_format({'font_color': 'black', 'bg_color': '#b7f0a6', 'border': True, 'border_color': '#F1FADA', 'align': 'center'})

            sheet.write(2, 2, 'Fecha de creación', title_cell)
            sheet.write(2, 3, 'Fecha de salida', title_cell)
            sheet.write(2, 4, 'Fecha de llegada', title_cell)
            sheet.write(2, 5, 'Referencia de ruta', title_cell)
            sheet.write(2, 6, 'Punto de venta', title_cell)
            sheet.write(2, 7, 'Litrometro inicial', title_cell)
            sheet.write(2, 8, 'Litrometro final', title_cell)
            sheet.write(2, 9, 'Diferencia Litrometro', title_cell)
            sheet.write(2, 10, 'Peso inicial', title_cell)
            sheet.write(2, 11, 'Peso final', title_cell)
            sheet.write(2, 12, 'Diferencia de Peso', title_cell)
            sheet.write(2, 13, 'Porcentaje inicial', title_cell)
            sheet.write(2, 14, 'Porcentaje final', title_cell)
            sheet.write(2, 15, 'Diferencia Porcentaje', title_cell)
            sheet.write(2, 16, 'Promedio sector', title_cell)
            sheet.write(2, 17, 'Promedio general', title_cell)
            sheet.write(2, 18, 'Carburación inicial', title_cell)
            sheet.write(2, 19, 'Carburación final', title_cell)
            sheet.write(2, 20, 'Diferencia de Carburación', title_cell)
            sheet.write(2, 21, 'Rotogauge inicial', title_cell)
            sheet.write(2, 22, 'Rotogauge final', title_cell)
            sheet.write(2, 23, 'Litros por cobrar', title_cell)
            sheet.write(2, 24, 'Litros para recargar', title_cell)
            sheet.write(2, 25, 'Estatus', title_cell)
            sheet.write(2, 26, 'Empleado', title_cell)
            sheet.write(2, 27, 'Ayudante', title_cell)
            sheet.write(2, 28, 'Justificación', title_cell)


            row = 3
            for line in ctrl.relacion_ids:
                #sheet.write(row, 2, line.date, format_cell_Date)
                sheet.write(row, 2, line.route_creation_date , format_cell_Date)
                sheet.write(row, 3, line.departure_date , format_cell_Date)
                sheet.write(row, 4, line.arrival_date , format_cell_Date)
                sheet.write(row, 5, line.name, format_cell)
                sheet.write(row, 6, line.pos_config_id.name, format_cell) 
                sheet.write(row, 7, line.st_volume_meter, format_cell)
                sheet.write(row, 8, line.en_volume_meter, format_cell)
                sheet.write(row, 9, line.dif_volume_meter, format_cell)
                sheet.write(row, 10, line.st_weight_aux, format_cell)
                sheet.write(row, 11, line.en_weight_aux, format_cell)
                sheet.write(row, 12, line.dif_weight, format_cell)
                sheet.write(row, 13, line.st_percent, format_cell)
                sheet.write(row, 14, line.en_percent, format_cell)
                sheet.write(row, 15, line.dif_percent, format_cell)
                sheet.write(row, 16, line.avg_sector , format_cell)        
                sheet.write(row, 17, line.hg_avg, format_cell) #promedio general  
                sheet.write(row, 18, line.st_carburation, format_cell)
                sheet.write(row, 19, line.en_carburation, format_cell)
                sheet.write(row, 20, line.dif_carburation, format_cell)
                sheet.write(row, 21, line.st_gauge, format_cell)
                sheet.write(row, 22, line.en_gauge, format_cell)
                sheet.write(row, 23, line.liters_receivable, format_cell)
                sheet.write(row, 24, line.refuel_liters, format_cell)
                if line.state == "new": 
                         sheet.write(row, 25, "Nuevo", format_cell_white)
                elif line.state == "New":
                       sheet.write(row, 25, "Nuevo", format_cell_white)
                elif line.state == "start": 
                        sheet.write(row, 25, "Configuración de ruta", format_cell_blue)
                elif line.state == "Route Configuration":
                       sheet.write(row, 25, "Configuración de ruta", format_cell_blue)
                elif line.state == "sale":
                       sheet.write(row, 25, "Ventas", format_cell_grey)
                elif line.state == "Sales":
                       sheet.write(row, 25, "Ventas", format_cell_grey)
                elif line.state == "reception":
                       sheet.write(row, 25, "Recepción de rutas", format_cell_orange)
                elif line.state == "Route Reception":
                       sheet.write(row, 25, "Recepción de rutas", format_cell_orange)
                elif line.state == "concil":
                       sheet.write(row, 25, "Conciliación de venta", format_cell_yellow)
                elif line.state == "Sale Conciliation":
                       sheet.write(row, 25, "Conciliación de venta", format_cell_yellow)
                elif line.state == "finish": #finish= cierre de caja para que coincida lo que hay en el la vista del reporte y el reporte en excel
                       sheet.write(row, 25, "Cierre de caja", format_cell_green)
                elif line.state == "Cash Box Closed":
                       sheet.write(row, 25, "Cierre de caja", format_cell_green)
                sheet.write(row, 26, line.employee_ids.name if line.employee_ids else '', format_cell)
                sheet.write(row, 27, line.x_studio_ayudante.name if line.x_studio_ayudante else '', format_cell)
                sheet.write(row, 28, line.justification, format_cell)
                row += 1