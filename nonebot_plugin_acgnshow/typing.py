from nonebot.adapters.onebot import v11, v12
from nonebot.adapters import satori
T_MessageEvent = v11.MessageEvent | v12.MessageEvent | satori.MessageEvent
