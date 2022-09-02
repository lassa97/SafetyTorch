from worker import Worker

with open('categories.txt', 'r') as file:
    categories = file.readlines()
    categories = [category.replace('\n', '') for category in categories]

Worker.get_lists('../lists.txt')
Worker.filter_lists(categories)
Worker.categorise_lists(categories)