import os
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

client = OpenAI(
  api_key = os.getenv('OPENAI_API_KEY')
)

def text_generation(dialogue_path, partner_name, question):
    with open(dialogue_path, 'r', encoding='utf-8') as f:
        full_text = f.read()

    # Prompt
    prompt = f"""
    너는 '{partner_name}'이라는 인물의 말투와 성격을 완벽하게 흉내 내는 인공지능이다.

    아래는 '{partner_name}'이 실제로 작성한 말만을 모아놓은 대화 내용이다.  
    이 사람은 고유한 문장 스타일, 말투, 맞춤법 습관, 띄어쓰기 특성뿐만 아니라  
    감정 표현 방식, 말투에서 드러나는 성격적 특징(예: 친근함, 장난기, 조심스러움 등)도 가지고 있다.

    너는 이 말투와 성격을 100% 모방하여 질문에 답해야 한다.  
    무조건 지켜야 할 지침은 다음과 같다:

    1. 문장을 교정하지 마라. 맞춤법, 띄어쓰기 오류가 있어도 그대로 따라라.
    2. 말끝 흐리기("~", "..."), 웃음("ㅋㅋ", "ㅎㅎ"), 이모지, 반말/존댓말 사용 등도 그대로 재현하라.
    3. 문장이 '.'으로 끝날 경우, 그 뒤에 '~'를 붙이지 않는다.
    4. 절대 문장 전체를 쌍따옴표로 감싸지 마라. (예: "안녕" → X, 안녕 → O)
    5. 말투뿐 아니라 **이 사람이 어떤 성격을 가진 사람인지**도 고려하여 감정과 태도를 반영해라.
    (예: 평소에 장난스럽거나 조심스럽다면, 그에 맞게 문장의 분위기나 말투를 조정하라)
    6. 답변은 50자 내외로 짧고 간결하게 작성하라. 문장은 하나 또는 두 문장 정도로 구성할 것.

    아래는 '{partner_name}'이 실제로 작성한 문장들이다:

    {full_text}

    이제 너는 질문에 대해 '{partner_name}'처럼 말투와 성격을 모두 반영하여 자연스럽게 대답하라.  
    형식이나 정답보다 **그 사람처럼 말하는 것**이 훨씬 중요하다.

    질문: {question}

    답변:
    """

    # GPT API call
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"너는 '{partner_name}'의 말투를 완벽히 흉내 내는 AI야."},
            {"role": "user", "content": prompt}
        ]
    )

    answer = response.choices[0].message.content.strip()
    total_tokens = response.usage.total_tokens

    # Save log
    save_log('logs', partner_name, question, answer, total_tokens)

    print('Answer:', answer)

def save_log(base_dir, partner_name, question, answer, tokens):
    # create log directory
    os.makedirs(base_dir, exist_ok=True)

    filename = f"{partner_name}_log.txt"
    log_path = os.path.join(base_dir, filename)

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(log_path, 'a', encoding='utf-8') as f:
        f.write(f"[{now}]\n")
        f.write(f"Question: {question}\n")
        f.write(f"Answer: {answer}\n")
        f.write(f"Tokens used: {tokens} (prompt + completion)\n")
        f.write("="*50 + "\n")