from django.conf import settings
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from django.utils.functional import cached_property
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import (
    FieldPanel,
    InlinePanel,
    MultiFieldPanel,
    StreamFieldPanel,
)
from wagtail.core.fields import StreamField
from wagtail.images.edit_handlers import ImageChooserPanel

from learning_equality.utils.blocks import StoryBlock
from learning_equality.utils.models import BasePage
from .choices import PersonType


class SocialMediaProfile(models.Model):
    person_page = ParentalKey("PersonPage", related_name="social_media_profile")
    site_titles = (("twitter", "Twitter"), ("linkedin", "LinkedIn"))
    site_urls = (
        ("twitter", "https://twitter.com/"),
        ("linkedin", "https://www.linkedin.com/in/"),
    )
    service = models.CharField(max_length=200, choices=site_titles)
    username = models.CharField(max_length=255)

    @property
    def profile_url(self):
        return dict(self.site_urls)[self.service] + self.username

    def clean(self):
        if self.service == "twitter" and self.username.startswith("@"):
            self.username = self.username[1:]


class PersonPagePhoneNumber(models.Model):
    page = ParentalKey("PersonPage", related_name="phone_numbers")
    phone_number = models.CharField(max_length=255)

    panels = [FieldPanel("phone_number")]


class PersonPage(BasePage):

    template = "patterns/pages/people/person_page.html"

    subpage_types = []
    parent_page_types = ["PersonIndexPage"]

    photo = models.ForeignKey(
        "images.CustomImage",
        null=True,
        blank=True,
        related_name="+",
        on_delete=models.SET_NULL,
    )
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    person_type = models.CharField(
        choices=PersonType.choices,
        max_length=255,
        null=True,
        blank=True,
    )
    job_title = models.CharField(max_length=255)
    biography = models.TextField(blank=True)
    email = models.EmailField(blank=True)

    content_panels = BasePage.content_panels + [
        MultiFieldPanel(
            [FieldPanel("first_name"), FieldPanel("last_name")], heading="Name"
        ),
        ImageChooserPanel("photo"),
        FieldPanel("person_type"),
        FieldPanel("job_title"),
        FieldPanel("biography"),
    ]


class PersonIndexPage(BasePage):
    template = "patterns/pages/people/person_index_page.html"

    subpage_types = ["PersonPage"]
    parent_page_types = ["home.HomePage"]

    @cached_property
    def people(self):
        return PersonPage.objects.child_of(self).live().specific().live().public()
        # return self.get_children().specific().live().public()

    def get_context(self, request, *args, **kwargs):
        page_number = request.GET.get("page")
        paginator = Paginator(self.people, settings.DEFAULT_PER_PAGE)
        people = (
            PersonPage.objects.live()
            .public()
            .descendant_of(self)
        )

        if request.GET.get('person_type'):
            if request.GET.get("person_type") == "all" or request.GET.get("person_type") is None:
                pass
            else:
                people = people.filter(person_type=request.GET.get("person_type"))

        # try:
        #     people = paginator.page(page_number)
        # except PageNotAnInteger:
        #     people = paginator.page(1)
        # except EmptyPage:
        #     people = paginator.page(paginator.num_pages)

        person_types = PersonType.choices


        context = super().get_context(request, *args, **kwargs)
        context.update(people=people, person_types=person_types)

        return context
