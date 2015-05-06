from tmate.models import *

hashtags = ["HTML&CSS", "User Experience Design", "Photoshop", "Illustrator", "InDesign", ]

for h in hashtags:
    ht = HashTag(content=h)
    ht.save()

