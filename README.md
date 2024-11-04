## WIM (Werkdruk Inzicht en Monitor)
Testing phase -- voor al uw inzicht in wie wanneer druk is binnen WIO

## Toevoegen van nieuwe collega's

## Verwijderen van oude collega's



## Development

Github actions build the docker image that's automatically deployed to the dashboard
server. Those actions also check a bit of formatting and do some basic syntax checks. To
do those checks + automatic fixes locally, install "pre-commit" and run it:

    $ pip install pre-commit  # You only need to do this once on your laptop
    $ pre-commit run --all    # This runs checks + formatting


## Server install

Installed via the regular dashboard auto-update setup.

Custom: the `/app/input_employees/` directory is a docker volume on the server, so it is
retained upon restarts. This also means that changes in the `input_employees/` directory
in this git repository are **not** synced to the directory on the server. (Apart from
initially copying over the files when the volume on the server is created).
