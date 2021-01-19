```
                                     _    __     __          __
                                    | |  / /____/ /_  ____  / /_
                                    | | / / ___/ __ \/ __ \/ __/
                                    | |/ (__  ) / / / /_/ / /_
                                    |___/____/_/ /_/\____/\__/

```

# :camera: Vshot

## Running in Docker

* Make an alis to this `docker run` command:
```
alias vshot="docker run -it --rm -v ~/.vshot:/root/.vshot lowess/vshot $@"
```

* Use it !
```
vshot --url https://google.com/ --above-the-fold --no-js
```

* Check results
```
open ~/.vshot/shots/https%3A%2F%2Fgoogle.com%2F/js-off-abovethefold.png
```

## Getting started

* Install chrome-driver

```
brew cask install chromedriver

# Remove from Apple quarantine (optional)
xattr -d com.apple.quarantine /usr/local/Caskroom/chromedriver/87.0.4280.88/chromedriver
```

* Install `requirements.txt`
