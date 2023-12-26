import os
import importlib
import pip
import time


current_working_directory = os.getcwd()
print("current working directory", current_working_directory)


def uninstall(package: str = "macrobond_data_api") -> None:
    pip.main(["uninstall", "-y", package])


def install(package: str = "macrobond_data_api") -> None:
    pip.main(["install", "-y", package])


def module_installed(name: str = "macrobond_data_api") -> bool:
    try:
        importlib.import_module(name)
        return True
    except ModuleNotFoundError:
        return False


def install_interpreted() -> None:
    path = os.path.join(current_working_directory, "dist")
    files = [f for f in os.listdir(path) if not f.endswith(".whl")]
    if len(files) != 1:
        raise Exception("More than one file in dist folder")
    file = os.path.join(current_working_directory, "dist", files[0])

    # if module_installed():
    #    uninstall()

    pip.main(["install", file])


def install_compiled() -> None:
    path = os.path.join(current_working_directory, "dist")
    files = [f for f in os.listdir(path) if f.endswith(".whl")]
    if len(files) != 1:
        raise Exception("More than one file in dist folder")
    file = os.path.join(current_working_directory, "dist", files[0])

    # if module_installed():
    #    uninstall()

    pip.main(["install", file])


def reload() -> None:
    import macrobond_data_api

    importlib.reload(macrobond_data_api)

    print("macrobond_data_api.__file__", macrobond_data_api.__file__)


def test() -> None:
    import macrobond_data_api as mb

    t0 = time.time()
    mb.get_all_vintage_series("usgdp")
    print(time.time() - t0)


uninstall()

install_interpreted()
reload()
test()
test()
test()

install_compiled()
reload()
test()
test()
test()


if __name__ == "__main__":
    ...
else:
    print("This module is not intended to be imported")
