# import nonebot
from nonebot import get_driver
from nonebot.plugin import on_startswith

from .config import Config

global_config = get_driver().config
config = Config(**global_config.dict())

# Export something for other plugin
# export = nonebot.export()
# export.foo = "bar"

# @export.xxx
# def some_function():
#     pass


from nonebot import on_command
from nonebot.rule import to_me
from nonebot.permission import Permission
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event

# weather = on_command("天气", rule=to_me(), permission=Permission(), priority=5)

# @weather.handle()
# async def handle_first_receive(bot: Bot, event: Event, state: T_State):
#     args = str(event.get_message()).strip()  # 首次发送命令时跟随的参数，例：/天气 上海，则args为上海
#     if args:
#         state["city"] = args  # 如果用户发送了参数则直接赋值


# @weather.got("city", prompt="你想查询哪个城市的天气呢？")
# async def handle_city(bot: Bot, event: Event, state: T_State):
#     city = state["city"]
#     if city not in ["上海", "北京"]:
#         await weather.reject("你想查询的城市暂不支持，请重新输入！")
#     city_weather = await get_weather(city)
#     await weather.finish(city_weather)

# async def get_weather(city: str):
#     return f"{city}的天气是..."

# fag_dice_event = on_startswith(',', rule=to_me, permission=Permission(), priority=5)
fag_dice_event = on_startswith(',',  permission=Permission(), priority=1)

# @fag_dice_event.handle()
@fag_dice_event.receive()
async def load_input_handle(bot: Bot, event: Event, state: T_State):
    raw_input = str(event.get_message()).strip()[1:]
    args = raw_input.split()
    if args:
        state['args'] = args

    # result = miaos_resolver(bot, event, state)
    # if result['action'] == 'send':
    #     # await bot.send(event, 'success')
    #     await fag_dice_event.finish(result['message'])
    #     await fag_dice_event.stop_propagation()
        

@fag_dice_event.got('args')
async def resolve_args(bot: Bot, event: Event, state: T_State):
    result = miaos_resolver(bot, event, state)
    if result['action'] == 'send':
        await fag_dice_event.finish(result['message'])
    