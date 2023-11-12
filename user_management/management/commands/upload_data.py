# yourapp/management/commands/insert_catalog_data.py
import pandas as pd
from django.core.management.base import BaseCommand
from user_management.models import UserCredentials, Catalog

class Command(BaseCommand):
    help = 'Insert data into the catalog table'

    def add_arguments(self, parser):
        parser.add_argument('excel_file', type=str, help='Path to the Excel file')

    def handle(self, *args, **kwargs):
        excel_file_path = kwargs['excel_file']

        try:
            df = pd.read_excel(excel_file_path)

            for index, row in df.iterrows():
                Catalog.objects.create(
                    product_id=row['product_id'],
                    product_category=row['Product_category'],
                    rank=row['Rank'],
                    brand_name=row['brand_name'],
                    product_description=row['product_description'],
                    price=row['price'],
                    image_link=row['image_link']
                )

            self.stdout.write(self.style.SUCCESS('Data inserted successfully.'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error: {e}'))

#used to insert out xlsx file in sqlited db