from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class LoanApplicant(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    income = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])

    def __str__(self):
        return self.name


class Loan(models.Model):
    LOAN_TYPES = [
        ('Home', 'Home Loan'),
        ('Auto', 'Auto Loan'),
        ('Personal', 'Personal Loan'),
        ('Education', 'Education Loan')
    ]
    
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected')
    ]

    applicant = models.ForeignKey(LoanApplicant, on_delete=models.CASCADE, related_name="loans")
    loan_amount = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    loan_type = models.CharField(max_length=50, choices=LOAN_TYPES, default='Personal')
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(100)])
    duration_months = models.IntegerField(validators=[MinValueValidator(1)])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    application_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.applicant.name} - {self.get_loan_type_display()} Loan"


class Payment(models.Model):
    PAYMENT_METHODS = [
        ('Bank Transfer', 'Bank Transfer'),
        ('Cash', 'Cash'),
        ('Credit Card', 'Credit Card'),
        ('Debit Card', 'Debit Card')
    ]
    
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name="payments")
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    payment_date = models.DateField(auto_now_add=True)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHODS)

    def __str__(self):
        return f"Payment of {self.amount_paid} for {self.loan}"


class Guarantor(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name="guarantors")
    name = models.CharField(max_length=100)
    relationship = models.CharField(max_length=50)
    contact_info = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} - Guarantor for {self.loan}"
