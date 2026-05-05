import requests
import asyncio
from pyrogram import filters
from pyrogram.types import Message
from VIVAANXMUSIC import app

WAIFU_IM_API_URL = "https://api.waifu.im/images"
WAIFU_PICS_API_URL = "https://api.waifu.pics/sfw/waifu"
WAIFU_PICS_TAGS = {
    "waifu",
    "neko",
    "shinobu",
    "megumin",
    "bully",
    "cuddle",
    "cry",
    "hug",
    "awoo",
    "kiss",
    "lick",
    "pat",
    "smug",
    "bonk",
    "yeet",
    "blush",
    "smile",
    "wave",
    "highfive",
    "handhold",
    "nom",
    "bite",
    "glomp",
    "slap",
    "kill",
    "kick",
    "happy",
    "wink",
    "poke",
    "dance",
    "cringe",
}


@app.on_message(filters.command("waifu"))
async def waifu_command_handler(_, message: Message):
    try:
        args = message.text.split(maxsplit=1)
        tag = args[1] if len(args) > 1 else "maid"

        waifu_data = await asyncio.to_thread(get_waifu_data, tag)

        if waifu_data and 'images' in waifu_data and waifu_data['images']:
            image = waifu_data['images'][0]
            await message.reply_photo(
                photo=image["url"],
                caption=f"🌸 ʜᴇʀᴇ'ꜱ ʏᴏᴜʀ ᴡᴀɪꜰᴜ ({tag})"
            )
        else:
            await message.reply_text("❌ ɴᴏ ᴡᴀɪꜰᴜꜱ ꜰᴏᴜɴᴅ ᴡɪᴛʜ ᴛʜᴀᴛ ᴛᴀɢ.")

    except Exception as e:
        await message.reply_text(f"⚠️ ᴇʀʀᴏʀ: `{str(e)}`")


def get_waifu_data(tag):
    normalized_tag = (tag or "waifu").strip().lower() or "waifu"

    for params in (
        {"IncludedTags": normalized_tag, "IsNsfw": "False", "PageSize": 1},
        {"IncludedTags": "waifu", "IsNsfw": "False", "PageSize": 1},
        {"IsNsfw": "False", "PageSize": 1},
    ):
        try:
            response = requests.get(
                WAIFU_IM_API_URL,
                params=params,
                timeout=12,
            )
            if response.status_code == 200:
                payload = response.json()
                items = payload.get("items") or []
                if items:
                    return {
                        "images": [{"url": items[0].get("url")}],
                        "source": "waifu.im",
                    }
        except Exception:
            pass

    fallback_tag = normalized_tag if normalized_tag in WAIFU_PICS_TAGS else "waifu"
    try:
        response = requests.get(
            f"{WAIFU_PICS_API_URL.rsplit('/', 1)[0]}/{fallback_tag}",
            timeout=12,
        )
        if response.status_code == 200:
            image_url = response.json().get("url")
            if image_url:
                return {"images": [{"url": image_url}], "source": "waifu.pics"}
    except Exception:
        pass

    return None
