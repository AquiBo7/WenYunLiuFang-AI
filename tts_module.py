import edge_tts
import asyncio

async def _generate(text,path):
    comm=edge_tts.Communicate(text,"zh-CN-XiaoxiaoNeural",rate="+0%")
    await comm.save(path)

def text_to_speech(text,path="speech.mp3"):
    try:
        asyncio.run(_generate(text,path))
        return path
    except Exception as e:
        return None