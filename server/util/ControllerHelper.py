import ast

from flask import Request


class ControllerHelper:
    """
    A helper class for controllers
    """

    @staticmethod
    def getDictFromRequestObj(request: Request) -> dict:
        return ast.literal_eval(request.data.decode("UTF-8"))
