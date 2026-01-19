# Vimmit

### The Retro Game Randomiser

Vimmit is a command-line tool for discovering retro games

## How to Vimmit ✌️🤮

### Install: WIP
...

**NOTE:** Depending how you installed Python, you may need a different keyword to run vimmit. e.g. `py`, `python`, `python3`

These examples use `py`, which will work if you installed Python using the Python install manager.

### First-Time Setup
Navigate to your vimmit/ folder in a terminal window, and run `py vimmit` to begin first-time setup.

After following the prompts, view a list of available systems with: `py vimmit --show-systems` or `py vimmit -s`

Download gamelists by running `py vimmit system1 system2 ... systemX --download` (or `-d`) with your selected systems.

### After Setup

Run `py vimmit system1 system2 ... systemX` to roll a random game!

You can also run `py vimmit *` to roll all downloaded systems.

Games that you have already seen won't be rerolled.

Run `py vimmit --help` (or `-h`) to view all available commands.

## Blacklist

You can blacklist keywords or phrases to prevent certain games from being rolled. After setup, vimmit will create a blacklist.txt file like this:

```
# All Systems

# Wintendo 64 (W64)

# Blaystation 1 (BS1)

```

Enter one phrase per line under the systems of your choice. In the example below:
- All games containing "basketball" are banned
- Games containing "football" or "baseball" are banned from the Wintendo 64
- Games containing "golf" or "soccer" are banned from the Blaystation 1

```
# All Systems
basketball

# Wintendo 64 (W64)
football
baseball

# Blaystation 1 (BS1)
golf
soccer

```
