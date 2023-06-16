from aiogram import Dispatcher, Bot

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
    '''
The LoadCogs class is responsible for loading and registering cogs in a project. It provides methods to load cogs from a specified directory, retrieve information about the loaded cogs, and register them in the project's dispatcher.

Constructor:

__init__(self, core_dp: Dispatcher, path_cogs: str, prefix="cog_")
Initializes the LoadCogs class with the core bot instance, dispatcher instance, path to the cog files directory, and optional prefix for cog file names.
Methods:

loadcogs(self) -> Generator
Loads cogs from the specified directory and returns a generator with information about the loaded cogs.
Yields a tuple containing the cog's module path, a boolean indicating whether the loading was successful, and any error or status message associated with the cog.
register(self, dp: RegisterCogs)
Registers the loaded cogs in the provided RegisterCogs dispatcher.
Adds the loaded cogs' handlers to the dispatcher's handlers list.
Usage:

Create an instance of the LoadCogs class, providing the necessary parameters.
Use the loadcogs() method to load the cogs from the specified directory and retrieve information about them.
Optionally, process and handle the information about the loaded cogs.
Register the loaded cogs in the dispatcher by calling the register() method and passing the appropriate RegisterCogs instance.
Note: The LoadCogs class assumes that the cogs follow a specific naming convention, where their file names start with the specified prefix and end with the ".py" extension.
    '''
    def __init__(self, core_dp: Dispatcher, path_cogs: str, prefix = "cog_") -> None:
        self.core_dp = core_dp
        self.cogs = path_cogs
        self.prefix_file = prefix

        self.lfic = [ 
            file for file in mlistdir(self.cogs) if \
             ( file.startswith(self.prefix_file) and file.endswith(".py") )
         ] # lfic -> list file in cogs

    def loadcogs(self):
        """ This method loads the cogs from the specified directory and returns a generator with information about the loaded cogs. In each iteration of the generator, a tuple in the format (file_path, loaded_successfully, load_info) is returned."""
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
        """This method registers the loaded cogs in the RegisterCogs dispatcher."""
        for hader in [hader for hader in self.core_dp.__dict__ if hader.endswith("_handlers")]:
            self.core_dp.__dict__[hader].handlers += dp.__dict__[hader].handlers