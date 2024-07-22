CREATOR_CATEGORY_CHOICES = (
    ('', ''),
    ('artist', 'Artist'),
    ('musician', 'Musician'),
    ('videocreator', 'Video Creator'),
    ('podcaster', 'Podcaster'),
    ('other', 'Other'),
)

ISP_CHOICES = (
    ('', ''),
    ('mtn', 'mtn'),
    ('airtel', 'airtel'),
)

CITY_CHOICES = (
    ('kitwe', 'Kitwe'),
    ('lusaka', 'Lusaka'),
    ('ndola', 'Ndola'),
)

default_socials = {
    'fb': 'https://facebook.com',
    'x': 'https://twitter.com',
    'lk': 'https://linkedin.com',
    'ig': 'https://instagram.com',
}

STATUS_CHOICES = (
    ('pending', 'pending'),
    ('success', 'success'),
    ('failed', 'failed'),
)

BUSINESS_CATEGORY_CHOICES = (
    ('school', 'School'),
    ('grocery', 'Grocery'),
    ('independent_online_retailers', 'Independent Online Retailers'),
    ('other', 'Other'),
)


INVOICE_STATUS_CHOICES = (
    ('pending', 'pending'),
    ('paid', 'paid'),
    ('rejected', 'rejected'),
)

zambia_provinces = {
    '01': 'Central',
    '02': 'Copperbelt',
    '03': 'Eastern',
    '04': 'Luapula',
    '05': 'Lusaka',
    '06': 'Muchinga',
    '07': 'Northern',
    '08': 'North-Western',
    '09': 'Southern',
    '10': 'Western'
}
