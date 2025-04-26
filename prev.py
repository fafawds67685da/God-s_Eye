import google.generativeai as genai
import time

# 🔐 Configure API Key
genai.configure(api_key="AIzaSyAv1zcbMVtQD2qEB8FUm-_HuQoTogXFWnE")

# Initialize model
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

generation_config = genai.types.GenerationConfig(
    max_output_tokens=100,  # ⬅️ Limit length of each reply
    temperature=0.5,        # Optional: controls creativity (0.0 = deterministic, 1.0+ = more creative)
    top_p=0.5,              # Optional: nucleus sampling
)
# Initialize two chat agents with separate histories
Dev = model.start_chat(history=[])
Nandini = model.start_chat(history=[])

# Set personalities
Dev_intro = "You're Dev 🌟 — College student learning about AI. Greet Nandini!"
Nandini_intro = "You're Nandini, you are sweet, studious, you have good smile, you are intelligent. Greet Dev!"

# Kick off the convo
Dev_response = Dev.send_message(Dev_intro, generation_config=generation_config).text
print("Dev:", Dev_response)
print('\n')
time.sleep(3) 
# Let them talk to each other
turns = 5
for i in range(turns):
    # Nova responds to Spark
    Nandini_response = Nandini.send_message(Dev_response, generation_config=generation_config).text
    print("Yash:", Nandini_response)
    time.sleep(5)
    print('\n') 

    # Spark responds to Nova
    Dev_response = Dev.send_message(Nandini_response, generation_config=generation_config).text
    print("Dev:", Dev_response)
    time.sleep(3) 
    print('\n')