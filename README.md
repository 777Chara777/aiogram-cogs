# aiogram-cogs

The project involves using the aiogram library to create a chat bot using the cogs mechanism. Cogs are modules that contain message and command handlers for the bot. They allow for a more organized code structure by logically separating it into individual components.

The project defines two classes: RegisterCogs and LoadCogs. The RegisterCogs class inherits from the Dispatcher class and is used to register cogs in the aiogram dispatcher. The LoadCogs class is used to load and register cogs in the project. It takes instances of the Bot and Dispatcher classes, the path to the directory containing the cog files, and the prefix for cog files.

The loadcogs method of the LoadCogs class loads cogs from the specified directory and returns a generator with information about the loaded cogs. The register method of the LoadCogs class registers the loaded cogs in the RegisterCogs dispatcher.


## Usage:

### In the file `index.py`:
```py
import aiogram
import aiogram_cogs.cogs as aiocogs

core_aiobot = aiogram.Bot(self.token)
core_dp = aiogram.Dispatcher(self.core_aiobot)

cogs = aiocogs.LoadCogs(self, "cogs/")

for name_module, respons, module_info in cogs.loadcogs():
    logger.log("INFO" if respons else "WARNING", \
        logger._core.options, \
        "['loadCogs'] %s is %s" % (name_module, "Done" if respons else f"Error \n - {module_info}") 
    )

aiogram.executor.start_polling(self.core_dp, skip_updates=True, on_startup=self.on_startup)
```

In the index.py file, instances of the Bot and Dispatcher classes are created, and then cogs are loaded and registered using the LoadCogs class. Information about the result of each loaded cog is printed. The message listening loop is started using the start_polling function.


### In the file `cogs_test.py`:

```py
from aiogram_cogs.cogs import RegisterCogs

dp = RegisterCogs()

@dp.message_handler(commands=["ping"], commands_prefix=prefix)
async def fun_chuck(message: types.Message):
    await message.reply("Pong")

def setup(cogs_logger):
    cogs_logger.register(dp)
```

In the cogs_test.py file, an example cog named fun_chuck is defined, which handles the "ping" commands. The setup function is used to register this cog in the dispatcher through the cogs_logger object.
