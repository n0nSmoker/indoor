UNAPPROVED = 'unapproved'
APPROVED = 'approved'
ACTIVE = 'active'
INACTIVE = 'inactive'

STATUSES = (
    ('Подтверждена', APPROVED),
    ('Не подтверждена', UNAPPROVED),
    ('Актиивна', ACTIVE),
    ('Не актиивна', INACTIVE),
)

SHOW_INFO = 'info'
RESTART = 'restart'
RESTART_DEVICE = 'restart device'
SEND_LOGS = 'logs'

COMMAND = (
    ('', SHOW_INFO),
    ('', RESTART),
    ('', RESTART_DEVICE),
    ('', SEND_LOGS),
)
