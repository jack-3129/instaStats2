import json, os, csv

for filename in os.listdir('inbox'):
    dir = os.path.join('inbox', filename)

    if os.path.isdir(dir):
      print('\n' + dir + '\n')

      # Load participants in from file
      participants = []
      with open(dir + '/participants.json', "r") as fp:
        for participant in json.load(fp):
          participants.append(participant['name'])

      # All variables to track for all participants
      data = {
        'messages' : {},
        'characters' : {},
        'videos' : {},
        'photos' : {},
        'share' : {},
        'reactionsGiven' : {},
        'reactionsReceived' : {},
        'call_duration' : {},
        'audio_files' : {}
      }

      # Initialise all values to 0 for all participants
      for statistic in data:
        for participant in participants:
          data[statistic][participant] = 0

      # ------------------------------

      def contentMessage(content, sender):
        phraseList = ['liked a message', 'reacted', 'started a video chat', 'started an audio call', 'Video chat ended', 'Audio call ended', 'named the group', 'changed the group photo', 'sent an attachment', 'shared a story']
        if any(phrase in content for phrase in phraseList):
          pass
        
        else:
          data['messages'][sender] += 1
          data['characters'][sender] += len(content)

      # ------------------------------

      def checkReactions(message, sender):
        try:
          for reaction in message['reactions']:
            data['reactionsReceived'][sender] += 1
            data['reactionsGiven'][reaction['actor']] += 1

        except KeyError:
          pass

      # ------------------------------

      def checkOther(message, sender):
        attributes = ['videos', 'photos', 'share', 'call_duration', 'audio_files']

        for attribute in attributes:
          try:
            _ = message[attribute]
            data[attribute][sender] += 1

          except KeyError:
            pass

      # ------------------------------

      # Load messages in from file
      with open(dir + '/messages.json', "r") as fp:
        messages = json.load(fp)

      for message in messages:
        try:
          content = message['content']
          sender = message['sender_name']

          if sender not in participants:
            raise ValueError

          contentMessage(content, sender)
        
        #If message doesn't have a content attribute
        except KeyError:
          pass

        #If the sender is not in the participants list
        except ValueError:
          pass

        checkReactions(message, sender)
        checkOther(message, sender)

      # Write to CSV
      with open('csvStatistics/' + filename + '.csv', 'w', newline='', encoding='utf-8') as fp:
        writer = csv.writer(fp)
        #manually add header row
        csvRow = ['participantName']
        for attribute in data:
          csvRow.append(attribute)
        writer.writerow(csvRow)

        for participant in participants:
          csvRow = [participant]
          for attribute in data:
            csvRow.append(data[attribute][participant])
          writer.writerow(csvRow)

    print('Finished ' + filename + '!')
    






  
