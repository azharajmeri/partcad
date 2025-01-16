import rich_click as click
from partcad.logging import info, debug


@click.command(help="Show the current user configuration")
@click.pass_obj
def cli(ctx) -> None:
    for key, value in vars(ctx.user_config).items():
        if not callable(value) and key[0] != "_":
            info(f"{key}: {value}")
    debug(f"File: {ctx.user_config.get_config_dir()}")
