# am i pwned?

Send password hashes to a simple web API which will return `200` for pwned and `404` for not pwned.

`amipwned` has two features, the web service and the `load` service. The `load` services takes a password dump as input and saves each password and its corresponding hash to a Postgresql database (other DBs may be supported if requested).

It's up to the user to load any password leak they want.

```                                                                                                     
                                                                                                         
 ▄▄▄       ██▀███  ▓█████    ▓██   ██▓ ▒█████   █    ██     ██▓███   █     █░███▄    █ ▓█████ ▓█████▄    
▒████▄    ▓██ ▒ ██▒▓█   ▀     ▒██  ██▒▒██▒  ██▒ ██  ▓██▒   ▓██░  ██▒▓█░ █ ░█░██ ▀█   █ ▓█   ▀ ▒██▀ ██▌   
▒██  ▀█▄  ▓██ ░▄█ ▒▒███        ▒██ ██░▒██░  ██▒▓██  ▒██░   ▓██░ ██▓▒▒█░ █ ░█▓██  ▀█ ██▒▒███   ░██   █▌   
░██▄▄▄▄██ ▒██▀▀█▄  ▒▓█  ▄      ░ ▐██▓░▒██   ██░▓▓█  ░██░   ▒██▄█▓▒ ▒░█░ █ ░█▓██▒  ▐▌██▒▒▓█  ▄ ░▓█▄   ▌   
 ▓█   ▓██▒░██▓ ▒██▒░▒████▒     ░ ██▒▓░░ ████▓▒░▒▒█████▓    ▒██▒ ░  ░░░██▒██▓▒██░   ▓██░░▒████▒░▒████▓    
 ▒▒   ▓▒█░░ ▒▓ ░▒▓░░░ ▒░ ░      ██▒▒▒ ░ ▒░▒░▒░ ░▒▓▒ ▒ ▒    ▒▓▒░ ░  ░░ ▓░▒ ▒ ░ ▒░   ▒ ▒ ░░ ▒░ ░ ▒▒▓  ▒    
  ▒   ▒▒ ░  ░▒ ░ ▒░ ░ ░  ░    ▓██ ░▒░   ░ ▒ ▒░ ░░▒░ ░ ░    ░▒ ░       ▒ ░ ░ ░ ░░   ░ ▒░ ░ ░  ░ ░ ▒  ▒    
  ░   ▒     ░░   ░    ░       ▒ ▒ ░░  ░ ░ ░ ▒   ░░░ ░ ░    ░░         ░   ░    ░   ░ ░    ░    ░ ░  ░    
      ░  ░   ░        ░  ░    ░ ░         ░ ░     ░                     ░            ░    ░  ░   ░       
                              ░ ░                                                              ░         
                                                                                                         
usage: amipwned [-h] [--web {start,stop,restart}] [--load FILENAME]                                      
                [--port PORT] [--config CONFIG]                                                          
                                                                                                         
Self-hosted service for checking if a given password has been recorded in                                
public password dumps. Created by @dubs3c                                                                
                                                                                                         
optional arguments:                                                                                      
  -h, --help            show this help message and exit                                                  
  --web {start,stop,restart}                                                                             
                        Control the amipwned web service                                                 
  --load FILENAME       Stop the amipwned web service                                                    
  --port PORT           Listening port for the web service                                               
  --config CONFIG       Configuration file location                                                      
```

## Motivation

A reason to try out `aiohttp` and writing some `asyncio` code! However, if you like the idea of this project, create an issue with your suggested improvements (or send a PR) and I'll maybe implement/merge them :)

## How to run

### For production

1. Install the project
`pip install amipwned`

2. Create the following configuration file at `~/.amipwned.ini`
```
[postgresql]
host = localhost
port = 5432
username = postgres
password =
databaseName = amipwned
```

3. Run it!
`amipwned --web start`

### For development
Recommended way of installing is using `poetry`.
1. Simply run `poetry install` after cloning the repo.

2. Create the following configuration file at `~/.amipwned.ini`
```
[postgresql]
host = localhost
port = 5432
username = postgres
password =
databaseName = amipwned
```

3. `poetry run amipwned --web start`


## Contributing
Any feedback or ideas are welcome! Want to improve something? Create a pull request!

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D