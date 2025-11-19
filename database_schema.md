# PrizeTalk Database Schema

## Tables and Attributes

### users
- id (PK)
- username
- password_hash
- email
- created_at

### booker_prize
- [Dynamic columns from CSV]

### golden_globes
- [Dynamic columns from CSV]

### grammy
- [Dynamic columns from CSV]

### nobel_laureates
- [Dynamic columns from CSV]

### nobel_prizes
- [Dynamic columns from CSV]

### oscars
- [Dynamic columns from CSV]

### award_categories
- id (PK)
- category_name
- award_name
- created_at

### community_posts
- id (PK)
- user_id (FK → users.id)
- title
- content
- created_at
- updated_at

### post_comments
- id (PK)
- post_id (FK → community_posts.id)
- user_id (FK → users.id)
- comment_text
- created_at

## Relationships

- users one-to-many community_posts
- users one-to-many post_comments
- community_posts one-to-many post_comments