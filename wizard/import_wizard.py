from odoo import models, fields
from odoo.exceptions import UserError
import base64
import tempfile
import openpyxl


class ImportPricelistWizard(models.TransientModel):
    _name = 'import.pricelist.wizard'
    _description = 'Import Pricelist Wizard'

    file = fields.Binary("Excel File", required=True)
    filename = fields.Char("Filename")
    pricelist_id = fields.Many2one('product.pricelist', string="Pricelist", required=True)

    def action_import(self):
        if not self.file:
            raise UserError("Please upload an Excel file.")

        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
                tmp.write(base64.b64decode(self.file))
                tmp_path = tmp.name

            wb = openpyxl.load_workbook(tmp_path)
            sheet = wb.active

            for i, row in enumerate(sheet.iter_rows(min_row=2, values_only=True), start=2):
                product_code = row[0]
                price = row[1]

                if not product_code:
                    continue
                if price is None:
                    raise UserError(f"Row {i}: Price is missing.")

                # product = self.env['product.product'].search([('default_code', '=', product_code)], limit=1)
                product = self.env['product.product'].search([('id', '=', int(product_code))], limit=1)
                if not product:
                    raise UserError(f"Row {i}: Product with code '{product_code}' not found.")

                self.env['product.pricelist.item'].create({
                    'pricelist_id': self.pricelist_id.id,
                    'applied_on': '1_product',
                    'product_id': product.id,
                    'fixed_price': price,
                })

        except Exception as e:
            raise UserError(f"An error occurred while importing: {str(e)}")
