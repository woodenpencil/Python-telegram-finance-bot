from typing import Dict, List, NamedTuple

import db


class Category(NamedTuple):
    """Category structure"""
    codename: str
    name: str
    is_base_expense: bool
    aliases: List[str]


Other_cat = Category("other", "other", True, [])


class Categories:
    """Class that manages all categories"""
    categories: List[Category]

    def __init__(self):
        self.categories = self._load_categories()

    def _load_categories(self) -> List[Category]:
        """Retrieves categories from db, calls _fill_aliases"""
        categories = db.fetch_all("category",
                                  list(filter(lambda att: not att.startswith("_"), Category.__dict__.keys())))
        categories = self._fill_aliases(categories)
        return categories

    def _fill_aliases(self, categories: List[Dict]) -> List[Category]:
        """Deals with aliases"""
        categories_result = []
        for index, category in enumerate(categories):
            aliases = category["aliases"].split(",")
            aliases = list(filter(None, map(str.strip, aliases)))
            aliases.append(category["codename"])
            aliases.append(category["name"])
            categories_result.append(Category(
                codename=category['codename'],
                name=category['name'],
                is_base_expense=category['is_base_expense'],
                aliases=aliases
            ))
        return categories_result

    def get_category(self, category_name: str) -> Category:
        """Returns category by it's alias"""
        found = None
        other_category = Other_cat
        for category in self.categories:
            if category.codename == "other":
                other_category = category
            for alias in category.aliases:
                if category_name == alias:
                    found = category
        if not found:
            found = other_category
        return found

    def get_all_categories(self) -> List[Category]:
        """Returns list of categories"""
        return self.categories
