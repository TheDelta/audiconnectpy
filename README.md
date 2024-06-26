# Fork of audiconnectpy

This is a fork to test and fix the API changes. The old api was shutdown ~ February 2024.

## Usage (example.py)

1. Clone / download this repository
2. Create a `.env` file next to the `example.py` file
3. The contents of the file should have at least `EMAIL` and `PASSWORD`.
   - You can also change `COUNTRY` and `SPIN`,
    ```
    EMAIL=<your-email>
    PASSWORD=<your-pw>
    COUNTRY=DE
    SPIN=1234
    ```
4. Ensure that you have the dependencies installed (`pip install -r requirements.txt`)
5. Execute the script with `python example.py` and you should see some DEBUG stuff and at the end your Audi data 😁

The output data key/values slightly changed and is not fully functional with legacy *yet*.

## changes

- Fix Vehicle Information & Position data
  - data format changed, so not compatible with legacy yet (homeassistant integration, etc.)
- Added python-env for safer credentials storage 😅
- Added some colors to the example 🥳
- Added json print example

> Was tested on my 2023 Audi RS 3 Sportback TFSI quattro S tronic 🚀

---


(below is the original readme)

# audiconnectpy

[![GitHub sourcecode](https://img.shields.io/badge/Source-GitHub-green)](https://github.com/cyr-ius/audiconnectpy/)
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/cyr-ius/audiconnectpy)](https://github.com/cyr-ius/audiconnectpy/releases/latest)
![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/audiconnectpy?label=PyPI%20Downloads)](https://pypi.org/project/audiconnectpy/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/weconnect)](https://pypi.org/project/audiconnectpy/)

The audiconnect component provides an integration with the Audi Connect cloud service. It adds presence detection, sensors such as range, mileage, and fuel level, and provides car actions such as locking/unlocking and setting the pre-heater.

Note: Certain functions require special permissions from Audi, such as position update via GPS.

Credit for initial API discovery go to the guys at the ioBroker VW-Connect forum, who were able to figure out how the API and the PIN hashing works. Also some implementation credit to davidgiga1993 of the original AudiAPI Python package, on which some of this code is loosely based.

## Warning

Use this API with care. If you use it wrong (e.g. too many logins, repeated login attempts with wrong password, ...) your account may get blocked.

## Install

Use the PIP package manager

```bash
pip install audiconnectpy
```

Or manually download and install the last version from github

```bash
git clone https://github.com/cyr-ius/audiconnectpy.git
python setup.py install
```

## Get started

```python
# Import the audiconnectpy package.
from audiconnectpy import AudiConnect

async def main():
    async with ClientSession() as session:
        api = AudiConnect(session, VW_USERNAME, VW_PASSWORD, COUNTRY, SPIN)
        await api.async_update()
        print(api.vehicles)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
```

Have a look at the [example.py](https://github.com/cyr-ius/audiconnectpy/blob/master/example.py) for a more complete overview.

## Login & Consent

Audiconectpy is based on the new Carnet ID API that was introduced with the new series of ID cars. If you use another car or hybrid you probably need to agree to the terms and conditions of the My Audi interface. Easiest to do so is by installing the My Audi app on your smartphone and login there. If necessary you will be asked to agree to the terms and conditions.

## Credits

Inspired by :

- [arjenvrh/audi_connect_ha](https://github.com/arjenvrh/audi_connect_ha)
- [tknaller/openhab-addons](https://github.com/tknaller/openhab-addons)
- [davidgiga1993/AudiAPI](https://github.com/davidgiga1993/AudiAPI)
