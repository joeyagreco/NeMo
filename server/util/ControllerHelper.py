import ast

from flask import Request


class ControllerHelper:
    """
    A helper class for controllers
    """

    @staticmethod
    def getDictFromRequestObj(requestObj: Request) -> dict:
        return ast.literal_eval(requestObj.data.decode("UTF-8"))
