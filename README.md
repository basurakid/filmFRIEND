# filmFRIEND
    #### Video Demo: [https://youtu.be/kC_MvwgCsr8]
    #### Description: A film recomendation web app based on collaborative filtering

## Project Overview
### Description
FilmFriend is a Flask-based web application designed to recommend movies tailored to your preferences. 
It employs item-item collaborative filtering, leveraging the latest small dataset from MovieLens to find films similar to
those you’ve enjoyed. For detailed movie information, FilmFriend integrates with the TMDB API, enriching the user experience 
when exploring specific titles. The web app dynamically generates HTML templates, ensuring that content is loaded efficiently,
only when needed by the user.

## Features
### Collaborative Filtering
- Description: Collaborative filtering recommends movies based on user preferences and similarities. 
- How It Works: The system compares a user's movie preferences with those of other users to identify movies that are likely to be enjoyed.

### TMDB API Integration

- Description: The TMDB API provides detailed movie information.
- Data Retrieval: The API is queried to fetch movie titles, posters, ratings, and other details.
    Integration: Retrieved data is processed and displayed within the application, enhancing the user experience.

### Dynamic HTML Generation

- Description: Flask and Jinja2 are used to create dynamic HTML content.
- Template Rendering: Data is passed from the backend to Jinja2 templates, which generate HTML to be displayed in the user’s browser.

### Search System

- Description: FuzzyWuzzy improves search accuracy by handling typos and incorrect entries.
- String Matching: Uses the Levenshtein Distance algorithm to match user input with movie titles, even when there are spelling errors.

### User Interaction Flow

- How Users Interact: Users search for movies, view recommendations, and explore details through an intuitive interface.
- Data Flow: User input triggers searches, which are processed and displayed using the methods described above.


## Installation
### Prerequisites
The libraries used on this program, as stated on the `requirements.txt`:
- __Scikit-learn:__ (v1.5.1): Recommended to install using Conda. [Scikit Webpage](https://scikit-learn.org/stable/install.html)
- __Pandas:__ (v2.2.2)
- __Numpy:__ (v1.26.4)
- __Fuzzywuzzy:__ (v0.18.0)
- __Scipy:__ (v1.14.1)
- __Urllib3:__ (v2.2.2)

### Setup Steps
1. Install conda. [Installation Guide](https://docs.anaconda.com/miniconda/miniconda-install/)
2. Install Scikit-learn
```conda create -n sklearn-env -c conda-forge scikit-learn```
3. Activate Scikit's environment
```conda activate sklearn-env```
4. Install the libraries required in the environment
5. The TMDB API key is pre-configured for use in this project, so no additional setup is required for the API integration at this stage.

## Usage
1. Access the web app by starting Flask in your Scikit-learn environment. Open your terminal and run:
```run flask```

2. Click on the ip that will appear on the terminal.
3. Use the searchbar in the homepage to search for a film you liked.
4. Click on any recommended film card in the results to view more detailed information about that movie.

## Files Overview
- __app.py:__ Here are the basic routes of the web, as well as some supporting routes like search and a single helper function related to search.
- __helpers.py:__ All of the functions in this file, are used in app.py. Some of them in here are used to create the CF grid and recommend movies, to retrieve data from the dataframes or make requests to TMDB.
- __script.js:__ the code in the scripts is only used to create and populate the suggested terms when making a search.
## Project structure
### __Collaborative Filtering__
This technique is used to recommend movies based on the user’s search. It predicts which films the user will enjoy by assuming
that they liked the movie they are searching for. The system compares the user's preferences with other users in the dataset,
identifying movies that similar users have enjoyed.

> "Collaborative filtering uses a matrix to map user behavior for each item in its system. The system then draws values from this matrix to plot as data points in a vector space. Various metrics then measure the distance between points as a means of calculating user-user and item-item similarity."
> --- [IBM](https://www.ibm.com/topics/collaborative-filtering)

In this particular application, we use item-item collaborative filtering, which means the similarity between the searched 
film and those recommended is based on the similarity of user ratings. This approach is simpler than user-user collaborative
filtering, has fewer errors, and is less prone to issues like cold-start.

### __TMDB API__
TMDB API offers a simple and efficient way to retrieve detailed movie data, such as titles, posters,
cast, and genres. We use it to enhance the user experience by providing relevant and up-to-date information.

- __Movie ID Mapping:__  We first use a dictionary to map MovieLens IDs to TMDB IDs, using MovieLens links.csv. These TMDB IDs are then used to
 request detailed movie information from the API. If the mapping fails, we perform a search by title and use the first result.
- __Data Extraction and Display:__ The HTML response is converted into a dictionary. We retrieve the necessary data, including movie details and
cast information, and pass this data to our HTML templates for display.

### __Dynamic HTML__ 
One of Flask's key strengths is its ability to dynamically generate HTML using Jinja templates. This allows us to pass 
all relevant data from the backend to the HTML, where we can iterate over it and display it.
- __Dynamic Content Generation:__ Flask enables the creation of HTML based on user interaction. Along with Jinja2, this means that we
don't need to generate static HTML pages or create a page per movie.
- __Template Inheritance:__ Jinja2 supports template inheritance, allowing us to create the basic layout needed, the header
and the footer. This avoids redundancy in our HTML and makes for a consistent result.
- __Control Structures:__ The powerful control structures provided by Jinja2, such as loops and conditionals, allow us to
display content iteratively. This is for example used in the results page, to generate the grid of rows and columns for the recommended
movies.

### __Responsive Website__
Using Bootstrap’s built-in classes and functionality has been key to building a responsive and visually appealing website. Allowing for easier, faster work and providing several advantages:
- __Responsive Grid System:__ Bootstrap's grid system allows for great responsiveness, ensuring that the layout adapts and scales to fit any desktop screen size. Making a separate layout would be necessary for it to look good on mobile devices.
- __Utility Classes for Easy Styling:__ the wide range of utility classes that simplify styling tasks.
- __Pre-built Components:__ Bootstrap provides a variety of pre-built components (e.g., navigation bars, buttons, modals) that are ready to use and customizable.

### __Search System__ 
A valuable addition to the project is the use of FuzzyWuzzy as a solution for the cases when the user enters a title
incorrectly or has a typo. This library simplifies string matching by leveraging the Levenshtein Distance algorithm to calculate the
differences between sequences, allowing the system to suggest relevant movies even when the input isn’t perfectly accurate.

## Development and Creation
### Motivation
From the get-go I knew one thing for sure, I would be making a flask based web app. The theme of it
wasn't quite firm at the beginning. It took a few weeks of thinking until I came to the conclusion to make
a film recommendation system. 

Films and media in general is one of my passions, so it very much made sense to make something that I myself would like to use.
It has already worked as I have found some interesting films I had never even before heard of.
### Learning Outcomes
We might not be aware of it all of the time, but everywhere we are on the internet, it's very likely
that some sort of machine learning or algorithm is at work to recommend content that is appealing to us. Be it Amazon, Netflix,
Youtube or whatever else.

With that in mind, trying to learn machine learning, in this case, collaborative filtering was something I thought would
be very valuable for me.
## Acknowledgements
- __CS50's own ducky:__ Thank you for your help dear rubber friend.
- __Toronto Machine Learning Series with Jill Cates:__ My CF system is based on [this tutorial](https://www.youtube.com/watch?v=XfAe-HLysOM&t=3071s), it has been the most helpful 
piece of data I have found throughout the whole project's development. 
- __Bootstrap:__ their [webpage](https://getbootstrap.com/docs/5.3/getting-started/introduction/) contains a lot of useful info, and their classes are very valuable for anyone starting in HTML.