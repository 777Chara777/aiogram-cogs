from aiogram import Dispatcher, Bot
from typing import Generator

import sys, os

mismodules = sys.modules

mlistdir = lambda path : os.listdir(path)

class __Module(Exception): pass
def initModule(Module: str) -> "False | __Module":
    """Module initialization"""
    try:
        __import__(Module)
    except Exception as ex:
        return {"Type": False, "Message": ex}
    if Module in mismodules:
        return {"Type": True, "Module": mismodules[Module]}
    return {"Type": False, "Message": None}

class RegisterCogs(Dispatcher):
    def __init__(self):
        super().__init__(Bot("0:F-1"))

class LoadCogs:
    def __init__(self, core_self: Bot, core_dp: Dispatcher, path_cogs: str, prefix = "cog_") -> None:
        self.main_core = core_self
        self.core_dp = core_dp
        self.cogs = path_cogs
        self.prefix_file = prefix

        self.lfic = [ 
            file for file in mlistdir(self.cogs) if \
             ( file.startswith(self.prefix_file) and file.endswith(".py") )
         ] # lfic -> list file in cogs

    def loadcogs(self) -> Generator:
        for file in self.lfic:
            path_file: str = self.cogs.replace("\\", "/") + file if self.cogs.endswith("/") else "/%s" % file

            data = initModule(path_file.replace("/", ".")[:-3])
            data_module_message = data["Module"] if data["Type"] else data["Message"]

            try:
                if data["Type"]:
                    data["Module"].setup(self)
            except Exception as ex:
                data_module_message = ex
                data["Type"] = False
            yield (path_file.replace("/", "."), data["Type"], data_module_message)

    def register(self, dp: RegisterCogs):
        for hader in [hader for hader in self.core_dp.__dict__ if hader.endswith("_handlers")]:
            self.core_dp.__dict__[hader].handlers += dp.__dict__[hader].handlers