DEFAULT_FROM_EMAIL = 'victor gichohi <victorgichohi48@gmail.com>'


MANAGERS = (
    ('victor gichohi', "victorgichohi48@gmail.com"),
)

ADMINS = MANAGERS

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'victorgichohi48@gmail.com'
EMAIL_HOST_PASSWORD = 'amsupperman7470'

SECRET_KEY = 'ieh%hb=gdjxt$05bg076+t2%m)c7!7%6-ib8@$j9q2_traa$2g'