import click

from typing import Optional

from archiver import Encoder, Decoder


def try_decode(decoder: Decoder, password: Optional[str]) -> None:
    try:
        decoder.decode(password)
    except PermissionError:
        password = click.prompt('Для этого файла требуется пароль',
                                hide_input=True)
        try_decode(decoder, password)
    except ValueError:
        click.echo("Неверный пароль.")
        exit(1)


@click.command()
@click.argument('files', nargs=-1)
@click.option('--encode', 'mode', flag_value='encode', default=True)
@click.option('--decode', 'mode', flag_value='decode')
@click.option('--password', '-p', help='Password')
@click.option('--listing', '-l', is_flag=True, help='Print listing')
@click.option('--output', '-o', help='Output path')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
def main(files, mode, password, listing, output, verbose):
    if mode == 'encode':
        encoder = Encoder(*files, output_path=output, password=password)
        encoder.encode()
        return

    decoder = Decoder(files[0], output_path=output)
    if listing:
        print(decoder.file_listings)

    if verbose:
        click.echo(f'Extracting {files[0]} to {output}')
        click.echo(decoder.file_listings)
        click.echo(f'Timestamp: {decoder.meta.timestamp}')

    try_decode(decoder, password)


if __name__ == '__main__':
    main()
