from django.contrib import admin

from mahi_app.models import Tag, Cause, Volunteer, Activity, Suggestion, Donation, Media, BenchmarkMedia

admin.site.register(Tag)
admin.site.register(Cause)
admin.site.register(Volunteer)
admin.site.register(Activity)
admin.site.register(Suggestion)
admin.site.register(Donation)
admin.site.register(Media)
admin.site.register(BenchmarkMedia)
