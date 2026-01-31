# Standard Library Imports
import cmd
import logging


logging.basicConfig(
    datefmt="\033[1m\033[2m%Y-%m-%d %H:%M:%S\033[0m",
    format="%(asctime)s %(levelname)-6s %(filename)s %(lineno)-3d %(message)s",
    level=logging.INFO,
)


class RevuShell(cmd.Cmd):
    intro = 'Revu: \n'
    prompt = '> '

    def __init__(self, config: dict) -> None:
        super().__init__()
        self.config = config
    
    def do_df(self, arg) -> bool:
        self.config["default"] = True
        logging.info("Loading default cogs!")
        return True
     
    def do_load(self, arg) -> None:
        cog = arg.strip()
        if cog:
            if cog in self.config["cogs"]:
                logging.error("Cog already added.")
            else:
                if cog in self.config["a_cogs"]:
                    self.config["cogs"].append(cog)
                    logging.info("Cog has been added!" )
                else:
                    logging.error("Cog does not exist.")

    def do_show(self, arg) -> None:
        logging.info(f"Current added cogs: {self.config["cogs"]}")


class GARYShell(cmd.Cmd):
    intro = 'GARY: \n'
    prompt = '> '

    def __init__(self, config: dict) -> None:
        super().__init__()
        self.config = config
    
    def do_df(self, arg) -> bool:
        self.config["default"] = True
        logging.info("Loading default cogs!")
        return True
     
    def do_load(self, arg) -> None:
        cog = arg.strip()
        if cog:
            if cog in self.config["cogs"]:
                logging.error("Cog already loaded.")
            else:
                if cog in self.config["a_cogs"]:
                    self.config["cogs"].append(cog)
                    logging.info("Cog has been loaded!" )
                else:
                    logging.error("Cog does not exist.")

    def do_show(self, arg) -> None:
        logging.info(f"Current loaded cogs: {self.config["cogs"]}")
