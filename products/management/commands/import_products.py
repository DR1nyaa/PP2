from django.core.management.base import BaseCommand
from apps.products.import_utils import import_products_from_yaml, import_products_from_excel
import os


class Command(BaseCommand):
    help = 'Import products from YAML or Excel files'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the import file')
        parser.add_argument('--format', type=str, default='yaml', choices=['yaml', 'excel'],
                            help='File format (yaml or excel)')

    def handle(self, *args, **options):
        file_path = options['file_path']
        file_format = options['format']

        if not os.path.exists(file_path):
            self.stderr.write(self.style.ERROR(f"File not found: {file_path}"))
            return

        try:
            if file_format == 'yaml':
                import_products_from_yaml(file_path)
                self.stdout.write(self.style.SUCCESS(f"Successfully imported products from YAML: {file_path}"))
            elif file_format == 'excel':
                import_products_from_excel(file_path)
                self.stdout.write(self.style.SUCCESS(f"Successfully imported products from Excel: {file_path}"))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error importing products: {str(e)}"))