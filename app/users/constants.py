ROLE_ADMIN = 'Admin'
ROLE_ANON = 'NotAuthorized'
ROLE_MANAGER = 'Manager'
ROLES = (
    (ROLE_ADMIN, 'Администратор'),
    (ROLE_MANAGER, 'Менеджер'),
    (ROLE_ANON, 'Аноним'),
)

STATUS_ACTIVE = 'Active'
STATUS_DISABLED = 'Disabled'
STATUS_DELETED = 'Deleted'
STATUS_ARCHIVE = 'Archive'

STATUSES = (
    (STATUS_ACTIVE, 'Активен'),
    (STATUS_DISABLED, 'Неактивен'),
    (STATUS_DELETED, 'Удален'),
    (STATUS_ARCHIVE, 'Архивный'),
)
