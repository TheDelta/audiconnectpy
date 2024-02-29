"""
    Example script
    Usage
        Install dependencies with `pip install async-timeout asyncio bs4 python-dotenv`
        Create a .env file in the same folder as this example.py file (or update the vars blow)
        Content of .env should be
        ```
        EMAIL=<your-email>
        PASSWORD=<your-pw>
        ```
        You can also change COUNTRY & SPIN
        ```
        COUNTRY=EN
        SPIN=1234
        ```
        Execute and hopefully you get some information :)
"""
import asyncio
import logging

from aiohttp import ClientSession
from audiconnectpy import AudiConnect, AudiException
from dotenv import dotenv_values

config = dotenv_values(".env")

#####################
## ACCESS VARIABLES (use .env is recommended)
##
VW_USERNAME = config.get("EMAIL", "test@example.de")
VW_PASSWORD = config.get("PASSWORD", "top-secret")
COUNTRY = config.get("COUNTRY", "DE")
SPIN = config.get("SPIN")
####################

"""Helper class for some CLI colors"""
class tcol:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    SUCCESS = '\033[92m'
    WARNING = '\033[93m'
    DANGER = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
# create console handler and set level to debug
ch = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s %(name)s [" + tcol.BOLD + "%(levelname)s" + tcol.END + "] | %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)

_LOGGER = logging.getLogger(__name__)

async def main() -> None:
    """Init method."""
    async with ClientSession() as session:
        api = AudiConnect(session, VW_USERNAME, VW_PASSWORD, COUNTRY, SPIN)

        try:
            await api.async_update()

            for vin, vehicle in api.vehicles.items():
                # 2024-02-29 atm not everything is due to new API format and endpoints!

                _LOGGER.info(tcol.CYAN + vin + tcol.END)
                _LOGGER.info(vehicle.model)
                _LOGGER.info(vehicle.model_year)
                _LOGGER.info(tcol.BOLD + "--- Supported Features ---" + tcol.END)
                # _LOGGER.info(vehicle.support_charger)
                # _LOGGER.info(vehicle.support_climater)
                # _LOGGER.info(vehicle.support_trip_cyclic)
                # _LOGGER.info(vehicle.support_trip_long)
                # _LOGGER.info(vehicle.support_trip_short)
                # _LOGGER.info(vehicle.support_position)
                # _LOGGER.info(vehicle.support_preheater)
                _LOGGER.info("Vehicle Info: %i", vehicle.support_vehicle)
                _LOGGER.info("Honkflash: %i", vehicle.support_honkflash or 0)
                # _LOGGER.info(vehicle.support_climater_timer)
    
                _LOGGER.info(tcol.BOLD + "--- Raw Data ---" + tcol.END)
                for attr, state in vehicle.states.items():
                    if isinstance(state, dict):
                        _LOGGER.info("%s", tcol.BOLD + tcol.UNDERLINE + attr + tcol.END)
                        for k, v in state.items():
                            if isinstance(v, list):   
                                _LOGGER.info("> %s:", tcol.BLUE + tcol.UNDERLINE + k + tcol.END)
                                for e in v:
                                    _LOGGER.info("=> %s", e)
                            else:
                                _LOGGER.info("> %s: %s", tcol.BLUE + k + tcol.END, v)
                    else:
                        _LOGGER.info("%s: %s", tcol.BOLD + attr + tcol.END, state)

                # vehicle.set_api_level("climatisation", 2)
                # vehicle.set_api_level("ventilation", 1)
                # vehicle.set_api_level("charger", 1)
                # await vehicle.async_set_lock(True)
                # await vehicle.async_set_battery_charger(True)
                # await vehicle.async_set_charger_max(32)
                # await vehicle.async_set_ventilation(True)
                # await vehicle.async_set_pre_heating(True)
                # await vehicle.async_set_climater(True)
                # await vehicle.async_set_climater_temp(20.5)
                # await vehicle.async_set_window_heating(Tru1e)
                # await vehicle.async_set_honkflash(mode="flash",duration=15)

        except AudiException as error:
            _LOGGER.error(error)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
