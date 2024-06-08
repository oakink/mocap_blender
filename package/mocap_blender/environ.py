from __future__ import annotations

import os
import platform
import importlib

def module_exists(module_name):
    try:
        importlib.import_module(module_name)
        return True
    except ImportError:
        return False

RUN_IN_BLENDER = module_exists('bpy')

def getEnvVar(key:str):
    return os.environ.get(key,"")

def getEnvVarAsList(key:str):
    value = getEnvVar(key)
    if not value:
        return [value]
    if platform.system().lower() == 'windows':
        return value.split(";")
    elif platform.system().lower() == 'linux':
        return value.split(":")
    else:
        raise Exception(f"系统未支持：{platform.system().lower()}")

def setEnvVar(key:str, value:str):
    os.environ[key] = value

def setEnvVarList(key:str, values:list[str]):
    if platform.system().lower() == 'windows':
        value = ";".join(values)
    elif platform.system().lower() == 'linux':
        value = ":".join(values)
    else:
        raise Exception(f"系统未支持：{platform.system().lower()}")
    setEnvVar(key, value)