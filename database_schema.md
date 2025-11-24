# PrizeTalk Database Schema

## Tables and Attributes

### users
- id (PK)
- username
- password_hash
- email
- created_at

### booker_prize
- SL. NO. (PK)
- [Other dynamic columns from CSV]

### golden_globes
- (index) (PK)
- [Other dynamic columns from CSV]

### grammy
- (index) (PK)
- [Other dynamic columns from CSV]

### nobel_laureates
- id (PK)
- [Other dynamic columns from CSV]

### nobel_prizes
- awardYear (PK, part of composite)
- category.en (PK, part of composite)
- [Other dynamic columns from CSV]

### oscars
- Ceremony (PK, part of composite)
- Category (PK, part of composite)
- [Other dynamic columns from CSV]

### award_categories
- id (PK)
- category_name
- award_name
- created_at

### community_posts
- id (PK)
- user_id (FK → users.id)
- category_id (FK → award_categories.id)
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

- award_categories (implicit one-to-many relation to prize tables via award_name matching)
- award_categories one-to-many community_posts
- users one-to-many community_posts
- users one-to-many post_comments
- community_posts one-to-many post_comments