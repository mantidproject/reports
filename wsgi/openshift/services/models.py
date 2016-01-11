from django.db import models

# Create your models here.
class Message(models.Model):
  author = models.CharField(max_length=20)
  text = models.CharField(max_length=140)
  timestamp = models.DateTimeField(auto_now_add=True)

  def __unicode__(self):
      return self.author

class Usage(models.Model):
    uid = models.CharField(max_length=32, help_text="md5 version of username")           # md5 ex: "c5a9b601408709f47417bcba3571262b"
    host = models.CharField(max_length=32, help_text="md5 version of hostname")          # md5 ex: "7defb184ceadab4e79eff323359ad373"
    dateTime = models.DateTimeField(db_index=True)               # ex: "2014-12-08T18:50:35.817942000"
    osName = models.CharField(max_length=32)        # ex: "Linux"
    osArch = models.CharField(max_length=16)        # ex: "x86_64"
    osVersion = models.CharField(max_length=32)     # ex: "3.17.4-200.fc20.x86_64"
    ParaView = models.CharField(max_length=16)      # ex: "3.98.1"
    mantidVersion = models.CharField(max_length=32) # ex: "3.2.20141208.1820"
    mantidSha1 = models.CharField(max_length=40, help_text="sha1 for specific mantid version")    # sha1 ex: "e9423bdb34b07213a69caa90913e40307c17c6cc"
    osReadable = models.CharField(max_length=80, default="", blank=True) # ex: "Fedora 20 (Heisenbug)"
    application = models.CharField(max_length=80, default="", blank=True)
    component = models.CharField(max_length=80, default="", blank=True)

class FeatureUsage(models.Model):
    type = models.CharField(max_length=32, help_text="Algorithm,Interface, Feature")          # type ex: "Algorithm,Interface, Feature"
    name = models.CharField(max_length=80)        # ex: "Rebin.v2"
    internal = models.BooleanField(default=False)    # ex: "False"
    count = models.IntegerField()        # ex: "3"
    mantidVersion = models.CharField(max_length=32)  # ex: "3.2.20141208.1820"

    class Meta:
        unique_together = ('mantidVersion','type','name','internal')
