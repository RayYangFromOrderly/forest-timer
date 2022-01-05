from typing import Any, Iterable, Optional
import time
import uuid
from termcolor import colored, cprint

import inspect

class FTNode:
    def __init__(self, timer, text: str, line_number: Optional[int] = None, parent=None, root=None, indent=0):
        self.line_count = line_number
        self.timer = timer
        self.text = text
        self.parent = parent
        self.indent = indent
        self.last_step = time.time()
        self.time = 0

    def update(self):
        self.time += time.time()-self.timer.last_step
        self.timer.visualize()
        self.timer.last_step = time.time()

    def get_time_display(self, seconds):
        if seconds < 1:
            color = 'green'
        elif seconds < 10:
            color = 'yellow'
        else:
            color = 'red'
        return colored(f'{seconds:.2f}', color)

    def display(self):
        return f'{colored(self.text, "cyan")} | {self.get_time_display(self.time)}'


class FTFor(FTNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.loop_size = 0
        self.loop_index = 0

    def update(self):
        self.time += time.time()-self.last_step
        self.timer.visualize()
        self.last_step = time.time()
        self.timer.last_step = time.time()
        self.loop_index += 1

    def setup(self, iter):

        self.ft_iter = FTIterator(self, iter)
        self.loop_size = len(iter)
        self.loop_index = 0
        self.last_step = time.time()
        if not self.text:
            self.text = str(iter)


    def display(self):
        title = colored(self.text, "cyan")
        if self.loop_size:
            rate = self.loop_index / self.loop_size*100
        else:
            rate = 0
        if self.loop_size == self.loop_index:
            progress = f'{colored("Completed", "green")} ({self.loop_size})'
        else:
            progress = f'{self.loop_index} / {self.loop_size} ({rate:.2f}%)'

        return f'{title} | {progress} {self.get_time_display(self.time)}'


class FTIterator:
    def __init__(self, node, target):
        self.node = node
        self.target = iter(target)

    def __iter__(self):
        return self

    def __next__(self):
        try:
            res = next(self.target)
            self.node.update()
            return res

        except StopIteration:
            if not self.node.parent:
                self.node.timer.visualize(flush=True)
            self.node.timer.indent -= 1
            raise StopIteration


class ForestTimer:
    def __init__(self):
        self.depth = 0
        self.node_at_line = {}
        self.last_line = '\033[F'
        self.root = None
        self.current_for = None
        self.indent = 1
        self.last_print = time.time()
        self.last_step = time.time()

    def _add_node(self, line, node: FTNode):
        self.node_at_line[line] = node

    def visualize(self, flush=False):
        if time.time()-self.last_print > 0.1 or flush:
            for line, node in self.node_at_line.items():
                print('      ' * (node.indent), node.display(), end='       \r')
                print(f'{colored(line, "grey")}')
            self.last_print = time.time()

            if not flush:
                print('\033[F' * len(self.node_at_line), end='')

    def __call__(self, iter:Iterable, name='') -> Any:
        previous_frame = inspect.currentframe().f_back
        (filename, line_number, function_name, lines, index) = inspect.getframeinfo(previous_frame)

        node = self.node_at_line.get(line_number, FTFor(self, name, line_number, parent=self.current_for, root=self.root, indent=self.indent))

        self.node_at_line[line_number] = node
        self.indent = node.indent
        self.indent += 1
        node.setup(iter)
        if not self.root:
            self.root = node

        self.current_for = node
        return node.ft_iter

    def step(self, name=''):
        previous_frame = inspect.currentframe().f_back
        (filename, line_number, function_name, lines, index) = inspect.getframeinfo(previous_frame)

        node = self.node_at_line.get(line_number, FTNode(self, name, line_number, parent=self.current_for, root=self.root, indent=self.indent))
        node.text = name
        node.update()
        self.node_at_line[line_number] = node



ft = ForestTimer()

for i in ft(range(100)):
    for j in ft(range(100)):
        ft.step(f'{i}, {j}')
        ft.step(f'{i}, {j}')
        ft.step(f'{i}, {j}')
        ft.step(f'{i}, {j}')

    for j in ft(range(100)):
        ft.step(f'{i}, {j}')

# for i in range(10):
#     for j in range(10):
#         ft.step(f'{i}, {j}')
#         ft.step(f'{i}, {j}')
#         ft.step(f'{i}, {j}')
#         ft.step(f'{i}, {j}')
