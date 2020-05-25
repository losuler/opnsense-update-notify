<div align="center">
<p align="center">
  <p align="center">
    <h3 align="center">OPNsense Update Notify</h3>
    <p align="center">
      An update notification script for OPNsense.
    </p>
  </p>
</p>
</div>

## About

This is a script that makes an API connection to OPNsense and checks if there is any pending updates and if there are, it sends a message with details.

Based on the script by Bart J. Smit, 'ObecalpEffect' and Franco Fichtner, forked from https://github.com/bartsmit/opnsense-update-email.

## Setup

It's recommended to create a user with access restricted to the API endpoints required to retrieve update information needed by the script. The steps to do this are as follows:

1. Add a new group under `System`>`Access`>`Groups`. All that is required here is `Group name`.

2. After creating the group, click on `Edit` for the newly created group. Under `Assigned Privileges` click `Edit`.

3. Scroll down to or search for `System: Firmware`. Tick to add the priviledges to the group (click the `i` to view the endpoints).

4. Add a new user under `System`>`Access`>`Users`. 

    1. Provide a `Username`. 

    2. Under `Password` tick `Generate a scrambled password to prevent local database logins for this user.`. 

    3. Then under `Group Memberships` click the previously created group and click `Add groups` (`->`).

5. After creating the new user, click on `Edit`. Under `API keys` click `Create API key` (`+`). Your browser will prompt you to download or open a text file. This file will have the `api_key` and `api_secret` values used in the config (see the [config](#config) below.

## Config

The configuration file `config.yml` has three main sections (see `config.yml.example`). The already filled in values in the example config are the defaults.

---

```yaml
emitter: telegram
```

The `emitter` refers to one of the emitters in `emitters`. 

---

```yaml
emitters:
  - telegram:
    token:
    chatid:
```

`token` is the token for the Telegram bot, which is provided by creating a bot by following the steps provided in the [Telegram bot API documentation](https://core.telegram.org/bots#3-how-do-i-create-a-bot).

`chatid` is the unique identifier for the target chat. It can be obtained by messaging the bot and executing the following command (replace `$BOT_TOKEN`). The ID may be found at `"chat": {"id": 12345678},`:

```sh
curl https://api.telegram.org/bot$BOT_TOKEN/getUpdates | python -m json.tool
```

---

```yaml
opnsense:
  host:
  self_signed: yes
  api_key:
  api_secret:
```

`host` is either the ip address or hostname of the OPNsense web interface.

`self_signed` refers to whether the TLS certificate is self signed or not, it maybe be either `yes` or `no`. Since OPNsense creates it's own self signed cert by default, the default for this value is `yes`.

`api_key` and `api_secret` refers to the values provided in step 5 of the [setup](#setup) section above.
