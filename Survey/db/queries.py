from db.config_db import db

async def execute_script(fname: str) -> None:
    with open(f'db/{fname}', 'r') as sql_script:
        await db.execute_script(sql_script.read())

async def save_results(**kwargs) -> None:
    keys = ','.join(list(kwargs.keys()))
    values = ','.join([f'''"{value}"''' if isinstance(value, str) else str(value)
                       for value in kwargs.values()])
    await db.execute(f"""
    INSERT INTO responses ({keys})
    VALUES ({values})
    """, perfomative=True)

async def check_user(user_id: int):
    result = await db.execute(f"""
    SELECT user_id FROM responses WHERE user_id={user_id}
    """)
    return True if result else False
