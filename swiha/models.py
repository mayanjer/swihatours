from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)
    description = models.TextField()
    region_tagline = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "destinations_country"
        verbose_name = "Country"
        verbose_name_plural = "Countries"
        ordering = ["name"]

    def __str__(self):
        return self.name
    
 
class Destination(models.Model):
    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        related_name="destinations",
    )
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    description = models.TextField()
    short_description = models.CharField(max_length=300)
    altitude_range = models.CharField(max_length=100, blank=True, null=True)
    best_visit_months = models.CharField(max_length=100, blank=True, null=True)
    wildlife_highlight = models.CharField(max_length=200, blank=True, null=True)
    cover_image_url = models.URLField(max_length=500)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 
    class Meta:
        db_table = "destinations_destination"
        verbose_name = "Destination"
        verbose_name_plural = "Destinations"
        ordering = ["display_order", "name"]
 
    def __str__(self):
        return f"{self.name} ({self.country.name})"
 
  
class TourCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)
    description = models.TextField(blank=True, null=True)
    display_order = models.PositiveSmallIntegerField(default=0)
 
    class Meta:
        db_table = "tours_category"
        verbose_name = "Tour Category"
        verbose_name_plural = "Tour Categories"
        ordering = ["display_order", "name"]
 
    def __str__(self):
        return self.name
    
class TourPackage(models.Model):
    DIFFICULTY_EASY = "easy"
    DIFFICULTY_MODERATE = "moderate"
    DIFFICULTY_CHALLENGING = "challenging"
    DIFFICULTY_CHOICES = [
        (DIFFICULTY_EASY, "Easy"),
        (DIFFICULTY_MODERATE, "Moderate"),
        (DIFFICULTY_CHALLENGING, "Challenging"),
    ]
 
    category = models.ForeignKey(
        TourCategory,
        on_delete=models.PROTECT,
        related_name="packages",
    )
    destination = models.ForeignKey(
        Destination,
        on_delete=models.PROTECT,
        related_name="packages",
    )
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=280, unique=True)
    short_description = models.CharField(max_length=400)
    full_description = models.TextField()
    duration_days = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    min_group_size = models.PositiveSmallIntegerField(default=1)
    max_group_size = models.PositiveSmallIntegerField()
    price_per_person = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    difficulty = models.CharField(
        max_length=20,
        choices=DIFFICULTY_CHOICES,
        default=DIFFICULTY_EASY,
    )
    cover_image_url = models.URLField(max_length=500)
    badge_label = models.CharField(max_length=50, blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    gorilla_permit_included = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 
    class Meta:
        db_table = "tours_package"
        verbose_name = "Tour Package"
        verbose_name_plural = "Tour Packages"
        ordering = ["-is_featured", "price_per_person"]
 
    def __str__(self):
        return self.title
    
class PackageHighlight(models.Model):
    package = models.ForeignKey(
        TourPackage,
        on_delete=models.CASCADE,
        related_name="highlights",
    )
    highlight_text = models.CharField(max_length=200)
    display_order = models.PositiveSmallIntegerField(default=0)
 
    class Meta:
        db_table = "tours_package_highlight"
        verbose_name = "Package Highlight"
        verbose_name_plural = "Package Highlights"
        ordering = ["display_order"]
 
    def __str__(self):
        return f"{self.package.title} — {self.highlight_text}"

    
class PackageItineraryDay(models.Model):
    package = models.ForeignKey(
        TourPackage,
        on_delete=models.CASCADE,
        related_name="itinerary_days",
    )
    day_number = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    title = models.CharField(max_length=200)
    description = models.TextField()
    accommodation = models.CharField(max_length=200, blank=True, null=True)
    meals_included = models.CharField(max_length=50, blank=True, null=True)
 
    class Meta:
        db_table = "tours_itinerary_day"
        verbose_name = "Itinerary Day"
        verbose_name_plural = "Itinerary Days"
        unique_together = [("package", "day_number")]
        ordering = ["package", "day_number"]
 
    def __str__(self):
        return f"{self.package.title} — Day {self.day_number}: {self.title}"
    
    
class PackageAddOn(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.CharField(max_length=400, blank=True, null=True)
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    price_is_per_person = models.BooleanField(default=False)
    price_is_per_day = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
 
    class Meta:
        db_table = "tours_package_addon"
        verbose_name = "Package Add-On"
        verbose_name_plural = "Package Add-Ons"
        ordering = ["name"]
 
    def __str__(self):
        return f"{self.name} (+${self.price})"
    
 
class TeamMember(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    other_name = models.CharField(max_length = 150, null = True, blank = True)
    role = models.CharField(max_length=150)
    bio = models.TextField()
    photo_url = models.URLField(max_length=500, blank=True, null=True)
    languages_spoken = models.CharField(max_length=200, blank=True, null=True)
    years_experience = models.PositiveSmallIntegerField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveSmallIntegerField(default=0)
 
    class Meta:
        db_table = "team_member"
        verbose_name = "Team Member"
        verbose_name_plural = "Team Members"
        ordering = ["display_order", "first_name", "last_name"]
 
    def __str__(self):
        return f"{self.full_name} — {self.role}"
    
class Booking(models.Model):
    STATUS_PENDING = "pending"
    STATUS_CONFIRMED = "confirmed"
    STATUS_CANCELLED = "cancelled"
    STATUS_COMPLETED = "completed"
    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_CONFIRMED, "Confirmed"),
        (STATUS_CANCELLED, "Cancelled"),
        (STATUS_COMPLETED, "Completed"),
    ]

    ACCOM_BUDGET = "budget"
    ACCOM_MID = "mid_range"
    ACCOM_LUXURY = "luxury"
    ACCOM_MIX = "mix"
    ACCOM_CHOICES = [
        (ACCOM_BUDGET, "Budget (Guesthouses & budget lodges)"),
        (ACCOM_MID, "Mid-range (Comfortable lodges)"),
        (ACCOM_LUXURY, "Luxury (Premium safari lodges & camps)"),
        (ACCOM_MIX, "Mix (Some budget, some mid-range)"),
    ]

    PAY_OPT_DEPOSIT = "deposit"
    PAY_OPT_FULL = "full"
    PAY_OPTION_CHOICES = [
        (PAY_OPT_DEPOSIT, "30% Deposit Now"),
        (PAY_OPT_FULL, "Pay in Full"),
    ]

    PAY_METHOD_BANK = "bank_transfer"
    PAY_METHOD_CARD = "card"
    PAY_METHOD_PAYPAL = "paypal"
    PAY_METHOD_MOBILE = "mobile_money"
    PAY_METHOD_DISCUSS = "discuss"
    PAY_METHOD_CHOICES = [
        (PAY_METHOD_BANK, "Bank Transfer (Wire)"),
        (PAY_METHOD_CARD, "Credit / Debit Card (Visa, Mastercard)"),
        (PAY_METHOD_PAYPAL, "PayPal"),
        (PAY_METHOD_MOBILE, "Mobile Money (MTN / Airtel)"),
        (PAY_METHOD_DISCUSS, "Discuss with team"),
    ]

    reference_number = models.CharField(max_length=20, unique=True)
    package = models.ForeignKey(
        TourPackage,
        on_delete=models.PROTECT,
        related_name="bookings",
    )
    travel_start_date = models.DateField()
    num_travellers = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    accommodation_preference = models.CharField(
        max_length=20,
        choices=ACCOM_CHOICES,
        default=ACCOM_MID,
    )
    lead_first_name = models.CharField(max_length=100)
    lead_last_name = models.CharField(max_length=100)
    lead_email = models.EmailField(max_length=254)
    lead_phone = models.CharField(max_length=30)
    lead_nationality = models.CharField(max_length=100, blank=True, null=True)
    lead_country_of_residence = models.CharField(max_length=100, blank=True, null=True)
    special_requirements = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default=STATUS_PENDING)
    payment_option = models.CharField(
        max_length=20,
        choices=PAY_OPTION_CHOICES,
        default=PAY_OPT_DEPOSIT,
    )
    preferred_payment_method = models.CharField(
        max_length=30,
        choices=PAY_METHOD_CHOICES,
        blank=True,
        null=True,
    )
    tour_subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    addons_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2)
    deposit_amount = models.DecimalField(max_digits=10, decimal_places=2)
    terms_accepted = models.BooleanField(default=False)
    internal_notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    confirmed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "bookings_booking"
        verbose_name = "Booking"
        verbose_name_plural = "Bookings"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.reference_number} — {self.lead_first_name} {self.lead_last_name}"

    def lead_full_name(self):
        return f"{self.lead_first_name} {self.lead_last_name}"
    
class BookingTraveller(models.Model):
    booking = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE,
        related_name="travellers",
    )
    full_name = models.CharField(max_length=200)
    date_of_birth = models.DateField(blank=True, null=True)
    passport_number = models.CharField(max_length=50, blank=True, null=True)
    passport_expiry = models.DateField(blank=True, null=True)
    nationality = models.CharField(max_length=100, blank=True, null=True)
    is_lead = models.BooleanField(default=False)
 
    class Meta:
        db_table = "bookings_traveller"
        verbose_name = "Booking Traveller"
        verbose_name_plural = "Booking Travellers"
 
    def __str__(self):
        lead = " (Lead)" if self.is_lead else ""
        return f"{self.full_name}{lead} — {self.booking.reference_number}"
        
 
class BookingAddOn(models.Model):
    booking = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE,
        related_name="selected_addons",
    )
    addon = models.ForeignKey(
        PackageAddOn,
        on_delete=models.PROTECT,
        related_name="booking_selections",
    )
    quantity = models.PositiveSmallIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
    )
    price_at_booking_usd = models.DecimalField(max_digits=8, decimal_places=2)
 
    class Meta:
        db_table = "bookings_addon"
        verbose_name = "Booking Add-On"
        verbose_name_plural = "Booking Add-Ons"
        unique_together = [("booking", "addon")]
 
    def __str__(self):
        return f"{self.booking.reference_number} — {self.addon.name} x{self.quantity}"

class Payment(models.Model):
    TYPE_DEPOSIT = "deposit"
    TYPE_BALANCE = "balance"
    TYPE_FULL = "full"
    TYPE_REFUND = "refund"
    PAYMENT_TYPE_CHOICES = [
        (TYPE_DEPOSIT, "Deposit"),
        (TYPE_BALANCE, "Balance"),
        (TYPE_FULL, "Full Payment"),
        (TYPE_REFUND, "Refund"),
    ]

    METHOD_BANK = "bank_transfer"
    METHOD_CARD = "card"
    METHOD_PAYPAL = "paypal"
    METHOD_MOBILE = "mobile_money"
    METHOD_CHOICES = [
        (METHOD_BANK, "Bank Transfer"),
        (METHOD_CARD, "Credit / Debit Card"),
        (METHOD_PAYPAL, "PayPal"),
        (METHOD_MOBILE, "Mobile Money"),
    ]

    PAY_STATUS_PENDING = "pending"
    PAY_STATUS_COMPLETED = "completed"
    PAY_STATUS_FAILED = "failed"
    PAY_STATUS_REFUNDED = "refunded"
    PAY_STATUS_CHOICES = [
        (PAY_STATUS_PENDING, "Pending"),
        (PAY_STATUS_COMPLETED, "Completed"),
        (PAY_STATUS_FAILED, "Failed"),
        (PAY_STATUS_REFUNDED, "Refunded"),
    ]

    booking = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE,
        related_name="payments",
    )
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPE_CHOICES)
    method = models.CharField(max_length=30, choices=METHOD_CHOICES)
    amount_usd = models.DecimalField(max_digits=10, decimal_places=2)
    currency_paid = models.CharField(max_length=10, default="USD")
    exchange_rate = models.DecimalField(
        max_digits=10, decimal_places=6, blank=True, null=True
    )
    transaction_reference = models.CharField(max_length=200, blank=True, null=True)
    status = models.CharField(
        max_length=20, choices=PAY_STATUS_CHOICES, default=PAY_STATUS_PENDING
    )
    paid_at = models.DateTimeField(blank=True, null=True)
    recorded_by = models.CharField(max_length=150, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "bookings_payment"
        verbose_name = "Payment"
        verbose_name_plural = "Payments"
        ordering = ["-created_at"]

    def __str__(self):
        return (
            f"{self.booking.reference_number} — {self.get_payment_type_display()} "
            f"${self.amount_usd} ({self.get_status_display()})"
        )
        
 
class BlogCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)
    display_order = models.PositiveSmallIntegerField(default=0)
 
    class Meta:
        db_table = "blog_category"
        verbose_name = "Blog Category"
        verbose_name_plural = "Blog Categories"
        ordering = ["display_order", "name"]
 
    def __str__(self):
        return self.name
    
 
class BlogTag(models.Model):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
 
    class Meta:
        db_table = "blog_tag"
        verbose_name = "Blog Tag"
        verbose_name_plural = "Blog Tags"
        ordering = ["name"]
 
    def __str__(self):
        return self.name

class BlogPost(models.Model):
    category = models.ForeignKey(
        BlogCategory,
        on_delete=models.PROTECT,
        related_name="posts",
    )
    author = models.ForeignKey(
        TeamMember,
        on_delete=models.PROTECT,
        related_name="blog_posts",
    )
    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=320, unique=True)
    excerpt = models.CharField(max_length=400)
    body = models.TextField()
    cover_image_url = models.URLField(max_length=500)
    read_time_minutes = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)
    published_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "blog_post"
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"
        ordering = ["-published_at"]

    def __str__(self):
        return self.title

class BlogPost(models.Model):
    category = models.ForeignKey(
        BlogCategory,
        on_delete=models.PROTECT,
        related_name="posts",
    )
    author = models.ForeignKey(
        TeamMember,
        on_delete=models.PROTECT,
        related_name="blog_posts",
    )
    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=320, unique=True)
    excerpt = models.CharField(max_length=400)
    body = models.TextField()
    cover_image_url = models.URLField(max_length=500)
    read_time_minutes = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)
    published_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "blog_post"
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"
        ordering = ["-published_at"]

    def __str__(self):
        return self.title
    

 
class GalleryCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)
    display_order = models.PositiveSmallIntegerField(default=0)
 
    class Meta:
        db_table = "gallery_category"
        verbose_name = "Gallery Category"
        verbose_name_plural = "Gallery Categories"
        ordering = ["display_order", "name"]
 
    def __str__(self):
        return self.name


class GalleryPhoto(models.Model):
    SOURCE_STAFF = "staff"
    SOURCE_TRAVELLER = "traveller"
    SOURCE_INSTAGRAM = "instagram"
    SOURCE_CHOICES = [
        (SOURCE_STAFF, "Staff"),
        (SOURCE_TRAVELLER, "Traveller"),
        (SOURCE_INSTAGRAM, "Instagram"),
    ]

    category = models.ForeignKey(
        GalleryCategory,
        on_delete=models.PROTECT,
        related_name="photos",
    )
    destination = models.ForeignKey(
        Destination,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="gallery_photos",
    )
    package = models.ForeignKey(
        TourPackage,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="gallery_photos",
    )
    image_url = models.URLField(max_length=500)
    thumbnail_url = models.URLField(max_length=500, blank=True, null=True)
    caption = models.CharField(max_length=300, blank=True, null=True)
    alt_text = models.CharField(max_length=200)
    photographer_credit = models.CharField(max_length=150, blank=True, null=True)
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES, default=SOURCE_STAFF)
    instagram_handle = models.CharField(max_length=100, blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveSmallIntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "gallery_photo"
        verbose_name = "Gallery Photo"
        verbose_name_plural = "Gallery Photos"
        ordering = ["display_order", "-uploaded_at"]

    def __str__(self):
        return self.alt_text or f"Photo {self.id}"


class Review(models.Model):
    SOURCE_DIRECT = "direct"
    SOURCE_TRIPADVISOR = "tripadvisor"
    SOURCE_GOOGLE = "google"
    SOURCE_MANUAL = "manual"
    SOURCE_CHOICES = [
        (SOURCE_DIRECT, "Direct (website form)"),
        (SOURCE_TRIPADVISOR, "TripAdvisor"),
        (SOURCE_GOOGLE, "Google"),
        (SOURCE_MANUAL, "Manually added by staff"),
    ]

    package = models.ForeignKey(
        TourPackage,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="reviews",
    )
    booking = models.OneToOneField(
        Booking,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="review",
    )
    reviewer_name = models.CharField(max_length=150)
    reviewer_country = models.CharField(max_length=100, blank=True, null=True)
    reviewer_country_flag = models.CharField(max_length=10, blank=True, null=True)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    review_text = models.TextField()
    source = models.CharField(max_length=30, choices=SOURCE_CHOICES, default=SOURCE_DIRECT)
    is_featured = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "reviews_review"
        verbose_name = "Review"
        verbose_name_plural = "Reviews"
        ordering = ["-submitted_at"]

    def __str__(self):
        return f"{self.reviewer_name} — {'★' * self.rating} ({self.get_source_display()})"
    

class ContactEnquiry(models.Model):
    STATUS_NEW = "new"
    STATUS_IN_PROGRESS = "in_progress"
    STATUS_REPLIED = "replied"
    STATUS_CLOSED = "closed"
    STATUS_CHOICES = [
        (STATUS_NEW, "New"),
        (STATUS_IN_PROGRESS, "In Progress"),
        (STATUS_REPLIED, "Replied"),
        (STATUS_CLOSED, "Closed"),
    ]

    TOUR_TYPE_CHOICES = [
        ("gorilla_trekking", "Gorilla Trekking"),
        ("wildlife_safari", "Wildlife Safari"),
        ("chimpanzee_tracking", "Chimpanzee Tracking"),
        ("bird_watching", "Bird Watching"),
        ("cultural_tour", "Cultural Tour"),
        ("adventure_jinja", "Adventure / Jinja"),
        ("honeymoon_package", "Honeymoon Package"),
        ("custom_itinerary", "Custom Itinerary"),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=30, blank=True, null=True)
    tour_type_interest = models.CharField(
        max_length=50, choices=TOUR_TYPE_CHOICES, blank=True, null=True
    )
    num_travellers = models.CharField(max_length=20, blank=True, null=True)
    preferred_travel_dates = models.CharField(max_length=100, blank=True, null=True)
    approximate_budget = models.CharField(max_length=50, blank=True, null=True)
    message = models.TextField()
    privacy_consent = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_NEW)
    assigned_to = models.ForeignKey(
        TeamMember,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="assigned_enquiries",
    )
    internal_notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    replied_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "contacts_enquiry"
        verbose_name = "Contact Enquiry"
        verbose_name_plural = "Contact Enquiries"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.first_name} {self.last_name} <{self.email}> [{self.get_status_display()}]"


class NewsletterSubscriber(models.Model):
    email = models.EmailField(max_length=254, unique=True)
    source_page = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    unsubscribed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "newsletter_subscriber"
        verbose_name = "Newsletter Subscriber"
        verbose_name_plural = "Newsletter Subscribers"
        ordering = ["-subscribed_at"]

    def __str__(self):
        status = "active" if self.is_active else "unsubscribed"
        return f"{self.email} ({status})"

class FAQ(models.Model):
    question = models.CharField(max_length=300)
    answer = models.TextField()
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        db_table = "core_faq"
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"
        ordering = ["display_order"]

    def __str__(self):
        return self.question

class Certification(models.Model):
    name = models.CharField(max_length=150, unique=True)
    description = models.CharField(max_length=300, blank=True, null=True)
    logo_url = models.URLField(max_length=500, blank=True, null=True)
    registration_number = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        db_table = "core_certification"
        verbose_name = "Certification"
        verbose_name_plural = "Certifications"
        ordering = ["display_order"]

    def __str__(self):
        return self.name