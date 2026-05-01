from django.core.management.base import BaseCommand
from django.utils.text import slugify
from store.models import Category, Product


class Command(BaseCommand):
    help = 'Seed the database with sample car fashion products'

    def handle(self, *args, **kwargs):
        # Categories
        categories_data = [
            ('Lighting & LEDs', 'lighting', 'Premium LED lighting upgrades for your car'),
            ('DRLs', 'drls', 'Daytime Running Light kits and upgrades'),
            ('Body Kits', 'body-kits', 'Stylish body modification kits'),
            ('Interior Accessories', 'interior', 'Premium interior styling accessories'),
            ('Performance Parts', 'performance', 'Boost your car performance'),
            ('Wraps & Vinyl', 'wraps', 'Car wraps and vinyl accessories'),
        ]

        cats = {}
        for name, slug, desc in categories_data:
            cat, _ = Category.objects.get_or_create(
                slug=slug, defaults={'name': name, 'description': desc}
            )
            cats[slug] = cat
            self.stdout.write(f'Category: {name}')

        # Products
        products = [
            # Lighting
            {'name': 'H4 LED Headlight Bulb Pair', 'category': 'lighting', 'price': 1499, 'stock': 50, 'brand': 'LumaPro', 'featured': True, 'desc': 'Ultra-bright 6000K LED headlight bulbs with easy plug-and-play installation. 12000LM output, waterproof IP68 rating. Fits most Indian cars.'},
            {'name': 'H11 Fog Light LED Bulbs', 'category': 'lighting', 'price': 899, 'stock': 35, 'brand': 'LumaPro', 'featured': False, 'desc': 'Yellow or white LED fog light bulbs for enhanced visibility in fog and rain. 45W equivalent brightness.'},
            {'name': 'Interior LED Strip Lights Kit', 'category': 'lighting', 'price': 649, 'stock': 80, 'brand': 'GlowFlex', 'featured': False, 'desc': 'RGB LED strip lights for car interior ambiance. App-controlled, music sync, 16 million colors.'},
            {'name': 'LED Number Plate Light', 'category': 'lighting', 'price': 299, 'stock': 100, 'brand': 'AutoGlow', 'featured': False, 'desc': 'Ultra-white LED license plate lights. Direct OEM replacement, no modifications required.'},

            # DRLs
            {'name': 'Universal DRL LED Strip 60cm', 'category': 'drls', 'price': 1299, 'stock': 40, 'brand': 'DayLight Pro', 'featured': True, 'desc': 'Universal flexible DRL strips with auto on/off with ignition. 12V, IP67 waterproof, aluminum housing.'},
            {'name': 'DRL + Turn Signal Combo Strip', 'category': 'drls', 'price': 1899, 'stock': 25, 'brand': 'DayLight Pro', 'featured': True, 'desc': 'DRL with integrated turn signal function. Sequential amber signal, white DRL. Plug and play.'},
            {'name': 'Round DRL Angel Eye 70mm', 'category': 'drls', 'price': 799, 'stock': 60, 'brand': 'AngelRing', 'featured': False, 'desc': 'Round halo ring DRL lights for fog lamp housing. 70mm diameter, ultra bright white.'},

            # Body Kits
            {'name': 'Universal Front Bumper Lip Spoiler', 'category': 'body-kits', 'price': 2499, 'stock': 15, 'brand': 'AeroStyle', 'featured': True, 'desc': 'Flexible ABS plastic front bumper lip. Universal fit, easy adhesive + screw installation. Available in gloss black.'},
            {'name': 'Side Skirt Extensions (Pair)', 'category': 'body-kits', 'price': 3499, 'stock': 10, 'brand': 'AeroStyle', 'featured': False, 'desc': 'Aerodynamic side skirt extensions to enhance the sporty look of your car. Lightweight ABS plastic.'},
            {'name': 'Rear Roof Spoiler - Universal', 'category': 'body-kits', 'price': 1899, 'stock': 20, 'brand': 'SportForm', 'featured': False, 'desc': 'Universal rear roof spoiler for a sporty look. Easy 3M tape installation. Gloss black finish.'},

            # Interior
            {'name': 'Carbon Fiber Interior Trim Kit', 'category': 'interior', 'price': 1599, 'stock': 30, 'brand': 'CarbonLux', 'featured': True, 'desc': 'Dashboard and door panel carbon fiber look trim kit. Universal set, high-quality vinyl wrap finish.'},
            {'name': 'Sports Steering Wheel Cover', 'category': 'interior', 'price': 449, 'stock': 70, 'brand': 'GripKing', 'featured': False, 'desc': 'Microfiber leather steering wheel cover with anti-slip grip. Universal 38cm size.'},
            {'name': 'LED Puddle Lights (Set of 4)', 'category': 'interior', 'price': 699, 'stock': 55, 'brand': 'AutoGlow', 'featured': False, 'desc': 'LED door puddle/courtesy lights with CarFashion logo projection. Waterproof, plug and play.'},
            {'name': 'Car Seat Cover Set - Sports', 'category': 'interior', 'price': 2999, 'stock': 12, 'brand': 'ComfortRide', 'featured': True, 'desc': 'Full set sport seat covers in breathable mesh fabric with cushion support. Universal fit for most sedans and hatchbacks.'},

            # Performance
            {'name': 'Short Throw Gear Shift Knob', 'category': 'performance', 'price': 899, 'stock': 45, 'brand': 'ShiftFast', 'featured': False, 'desc': 'Weighted aluminum gear shift knob for sporty feel and precise gear changes. Universal thread adapters included.'},
            {'name': 'Sport Air Filter (Universal)', 'category': 'performance', 'price': 599, 'stock': 35, 'brand': 'FlowMax', 'featured': False, 'desc': 'High-flow reusable sport air filter for improved throttle response and engine breathing.'},

            # Wraps
            {'name': 'Matte Black Vinyl Wrap Film 1.52m x 1m', 'category': 'wraps', 'price': 849, 'stock': 50, 'brand': 'WrapKing', 'featured': True, 'desc': 'Premium air-release matte black vinyl wrap film. Easy application, removable, no residue. Perfect for roof, hood, mirrors.'},
            {'name': 'Chrome Delete Kit - Gloss Black', 'category': 'wraps', 'price': 1199, 'stock': 25, 'brand': 'WrapKing', 'featured': False, 'desc': 'Pre-cut chrome delete vinyl strips for grille, window trim, and door handles. Gloss or satin black finish.'},
        ]

        for p_data in products:
            name = p_data['name']
            slug = slugify(name)
            # Make slug unique if needed
            counter = 1
            original_slug = slug
            while Product.objects.filter(slug=slug).exists():
                slug = f'{original_slug}-{counter}'
                counter += 1

            Product.objects.get_or_create(
                slug=slug,
                defaults={
                    'name': name,
                    'category': cats[p_data['category']],
                    'price': p_data['price'],
                    'stock': p_data['stock'],
                    'brand': p_data['brand'],
                    'is_featured': p_data['featured'],
                    'description': p_data['desc'],
                    'is_available': True,
                }
            )
            self.stdout.write(f'Product: {name}')

        self.stdout.write(self.style.SUCCESS('\n✅ Sample data seeded successfully!'))
        self.stdout.write('Categories: 6 | Products: 18')
        self.stdout.write('Run: python manage.py createsuperuser — to create admin account')
