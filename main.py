from agent import baseagent


def ask_agent(user_input):
    try:
        output = baseagent(user_input)
    except:
        print("loop is broken!")

    return output

while True:
    user_input = input("you: ")
    response = ask_agent(user_input)
    print(f"Agent:: {response}")