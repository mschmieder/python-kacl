# -*- coding: utf-8 -*-

"""kacl.kacl-cli: provides entry point main()."""

import sys
import os
import kacl
import chalk
import click
import json
import traceback

@click.group()
@click.option('-c', '--config', required=False, default='.kacl.conf', type=click.Path(exists=False), help='Path to kacl config file', show_default=True)
@click.option('-f', '--file', required=False, default='CHANGELOG.md', type=click.Path(exists=False), help='Path to changelog file', show_default=True)
@click.pass_context
def cli(ctx, config, file):
    if ctx.invoked_subcommand != 'init':
        changelog_file = os.path.join(os.getcwd(), file)
        if not os.path.exists(changelog_file):
            click.echo(click.style("Error: ", fg='red') +
                       f"{changelog_file} not found")
            sys.exit(1)

        kacl_changelog = kacl.load(changelog_file)
        ctx.obj['changelog'] = kacl_changelog
        ctx.obj['changelog_filepath'] = changelog_file


@cli.command()
@click.pass_context
@click.argument('section', type=str)
@click.argument('message', type=str)
@click.option('--inline', is_flag=True, help='This option will add the changes directly into changelog file')
def add(ctx, section, message, inline):
    kacl_changelog = ctx.obj['changelog']
    kacl_changelog_filepath = ctx.obj['changelog_filepath']

    # add changes to changelog
    kacl_changelog.add(section=section, content=message)
    kacl_changelog_content = kacl.dump(kacl_changelog)
    if inline:
        with open(kacl_changelog_filepath, 'w') as f:
            f.write(kacl_changelog_content)
        f.close()
    else:
        click.echo(kacl_changelog_content)


@cli.command()
@click.pass_context
@click.option('--json', 'as_json', is_flag=True, help='Print validation output as yaml')
@click.option('-o', '--output-file', required=False, type=click.Path(exists=False), help='Write verification output to file')
def verify(ctx, as_json, output_file):
    kacl_changelog = ctx.obj['changelog']
    kacl_changelog_filepath = os.path.basename(ctx.obj['changelog_filepath'])

    valid = kacl_changelog.is_valid()
    if not valid:
        validation = kacl_changelog.validate()

        if as_json:
            validation_map = validation.convert_to_dict()
            click.echo(json.dumps(validation_map, sort_keys=True, indent=4))
        else:
            green = chalk.Chalk('green')
            red = chalk.Chalk('red')
            white = chalk.Chalk('white')
            bold = chalk.bold

            for error in validation.errors():
                start_char_pos, end_char_pos = error.position()

                char_indicator = start_char_pos
                if start_char_pos == None:
                    char_indicator = 0

                click.echo(bold + kacl_changelog_filepath + ':' +
                        f'{error.line_number()}:{char_indicator}: ' +
                        red + 'error: ' +
                        white + error.error_message() +
                        chalk.RESET)

                if error.line():
                    click.echo(error.line())
                    if start_char_pos != None and end_char_pos != None:
                        mark_length = end_char_pos-start_char_pos-1
                        click.echo(' '*start_char_pos +
                                green + '^' +
                                '~'*(mark_length) +
                                chalk.RESET)

            click.echo(f'{len(validation.errors())} error(s) generated.')

    if not valid:
        sys.exit(len(validation.errors()))


@cli.command()
@click.pass_context
@click.argument('version', type=str)
@click.option('--inline', is_flag=True, help='This option will add the changes directly into changelog file')
@click.option('-l', '--link', required=False, default=None, type=str, help='A url that the version will be linked with', show_default=True)
def release(ctx, version, inline, link):
    kacl_changelog = ctx.obj['changelog']
    kacl_changelog_filepath = ctx.obj['changelog_filepath']

    # release changes
    kacl_changelog.release(version=version, link=link)
    kacl_changelog_content = kacl.dump(kacl_changelog)
    if inline:
        with open(kacl_changelog_filepath, 'w') as f:
            f.write(kacl_changelog_content)
        f.close()
    else:
        click.echo(kacl_changelog_content)


@cli.command()
@click.option('-o', '--output-file', required=False, type=click.Path(exists=False), help='File to write Changelog to')
def init(output_file):
    kacl_changelog = kacl.init()
    kacl_changelog_content = kacl.dump(kacl_changelog)
    if output_file:
        with open(output_file, 'w') as f:
            f.write(kacl_changelog_content)
        f.close()
    else:
        click.echo(kacl_changelog_content)


def start():
    try:
        cli(obj={})
    except SystemExit as e:
        sys.exit(e.code)
    except:
        click.secho('Unexpected error occured. Make sure your file is a valid Mardown file.', fg='red')
        click.echo(traceback.format_exc())
        sys.exit(1)

if __name__ == '__main__':
    start()
