import os
import shutil
import subprocess
from typing import List, Tuple, Optional
from pathlib import Path

from pdoc import pdoc
from pdoc import render


class Git:
    def __init__(self, path: str) -> None:
        self.path = path

    def list_tags(self) -> List[str]:
        stdout = self._run(['tag', '-l'])
        return list(x for x in stdout.split("\n",) if x != "")

    def checkout_tag(self, tag: str) -> None:
        r = self._run(['checkout', tag])
    
    def checkout_head(self) -> None:
        self._run(['checkout', "HEAD"])
        
    def _run(self, args: List[str]) -> str:
        r = subprocess.run(['git'] + args, cwd = self.path, stdout=subprocess.PIPE)
        stdout = r.stdout.decode()
        if r.returncode != 0:
            raise Exception("none 0 exit code: " + str(r.returncode) + "\n" + stdout)
        return stdout
    

class Verison:

    @property
    def name(self):
        if self.is_dev:
            return "dev"    
        if self.is_current:
           return "current v" + self.verison_str
        return "v"+ self.verison_str
    
    @property
    def url(self):
        if self.is_dev:
            return "dev"
        return self.verison_str
    
    def __init__(self,path: str, tag:str = None) -> None:
        self.path = path
        self.tag: Optional[str] = tag
        self.is_dev = tag is None
        if self.is_dev:
            self.verison: Tuple[int,int,int] = (999,999,999)
        else:
            self.verison = tuple(int(x) for x in tag.lower().replace("v","").split("."))
        self.verison_str =  ".".join(str(x) for x in self.verison)
        self.is_current = False

    @classmethod
    def get_verisons(cls, path: str, tags: List[str]) -> Tuple[List["Verison"], List[str]]:
        def is_verison(tag:str) -> bool:
            tag = tag.lower()
            return tag.count(".") == 3 and tag[0].isnumeric() or (tag[0] == "v" and tag[1].isnumeric())
        verisons = list(Verison(path, x) for x in tags if is_verison(x))
        verisons.sort()
        verisons[-1].is_current = True;
        verisons.append(Verison(path))

        non_verisons = list(x for x in tags if not is_verison(x))
        non_verisons.sort()
        
        return verisons, non_verisons
    
    def __eq__(self, other):
        return self.verison == other.verison
    
    def __lt__(self, other):
        return self.verison < other.verison
    
    def __str__(self) -> str:
        return self.name
    
    def __repr__(self) -> str:
        return str(self)


# use https://pypi.org/project/Jinja2/

here = Path(__file__).parent
doc_git_path = os.path.join(here, ".doc_git")
template_directory = os.path.join(here, "template")
output_directory = os.path.join(here , "build")

logo="data:image/svg+xml,%3C%3Fxml%20version%3D%221.0%22%20encoding%3D%22UTF-8%22%3F%3E %3C%21--%20Generator%3A%20Adobe%20Illustrator%2025.0.0%2C%20SVG%20Export%20Plug-In%20.%20SVG%20Version%3A%206.00%20Build%200%29%20%20--%3E %3Csvg%20version%3D%221.1%22%20id%3D%22Layer_1%22%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20xmlns%3Axlink%3D%22http%3A%2F%2Fwww.w3.org%2F1999%2Fxlink%22%20x%3D%220px%22%20y%3D%220px%22%20viewBox%3D%220%200%201903.2%20390.8%22%20style%3D%22enable-background%3Anew%200%200%201903.2%20390.8%3B%22%20xml%3Aspace%3D%22preserve%22%3E %3Cstyle%20type%3D%22text%2Fcss%22%3E .st0{fill%3A%232567A5%3B} .st1{fill%3A%231C355E%3B} .st2{fill%3A%23FFFFFF%3B} .st3{fill%3A%23666666%3B} .st4{fill%3A%23CCCCCC%3B} .st5{fill%3A%2324272A%3B} %3C%2Fstyle%3E %3Cg%3E %3Cg%3E %3Cpath%20class%3D%22st1%22%20d%3D%22M900.7%2C2c45-5.9%2C92.4%2C0.8%2C132.5%2C22.8c19.6%2C10.6%2C37.6%2C24.4%2C52.2%2C41.3c-7.5-0.2-14.5%2C3.2-21.8%2C3.8%20%20%20%20c-11.1-10.6-23.2-20.3-36.7-27.9c-21.6-12.6-45.8-20.3-70.5-23.3c-27.4-2.7-55.5-1.5-81.9%2C6.7c-34.7%2C10.3-66.1%2C31.6-88.3%2C60.2%20%20%20%20c-5.2-3.5-10.8-6.5-16.6-9C800.5%2C34.9%2C849.6%2C8.4%2C900.7%2C2z%22%2F%3E %3Cpath%20class%3D%22st1%22%20d%3D%22M1037.7%2C342.1c9.2-6%2C17.4-13.4%2C25.5-20.8c7.1%2C1.6%2C14%2C4%2C21.3%2C4.3c-24.3%2C27.5-57.1%2C46.9-92.3%2C57%20%20%20%20c-36.6%2C10.2-75.8%2C10.8-112.8%2C2.3c-23-5.4-45-15-64.7-28.1c-13.2-8.9-25.7-19.2-36-31.4c8-0.3%2C16.2%2C0.7%2C24-1.7%20%20%20%20c16%2C15.2%2C34.8%2C27.4%2C55.2%2C35.8c24.8%2C10.3%2C51.9%2C14.6%2C78.7%2C13.8C972.4%2C373%2C1008.1%2C362.2%2C1037.7%2C342.1z%22%2F%3E %3C%2Fg%3E %3Cg%3E %3Cpath%20class%3D%22st1%22%20d%3D%22M462.3%2C126.9c15-13.8%2C34.4-22.4%2C54.6-25c7.9-0.7%2C15.8-1.4%2C23.7-0.6c23.5%2C1.1%2C47.3%2C10.6%2C62.8%2C28.7%20%20%20%20c-5.9%2C5.5-11.4%2C11.5-17.6%2C16.5c-11.1-11.5-26.1-19.5-42.2-21.1c-10.3-1.4-21-0.6-31.1%2C1.9c-16.3%2C4.1-31.1%2C14.2-40.5%2C28.2%20%20%20%20c-17.6%2C25.7-15.9%2C63.1%2C4.4%2C86.8c21.4%2C25.2%2C60.5%2C32%2C89.7%2C17.4c7.5-3.6%2C13.8-9.1%2C20-14.7c5.7%2C5.6%2C11.7%2C11%2C17.2%2C16.8%20%20%20%20c-11.9%2C13.4-28.3%2C22.3-45.6%2C26.2c-28.6%2C6.6-60.2%2C2.3-84.6-14.5c-15.8-10.6-28-26.4-34.5-44.3c-6.2-17.3-7-36.2-3.6-54.1%20%20%20%20C438.9%2C156.8%2C448.5%2C139.6%2C462.3%2C126.9z%22%2F%3E %3Cg%3E %3Cpath%20class%3D%22st1%22%20d%3D%22M914.1%2C102.1c14.4-1.6%2C29.1-1.6%2C43.2%2C1.8c20.8%2C4.8%2C40%2C16.4%2C53.3%2C33.2c26%2C32.5%2C26.5%2C82.5%2C1.5%2C115.7%20%20%20%20%20c-11.3%2C15.2-27.5%2C26.4-45.4%2C32.5c-21.7%2C7.3-45.7%2C7.6-67.7%2C1.2c-21.1-6.2-40.3-19.7-52.4-38.3c-16.2-24.2-19.4-55.9-10.3-83.4%20%20%20%20%20c7.4-22.3%2C23.8-41.3%2C44.7-52C891.4%2C107.3%2C902.6%2C103.8%2C914.1%2C102.1z%20M924.1%2C125c-16.4%2C1.1-32.4%2C8-44.4%2C19.3%20%20%20%20%20c-10.1%2C9.6-17%2C22.3-19.9%2C35.8c-2.7%2C14.9-1.9%2C30.6%2C4.1%2C44.6c5.5%2C13%2C15.2%2C24.3%2C27.3%2C31.6c27.2%2C16.7%2C65.4%2C14.4%2C89.2-7.3%20%20%20%20%20c14.8-13.2%2C23.5-33.1%2C22.9-52.9c0.7-20.6-8.5-41.3-24.2-54.6C964.1%2C128.7%2C943.6%2C123.1%2C924.1%2C125z%22%2F%3E %3C%2Fg%3E %3Cg%3E %3Cpath%20class%3D%22st1%22%20d%3D%22M1349.9%2C102c21-2.5%2C43-0.7%2C62.3%2C8.5c18.5%2C8.5%2C34.2%2C23.1%2C43.5%2C41.2c9.6%2C18.3%2C12.1%2C39.7%2C9.1%2C60.1%20%20%20%20%20c-2.9%2C19.4-12.2%2C37.8-26.2%2C51.5c-14.6%2C14.1-33.8%2C23.4-53.9%2C26.3c-20.1%2C3.3-41.2%2C1.1-60.1-6.7c-17.9-7.4-33.6-20.4-43.8-37%20%20%20%20%20c-12-19.1-16-42.5-12.7-64.7c2.5-18.7%2C11.3-36.5%2C24.2-50.2C1307.5%2C115.1%2C1328.3%2C105.1%2C1349.9%2C102z%20M1364.9%2C124.6%20%20%20%20%20c-19.7%2C0.4-39.5%2C8.3-52.8%2C23.1c-11.9%2C13-18.5%2C30.8-18.1%2C48.4c-0.4%2C21.6%2C9.8%2C43.3%2C27.2%2C56.3c27.9%2C21.3%2C71.3%2C19.7%2C96.6-5%20%20%20%20%20c16.2-15.4%2C23.8-38.7%2C20.7-60.7c-1.8-18.3-11.5-35.5-25.9-46.8C1399.3%2C129.2%2C1381.9%2C124.3%2C1364.9%2C124.6z%22%2F%3E %3C%2Fg%3E %3Cpath%20class%3D%22st1%22%20d%3D%22M0%2C103.1c7.3-0.1%2C14.7%2C0%2C22%2C0c26.3%2C43.2%2C52%2C86.8%2C78.1%2C130.2c23.9-40.2%2C47.6-80.6%2C71.4-120.9%20%20%20%20c1.8-2.9%2C3.3-6.1%2C5.4-8.8c1.4-0.8%2C3.1-0.4%2C4.6-0.5c5.8%2C0.1%2C11.7-0.2%2C17.5%2C0.2c0.2%2C61.8%2C0.1%2C123.7%2C0.3%2C185.6%20%20%20%20c-8.6%2C0.1-17.3%2C0.1-25.9%2C0c0-44.9-0.2-89.8-0.2-134.7c-22.7%2C37.2-44.8%2C74.8-67.4%2C112c-3.7%2C0-7.4%2C0.1-11%2C0%20%20%20%20c-1.5%2C0.2-2.1-1.4-2.9-2.4C69.9%2C227.5%2C48.1%2C191.2%2C26%2C154.9c-0.2%2C44.6%2C0%2C89.3-0.1%2C133.9c-8.6%2C0-17.3%2C0-25.9%2C0%20%20%20%20C0%2C227%2C0%2C165.1%2C0%2C103.1z%22%2F%3E %3Cg%3E %3Cpath%20class%3D%22st1%22%20d%3D%22M309.4%2C108.4c0.9-1.7%2C1.3-3.9%2C2.9-5.2c8.6-0.3%2C17.3%2C0%2C26-0.1c6.3%2C12.5%2C11.7%2C25.5%2C17.8%2C38.2%20%20%20%20%20c22.4%2C49.2%2C45.1%2C98.3%2C67.4%2C147.5c-9.4%2C0.1-18.8%2C0-28.2%2C0c-6.8-15.5-13.7-31-20.6-46.5c-33-0.2-66.1%2C0-99.1-0.1%20%20%20%20%20c-6.9%2C15.4-13.8%2C30.9-20.6%2C46.4c-9.3%2C0.4-18.5%2C0.1-27.8%2C0.1C254.4%2C228.7%2C282%2C168.6%2C309.4%2C108.4z%20M325%2C130.5%20%20%20%20%20c-13.3%2C30.2-26.9%2C60.3-40.1%2C90.6c26.8%2C0.1%2C53.5%2C0.1%2C80.3%2C0C352%2C190.8%2C338.5%2C160.7%2C325%2C130.5z%22%2F%3E %3C%2Fg%3E %3Cg%3E %3Cpath%20class%3D%22st1%22%20d%3D%22M641.8%2C103.3c17.5-0.4%2C34.9-0.1%2C52.4-0.2c17.9%2C0.2%2C36.3-1.2%2C53.6%2C4.4c16.5%2C4.9%2C31.8%2C15.8%2C39.2%2C31.6%20%20%20%20%20c6.1%2C13.3%2C7.6%2C28.6%2C4.6%2C42.9c-2.3%2C13.4-9.7%2C25.9-20.5%2C34.2c-5.7%2C4.5-12.3%2C7.9-19.2%2C10.2c14.6%2C20.9%2C29.7%2C41.5%2C44.3%2C62.4%20%20%20%20%20c-9.7%2C0.1-19.4%2C0.1-29.1%2C0c-13.2-18.1-25.9-36.6-38.9-54.8c-0.8-0.9-1.5-2.5-3-2.2c-18.8%2C0.9-37.6%2C0.2-56.4%2C0.5%20%20%20%20%20c-0.1%2C18.9%2C0.1%2C37.7-0.1%2C56.5c-9%2C0-17.9%2C0.1-26.9-0.1C641.8%2C227%2C641.8%2C165.1%2C641.8%2C103.3z%20M668.7%2C126.4c0%2C27.7%2C0%2C55.5%2C0%2C83.2%20%20%20%20%20c12.8%2C0.1%2C25.6%2C0%2C38.4%2C0c8%2C0%2C16.1%2C0.4%2C24-1.5c12.1-2.1%2C24.4-8.5%2C30.2-19.7c4.8-8.5%2C5.2-18.6%2C4.2-28.1%20%20%20%20%20c-1.2-9.8-6.5-19.2-14.8-24.7c-10.1-7-22.7-8.9-34.7-9.4C700.3%2C126.3%2C684.5%2C125.9%2C668.7%2C126.4z%22%2F%3E %3C%2Fg%3E %3Cg%3E %3Cpath%20class%3D%22st1%22%20d%3D%22M1079.3%2C103.2c28.9-0.1%2C57.8-0.1%2C86.7%2C0c17.1%2C0.2%2C35.3%2C3.2%2C49%2C14.1c10%2C7.7%2C15.9%2C20.4%2C15.5%2C33%20%20%20%20%20c0.6%2C11.4-3.1%2C23.2-10.9%2C31.7c-3.8%2C4.4-8.6%2C7.6-13.6%2C10.6c9.5%2C2.8%2C18.5%2C7.9%2C24.7%2C15.7c10.4%2C12.9%2C12.1%2C31.3%2C7.3%2C46.8%20%20%20%20%20c-3.9%2C12.2-14.1%2C21.5-25.7%2C26.4c-16.7%2C7.2-35.3%2C7.8-53.3%2C7.5c-26.6%2C0-53.2%2C0-79.8%2C0C1079.2%2C227%2C1079.2%2C165.1%2C1079.3%2C103.2z%20%20%20%20%20%20M1106.4%2C124.6c0%2C19.8%2C0%2C39.5%2C0%2C59.3c17.5%2C0.1%2C35.1%2C0%2C52.6%2C0c9%2C0.1%2C18.2-0.5%2C26.7-3.9c6.5-2.5%2C12.5-7%2C15.5-13.5%20%20%20%20%20c3.7-8.3%2C3.5-18.5-1.1-26.5c-4.9-8.3-14.5-12.3-23.5-14.1c-6.8-1-13.7-1.6-20.5-1.4C1139.5%2C124.6%2C1122.9%2C124.5%2C1106.4%2C124.6z%20%20%20%20%20%20M1106.5%2C205.6c-0.1%2C20.5-0.1%2C41%2C0%2C61.5c22.2%2C0.2%2C44.4%2C0.1%2C66.5%2C0c9.6-0.6%2C19.7-1.9%2C28.1-7c6.5-3.7%2C11-10.7%2C11.7-18.1%20%20%20%20%20c1.3-8.8-0.2-18.7-6.7-25.2c-7.3-7.4-17.9-9.7-27.8-10.9c-8.1-0.6-16.2-0.2-24.3-0.4C1138.2%2C205.6%2C1122.3%2C205.6%2C1106.5%2C205.6z%22%2F%3E %3C%2Fg%3E %3Cpath%20class%3D%22st1%22%20d%3D%22M1506.2%2C103.2c7.4%2C0.2%2C15.1-0.7%2C22.4%2C0.4c37.5%2C45.6%2C74.4%2C91.8%2C111.9%2C137.6c0.1-46-0.1-92%2C0.1-138%20%20%20%20c8.9-0.1%2C17.9-0.1%2C26.8%2C0c0%2C61.9%2C0%2C123.7%2C0%2C185.6c-6.9%2C0.1-13.8%2C0.1-20.7%2C0c-1.4%2C0.2-2.2-1.1-3-2c-24.8-30.7-49.7-61.3-74.6-92%20%20%20%20c-12-14.6-23.6-29.5-35.8-43.9c-0.2%2C46%2C0%2C91.9-0.1%2C137.8c-9%2C0.1-18%2C0.1-27.1%2C0C1506.2%2C227%2C1506.2%2C165.1%2C1506.2%2C103.2z%22%2F%3E %3Cg%3E %3Cpath%20class%3D%22st1%22%20d%3D%22M1723.3%2C103.2c27.3-0.1%2C54.7-0.1%2C82%2C0c21.9%2C0.2%2C44%2C6.2%2C61.9%2C19.1c17.1%2C12.1%2C29.2%2C30.9%2C33.6%2C51.3%20%20%20%20%20c3.8%2C18.2%2C3.1%2C37.6-3%2C55.2c-6.8%2C19.4-20.8%2C36-38.7%2C46c-16.9%2C9.8-36.5%2C13.7-55.8%2C14.1c-26.7-0.1-53.4%2C0-80.1%2C0%20%20%20%20%20C1723.2%2C227%2C1723.1%2C165.1%2C1723.3%2C103.2z%20M1750.1%2C126.2c-0.1%2C36.9%2C0%2C73.9-0.1%2C110.8c0.2%2C9.5-0.5%2C19.1%2C0.3%2C28.6%20%20%20%20%20c13.7-0.2%2C27.3%2C0%2C41-0.1c9-0.1%2C18.2%2C0.4%2C27-1.6c18-3%2C35.5-12.5%2C46-27.7c10.7-15.2%2C13.8-34.9%2C10.9-53.1%20%20%20%20%20c-2.4-16.8-11.7-32.6-25.5-42.4c-13.9-10.2-31.4-14.3-48.4-14.6C1784.2%2C126.2%2C1767.2%2C126.1%2C1750.1%2C126.2z%22%2F%3E %3C%2Fg%3E %3C%2Fg%3E %3C%2Fg%3E %3C%2Fsvg%3E",
logo_link="https://www.macrobond.com/"


def main() -> None:
    print(doc_git_path)

    if os.path.isdir(doc_git_path):
        src_path = os.path.join(doc_git_path, "macrobond_data_api")
        git = Git(doc_git_path)

        verisons_tags = git.list_tags()
        verisons, non_verisons_tags = Verison.get_verisons(doc_git_path ,verisons_tags)
        print("non_verisons_tags:", non_verisons_tags)
        non_verisons_tags.sort()
    else:
        src_path = os.path.join(here, "..", "macrobond_data_api")
        verisons = [Verison(src_path)]

    print("verisons:", verisons)

    shutil.rmtree(output_directory)

    # build index

    for verison in verisons:

        render.configure(
            edit_url_map={
                "macrobond_data_api": "https://github.com/macrobond/macrobond-data-api/blob/main/macrobond_data_api/",
            },
            mermaid=True,
            favicon="/favicon.svg",
            logo=logo,
            logo_link="https://www.macrobond.com/",
            footer_text="Macrobond Data API for Python, " + verison.name,
            template_directory=template_directory,
        )

        pdoc(
            verison.path,
            output_directory=os.path.join(output_directory , verison.url),
        )

        if verison.is_current:
            ...
        
        if verison.is_dev:
            ...

    #if command:
    #    print("bad args " + command)
    #else:
    #    print("no args")

    #sys.exit(1)
    

if __name__ == "__main__":
    main()
