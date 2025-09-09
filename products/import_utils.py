import yaml
import openpyxl
from django.db import transaction
from .models import Product, Category, ProductAttribute, ProductAttributeValue, Supplier, SupplierProduct


def import_products_from_yaml(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = yaml.safe_load(file)

    with transaction.atomic():
        for product_data in data.get('products', []):
            # Get or create category
            category_name = product_data.get('category')
            category, created = Category.objects.get_or_create(
                name=category_name,
                defaults={'description': f'Automatically created category for {category_name}'}
            )

            # Create product
            product, created = Product.objects.get_or_create(
                sku=product_data['sku'],
                defaults={
                    'name': product_data['name'],
                    'description': product_data.get('description', ''),
                    'category': category,
                    'weight': product_data.get('weight'),
                    'dimensions': product_data.get('dimensions'),
                }
            )

            # Add attributes
            for attr_name, attr_value in product_data.get('attributes', {}).items():
                attribute, created = ProductAttribute.objects.get_or_create(name=attr_name)
                ProductAttributeValue.objects.create(
                    product=product,
                    attribute=attribute,
                    value=attr_value
                )

            # Add supplier products
            for supplier_data in product_data.get('suppliers', []):
                supplier, created = Supplier.objects.get_or_create(
                    company_name=supplier_data['company_name'],
                    defaults={
                        'contact_person': supplier_data.get('contact_person', ''),
                        'phone_number': supplier_data.get('phone_number', ''),
                        'email': supplier_data.get('email', ''),
                        'address': supplier_data.get('address', ''),
                    }
                )

                SupplierProduct.objects.create(
                    supplier=supplier,
                    product=product,
                    price=supplier_data['price'],
                    stock_quantity=supplier_data.get('stock_quantity', 0),
                    min_order_quantity=supplier_data.get('min_order_quantity', 1),
                    lead_time_days=supplier_data.get('lead_time_days', 0)
                )


def import_products_from_excel(file_path):
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active

    with transaction.atomic():
        for row in sheet.iter_rows(min_row=2, values_only=True):
            sku, name, category_name, description, price, stock_quantity, supplier_name = row

            # Get or create category
            category, created = Category.objects.get_or_create(
                name=category_name,
                defaults={'description': f'Automatically created category for {category_name}'}
            )

            # Create product
            product, created = Product.objects.get_or_create(
                sku=sku,
                defaults={
                    'name': name,
                    'description': description,
                    'category': category,
                }
            )

            # Get or create supplier
            supplier, created = Supplier.objects.get_or_create(
                company_name=supplier_name,
                defaults={
                    'contact_person': 'Unknown',
                    'email': 'info@example.com',
                    'address': 'Unknown address',
                }
            )

            # Create supplier product
            SupplierProduct.objects.create(
                supplier=supplier,
                product=product,
                price=price,
                stock_quantity=stock_quantity,
                min_order_quantity=1,
                lead_time_days=0
            )