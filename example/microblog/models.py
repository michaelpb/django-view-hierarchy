from django.db import models

# NOTE: These models are also used in unit test suite


class Author(models.Model):
    name = models.CharField(max_length=140)
    bio = models.CharField(max_length=220)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return '/posts/%s/' % self.name

    def get_django_view_hierarchy_relations(self, event):
        return {'subject': self}

    def get_django_view_hierarchy_json(self, event):
        verb = 'joined' if event.is_creation else 'updated their profile'
        return {
            'subject': self.name,
            'subject_url': self.get_absolute_url(),
            'verb': verb,
        }


class MicroPost(models.Model):
    author = models.ForeignKey(Author)
    title = models.CharField(max_length=140)
    body = models.TextField()

    def __str__(self):
        return self.title

    def get_django_view_hierarchy_relations(self, event):
        return {
            'subject': self.author,
            'object': self,
        }

    def get_absolute_url(self):
        return '/post/%s/' % str(self.id)

    def get_django_view_hierarchy_json(self, event):
        verb = 'wrote' if event.is_creation else 'updated'
        return {
            'subject': self.author.name,
            'subject_url': self.author.get_absolute_url(),
            'object': self.title,
            'object_url': self.get_absolute_url(),
            'verb': verb,
        }

    def get_django_view_hierarchy_html(self, event):
        return '<strong>%s</strong> wrote %s' % (self.author.name, self.title)


class Follow(models.Model):
    author = models.ForeignKey(Author, related_name='following')
    follower = models.ForeignKey(Author, related_name='followers')

    def __str__(self):
        return '%s -> %s' % map(str, [self.author, self.follower])

    def get_django_view_hierarchy_relations(self, event):
        return {
            'subject': self.follower,
            'object': self.author,
        }

    def get_django_view_hierarchy_json(self, event):
        return {
            'subject': self.follower.name,
            'subject_url': self.follower.get_absolute_url(),
            'object': self.author.name,
            'object_url': self.author.get_absolute_url(),
            'verb': 'followed',
        }
