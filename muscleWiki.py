'''
Scrape data from Muscle Wiki
'''

import requests
from bs4 import BeautifulSoup
import json

def muscleList(string):
    words = string.split(' ')
    new_list = []
    i = 0
    while i < len(words):
        if words[i] == 'Lower' and i+1 < len(words) and words[i+1] == 'back':
            new_list.append('Lower back')
            i += 2
        elif words[i] == 'Traps' and i+1 < len(words) and words[i+1] == '(mid-back)':
            new_list.append('Mid back')
            i += 2
        elif words[i] == '(mid-back)':
            new_list.append('Mid back')
            i += 1
        else:
            new_list.append(words[i])
            i += 1
    return new_list


def html_table_to_json(table,exerciseRowJson):
    rowsHTML = table.find_all('tr')
    for rowHTML in rowsHTML:
        td = rowHTML.find_all('td')
        if td:
            exerciseRowJson[td[0].text] = td[1].text


def getSteps(stepList):
    steps = []
    stepList = stepList.find_all('li')
    steps = [step.text for step in stepList]
    return steps

def getVideos(video):
    video_urls = []
    for video_tag in video.find_all('video', {'class': 'workout-img'}):
        src = video_tag['src']
        video_urls.append(src)
    return video_urls

def get_exercise_data(exercise_url,exerciseRowJson):
    response = requests.get(exercise_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    videosHTML = soup.find(class_='exercise-images-grid')
    exerciseRowJson['videoURL'] = getVideos(videosHTML)

    stepsHTML = soup.find(class_='steps-list')
    exerciseRowJson['steps'] = getSteps(stepsHTML)

    table1HTML = soup.find('table', {'class': 'table wikitable wikimb'})
    html_table_to_json(table1HTML,exerciseRowJson)

    table2HTML = soup.find('table', {'class': 'table wikitable wikimb','title':'Muscles  Targeted'})
  
    exerciseRowJson['target'] = {}
    html_table_to_json(table2HTML,exerciseRowJson['target'])

    if 'Primary' in exerciseRowJson['target']:
      exerciseRowJson['target']['Primary'] = muscleList(exerciseRowJson['target']['Primary'] )

    if 'Secondary' in exerciseRowJson['target']:
      exerciseRowJson['target']['Secondary'] = muscleList(exerciseRowJson['target']['Secondary'] )

    if 'Tertiary' in exerciseRowJson['target']:
      exerciseRowJson['target']['Tertiary'] = muscleList(exerciseRowJson['target']['Tertiary'] )

    

    youtubeHTML = soup.find(class_='long-form-video')
    if youtubeHTML:
        youtubeHTML = youtubeHTML.find('iframe',{'title': 'YouTube video player'})
        exerciseRowJson['youtubeURL'] = youtubeHTML['src']
    else:
        exerciseRowJson['youtubeURL'] = ''
    
    detailsHTML = soup.find('div', {'class': 'summernote-content'})
    if detailsHTML:
        detailsText = detailsHTML.text
        detailsText.replace('\n', '\n\n')
        detailsText.replace('*', '\\*')
        detailsText.replace('-', '\\-')
        detailsText.replace('\n', '\n\n')
        exerciseRowJson['details'] = detailsText


# Function to get the workout data from muscle wiki
def get_musclewiki_data():
    url = "https://musclewiki.com/directory"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    exercises = soup.find_all('table', class_='wikitable')

    musclewiki_data = []
    count = 0
    for exercise in exercises:
        rows = exercise.find_all('tr')[1:]
        for row in rows:
            columns = row.find_all('td')
            exercise_name = columns[0].find('a').text.strip()
            video_links = columns[1].find_all('a')

            print(f'{count}) Fetching {exercise_name}')
            exerciseRowJson =  {
                'exercise_name': exercise_name,
            }

            get_exercise_data('https://musclewiki.com'+video_links[0]['href'],exerciseRowJson)

            musclewiki_data.append(exerciseRowJson)
            count+=1

    workouts = musclewiki_data
    categories = {}
    difficulties = {}
    forces = {}
    muscles = {}

    for workout in workouts:
      categories[workout['Category']] = 1

      if 'Difficulty' in workout:
        difficulties[workout['Difficulty']] = 1

      if 'Force' in workout:
        forces[workout['Force']] = 1

      workout_muscles =[]
      if 'Primary' in workout['target']:
        workout_muscles.extend(workout['target']['Primary'])
      if 'Secondary' in workout['target']: 
        workout_muscles.extend(workout['target']['Secondary'])
      if 'Tertiary' in workout['target']:
        workout_muscles.extend(workout['target']['Tertiary'])
      for wm in workout_muscles:
        muscles[wm] = 1
  
    workout_attributes = {
      'categories': list(categories.keys()),
      'difficulties': list(difficulties.keys()),
      'forces': list(forces.keys()),
      'muscles': list(muscles.keys())
    }
    
    with open('workout_attributes.json', 'w') as f:
            json.dump(workout_attributes, f,indent=4)
  
    with open('musclewiki_data.json', 'w') as f:
        json.dump(musclewiki_data, f,indent=4)

get_musclewiki_data()