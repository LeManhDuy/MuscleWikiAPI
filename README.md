# Unofficial MuscleWiki API
This is an API to retreive data from [musclewiki](https://musclewiki.com/). It was created by scraping data from [musclewiki](https://musclewiki.com/).

The API provides information about exercises, including the name, category, target muscles,instructions for performing the exercise and a short video demonstration.

## Endpoints
The API provides the following endpoints:

### Get workout attributes
This endpoint returns the workout attributes you can filter exercises by.
```
GET /attributes
```

### Get all exercises

This endpoint returns a list of all exercises.

```
GET /exercises
GET /exercises?target=<target>&name=<name>&category=<category>
```

### Get exercise by ID
This endpoint returns a single exercise with the given ID.
```
GET /exercises/int:exercise_id
```

## Deployment
This API has been deployed to Vercel at `https://workoutapi.vercel.app/`. To deploy the API to your own Vercel account, follow these steps:

1. Clone the repository to your local machine.
2. Create a new Vercel project and link it to the repository.
3. Configure the required environment variables (if any).
4. Deploy the project to Vercel.

## API Documentation
Full API documentation, including detailed descriptions of the endpoints and response formats, can be found on [RapidAPI](https://rapidapi.com/rahulbanerjee26/api/musclewiki).

