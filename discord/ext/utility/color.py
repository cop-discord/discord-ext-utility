import asyncio, re, discord, pickle, math, webcolors, pkg_resources, os
from colorgram_rs import get_dominant_color
from itertools import chain
from discord.ext import commands
from fast_string_match import closest_match_distance as cmd, closest_match
from typing import Optional, Tuple, Any
from dataclasses import dataclass
from .globals import get_global, set_global

@dataclass
class NamedColor:
    hex: str
    name: str

def split_tuple_of_tuples(tuple_of_tuples: Tuple[Tuple[Any, Any]], size: Optional[int] = 4):
    chunk_size = len(tuple_of_tuples) // size
    return tuple(tuple_of_tuples[i:i + chunk_size] for i in range(0, len(tuple_of_tuples), chunk_size))

def load_color_map():
    try:
        colors = get_global("colors")
    except:
        package_dir = pkg_resources.resource_filename(__name__, '')
        pkl_file_path = os.path.join(package_dir, "colors.pkl")
        with open(pkl_file_path,'rb') as file:
            colors = split_tuple_of_tuples(pickle.load(file))
        set_global("colors", colors)
        return colors
    
colors = load_color_map()

async def color_picker_(query: str, colors: tuple):
    if match := cmd(query, [k[0] for k in colors]):
        return [m for m in colors if m[0] == match]
    return None

def hex_to_rgb(hex_color):
    # Remove '#' if present and split into RGB components
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_distance(color1, color2):
    r1, g1, b1 = color1
    r2, g2, b2 = color2
    return math.sqrt((r1 - r2)**2 + (g1 - g2)**2 + (b1 - b2)**2)

def nearest_color(target_color, color_list):
    target_rgb = hex_to_rgb(target_color)
    closest_color = None
    min_distance = float('inf')
    
    for color in color_list:
        color_rgb = hex_to_rgb(color)
        distance = rgb_distance(target_rgb, color_rgb)
        if distance < min_distance:
            min_distance = distance
            closest_color = color
            
    return closest_color

async def find_name(hex_: str):
    async def _find_name(hex_: str, colors: tuple):
        try: return [c for c in colors if c[1] == hex_][0]
        except: return None
    data = await asyncio.gather(*[_find_name(hex_, c) for c in colors])
    data = [d for d in data if d != None]
    if len(data) != 0: return data[0]
    else: return 'unnamed'

async def closest_color(color_hex: str, name: Optional[bool] = False):
    color_list = []
    for colo in colors:
        _color_list = [c[1] for c in colo]
        color_list.extend(_color_list)
    nearest = nearest_color(color_hex, color_list)
    match = next((c for colo in colors for c in colo if c[1] == nearest), None)
    rgb = webcolors.hex_to_rgb(color_hex)
    web_safe_rgb = [round(val / 51) * 51 for val in rgb]
    web_safe_hex = webcolors.rgb_to_hex(web_safe_rgb)
    if name == True:
        color_name = await find_name(web_safe_hex)
        data = (nearest, color_name[0])
    else:
        data = nearest
    return data

async def color_search(query: str):
    if query == 'black': return ('Black','#010101')
    if hex_match := re.match(r"#?[a-f0-9]{6}", query.lower()):
        color_name = await closest_color(query)

        return (color_name,query)
    matches = []
    matches = list(chain.from_iterable(await asyncio.gather(*[color_picker_(query, _) for _ in colors])))
    match = cmd(query, tuple([k[0] for k in matches]))
    return [m for m in matches if m[0] == match][0]


class ColorConverter(commands.ColourConverter):
    async def convert(self, ctx: commands.Context, argument: str) -> Optional[discord.Color]:
        if argument.lower().startswith("0x"):
            return discord.Color.from_str(argument)
        if argument.lower() == "dominant":
            _hex = await asyncio.to_thread(get_dominant_color,ctx.author.display_avatar.url)
        else:
            _hex = await color_search(argument)
            if isinstance(_hex, tuple): _hex = _hex[1]
        return discord.Color.from_str(f"#{_hex}" if not _hex.startswith("#") else _hex)

commands.converter.ColourConverter.convert = ColorConverter.convert

class NamedColorConverter(commands.Converter):
    async def convert(self, ctx: commands.Context, argument: str) -> Optional[NamedColor]:
        if argument.lower() == "dominant":
            _hex = await asyncio.to_thread(get_dominant_color,ctx.author.display_avatar.url)
            _hex = ('unnamed', _hex)
            color = await closest_color(_hex, True)
            _hex[1] = color[1]
        elif hex_match := re.match(r"#?[a-f0-9]{6}", argument.lower()):
            color_name = await closest_color(argument, True)
            _hex = (argument, color_name[1])
        else:
            _hex = await color_search(argument)
        return NamedColor(hex = _hex[1], name = _hex[0])
    
commands.converter.NamedColorConverter = NamedColorConverter

