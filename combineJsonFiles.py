import json, os

for filename in os.listdir('inbox'):
    dir = os.path.join('inbox', filename)
    print(filename)

    moreFiles = True
    counter = 1
    tempParticipants = []
    participants = []
    messages = []

    while moreFiles:
        file = dir + '\message_' + str(counter) + '.json'

        try:
            with open(file, "r") as fp:
                data = json.load(fp)
                tempParticipants.extend(data['participants'])
                messages.extend(data['messages'])
                counter = counter + 1

        except FileNotFoundError:
            moreFiles = False

        for participant in tempParticipants:
            if participant not in participants:
                participants.append(participant)

    with open(dir + '/messages.json', 'w') as fp:
        json.dump(messages, fp)

    with open(dir + '/participants.json', 'w') as fp:
        json.dump(participants, fp)

