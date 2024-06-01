import aiosqlite
import warnings


class FitData:

    def __init__(self, fname: str):
        self.fname = fname

    async def execute(self, q: str, perfomative: bool = False, only_first: bool = False):
        # так как мы работаем асинхронно， то должны создавать соединение для каждой транзакции
        async with aiosqlite.connect(self.fname) as connection:
            connection.row_factory = aiosqlite.Row
            cursor = await connection.execute(q)
            if perfomative:
                if only_first:
                    warnings.warn(message='only_first has not effect when perfomative is True', category=SyntaxWarning)
                await connection.commit()
            else:
                if only_first:
                    return await cursor.fetchone()
                else:
                    return await cursor.fetchall()

    async def execute_script(self, script: str) -> None:
        async with aiosqlite.connect(self.fname) as connection:
            cursor = await connection.cursor()
            await cursor.executescript(script)
            await connection.commit()


db = FitData('survey.db')
