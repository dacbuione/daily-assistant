import json
import requests
from db import insert_user_info, get_user_info
from retrieval_module import search_data

url = "https://api.awanllm.com/v1/chat/completions"
AWANLLM_API_KEY = "7f6ad997-97b7-46b5-8e02-6520f7616c19"

def analyze_question(user_message):
    # Use LLM to analyze the question and determine what information is needed
    analysis_prompt = f"Phân tích câu hỏi: {user_message}. Xác định thông tin cần thiết để trả lời."
    payload = json.dumps({
        "model": "Meta-Llama-3-8B-Instruct",
        "messages": [{"role": "user", "content": analysis_prompt}],
        "max_tokens": 150
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {AWANLLM_API_KEY}"
    }
    response = requests.post(url, headers=headers, data=payload)
    analysis_result = response.json().get('choices', [{}])[0].get('message', {}).get('content', '')
    return analysis_result

def process_chat(user_message):
    user_info = get_user_info()

    if not user_info:
        # If no user info, ask for name
        if "tên" in user_message.lower():
            return "Vui lòng cho tôi biết tên của bạn."
        elif "cân nặng" in user_message.lower():
            return "Bạn nặng bao nhiêu kg?"
        elif "chiều cao" in user_message.lower():
            return "Bạn cao bao nhiêu cm?"
        elif "mục tiêu sức khỏe" in user_message.lower():
            return "Mục tiêu sức khỏe của bạn là gì?"
        else:
            # Collect user information
            return "Xin chào! Tôi cần một số thông tin để bắt đầu. Bạn có thể cho tôi biết tên của bạn không?"

    # If user info exists, process normally
    analysis_result = analyze_question(user_message)
    relevant_data = search_data(analysis_result)
    relevant_text = " ".join([item[0] for item in relevant_data]) if relevant_data else "Không có dữ liệu liên quan."

    # Step 3: Fetch user information if needed
    user_info = get_user_info()
    if user_info:
        weight, height, health_goal = user_info[0][1], user_info[0][2], user_info[0][4]
        user_context = f"Cân nặng: {weight}kg, Chiều cao: {height}cm, Mục tiêu sức khỏe: {health_goal}."
    else:
        user_context = "Không có thông tin người dùng."

    # Step 4: Construct the final prompt with analysis, retrieved data, and user context
    final_prompt = f"Người dùng hỏi: {user_message}. {user_context} {relevant_text} Trả lời như một trợ lý cá nhân của người dùng."

    payload = json.dumps({
        "model": "Meta-Llama-3-8B-Instruct",
        "messages": [{"role": "user", "content": final_prompt}],
        "repetition_penalty": 1.1,
        "temperature": 0.7,
        "top_p": 0.9,
        "top_k": 40,
        "max_tokens": 1024,
        "stream": True
    })

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {AWANLLM_API_KEY}"
    }

    try:
        response = requests.request("POST", url, headers=headers, data=payload, stream=True)

        if response.status_code != 200:
            return f"Lỗi API: {response.status_code} - {response.text}"

        full_message = ""
        for line in response.iter_lines():
            if line.strip():
                try:
                    data = json.loads(line.decode('utf-8').replace("data: ", ""))
                    if 'choices' in data:
                        full_message += data['choices'][0]['delta'].get('content', '')
                except json.JSONDecodeError:
                    continue

        return full_message.strip()

    except requests.exceptions.RequestException as e:
        return f"Lỗi khi kết nối tới API: {str(e)}"
