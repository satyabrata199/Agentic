from agent import baseagent


def ask_agent(user_input):

    output = baseagent(user_input)


    return output

while True:
    user_input = input("you: ")
    response = ask_agent(user_input)
    print(f"Agent:: {response}")