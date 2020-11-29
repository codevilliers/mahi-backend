from django.contrib import admin

from mahi_app.models import BankDetails, Tags, Cause, Volunteer, Activity, Suggestion, Donation, Media

admin.site.register(BankDetails)
admin.site.register(Tags)
admin.site.register(Cause)
admin.site.register(Volunteer)
admin.site.register(Activity)
admin.site.register(Suggestion)
admin.site.register(Donation)
admin.site.register(Media)
