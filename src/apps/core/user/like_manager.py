class LikeManager:
    def __init__(self, liked_list):
        self.liked_list = liked_list

    def like(self, instance):
        self.liked_list.add(instance)

    def remove_like(self, instance):
        self.liked_list.remove(instance)

    def has_liked(self, instance):
        return self.liked_list.filter(pk=instance.pk).exists()
