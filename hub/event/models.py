from django.db import models

#class:command;protocol:arctech;model:selflearning;house:2887766;unit:1;group:0;method:turnon;
#class:command;protocol:sartano;model:codeswitch;code:1111011001;method:turnoff;


# a specific sender
class Sender(models.Model):
    house = models.CharField(max_length=256, blank=True, null=True, default=None)
    unit = models.CharField(max_length=256, blank=True, null=True, default=None)
    code = models.CharField(max_length=256, blank=True, null=True, default=None)

    created = models.DateTimeField(auto_now_add=True)

    last_signal_received = models.DateTimeField(null=True, blank=True, default=None)

    def get_unit(self):
        try:
            return self.units.all()[0]
        except Exception:
            return None

    def __str__(self):
        return 'house: {sender.house}, unit: {sender.unit}, code: {sender.code}, last signal: {sender.last_signal_received}'.format(
            sender=self
        )


# The signal, every signal event that comes through the tellstick is recorded here!
class Signal(models.Model):
    created = models.DateTimeField(auto_now_add=True)

    raw_command = models.TextField()

    protocol = models.CharField(max_length=256, blank=True, null=True, default=None)
    house = models.CharField(max_length=256, blank=True, null=True, default=None)
    unit = models.CharField(max_length=256, blank=True, null=True, default=None)
    model = models.CharField(max_length=256, blank=True, null=True, default=None)
    code = models.CharField(max_length=256, blank=True, null=True, default=None)
    group = models.CharField(max_length=256, blank=True, null=True, default=None)
    method = models.CharField(max_length=256, blank=True, null=True, default=None)
    event_class = models.CharField(max_length=256, blank=True, null=True, default=None)
    humidity = models.CharField(max_length=256, blank=True, null=True, default=None)
    temp = models.CharField(max_length=256, blank=True, null=True, default=None)

    sender = models.ForeignKey(Sender, null=True, blank=True, default=None)

    def get_unit(self):
        return self.sender.get_unit()

    def propagate(self):
        pass
