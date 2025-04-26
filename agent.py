import google.generativeai as genai
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, Response
import threading
import uvicorn

# 🔐 Configure API Key
genai.configure(api_key="AIzaSyAv1zcbMVtQD2qEB8FUm-_HuQoTogXFWnE")

# 🎯 Initialize the model
model = genai.GenerativeModel(model_name="gemini-2.5-flash")

# ⚙️ Configuration
generation_config = genai.types.GenerationConfig(
    max_output_tokens=100,
    temperature=0.5,
    top_p=0.5,
)

# 🤖 Create Dev agent
Dev = model.start_chat(history=[])
Dev_intro = "You're Dev 🌟 — a college student who loves exploring AI. Greet the user!"
print("Say hi to Dev! Type 'exit' to quit.\n")
Dev_response = Dev.send_message(Dev_intro, generation_config=generation_config).text

# FastAPI app
app = FastAPI()
detected_class = []

@app.post("/detect")
async def receive_detected_objects(request: Request):
    data = await request.json()
    obj = data.get('objects', [])
    
    objects = data.get('objects', [])
    if objects:
        detected_class.extend(objects)  # <<-- use extend to add each object separately
        print("object(s) detected\n")


    return Response(status_code=204)

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_input = data.get("user_input", "")

    # Compose message
    msg = user_input
    if detected_class:
        # If we have detected objects, add them to the message
        msg += f" (Detected objects in the background: {', '.join(detected_class)}. Comment on them and take into consideration for your response.)"
        print(msg)
        
    response = Dev.send_message(msg, generation_config=generation_config).text
    return JSONResponse(content={"response": response})

# Start the FastAPI server in a separate thread
def start_fastapi():
    uvicorn.run(app, host="0.0.0.0", port=5001)

threading.Thread(target=start_fastapi).start()
