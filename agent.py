from utils import generate
from system_prompt import system_prompt
from parser import parse_llm_json
from tools import TOOLS , calculator,save_note,web_search,get_datetime
from memory import add_memory , get_memory

def baseagent(user_input):
    Systemprompt = system_prompt()

    mem_context = get_memory()

    observation = ""
    history = ""

    prev_step = None
    prev_observation = None
    repeat_count = 0
    MAX_REPEATS = 2

    for steps in range(10):
        
        mem_context = get_memory()
        #full prompt----------
        full_prompt = f"""

        {Systemprompt}

        Conversation memory:
        {mem_context}

        USER TASK:
        {user_input}

        PREVIOUS STEPS:
        {history}

        LATEST OBSERVATION:
        {observation}

        INSTRUCTIONS:

        You are solving the task step-by-step.

        At each step:
        1. Look at the USER TASK
        2. Look at PREVIOUS STEPS
        3. Look at the LATEST OBSERVATION

        DECIDE the NEXT BEST ACTION.

        IMPORTANT RULES:

        - If you already have enough information to answer → use action = "finish"
        - If a tool result contains the answer → extract it and finish
        - If more computation is needed → continue step-by-step
        - NEVER repeat the same action with the same input
        - NEVER restart from the beginning

        WHEN TO FINISH:

        - The answer is clearly known
        - The observation already contains the answer
        - No more tools are needed

        OUTPUT:
        Return ONLY one valid JSON object.

        """
        # parsing to llm -----------------

        output = generate(full_prompt)
        get_data = parse_llm_json(output)

        thought = get_data.get("thought")
        action = get_data.get("action")
        agent_inp = get_data.get("input")

        # fall back loop logic ------------
        current_step = (action, agent_inp)
        if current_step == prev_step:
            repeat_count += 1
        else:
            repeat_count = 0

        if prev_observation == observation:
            repeat_count += 1

        if repeat_count >= MAX_REPEATS:
            print("Loop detected → forcing finish")

            final_answer = observation if observation else agent_inp
            add_memory(user_input, final_answer)
            return final_answer

        # tool calling logic -------------------
        if action == "finish":
            print(f"final answer with  observation {observation}")
            add_memory(user_input,agent_inp)
            return agent_inp

        tool = TOOLS.get(action)

        if tool:
            observation = tool(agent_inp)
        else:
            observation = "unknown action"

        # History and observation (work memory)
        history+= f"""
        step: {steps+1}
        thought: "{thought}"
        action: "{action}"
        input: "{agent_inp}"
        observation: "{observation}"
        """



    return observation









