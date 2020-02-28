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
RESTART_DEVICE = 'restart_device'
SEND_LOGS = 'logs'

COMMANDS_REDIS_KEY = 'temp'

COMMANDS = (
    ('Показать информацию', SHOW_INFO),
    ('Перезагрузить программу', RESTART),
    ('Перезапустить устройство', RESTART_DEVICE),
    ('Отправить логи', SEND_LOGS),
)
