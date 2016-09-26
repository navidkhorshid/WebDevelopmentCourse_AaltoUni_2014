from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum
from datetime import datetime, timedelta


class Player(models.Model):
    user = models.OneToOneField(User, related_name='players')

    def __str__(self):
            return "{}-{}".format(self.id, self.user.username)


class Developer(models.Model):
    user = models.OneToOneField(User, related_name='developers')

    def __str__(self):
            return "{}-{}".format(self.id, self.user.username)


class Game(models.Model):
    title = models.CharField(max_length=100, unique=True)
    picture_url = models.URLField(max_length=200, null=True, blank=True)
    game_url = models.URLField(max_length=200)
    price = models.FloatField(default=0)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey('Category', related_name='games')
    developer = models.ForeignKey('Developer', related_name='games')

    def __str__(self):
            return "{}-{}".format(self.id, self.title)

    def calculate_invoices(self):
            return Player_Game.objects.filter(game=self).count()

    invoices = property(calculate_invoices)

    def calculate_total_sell(self):  # total sell of a game
        if Player_Game.objects.filter(game=self).first() is None:
            return 0;
        else:
            return Player_Game.objects.filter(game=self).aggregate(Sum('purchasePrice'))

    total_sell = property(calculate_total_sell)

    # This was for SALES charts but MATPLOTLIB was too heavy for heroku and I omitted this part
    #def calculate_total_sell_in_month(self):  # for the chart of last 30 days sales
    #    init_date = datetime(datetime.now()-timedelta(days=30))
    #    y = ""
    #    for i in range(30):
    #        pg = Player_Game.objects.filter(game=self, purchaseTime=init_date)  # sales for the last 30 days
    #        if pg.first() is not None:
    #            y = str(pg.aggregate(Sum('purchasePrice'))) + ","
    #        else:
    #            y = str(0) + ","
    #        init_date = datetime(init_date+timedelta(days=1))
    #    return y

    #total_sell_in_month = property(calculate_total_sell_in_month)


class Player_Game(models.Model):
    player = models.ForeignKey('Player', related_name='player_games')
    game = models.ForeignKey('Game', related_name='player_games')
    score = models.FloatField(null=True, blank=True, default=0)
    playerItems = models.TextField(null=True, blank=True)
    purchaseTime = models.DateTimeField(auto_now_add=True, blank=True)
    purchasePrice = models.FloatField(default=0)


    class Meta:
        ordering = ["-score"]  # ordering = ["purchaseTime"] remember to change sth in dev statistics


class Category(models.Model):
    title = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return "{}".format(self.title)


# needed for sending activation key
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    activation_key = models.CharField(max_length=40, blank=True)
    key_expires = models.DateTimeField(default=datetime.today() + timedelta(1))


    class Meta:
        verbose_name_plural=u'User profiles'