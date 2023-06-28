from core import crypto
from core.ui import cli, gui

instance = crypto.Crypto()

cli.start(instance)
