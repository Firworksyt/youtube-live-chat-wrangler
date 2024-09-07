from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import yt_dlp
import json
from typing import List
import os

from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import yt_dlp
import json
from typing import List
import os
import tempfile

app = FastAPI()

# Global variable to store the path of the temporary directory
temp_dir = None

# Get the directory of the current file
current_dir = os.path.dirname(os.path.abspath(__file__))

# Mount static files
app.mount("/static", StaticFiles(directory=os.path.join(current_dir, "static")), name="static")

# Setup Jinja2 templates
templates = Jinja2Templates(directory=os.path.join(current_dir, "templates"))

class ChatMessage(BaseModel):
    username: str
    timestamp: str
    message: str

def process_emoji(run):
    if 'emoji' in run:
        emoji = run['emoji']
        if 'image' in emoji and 'thumbnails' in emoji['image']:
            # Get the smallest thumbnail URL (usually 24x24)
            thumbnail = min(emoji['image']['thumbnails'], key=lambda t: t.get('width', 0) or 0)
            if thumbnail:
                shortcut = emoji['shortcuts'][0] if 'shortcuts' in emoji and emoji['shortcuts'] else ''
                return f"<emoji-img src='{thumbnail['url']}' alt='{shortcut}'>"
    return run.get('text', '')

chat_messages: List[ChatMessage] = []

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "chat_messages": chat_messages})


@app.post("/download")
async def download_chat(url: str = Form(...)):
    global chat_messages, temp_dir
    chat_messages = []

    # Create a new temporary directory if it doesn't exist
    if not temp_dir or not os.path.exists(temp_dir):
        temp_dir = tempfile.mkdtemp()

    ydl_opts = {
        'skip_download': True,
        'writesubtitles': True,
        'subtitlesformat': 'json3',
        'subtitleslangs': ['live_chat'],
        'outtmpl': f'{temp_dir}/%(id)s.%(ext)s',
    }
  
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            video_id = info['id']
            chat_file = f"{temp_dir}/{video_id}.live_chat.json"
            
            if os.path.exists(chat_file):
                with open(chat_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        try:
                            chat_json = json.loads(line.strip())
                            if 'replayChatItemAction' in chat_json:
                                action = chat_json['replayChatItemAction']['actions'][0]
                                if 'addChatItemAction' in action:
                                    item = action['addChatItemAction']['item']
                                    if 'liveChatTextMessageRenderer' in item:
                                        message = item['liveChatTextMessageRenderer']
                                        processed_message = ''.join(process_emoji(run) for run in message['message']['runs'])
                                        chat_messages.append(ChatMessage(
                                            username=message['authorName']['simpleText'],
                                            timestamp=chat_json['replayChatItemAction']['videoOffsetTimeMsec'],
                                            message=processed_message
                                        ))
                        except json.JSONDecodeError as e:
                            print(f"Error parsing JSON line: {e}")
                            continue
                        except KeyError as e:
                            print(f"KeyError while processing message: {e}")
                            continue
                
                return JSONResponse(content={"status": "success", "message_count": len(chat_messages)})
            else:
                return JSONResponse(content={"status": "error", "message": f"Chat file not found: {chat_file}"}, status_code=404)
    except Exception as e:
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=500)
    
# Add a cleanup endpoint (optional, for manual cleanup)
@app.post("/cleanup")
async def cleanup_temp_files():
    global temp_dir
    if temp_dir and os.path.exists(temp_dir):
        for file in os.listdir(temp_dir):
            os.remove(os.path.join(temp_dir, file))
        os.rmdir(temp_dir)
        temp_dir = None
    return {"status": "success", "message": "Temporary files cleaned up"}

@app.get("/search")
async def search_chat(query: str = ''):
    filtered_messages = [msg.dict() for msg in chat_messages if query.lower() in msg.message.lower()]
    return JSONResponse(content=filtered_messages)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)