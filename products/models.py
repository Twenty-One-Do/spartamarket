from django.db import models

# Create your models here.
class Posts(models.Model):
    image = models.ImageField(upload_to="images/", blank=True)
    title = models.CharField(max_length=20)
    body = models.TextField(max_length=100)
    user_id = models.ForeignKey("accounts.UserProfile", on_delete=models.CASCADE)
    likes_num = models.PositiveIntegerField(default=0)
    views_num = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class LikeRelationship(models.Model):
    user_id = models.ForeignKey("accounts.UserProfile", on_delete=models.CASCADE, related_name="like_posts", related_query_name="like_posts")
    post_id = models.ForeignKey("Posts", on_delete=models.CASCADE, related_name="like_users", related_query_name="like_users")

class ViewRelationship(models.Model):
    user_id = models.ForeignKey("accounts.UserProfile", on_delete=models.CASCADE, related_name="view_posts", related_query_name="view_posts")
    post_id = models.ForeignKey("Posts", on_delete=models.CASCADE, related_name="view_users", related_query_name="view_users")
    created_at = models.DateTimeField(auto_now=True)
    
class TagRelationship(models.Model):
    tag_id = models.ForeignKey("Tags", on_delete=models.CASCADE, related_name="posts", related_query_name="posts")
    post_id = models.ForeignKey("Posts", on_delete=models.CASCADE, related_name="tags", related_query_name="tags")

class Tags(models.Model):
    name = models.CharField(max_length=8, unique=True)