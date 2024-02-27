import os
import shutil
import sys
from context import WorkItem, run


class Pdoc(WorkItem):
    async def run(self) -> None:
        await self.python_run("pdoc", "./macrobond_data_api/ -o ./docs/build/")

        if os.path.isdir("docs/build/macrobond_data_api/assets"):
            shutil.rmtree("docs/build/macrobond_data_api/assets")
        shutil.copytree("docs/assets", "docs/build/macrobond_data_api/assets")

        file_url = os.path.join(os.getcwd(), "docs", "build", "macrobond_data_api", "index.html").replace("\\", "/")

        self.print("file:///" + file_url)


class PdocServer(WorkItem):
    async def run(self) -> None:
        await self.python_run("pdoc", " --http : --html --template-dir docs --force -o docs/build macrobond_data_api")


def main() -> None:
    command = sys.argv[1] if len(sys.argv) <= 2 else None

    if command == "--no_server":
        run(Pdoc)

    if command == "--server":
        run(PdocServer)

    if command:
        print("bad args " + command)
    else:
        print("no args")

    sys.exit(1)


if __name__ == "__main__":
    main()
