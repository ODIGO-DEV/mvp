# Favorites Feature Migration

## New Database Table

A new `favorites` table has been created to store user favorite recipes.

## Run Migration

To apply the database changes, run:

```bash
flask db migrate -m "Add favorites table"
flask db upgrade
```

Or with alembic directly:

```bash
alembic revision --autogenerate -m "Add favorites table"
alembic upgrade head
```

## Features Implemented

1. **Favorite Model** - Many-to-many relationship between users and recipes
2. **Favorites Blueprint** - Routes for viewing and managing favorites
3. **Favorites Page** - Beautiful UI to display all favorited recipes
4. **Toggle Favorite API** - AJAX endpoint to add/remove favorites
5. **Sidebar Link** - Quick access to favorites from the dashboard
6. **Recipe Detail Integration** - Heart button to favorite/unfavorite recipes

## Usage

- Click the heart icon on any recipe detail page to add/remove from favorites
- Access your favorites from the sidebar under "Recipes > Favorites"
- Filter and search your favorite recipes
- View your favorite count and collection
