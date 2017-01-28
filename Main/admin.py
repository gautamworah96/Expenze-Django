from django.contrib import admin

# Register your models here.
from Main.models import Expense,LoanPremium,Balance,UserDetails
admin.site.register(Expense)
admin.site.register(Balance)
admin.site.register(LoanPremium)
admin.site.register(UserDetails)
