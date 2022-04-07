from setuptools import setup, find_packages

setup (name='WooCommerceTesting',
    version = '1.0',
    description = 'API testing',
    Auther = 'LouisLiu',
    auther_email = 'yiliu915@gmail.com',
    packages = [
        'WooCommerceTesting',
        'WooCommerceTesting.src',
        'WooCommerceTesting.test',
    ],
    zip_safe=False,
    install_requires=[
        "pytest==6.2.5",
        "pytest-html==3.1.1",
        "requests==2.26.0",
        "requests-oauthlib==1.3.0",
        "PyMySQL==1.0.2",
        "WooCommerce==3.0.0"
    ]
    
       )