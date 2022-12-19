import click


@click.command()
@click.argument('files', nargs=-1)
@click.option('--encode', 'mode', case_sensitive=False, flag_value='encode', default=True)
@click.option('--decode', 'mode', case_sensitive=False, flag_value='decode')
@click.option('--checksum', '-c', is_flag=True, help='Print checksums')
@click.option('--stats', '-s', is_flag=True, help='Print statistics')
@click.option('--password', '-p', help='Password')
@click.option('--listing', '-l', is_flag=True, help='Print listing')
def main(files, mode, checksum, stats, password, listing):
    """This is a simple archiver."""
    print(files, mode, checksum, stats, password, listing)