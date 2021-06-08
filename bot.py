import discord 
import os
import requests as req
import json
from keep_alive import keep_alive
client = discord.Client()

def get_quote():
  response = req.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + '\n-' + json_data[0]['a']
  return quote

def get_poem():
  response = req.get("https://www.poemist.com/api/v1/randompoems")
  json_data = json.loads(response.text)
  poem = json_data[1]["title"] + "\n\n" + json_data[1]["content"] + "\n" + "\n    -" + json_data[1]["poet"]["name"]
  return poem

def search_books(book):
  parsed_book = ''
  for s in book:
    if s == " ":
      parsed_book += "+"
    else:
      parsed_book += s
  response = req.get(f"https://www.googleapis.com/books/v1/volumes?q={parsed_book}")
  json_data = json.loads(response.text)
  #data
  title = json_data['items'][0]['volumeInfo']['title']
  
  authors = ', '.join(json_data['items'][0]['volumeInfo']['authors'])
  
  publisher = json_data['items'][0]['volumeInfo']['publisher'] + " in " + json_data['items'][0]['volumeInfo']['publishedDate']
  
  description = json_data['items'][0]['volumeInfo']['description']
  
  isbn = "ISBN 10: " + json_data['items'][0]['volumeInfo']['industryIdentifiers'][0]['identifier'] + ", ISBN 13: " + json_data['items'][0]['volumeInfo']['industryIdentifiers'][1]['identifier']
  
  categories = ", ".join(json_data['items'][0]['volumeInfo']['categories'])
  
  try:
    rating = json_data['items'][0]['volumeInfo']['averageRating']
  except:
    rating = "Not Available"
  
  book_data = "Title: " + title + '\nAuthors: ' + authors + "\nPublisher: " + publisher + "\n" + isbn + "\nCategories: " + str(categories) + "\nRating: " + str(rating) + "\nDescription: " + description
  
  return book_data


@client.event
async def on_ready():
  print("Logged in as {0.user}".format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return 
  if message.content.startswith('-quote'):
    quote = get_quote()
    await message.channel.send(quote)
  if message.content.startswith("-poem"):
    poem = get_poem()
    await message.channel.send(poem)  
  if message.content.startswith("-book "):
    book = message.content[5:]
    book_data = search_books(book)
    await message.channel.send(book_data[:1999])

keep_alive()
client.run(os.getenv('TOKEN')) 
