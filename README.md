# PowerScheduler

Shutdown scheduler for Ubuntu and Ubuntu Core systems.


## Utilities
This snap provides a simple set of API for scheduling the shutdown of Ubuntu and Ubuntu Core systems using curl.

***

## Snap building
The snap can be built using snapcraft. The snapcraft.yaml file is located in the snap directory. To build the snap, use the following command:

`snapcraft`

Remember to put yourself in the snap-power-scheduler directory before running the command.

## Snap installation
The installation process is pretty straight forward and you can install the snap in two different ways:
- From the snap store
- From a local file

The easiest way is to install the snap from the snap store. To do so, use the following command:

`snap install powerscheduler`


If you prefer to install the snap from a local file, follow the instructions below.

For installing the snap in devmode from a local file, use the following command:

`snap install powerscheduler_0.1_amd64.snap --dangerous --devmode`

For installing the snap in confined mode from a local file, use the following command:

`snap install powerscheduler_0.1_amd64.snap --dangerous`

## Snap configuration
After installing the snap, you need to connect the snap to the following interfaces:
- `snap connect powerscheduler:shutdown`

## Usage
Using the snap is pretty straight forward.

To setup your scheduling, use:
```
curl --header "Content-Type: application/json" --request POST
--data '{
    "mon": null,
    "tue": "20:48:00",
    "wed": "23:07:10",
    "thu": "08:39:00",
    "fri": null,
    "sat": "18:44:35",
    "sun": null
    }' http://target-ip-address:3535/set-shutdown-schedule
```
