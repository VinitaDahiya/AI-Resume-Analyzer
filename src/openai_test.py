'''
Because openai_test.py is inside src while config.py is in the project root, 
Python may not automatically find config.py when we execute: python src/openai_test.py

So before running it, let's make the import robust.
'''




import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))


from openai import OpenAI

from config import OPENAI_API_KEY


client = OpenAI(api_key=OPENAI_API_KEY)


response = client.responses.create(
    model="gpt-5.6-luna",
    input="Explain in one sentence what a resume analyzer does."
)


print(response.output_text)


