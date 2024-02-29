"""Example script to output everything as JSON string"""
import asyncio
import logging

from aiohttp import ClientSession
from audiconnectpy import AudiConnect, AudiException
from dotenv import dotenv_values
import json 

config = dotenv_values(".env")

#####################
## ACCESS VARIABLES (use .env is recommended)
##
VW_USERNAME = config.get("EMAIL", "test@example.de")
VW_PASSWORD = config.get("PASSWORD", "top-secret")
COUNTRY = config.get("COUNTRY", "DE")
SPIN = config.get("SPIN")
####################

JSON_INDENT=None # None to disable pretty print or > 0 for pretty print

logger = logging.getLogger()
logger.setLevel(logging.WARNING)

async def main() -> None:
    """Init method."""
    async with ClientSession() as session:
        api = AudiConnect(session, VW_USERNAME, VW_PASSWORD, COUNTRY, SPIN)
        try:
            await api.async_update()
            
            out = {}
            for vin, vehicle in api.vehicles.items():
                out[vin] = {
                    'vin': vin,
                    'model': vehicle.model,
                    'model_year': vehicle.model_year,
                    'title': vehicle.title,
                    'states': vehicle.states
                }
                
            print(json.dumps(out, indent=JSON_INDENT, default=str))  
        except AudiException as error:
            print(json.dumps({ 'error': str(error) }, indent=JSON_INDENT, default=str))

if __name__ == "__main__":
    asyncio.run(main())

