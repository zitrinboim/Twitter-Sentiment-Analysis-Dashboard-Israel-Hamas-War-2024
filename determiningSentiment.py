from openai import OpenAI
import json


def sentiment(text):
    api_key = "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"
    client = OpenAI(api_key=api_key)
    post_text = text
    user_text = post_text + """ So, in short, is it positive towards Israel  or not?
  And is it positive towards Hamas or not?
  Answer in this structure
  'Positive to Israel': yes or no or neutral
  'Positive to Hamas': yes or no or neutral"""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
            {"role": "user", "content": user_text}
        ]
    )
    message_text1 = response.choices[0]
    message_text2 = message_text1.message.content
    json_data = json.loads(message_text2, strict=False)
    try:
        if json_data['Positive to Israel'].lower() == 'no' or json_data['Positive to Hamas'].lower() == 'yes':
            return 'Negative'
        elif json_data['Positive to Israel'].lower() == 'yes' or json_data['Positive to Hamas'].lower() == 'no':
            return 'Positive'
        else:
            return 'Neutral'
    except KeyError:
        if 'Positive' in json_data:
            return 'Positive'
        elif 'Negative' in json_data:
            return 'Negative'
        else:
            return 'Neutral'
