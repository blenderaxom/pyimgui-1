# -*- coding: utf-8 -*-
from docutils import nodes
from docutils.parsers.rst import Directive
from docutils.parsers.rst import directives
import os
import re
from hashlib import sha1

try:
    from gen_example import render_snippet
except ImportError:
    render_snippet = None


VISUAL_EXAMPLES_DIR = "visual_examples"

# todo: maybe should be more generic from sphinx conf
SOURCE_DIR = os.path.join(os.path.dirname(__file__))


def flag(argument):
    """Reimplement directives.flag to return True instead of None
    Check for a valid flag option (no argument) and return ``None``.
    (Directive option conversion function.)

    Raise ``ValueError`` if an argument is found.
    """
    if argument and argument.strip():
        raise ValueError('no argument is allowed; "%s" supplied' % argument)
    else:
        return True


def wraps_role(name, rawtext, text, lineno, inliner, options={}, content=[]):
    """Mark something as wrapping given API element

    Returns 2 part tuple containing list of nodes to insert into the
    document and a list of system messages.  Both are allowed to be
    empty.

    :param name: The role name used in the document.
    :param rawtext: The entire markup snippet, with role.
    :param text: The text marked with the role.
    :param lineno: The line number where rawtext appears in the input.
    :param inliner: The inliner instance that called us.
    :param options: Directive options for customization.
    :param content: The directive content for customization.
    """
    return [
        nodes.strong(rawtext, "Wraps API: "),
        nodes.literal(rawtext, text)
    ], []


class VisualDirective(Directive):
    has_content = True

    final_argument_whitespace = True
    option_spec = {
        'title': directives.unchanged,
        'width': directives.positive_int,
        'height': directives.positive_int,
        'without_window': flag,
    }

    def run(self):
        source = '\n'.join(self.content.data)
        literal = nodes.literal_block(source, source)
        literal['language'] = 'python'

        # docutils document model is insane!
        head1 = nodes.paragraph()
        head1.append(nodes.strong("Example:", "Example: "))

        head2 = nodes.paragraph()
        head2.append(
            nodes.section("foo", nodes.strong("Outputs:", "Outputs: "))
        )

        directive_nodes = [
            head1,
            literal,
            head2,
            self.get_image_node(source)
        ]

        return directive_nodes

    def phrase_to_filename(self, phrase):
        """Convert phrase to normilized file name.

        """
        # remove non-word characters
        name = re.sub(r"[^\w\s]", '', phrase.strip().lower())
        # replace whitespace with underscores
        name = re.sub(r"\s+", '_', name)

        return name + '.png'

    def get_image_node(self, source):
        title = self.options.get(
            'title',
            sha1(source).hexdigest()
        )

        file_path = os.path.join(
            VISUAL_EXAMPLES_DIR,
            self.phrase_to_filename(title)
        )

        env = self.state.document.settings.env

        if render_snippet and env.config['render_examples']:
            render_snippet(
                source,
                file_path,
                output_dir=SOURCE_DIR, **self.options
            )

        img = nodes.image()
        img['uri'] = "/" + file_path
        return img


def setup(app):
    app.add_config_value('render_examples', False, 'html')

    app.add_role('wraps', wraps_role)
    app.add_directive('visual-example', VisualDirective)
    return {'version': '0.1'}
