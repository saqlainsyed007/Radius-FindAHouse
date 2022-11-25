# Radius-FindAHouse

# Problem Statement

Agentdesks have a lot of properties from property sellers and search requirements from property buyers which get added to a SQL database every day. Every day these multiple properties and search criteria get added through our application by agents. Write an algorithm to match these properties and search criteria as they come in based on 4 parameters such that each match has a  match percentage.

The 4 parameters are:
- Distance - radius (high weightage)
- Budget (high weightage)
- Number of bedrooms (low weightage)
- Number of bathrooms (Low weightage)


Each match should have a percentage that indicates the quality of the match. Ex: if a property exactly matches a buyer's search requirement for all 4 constraints mentioned above, it’s a 100% match.


Each property has these 6 attributes - Id, Latitude, Longitude, Price, Number of bedrooms, Number of bathrooms


Each requirement has these 9 attributes - Id, Latitude, Longitude, Min Budget, Max budget, Min Bedrooms required, Max bedroom reqd, Min bathroom reqd, Max bathroom reqd.


## Functional requirements
- All matches above 40% can only be considered useful.
- The code should scale up to a million properties and requirements in the system.
- All corner cases should be considered and assumptions should be mentioned
- Requirements can be without a min or a max for the budget, bedroom, and a bathroom but either min or max would be surely present.
- For property and requirement to be considered a valid match, distance should be within 10 miles, the budget is +/- 25%, bedroom and bathroom should be +/- 2.
- If the distance is within 2 miles, distance contribution for the match percentage is fully 30%
- If the budget is within min and max budget, the budget contribution for the match percentage is full 30%. If min or max is not given, +/- 10% budget is a full 30% match.
- If the bedroom and bathroom fall between min and max, each will contribute a full 20%. If min or max is not given, the match percentage varies according to the value.
- The algorithm should be reasonably fast and should be quick in responding with matches for the users once they upload their property or requirement.


# Setup Instructions

## Pyenv Setup(MacOS 10.9+)

#### Step 1: Install Pre-Requisites

```
brew install openssl readline sqlite3 xz zlib

export LIBRARY_PATH=$LIBRARY_PATH:/usr/local/opt/openssl/lib/
```

#### Step 2: Install pyenv

```
curl https://pyenv.run | bash
```

Add the following code to your `~/.bash_profile` file
```
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
```
This will load pyenv when a terminal is started

#### Step 3: Install Python 3.7.9

```
pyenv install -v 3.7.9
```
Here `-v` represents the python version. In our case it is `3.7.9`.
You could install different versions using the `-v` option.

#### Step 4: Create Virtual Environment

```
pyenv virtualenv 3.7.9 radius-3.7.9
```
The above command creates a virtual environment with name `radius-3.7.9` using python version `3.7.9`. You can choose a name that is preferable to you.

#### Step 5: Activate Virtual Environment

```
pyenv activate radius-3.7.9
```
Once the virtual environment that you created is activated, you can install the requirements and run the server. Once the work is completed you could deactivate your virtual environment using `pyenv deactivate`# Setup Instructions


## DB Setup

Using sqlite3 for this project to keep things simple.
```
brew install sqlite3
```

## Django Project Setup

#### Pre-Requisites

- Forked and cloned this repository.
- Navigate into cloned location.
- An activated virtual environment with python version 3.7.9

#### Step 1: Install requirements.

```
pip install -r requirements.txt
```

#### Step 2: Migrate

```
python manage.py migrate
```

#### Step 3: SeedData

```
python manage.py seed_data
```
This will create 25000 records


#### Step 4: Create an admin user

```
python manage.py createsuperuser
```

#### Step 5: Runserver

```
python manage.py runserver 0:8000
```

## Testing the Application

#### Admin URL for viewing/creating Houses
```
http://localhost:8000/admin/house/house/
```

#### Postman Collection for Testing the Search API.
```
https://www.getpostman.com/collections/63ba85bae34506db3335
```
