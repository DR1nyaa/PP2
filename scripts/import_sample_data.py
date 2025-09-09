#!/usr/bin/env python3
"""
Script to import sample data for testing.
"""
import os
import yaml
from django.core.management import execute_from_command_line


def create_sample_yaml():
    """Create sample YAML data file."""
    sample_data = {
        'products': [
            {
                'name': 'Ноутбук Dell XPS 13',
                'sku': 'DLXPS13-001',
                'description': '13-дюймовый бизнес-ноутбук',
                'category': 'Ноутбуки',
                'weight': 1.2,
                'attributes': {
                    'Процессор': 'Intel Core i7',
                    'Оперативная память': '16GB',
                    'SSD': '512GB'
                },
                'suppliers': [
                    {
                        'company_name': 'TechSupplier Inc.',
                        'contact_person': 'Иван Петров',
                        'email': 'tech@example.com',
                        'phone_number': '+79991234567',
                        'address': 'Москва, ул. Техническая, 1',
                        'price': 89999.99,
                        'stock_quantity': 15,
                        'min_order_quantity': 1,
                        'lead_time_days': 2
                    }
                ]
            }
        ]
    }

    os.makedirs('data', exist_ok=True)
    with open('data/sample_products.yaml', 'w', encoding='utf-8') as f:
        yaml.dump(sample_data, f, allow_unicode=True, default_flow_style=False)

    print("✅ Created sample data file: data/sample_products.yaml")


if __name__ == "__main__":

    create_sample_yaml()


    print("📦 Importing sample data...")
    execute_from_command_line(['manage.py', 'import_products', 'data/sample_products.yaml', '--format', 'yaml'])

    print("✅ Sample data imported successfully!")