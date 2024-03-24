from typing import List, Tuple, Optional

class Verison:

    @property
    def name(self):
        if self.is_dev:
            return "dev"    
        verison_str = ".".join(str(x) for x in self.verison)
        if self.is_current:
           return "current v" + verison_str
        return "v"+ verison_str
    
    def __init__(self, tag:str = None) -> None:
        self.tag: Optional[str] = tag
        self.is_dev = tag is None
        if self.is_dev:
            self.verison: Tuple[int,int,int] = (999,999,999)
        else:
            self.verison = tuple(int(x) for x in tag.lower().replace("v","").split("."))
        self.is_current = False

    @classmethod
    def get_verisons(cls, tags: List[str]) -> Tuple[List["Verison"], List[str]]:
        def is_verison(tag:str) -> bool:
            tag = tag.lower()
            return tag.count(".") == 3 and tag[0].isnumeric() or (tag[0] == "v" and tag[1].isnumeric())
        verisons = list(Verison(x) for x in tags if is_verison(x))
        verisons.sort()
        verisons[-1].is_current = True;
        verisons.append(Verison())

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
