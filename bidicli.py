import click
from python_bidi_tools import get_display_mod

# @click.command()
# def cli():
#     click.echo("Hello World")

@click.command()
@click.argument('string')
def main(string):
    # click.echo(click.style(string+'B', fg='magenta'))
    # click.echo(get_display_mod(string))
    click.echo(click.style(get_display_mod(string), fg='magenta'))

if __name__ == "__main__":
    main()