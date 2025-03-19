from django.db import models
from wagtail.models import Page
from wagtail.fields import StreamField, RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail.blocks import CharBlock, TextBlock, StructBlock
from wagtail.snippets.models import register_snippet
from modelcluster.fields import ParentalManyToManyField
from wagtail_localize.models import TranslatableMixin
from wagtail_localize.fields import TranslatableField
# Testimonial Snippet (for reusable testimonials)
@register_snippet
class Testimonial(models.Model):
    name = models.CharField(max_length=255)
    quote = models.TextField()

    panels = [
        FieldPanel("name"),
        FieldPanel("quote"),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"


# Language Model
@register_snippet
class Language(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Language"
        verbose_name_plural = "Languages"


# Program Model
@register_snippet
class Program(models.Model):
    name = models.CharField(max_length=100, unique=True)
    language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='programs')

    def __str__(self):
        return f"{self.name} ({self.language.name})"

    class Meta:
        verbose_name = "Program"
        verbose_name_plural = "Programs"


class BlogPage( Page, TranslatableMixin):
    banner_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    introduction = RichTextField(blank=True)

    # Content panels for Wagtail admin
    content_panels = Page.content_panels + [
        FieldPanel('banner_image'),
        FieldPanel('introduction'),
    ]

    # Method to get all CoursePage instances
    def get_events(self):
        return EventPage.objects.live().public().order_by('-first_published_at')

    # Register for translation
    translatable_fields = [
       
       TranslatableField("introduction"),
    ]



class EventPage(Page):
    # Hero Section
    hero_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    hero_title = models.CharField(max_length=255, blank=True)
    
    # Event Overview
    event_date = models.DateField()
    event_overview = RichTextField(blank=True)
    
    # Dynamic Sections
    sections = StreamField(
        [
            ("sections", StructBlock([
                ("image", ImageChooserBlock(required=True)),
                ("title", CharBlock(required=True)),
                ("text", TextBlock(required=True)),
            ]))
        ],
        use_json_field=True,
        blank=True,
        help_text="Add as many sections as you want",
    )
    # Testimonials
    testimonials = StreamField(
        [
            ("testimonials", StructBlock([
          
                ("user", CharBlock(required=True)),
                ("quote", TextBlock(required=True)),
            ]))
        ],
        use_json_field=True,
        blank=True,
        help_text="Add as many testimonials as you want",
    )

    # Panels for Wagtail Admin
    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel('hero_image'),
                FieldPanel('hero_title'),
            ],
            heading="Hero Section"
        ),
        MultiFieldPanel(
            [
                FieldPanel('event_date'),
                FieldPanel('event_overview'),
            ],
            heading="Event Overview"
        ),
        FieldPanel('sections'),
        FieldPanel('testimonials'),
    ]

# Target Learner Choices
TARGET_LEARNER_CHOICES = [
    ('students', 'Students'),
    ('teachers', 'Teachers'),
]

class CoursesPage( Page, TranslatableMixin):
    banner_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    introduction = RichTextField(blank=True)

    # Content panels for Wagtail admin
    content_panels = Page.content_panels + [
        FieldPanel('banner_image'),
        FieldPanel('introduction'),
    ]

    # Method to get all CoursePage instances
    def get_courses(self):
        return CoursePage.objects.live().public().order_by('-first_published_at')

    # Register for translation
    translatable_fields = [
       
       TranslatableField("introduction"),
    ]

# CoursePage Model
class CoursePage(Page, TranslatableMixin):
    # Banner Section
    banner_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    banner_title = models.CharField(max_length=255, default="English Course")

    # Course Details
    course_overview = RichTextField(blank=True)
    what_you_will_learn = RichTextField(blank=True)
    who_should_enroll = RichTextField(blank=True)

    # Target Learner
    target_learner = models.CharField(
        max_length=50,
        choices=TARGET_LEARNER_CHOICES,
        default='students'
    )

    # ForeignKey to Language
    language = models.ForeignKey(
        Language,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='courses'
    )

    # ForeignKey to Program
    program = models.ForeignKey(
        Program,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='courses'
    )

    # Course Details Grid
    course_duration = models.CharField(max_length=100, default="12 Weeks")
    course_schedule = models.CharField(max_length=100, default="Mon, Wed, Fri - 6:00 PM to 8:00 PM")

    # Content Panels for Wagtail Admin
    content_panels = Page.content_panels + [
        FieldPanel('banner_image'),
        FieldPanel('banner_title'),
        FieldPanel('course_overview'),
        FieldPanel('what_you_will_learn'),
        FieldPanel('who_should_enroll'),
        FieldPanel('target_learner'),
        FieldPanel('language'),
        FieldPanel('program'),
        MultiFieldPanel([
            FieldPanel('course_duration'),
            FieldPanel('course_schedule'),
        ], heading="Course Details"),
    ]

    # Register translatable fields
    translatable_fields = [
         TranslatableField("banner_title"),
         TranslatableField("course_overview"),
         TranslatableField("what_you_will_learn"),
         TranslatableField("who_should_enroll"),
    ]

# HomePage Model
class HomePage(Page, TranslatableMixin):
    # Hero Section
    hero_background_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    hero_heading = models.CharField(max_length=255, blank=True)
    hero_subheading = models.CharField(max_length=255, blank=True)

    palace_language_description = RichTextField(blank=True)

    # Add-Ons Section
    add_ons = StreamField(
        [
            ("add_on", StructBlock([
                ("image_or_video", ImageChooserBlock(required=True)),
                ("title", CharBlock(required=True)),
                ("text", TextBlock(required=True)),
            ]))
        ],
        use_json_field=True,
        blank=True,
    )

    # Testimonials Section
    testimonials = ParentalManyToManyField("home.Testimonial", blank=True)

    # Trusted by Brands Section
    trusted_by_brands = StreamField(
        [
            ("brand", StructBlock([
                ("logo", ImageChooserBlock(required=True)),
                ("name", CharBlock(required=True)),
            ]))
        ],
        use_json_field=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("hero_background_image"),
                FieldPanel("hero_heading"),
                FieldPanel("hero_subheading"),
            ],
            heading="Hero Section",
        ),
        MultiFieldPanel(
            [
                FieldPanel("palace_language_description"),
            ],
            heading="Palace Language Section",
        ),
        MultiFieldPanel(
            [
                FieldPanel("add_ons"),
            ],
            heading="Add-Ons Section",
        ),
        MultiFieldPanel(
            [
                FieldPanel("testimonials"),
            ],
            heading="Testimonials Section",
        ),
        MultiFieldPanel(
            [
                FieldPanel("trusted_by_brands"),
            ],
            heading="Trusted by Brands Section",
        ),
    ]

    # Register translatable fields
    translatable_fields = [
        TranslatableField("hero_heading"),
        TranslatableField("hero_subheading"),
        TranslatableField("palace_language_description"),
        TranslatableField("add_ons") ,
        TranslatableField("trusted_by_brands"),
    ]


