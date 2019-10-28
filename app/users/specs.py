from app.common.specs import success_response_schema


USER_MODEL_NAME = 'User'


models = {
    USER_MODEL_NAME: {
        'id': int,
        'name': str,
        'email': str,
        'role': str,
        'status': str,
        'created_at': str,
        'updated_at': str,
    },
}

list_view = dict(
    summary='User list',
    tags=['USERS'],
    responses={
        '200': success_response_schema(
            description='Example of request',
            resp=USER_MODEL_NAME,
            is_list=True
        )
    }
)

user_by_id_view = dict(
    summary='User by id',
    tags=['USERS'],
    responses={
        '200': success_response_schema(
            description='Example of request',
            resp=USER_MODEL_NAME
        )
    }
)

add_user_view = dict(
    summary='User create',
    tags=['USERS'],
    responses={
        '200': success_response_schema(
            description='Example of request',
            resp=USER_MODEL_NAME
        )
    }
)

update_user_view = dict(
    summary='User update',
    tags=['USERS'],
    responses={
        '200': success_response_schema(
            description='Example of request',
            resp=USER_MODEL_NAME
        )
    }
)

delete_user_view = dict(
    summary='User by id',
    tags=['USERS'],
    responses={
        '200': success_response_schema(
            description='Example of request',
            resp=USER_MODEL_NAME
        )
    }
)
