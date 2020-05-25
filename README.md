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

## Config



## Setup

It's recommended to create a user with access restricted to the API endpoints required to retrieve update information needed by the script. The steps to do this are as follows:

1. Add a new group under `System`>`Access`>`Groups`. All that is required here is `Group name`.

2. After creating the group, click on `Edit` for the newly created group. Under `Assigned Privileges` click `Edit`.

3. Scroll down to or search for `System: Firmware`. Tick to add the priviledges to the group (click the `i` to view the endpoints).

4. Add a new user under `System`>`Access`>`Users`. 

    1. Provide a `Username`. 

    2. Under `Password` tick `Generate a scrambled password to prevent local database logins for this user.`. 

    3. Then under `Group Memberships` click the previously created group and click `Add groups` (`->`).

5. After creating the new user, click on `Edit`. Under `API keys` click `Create API key` (`+`).
