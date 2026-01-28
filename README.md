# April Cogs

A collection of cogs for [Red-DiscordBot](https://github.com/Cog-Creators/Red-DiscordBot).

## Installation

These are cogs for Red-DiscordBot V3. You need to have a working Red instance to use these cogs.

### Adding the Repository

First, add this repository to your Red instance:

```
[p]repo add april-cogs https://github.com/drraccoony/april-cogs
```

### Installing Cogs

After adding the repository, install the desired cog(s):

```
[p]cog install april-cogs ahelp_replies
```

Then load the cog:

```
[p]load ahelp_replies
```

**Note:** Replace `[p]` with your bot's prefix.

### Dependencies

Install the required Python dependencies:

```bash
pip install -r requirements.txt
```

Or install them in your Red environment:

```bash
python -m pip install python-dotenv
```

## Configuration

### SSL Configuration

This project uses environment variables to configure SSL certificate verification.

#### Setup

1. **Find your Red data directory:**
   ```
   [p]datapath
   ```
   This will show you where Red stores its data.

2. **Navigate to the cog's data directory:**
   - The `.env` file should be placed in: `<datapath>/cogs/ahelp_replies/.env`
   - Alternatively, you can place it in Red's base directory (where you run Red from)

3. **Create the `.env` file:**
   
   Create a file named `.env` in one of the locations above with the following content:
   
   ```env
   # SSL Configuration
   VERIFY_SSL=true
   
   # API Timeout (in seconds)
   ACTION_TIMEOUT=5
   
   # Authentication API URL
   AUTH_API_URL=https://auth.spacestation14.com
   ```

4. **Configure the optional environment variables:**

   - **`VERIFY_SSL`** (default: `true`)
     - Set to `true` to enable SSL certificate verification (recommended for production)
     - Set to `false` to disable SSL certificate verification (use only in development/testing with self-signed certificates)
   
   - **`ACTION_TIMEOUT`** (default: `5`)
     - Timeout in seconds for API requests to game servers and auth server
     - Increase if you have slow network connections or servers that take longer to respond
     - Example: `ACTION_TIMEOUT=10`
   
   - **`AUTH_API_URL`** (default: `https://auth.spacestation14.com`)
     - URL for the Space Station 14 authentication API
     - Change this if you're using a custom auth server or testing environment
     - Example: `AUTH_API_URL=https://your-custom-auth.example.com`

5. **Reload the cog:**
   ```
   [p]reload ahelp_replies
   ```

#### Where to place the `.env` file

The cog will look for the `.env` file in these locations (in order):

1. **Cog data directory** (recommended): `<datapath>/cogs/ahelp_replies/.env`
2. **Red's base directory** (fallback): Where you run Red from

**Example on Windows:**
```
C:\Users\YourName\AppData\Local\Red-DiscordBot\data\<instance_name>\cogs\ahelp_replies\.env
```

**Example on Linux:**
```
~/.local/share/Red-DiscordBot/data/<instance_name>/cogs/ahelp_replies/.env
```

**⚠️ Security Warning:** Disabling SSL verification (`VERIFY_SSL=false`) should only be used in development or testing environments with self-signed certificates.

## Cogs

### ahelp_replies

AHelp replies cog for discord-game communication with Space Station 14 servers.

**Commands:**
- `[p]ahrcfg add` - Add a server configuration
- `[p]ahrcfg remove <identifier>` - Remove a server configuration
- `[p]ahrcfg use_channel <identifier>` - Set the current channel to watch for AHelp relays
- `[p]ahrcfg list` - List all configured servers

**Note:** All commands require admin permissions.
