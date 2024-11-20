# Tarnung
Simple python script to camouflage your (probably malicious) domain as another domain. 

## Inspiration
This repo: [Humble Chameleon](https://github.com/claissg/humble_chameleon)  
By this hacker: [fkasler](https://github.com/fkasler)

## Installing
**Cloning then installing**
```
git clone https://github.com/Plensu/tarnung.git
cd tarnung
python3 -m venv .
source bin/activate
pip install .
```

**Pip installing from git**
```
pip install git+ssh://git@github.com:Plensu/tarnung.git
```
**Pip Install From Pypi**
```
not done yet
```

## Running Tarnung
You'll need a config file that looks similar to the one in the repo.

```yaml
Listener:
    listenIP: 0.0.0.0
    port: 8000
Domains:
  my.domain.tld : target.com
  example.com : plensu.me
  plensu.com : stackoverflow.com
```

Tarnung will look for `config.yml` in the directory you are currently in, or you can provide it a path as an argument. 
```
python3 -m tarnung /path/to/config.yml
```

## Docker
Coming soon...