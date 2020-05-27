# -*- coding: utf-8 -*-

"""kacl.kacl-cli: provides entry point main()."""

import sys
import os
import kacl
import chalk
import click
import json
import semver
import traceback
import git
from datetime import datetime

def load_changelog(ctx):
    config = ctx.obj['config']
    file = ctx.obj['file']

    changelog_file = os.path.join(os.getcwd(), file)
    if not os.path.exists(changelog_file):
        click.echo(click.style("Error: ", fg='red') +
                    f"{changelog_file} not found")
        sys.exit(1)

    if config is None:
        default_config_path = os.path.join(os.getcwd(), '.kacl.yml')
        config = default_config_path if os.path.exists(default_config_path) else None

    kacl_config = kacl.KACLConfig(config)
    if file:
        kacl_config.set_changelog_file_path(file)

    # read the changelog
    kacl_changelog = kacl.load(kacl_config.changelog_file_path())
    kacl_changelog.set_config(kacl_config)

    # share the objects
    return (kacl_changelog, changelog_file)

def prefixed_environ():
    return dict((("${}".format(key), value) for key, value in os.environ.items()))

@click.group(invoke_without_command=True)
@click.option('-v', '--version', is_flag=True, required=False, help='Prints the current version of the CLI.')
@click.option('-c', '--config', required=False, default=None, type=click.Path(exists=False), help='Path to kacl config file.', show_default=True)
@click.option('-f', '--file', required=False, default='CHANGELOG.md', type=click.Path(exists=False), help='Path to changelog file.', show_default=True)
@click.pass_context
def cli(ctx, version=None, config=None, file=None):
    if ctx.obj is None:
        ctx.obj = dict()

    ctx.obj['config'] = config
    ctx.obj['file'] = file

    # if --version was given, print version and exit directly
    if version:
        click.echo(kacl.__version__)
        sys.exit(0)


@cli.command()
@click.pass_context
@click.argument('section', type=str)
@click.argument('message', type=str)
@click.option('-m', '--modify', is_flag=True, help='This option will add the changes directly into changelog file.')
def add(ctx, section, message, modify):
    """Adds a given message to a specified unreleased section. Use '--modify' to directly modify the changelog file.
    """
    kacl_changelog, kacl_changelog_filepath = load_changelog(ctx)

    # add changes to changelog
    kacl_changelog.add(section=section, data=message)
    kacl_changelog_content = kacl.dump(kacl_changelog)
    if modify:
        with open(kacl_changelog_filepath, 'w') as f:
            f.write(kacl_changelog_content)
        f.close()
    else:
        click.echo(kacl_changelog_content)


@cli.command()
@click.pass_context
def current(ctx):
    """Returns the current version from the Changelog.
    """
    kacl_changelog, kacl_changelog_filepath = load_changelog(ctx)

    current_version = kacl_changelog.current_version()
    click.echo(current_version)


@cli.command()
@click.pass_context
@click.argument('version', type=str)
def get(ctx, version):
    """Returns a given version from the Changelog.
    """
    kacl_changelog, kacl_changelog_filepath = load_changelog(ctx)

    # add changes to changelog
    kacl_version = kacl_changelog.get(version)

    if kacl_version:
        kacl_changelog_content = kacl.dump(kacl_version)
        click.echo(kacl_changelog_content)
    else:
        click.echo(click.style("Error: ", fg='red') +
                   f'"{version}" could not be found in changelog.')
        sys.exit(1)


@cli.group(invoke_without_command=True)
@click.pass_context
def link(ctx):
    """Lets you modify version links
    """
    pass

@link.command()
@click.pass_context
@click.option('-m', '--modify', is_flag=True, help='This option will add the changes directly into changelog file.')
@click.option('--host-url', required=False, default=None, type=str, help='Host url to the git service. (i.e https://github.com/mschmieder/python-kacl)', show_default=True)
@click.option('--compare-versions-template', required=False, default=None, type=str, help='Template string for version comparison link.', show_default=True)
@click.option('--unreleased-changes-template', required=False, default=None, type=str, help='Template string for unreleased changes link.', show_default=True)
@click.option('--initial-version-template', required=False, default=None, type=str, help='Template string for initial version link.', show_default=True)
def generate(ctx, modify, host_url, compare_versions_template, unreleased_changes_template, initial_version_template):
    kacl_changelog, kacl_changelog_filepath = load_changelog(ctx)

    kacl_changelog.generate_links(host_url=host_url,
                                  compare_versions_template=compare_versions_template,
                                  unreleased_changes_template=unreleased_changes_template,
                                  initial_version_template=initial_version_template)

    kacl_changelog_content = kacl.dump(kacl_changelog)
    if modify:
        with open(kacl_changelog_filepath, 'w') as f:
            f.write(kacl_changelog_content)
        f.close()
    else:
        click.echo(kacl_changelog_content)


@cli.command()
@click.pass_context
@click.option('--json', 'as_json', is_flag=True, help='Print validation output as yaml.')
def verify(ctx, as_json):
    """Veryfies if the changelog is in "keep-a-changlog" format.
    Use '--json' get JSON formatted output that can be easier integrated into CI workflows.
    Exit code is the number of identified errors.
    """
    kacl_changelog, kacl_changelog_filepath = load_changelog(ctx)
    kacl_changelog_filepath = os.path.basename(kacl_changelog_filepath)

    valid = kacl_changelog.is_valid()
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
        if not valid:
            click.echo(f'{len(validation.errors())} error(s) generated.')
        else:
            click.secho('Success', fg='green')

    if not valid:
        sys.exit(len(validation.errors()))


@cli.command()
@click.pass_context
@click.argument('version', type=str)
@click.option('-m', '--modify', is_flag=True, help='This option will add the changes directly into changelog file.')
@click.option('-l', '--link', required=False, default=None, type=str, help='A url that the version will be linked with.', show_default=True)
@click.option('-g', '--auto-link', is_flag=True, help='Will automatically create and update necessary links.')
@click.option('-c', '--commit', is_flag=True, help='If passed this will create a git commit with the changed Changelog.')
@click.option('--commit-message', required=False, default=None, type=str, help='The commit message to use when using --commit flag')
@click.option('-t', '--tag', is_flag=True, help='If passed this will create a git tag for the newly released version.')
@click.option('--tag-name', required=False, default=None, type=str, help='The tag name to use when using --tag flag')
@click.option('--tag-description', required=False, default=None, type=str, help='The tag description text to use when using --tag flag')
@click.option('-d', '--allow-dirty', is_flag=True, help='If passed this will allow to commit/tag even on a "dirty".')
def release(ctx, version, modify, link, auto_link, commit, commit_message, tag, tag_name, tag_description, allow_dirty):
    """Creates a release for the latest 'unreleased' changes. Use '--modify' to directly modify the changelog file.
    You can automatically use the latest version by using the version keywords 'major', 'minor', 'patch'

    Example:

        kacl-cli release 1.0.0

        kacl-cli release major|minor|patch
    """
    kacl_changelog, kacl_changelog_filepath = load_changelog(ctx)
    kacl_config = kacl_changelog.config()

    if not kacl_changelog.is_valid():
        click.echo(click.style("Error: ", fg='red') +
                       f"Changelog is not valid. Run 'kacl-cli verify' for more information.")
        sys.exit(1)

    # check if the version string indicates automatic increment
    increment = None
    if version in ['major', 'minor', 'patch']:
        increment = version
        version = None  # reset
    else:
        # check if version is a valid semantic version
        try:
            semver.parse(version)
        except:
            click.echo(click.style("Error: ", fg='red') +
                       f'"{version}" not a valid semantic version.')
            sys.exit(1)

    if not kacl_changelog.has_changes():
        click.echo(click.style("Error: ", fg='red') +
                   'The current changlog has no changes. You can only release if changes are available.')
        sys.exit(1)

    # get the latest_version before the release
    latest_version = kacl_changelog.current_version()

    # check config to see if we need to autogenerate changes
    if auto_link is False and kacl_config.link_auto_generate():
        auto_link = True

    kacl_changelog.release(version=version, link=link, auto_link=auto_link, increment=increment)

    # get the new version
    new_version = kacl_changelog.current_version()

    # dump the content
    kacl_changelog_content = kacl.dump(kacl_changelog)

    # check if we should modify the file
    if modify:
        with open(kacl_changelog_filepath, 'w') as f:
            f.write(kacl_changelog_content)
        f.close()

        if commit or tag or kacl_config.git_create_commit() or kacl_config.git_create_tag():
            vcs_context = {
                "latest_version": latest_version,
                "new_version": new_version,
            }
            time_context = {
                'now': datetime.now(),
                'utcnow': datetime.utcnow(),
            }
            vcs_context.update(time_context)
            vcs_context.update(prefixed_environ())

            commit_message  = commit_message if commit_message != None else kacl_config.git_commit_message()
            tag_name        = tag_name if tag_name != None else kacl_config.git_tag_name()
            tag_description = tag_description if tag_description != None else kacl_config.git_tag_description()

            try:
                repo = git.Repo(os.getcwd())
            except git.InvalidGitRepositoryError:
                click.echo(click.style("Error: ", fg='red') +
                           f'"{os.getcwd()}" is no valid git repository.')

            if not repo.is_dirty() and not allow_dirty:
                click.echo(click.style("Error: ", fg='red') +
                           f"Repository is marked 'dirty'. Use --allow-dirty if you want to commit/tag on a dirty repository")

            if commit or kacl_config.git_create_commit():
                repo.git.add(kacl_config.changelog_file_path())
                for f in kacl_config.git_commit_additional_files():
                    repo.git.add(f)
                repo.git.commit('-m', commit_message.format(**vcs_context))

            if tag or kacl_config.git_create_tag():
                repo.create_tag(tag_name.format(**vcs_context),
                                message=tag_description.format(**vcs_context))

    else:
        click.echo(kacl_changelog_content)


@cli.command()
@click.option('-o', '--output-file', required=False, type=click.Path(exists=False), help='File to write the created changelog to.')
def new(output_file):
    """Creates a new changlog.
    """
    kacl_changelog = kacl.new()
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
        click.secho(
            'Unexpected error occured. Make sure your file is a valid Mardown file.', fg='red')
        click.echo(traceback.format_exc())
        sys.exit(1)


if __name__ == '__main__':
    start()
