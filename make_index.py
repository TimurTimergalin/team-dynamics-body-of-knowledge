from __future__ import annotations

from markdown_it import MarkdownIt
from markdown_it.token import Token
from dataclasses import dataclass, field

import os
from io import StringIO
import sys

text_ = """
# Title 1 `with code`
## Title 2
> Lol
>> keke
"""

md = MarkdownIt()

excluded_prefixes = [
    r'.\.'
]


def get_title(text, path):
    tokens = md.parse(text)
    match tokens:
        case [
            Token(type='heading_open', markup='#'),
            Token(
                type='inline',
                content=content
            ),
            *_
        ]:
            return content
        case _:
            raise ValueError(f"'{path}' does not start with a level 1 heading")


@dataclass
class Link:
    title: str
    name: str
    dirs: tuple[str, ...]

    def tree_up(self, dir_name):
        return Link(
            title=self.title,
            name=self.name,
            dirs=(dir_name,) + self.dirs
        )

    def render(self):
        href = '/'.join([*self.dirs, self.name])
        if ' ' in href:
            raise RuntimeError(f'Links to files should not contain spaces, but link \'{href}\' does')
        return f"[{self.title}]({href})"


@dataclass
class IndexFile:
    path: str
    content: list[Link]


def perform_walk(walk_gen):
    full_path, dirs, files = next(walk_gen)

    files = (x for x in files if x.endswith('.md'))
    files = (x for x in files if x.lower() != 'readme.md')
    links = []

    for file in files:
        file_full_path = os.path.join(full_path, file)
        with open(file_full_path, encoding='utf-8') as f:
            content = f.read()
        links.append(Link(
            title=get_title(content, file_full_path),
            name=file,
            dirs=(),
        ))

    for dir_ in dirs:
        inner_index = yield from perform_walk(walk_gen)
        if inner_index:
            links.extend(x.tree_up(dir_) for x in inner_index.content)

    res = IndexFile(
        path=os.path.join(full_path, 'README.md'),
        content=links
    )

    for exc in excluded_prefixes:
        if full_path.startswith(exc):
            return
    yield res
    return res


@dataclass
class IndexFileTree:
    node_links: list[Link] = field(default_factory=list)
    children: dict[str, IndexFileTree] = field(default_factory=dict)

    def add_link(self, link: Link, destination=None):
        if destination is None:
            destination = link.dirs
        if not destination:
            self.node_links.append(link)
        else:
            el, *rest = destination
            if el not in self.children:
                self.children[el] = IndexFileTree()
            self.children[el].add_link(link, rest)

    def render_to_file(self, f, level=0):
        for link in self.node_links:
            print(link.render(), file=f, end='\n\n')
        for child_name, child in self.children.items():
            h_lvl = level + 2
            if h_lvl > 6:
                print(child_name, "[Слишком глубоко]")
            else:
                print('#' * h_lvl, child_name, file=f, end='\n\n')
                child.render_to_file(f, level + 1)

    def render(self):
        with StringIO() as f:
            print("# Содержание", file=f)
            self.render_to_file(f)
            return f.getvalue()


@dataclass
class FinalizedFile:
    path: str
    content: str


def finalize_file(file: IndexFile):
    tree = IndexFileTree()
    for link in file.content:
        tree.add_link(link)

    return FinalizedFile(
        path=file.path,
        content=tree.render()
    )


def get_files():
    walk_gen = os.walk('.')
    files = perform_walk(walk_gen)
    return map(finalize_file, files)


def create_files(files):
    for file in files:
        with open(file.path, 'w', encoding='utf-8') as f:
            f.write(file.content)


def validate_files(files):
    error = RuntimeError("You seem to have forgotten to remake the index")
    for file in files:
        f = None
        try:
            f = open(file.path, encoding='utf-8')
        except IOError:
            raise error
        else:
            if f.read() != file.content:
                raise error
        finally:
            if f:
                f.close()


def main(argv):
    if len(argv) != 2:
        raise RuntimeError("Invalid args")

    action = argv[1]

    supported = ['generate', 'validate']
    if action.lower() not in supported:
        raise RuntimeError(f"Invalid action '{action}', the only supported are {', '.join(supported)}")

    match action:
        case 'generate':
            create_files(get_files())
            os.system('git add */README.md')
            os.system('git add README.md')
        case 'validate':
            validate_files(get_files())


if __name__ == '__main__':
    assert False
    main(sys.argv)
