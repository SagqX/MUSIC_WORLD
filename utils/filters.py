# Optional simple command filter aliasing, can be extended

from pyrogram import filters
import config

def command(names):
    return filters.command(names, prefixes=config.COMMAND_PREFIXES)
