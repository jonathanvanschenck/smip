import click

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.command(context_settings=CONTEXT_SETTINGS)
def smip():
    """Render markdown with scripture references
    """
    click.echo("I'll do something someday . . .")
