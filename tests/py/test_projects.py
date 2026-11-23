"""Every project follows the rules of the README, read from its source
without running it. Run: python3 -m unittest discover tests/py

- the folder holds <name>.py with a <name>() function that takes no arguments
- it imports only the standard library, NumPy, common and its own modules
- a soundscape is reproducible: its randomness comes from one
  numpy.random.default_rng(SEED), and its settings come first
- every soundscape scene has its ten takes, each with its own seed
- the README counts the projects right
"""
import ast
import re
import sys
import unittest
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "scripts"
TAKES = [f"{take:02}" for take in range(10)]
THEMES = ("cyberpunk", "nature", "steampunk")


def projects():
    """{path inside scripts/: folder}, like project.sh lists them."""
    found = {}
    for script in SCRIPTS.glob("**/*.py"):
        folder = script.parent
        if folder != SCRIPTS and script.stem == folder.name.rsplit("-", 1)[-1]:
            found[folder.relative_to(SCRIPTS).as_posix()] = folder
    return dict(sorted(found.items()))


PROJECTS = projects()
SOUNDSCAPES = {k: v for k, v in PROJECTS.items() if k.startswith("soundscapes/")}


def parse(path):
    return ast.parse(path.read_text(), filename=str(path))


def settings(tree):
    """{name: value} of the constants assigned at the top level."""
    out = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 \
                and isinstance(node.targets[0], ast.Name):
            try:
                out[node.targets[0].id] = ast.literal_eval(node.value)
            except ValueError:
                pass  # computed, e.g. FRAMES = round(SECONDS * RATE)
    return out


class ProjectTest(unittest.TestCase):

    def test_there_are_projects(self):
        self.assertGreater(len(PROJECTS), 0)
        self.assertGreater(len(SOUNDSCAPES), 0)

    def test_each_has_its_function(self):
        for project, folder in PROJECTS.items():
            with self.subTest(project=project):
                name = folder.name.rsplit("-", 1)[-1]
                tree = parse(folder / f"{name}.py")
                functions = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)}
                self.assertIn(name, functions, f"{name}.py has no def {name}()")
                arguments = functions[name].args
                required = len(arguments.args) - len(arguments.defaults)
                self.assertEqual(required, 0, f"{name}() must take no arguments")

    def test_imports_stay_inside_the_project(self):
        # a project needs nothing outside its folder apart from common.py
        allowed = set(sys.stdlib_module_names) | {"numpy", "common"}
        for project, folder in PROJECTS.items():
            own = {path.stem for path in folder.glob("*.py")}
            for path in folder.glob("*.py"):
                with self.subTest(project=project, file=path.name):
                    for node in ast.walk(parse(path)):
                        if isinstance(node, ast.Import):
                            modules = [alias.name for alias in node.names]
                        elif isinstance(node, ast.ImportFrom):
                            self.assertEqual(node.level, 0, "relative import")
                            modules = [node.module]
                        else:
                            continue
                        for module in modules:
                            top = module.split(".")[0]
                            self.assertIn(top, allowed | own, f"line {node.lineno}: import {module}")


class SoundscapeTest(unittest.TestCase):

    def test_names(self):
        pattern = re.compile(rf"soundscapes/({'|'.join(THEMES)})-[a-z]+\d\d$")
        for project in SOUNDSCAPES:
            with self.subTest(project=project):
                self.assertRegex(project, pattern)

    def test_every_scene_has_ten_takes_with_their_own_seeds(self):
        scenes = defaultdict(dict)
        for project, folder in SOUNDSCAPES.items():
            scene, take = project[:-2], project[-2:]
            name = folder.name.rsplit("-", 1)[-1]
            scenes[scene][take] = settings(parse(folder / f"{name}.py")).get("SEED")
        for scene, takes in scenes.items():
            with self.subTest(scene=scene):
                self.assertEqual(sorted(takes), TAKES)
                seeds = list(takes.values())
                self.assertEqual(len(set(seeds)), len(seeds), f"seeds repeat: {takes}")

    def test_settings(self):
        for project, folder in SOUNDSCAPES.items():
            with self.subTest(project=project):
                name = folder.name.rsplit("-", 1)[-1]
                found = settings(parse(folder / f"{name}.py"))
                seconds, seed, fade = (found.get(k) for k in ("SECONDS", "SEED", "FADE"))
                self.assertIsInstance(seed, int, "SEED must be an int")
                self.assertIsInstance(seconds, (int, float), "SECONDS must be a number")
                self.assertTrue(10 <= seconds <= 600, f"SECONDS = {seconds}")
                self.assertIsInstance(fade, (int, float), "FADE must be a number")
                self.assertTrue(0 <= fade <= seconds / 2, f"FADE = {fade}, SECONDS = {seconds}")

    def test_randomness_comes_from_the_seed(self):
        # anything else would give another sound on every run
        for project, folder in SOUNDSCAPES.items():
            with self.subTest(project=project):
                name = folder.name.rsplit("-", 1)[-1]
                tree = parse(folder / f"{name}.py")
                rngs = []
                for node in ast.walk(tree):
                    if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Attribute) \
                            and node.value.attr == "random":
                        self.assertEqual(node.attr, "default_rng",
                                         f"line {node.lineno}: np.random.{node.attr}")
                    if isinstance(node, ast.Call) and getattr(node.func, "attr", "") == "default_rng":
                        rngs.append(node)
                self.assertEqual(len(rngs), 1, "one default_rng(SEED)")
                self.assertEqual(ast.unparse(rngs[0].args[0]) if rngs[0].args else "", "SEED")


class ReadmeTest(unittest.TestCase):

    WORDS = ("zero one two three four five six seven eight nine ten eleven twelve "
             "thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty "
             "thirty forty fifty sixty seventy eighty ninety").split()

    def spell(self, count):
        if count < 20:
            return self.WORDS[count]
        tens, ones = divmod(count, 10)
        word = self.WORDS[18 + tens] if count < 100 else str(count)
        return word if ones == 0 or count >= 100 else f"{word}-{self.WORDS[ones]}"

    def test_counts_the_projects_right(self):
        readme = " ".join((ROOT / "README.md").read_text().split()).lower()
        scenes = len({p[:-2] for p in SOUNDSCAPES})
        # (what the README counts, as a regex after the number; the count)
        claims = {
            r"projects[:.]": len(PROJECTS),
            r"arrangements of classical music": len(PROJECTS) - len(SOUNDSCAPES),
            r"ambient soundscapes": len(SOUNDSCAPES),
            r"ambient scenes": scenes,
            r"scenes</summary>": scenes,
        }
        number = rf"\d+|(?:{'|'.join(self.WORDS)})(?:-\w+)?"
        for claim, count in claims.items():
            with self.subTest(claim=claim):
                found = re.findall(rf"\b({number}) {claim}", readme)
                self.assertTrue(found, f"the README never counts its {claim}")
                wrong = [n for n in found if n not in (str(count), self.spell(count))]
                self.assertEqual(wrong, [], f"the README counts {count} as {wrong}")


if __name__ == "__main__":
    unittest.main()
