from abc import ABC, abstractmethod


class IModel:

    @abstractmethod
    async def add():
        pass

    @abstractmethod
    async def delete():
        pass

    @abstractmethod
    async def get():
        pass

    @abstractmethod
    async def update():
        pass
