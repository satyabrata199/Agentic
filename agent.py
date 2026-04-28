from utils import generate
from system_prompt import system_prompt
from parser import parse_llm_json
from tools import TOOLS , calculator,save_note,web_search,get_datetime

def baseagent(user_input):
    Systemprompt = system_prompt()
    observation = ""
    history = ""

    for steps in range(10):
        full_prompt = f"""

        {Systemprompt}

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
        output = generate(full_prompt)
        get_data = parse_llm_json(output)

        thought = get_data.get("thought")
        action = get_data.get("action")
        agent_inp = get_data.get("input")

        if action == "finish":
            print(f"final answer ---------------------------------")
            return agent_inp

        tool = TOOLS.get(action)

        if tool:
            observation = tool(agent_inp)
        else:
            observation = "unknown action"

        print(f"step {steps+1}")

        print(f"think : {thought}")
        print(f"action : {action}")
        print(f"process : {agent_inp}")
        print(f"observation : {observation}")

        history+= f"""
        step: {steps+1}
        thought: "{thought}"
        action: "{action}"
        input: "{agent_inp}"
        observation: "{observation}"
        """
    return observation

while True:
    user_input = input("you: ")
    response = baseagent(user_input)
    print(f"Agent:: {response}")








