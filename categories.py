from typing import Dict, List, NamedTuple

import db


class Category(NamedTuple):
    """Category structure"""
    codename: str
    name: str
    is_base_expense: bool
    aliases: List[str]


class Categories:
    """Class that manages all categories"""
    def __init__(self):
        self._categories = self._load_categories()

    def _load_categories(self):
        """Returns """
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
        """Returns category by it's aliase"""
        found = None
        other_category = None
        for category in self._categories:
            if category.codename == "other":
                other_category = category
            for alias in category.aliases:
                if category_name == alias:
                    found = category
        if not found:
            found = other_category
        return found

