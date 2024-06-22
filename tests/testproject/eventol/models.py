# pylint: disable=arguments-differ
# pylint: disable=too-many-lines

import re

from uuid import uuid4
from random import SystemRandom
from string import digits, ascii_lowercase, ascii_uppercase

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _, gettext_noop as _noop


def validate_url(url):
    if not re.match("^[a-zA-Z0-9-_]+$", url):
        raise ValidationError(_("URL can only contain letters or numbers"))


def generate_ticket_code():
    chars = digits + ascii_lowercase + ascii_uppercase
    length = 21
    return "".join([SystemRandom().choice(chars) for _ in range(length)])


class EventTag(models.Model):
    """A Event grouper"""

    name = models.CharField(
        _("EventTag Name"),
        max_length=50,
        unique=True,
        help_text=_("This name will be used as a slug"),
    )
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)
    background = models.ImageField(
        null=True, blank=True, help_text=_("A image to show in the background of")
    )
    logo_header = models.ImageField(
        null=True,
        blank=True,
        help_text=_("This logo will be shown in the right corner of the page"),
    )
    logo_landing = models.ImageField(
        null=True, blank=True, help_text=_("Logo to show in the center of the page")
    )
    message = models.TextField(
        max_length=280,
        null=True,
        blank=True,
        help_text=_("A message to show in the center of the page"),
    )
    slug = models.SlugField(
        _("URL"), max_length=100, help_text=_("For example: flisol-caba"), unique=True
    )

    def __str__(self):
        return self.name


class Event(models.Model):
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)
    name = models.CharField(_("Event Name"), max_length=50)
    abstract = models.TextField(
        _("Abstract"),
        max_length=250,
        help_text=_(
            "Idea of the event \
                                            (one or two sentences)"
        ),
    )
    limit_proposal_date = models.DateField(
        _("Limit Proposals Date"), help_text=_("Limit date to submit talk proposals")
    )
    registration_closed = models.BooleanField(
        default=False,
        help_text=_("set it to True to force the registration to be closed"),
    )

    tags = models.ManyToManyField(
        EventTag,
        blank=True,
        help_text=_("Select tags to show this event in the EventTag landing"),
    )
    event_slug = models.SlugField(
        _("URL"), max_length=100, help_text=_("For example: flisol-caba"), unique=True
    )
    cname = models.CharField(
        _("CNAME"),
        max_length=50,
        blank=True,
        null=True,
        help_text=_("For example: flisol-caba"),
        validators=[validate_url],
    )
    registration_code = models.UUIDField(
        default=uuid4,
        editable=False,
        unique=True,
        verbose_name=_("code"),
        help_text=_("Code validator for in-place event self-registration"),
    )
    external_url = models.URLField(
        _("External URL"),
        blank=True,
        null=True,
        default=None,
        help_text=_("http://www.my-awesome-event.com"),
    )
    email = models.EmailField(verbose_name=_("Email"))
    schedule_confirmed = models.BooleanField(_("Schedule Confirmed"), default=False)
    use_installations = models.BooleanField(_("Use Installations"), default=True)
    use_installers = models.BooleanField(_("Use Installers"), default=True)
    use_collaborators = models.BooleanField(_("Use Collaborators"), default=True)
    use_proposals = models.BooleanField(_("Use Proposals"), default=True)
    use_talks = models.BooleanField(_("Use Talks"), default=True)
    is_flisol = models.BooleanField(_("Is FLISoL"), default=False)
    use_schedule = models.BooleanField(_("Use Schedule"), default=True)
    place = models.TextField(_("Place"), null=True, blank=True)
    template = models.FileField(
        _("Template"),
        upload_to="templates",
        blank=True,
        null=True,
        help_text=_("Custom template HTML for event index page"),
    )
    css_custom = models.FileField(
        _("Custom CSS"),
        upload_to="custom_css",
        blank=True,
        null=True,
        help_text=_("Custom CSS file for event page"),
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = _("Event")
        verbose_name_plural = _("Events")


class EventDate(models.Model):
    event = models.ForeignKey(
        Event,
        verbose_name=_noop("Event"),
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    date = models.DateField(_("Date"), help_text=_("When will your event be?"))

    def __str__(self):
        return "{} - {}".format(self.event, self.date)

    class Meta:
        verbose_name = _("Event Date")
        verbose_name_plural = _("Event Dates")


class ContactMessage(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Name"))
    email = models.EmailField(verbose_name=_("Email"))
    message = models.TextField(verbose_name=_("Message"))
    event = models.ForeignKey(
        Event,
        verbose_name=_noop("Event"),
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return _noop(
            "Message received from: {name}\n" "User email: {email}\n\n" "{message}"
        ).format(name=self.name, email=self.email, message=self.message)

    class Meta:
        verbose_name = _("Contact Message")
        verbose_name_plural = _("Contact Messages")


class ContactType(models.Model):
    """
    For example:
        Name: Facebook
        Icon Class: fa-facebook-square
    """

    validator_choices = (
        ("1", _("Validate URL")),
        ("2", _("Validate Email")),
        ("3", _("Don't validate")),
    )
    name = models.CharField(_("Name"), unique=True, max_length=200)
    icon_class = models.CharField(_("Icon Class"), max_length=200)
    validate = models.CharField(
        _("Level"),
        choices=validator_choices,
        max_length=10,
        help_text=_("Type of field validation"),
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Contact Type")
        verbose_name_plural = _("Contact Types")


class Contact(models.Model):
    type = models.ForeignKey(
        ContactType, verbose_name=_("Contact Type"), on_delete=models.CASCADE
    )
    url = models.CharField(
        _noop("Direccion"),
        help_text=_("i.e. https://twitter.com/flisol"),
        max_length=200,
    )
    text = models.CharField(_("Text"), max_length=200, help_text=_("i.e. @Flisol"))
    event = models.ForeignKey(
        Event,
        verbose_name=_noop("Event"),
        related_name="contacts",
        blank=True,
        null=False,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return "{} - {} - {}".format(self.event, self.type, self.text)

    class Meta:
        verbose_name = _("Contact")
        verbose_name_plural = _("Contacts")


class Ticket(models.Model):
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)
    sent = models.BooleanField(_("Sent"), default=False)
    code = models.CharField(
        max_length=21,
        default=generate_ticket_code,
        editable=False,
        unique=True,
        verbose_name=_("number"),
        help_text=_("Unique identifier for the ticket"),
    )

    def __str__(self):
        return self.code


class EventUser(models.Model):
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)
    user = models.ForeignKey(
        User, verbose_name=_("User"), blank=True, null=True, on_delete=models.CASCADE
    )
    event = models.ForeignKey(Event, verbose_name=_("Event"), on_delete=models.CASCADE)
    ticket = models.ForeignKey(
        Ticket,
        verbose_name=_("Ticket"),
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        if self.user:
            return "{} at event:{}".format(self.user.username, self.event)
        return "{}".format(self.event)

    class Meta:
        unique_together = (("event", "user"),)
        verbose_name = _("Event User")
        verbose_name_plural = _("Event Users")


class EventUserAttendanceDate(models.Model):
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)
    event_user = models.ForeignKey(
        EventUser,
        verbose_name=_noop("Event User"),
        blank=False,
        null=False,
        on_delete=models.CASCADE,
    )
    date = models.DateTimeField(
        _("Date"), help_text=_("The date of the attendance"), auto_now_add=True
    )
    attendance_mode_choices = (
        ("1", _("Qr autoregistration")),
        ("2", _("Qr ticket")),
        ("3", _("Previous registration")),
        ("4", _("unregistred")),
    )
    mode = models.CharField(
        _("Mode"),
        choices=attendance_mode_choices,
        max_length=200,
        blank=True,
        null=True,
        help_text=_("Attendance mode"),
    )

    def __str__(self):
        return "{} - {}".format(self.event_user, self.date)


class Collaborator(models.Model):
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)
    event_user = models.ForeignKey(
        EventUser,
        verbose_name=_("Event User"),
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    assignation = models.CharField(
        _("Assignation"),
        max_length=200,
        blank=True,
        null=True,
        help_text=_(
            "Anything you can help with \
                                               (i.e. Talks, Coffee…)"
        ),
    )
    time_availability = models.CharField(
        _("Time Availability"),
        max_length=200,
        blank=True,
        null=True,
        help_text=_(
            'Time period in which you can \
                                                     help during the event. i.e. \
                                                     "All the event", "Morning", \
                                                     "Afternoon", …'
        ),
    )
    phone = models.CharField(_("Phone"), max_length=200, blank=True, null=True)
    address = models.CharField(_("Address"), max_length=200, blank=True, null=True)
    additional_info = models.CharField(
        _("Additional Info"),
        max_length=200,
        blank=True,
        null=True,
        help_text=_("Additional info you consider relevant"),
    )

    class Meta:
        verbose_name = _("Collaborator")
        verbose_name_plural = _("Collaborators")

    def __str__(self):
        return str(self.event_user)


class Organizer(models.Model):
    """Event organizer"""

    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)
    event_user = models.ForeignKey(
        EventUser,
        verbose_name=_("Event User"),
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = _("Organizer")
        verbose_name_plural = _("Organizers")

    def __str__(self):
        return str(self.event_user)


class Reviewer(models.Model):
    """User that collaborates with activities review"""

    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)
    event_user = models.ForeignKey(
        EventUser,
        verbose_name=_("Event User"),
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return str(self.event_user)


class Attendee(models.Model):
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)
    first_name = models.CharField(
        _("First Name"), max_length=200, blank=True, null=True
    )
    last_name = models.CharField(_("Last Name"), max_length=200, blank=True, null=True)
    nickname = models.CharField(_("Nickname"), max_length=200, blank=True, null=True)
    email = models.EmailField(_("Email"))
    event = models.ForeignKey(Event, verbose_name=_("Event"), on_delete=models.CASCADE)
    ticket = models.ForeignKey(
        Ticket,
        verbose_name=_("Ticket"),
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    is_installing = models.BooleanField(_("Is going to install?"), default=False)
    additional_info = models.CharField(
        _("Additional Info"),
        max_length=200,
        blank=True,
        null=True,
        help_text=_(
            "Additional info you consider \
                                                   relevant to the organizers"
        ),
    )
    email_confirmed = models.BooleanField(_("Email confirmed?"), default=False)
    email_token = models.CharField(
        _("Confirmation Token"), max_length=200, blank=True, null=True
    )
    registration_date = models.DateTimeField(
        _("Registration Date"), blank=True, null=True
    )
    event_user = models.ForeignKey(
        EventUser,
        verbose_name=_noop("Event User"),
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = _("Attendee")
        verbose_name_plural = _("Attendees")
        unique_together = (("event", "email"),)

    def __str__(self):
        if self.event_user:
            return str(self.event_user)
        return "{} - {} {} - {} - {}".format(
            self.event, self.first_name, self.last_name, self.nickname, self.email
        )


class AttendeeAttendanceDate(models.Model):
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)
    attendee = models.ForeignKey(
        Attendee,
        verbose_name=_noop("Attendee"),
        blank=False,
        null=False,
        on_delete=models.CASCADE,
    )
    date = models.DateTimeField(
        _("Date"), help_text=_("The date of the attendance"), auto_now_add=True
    )
    attendance_mode_choices = (
        ("1", _("Qr autoregistration")),
        ("2", _("Qr ticket")),
        ("3", _("Previous registration")),
        ("4", _("unregistred")),
    )
    mode = models.CharField(
        _("Mode"),
        choices=attendance_mode_choices,
        max_length=200,
        blank=True,
        null=True,
        help_text=_("Attendance mode"),
    )

    def __str__(self):
        return "{} - {}".format(self.attendee, self.date)


class InstallationMessage(models.Model):
    event = models.ForeignKey(
        Event, verbose_name=_noop("Event"), on_delete=models.CASCADE
    )
    contact_email = models.EmailField(verbose_name=_("Contact Email"))

    class Meta:
        verbose_name = _("Post-install Email")
        verbose_name_plural = _("Post-install Emails")

    def __str__(self):
        return str(self.event)


class Installer(models.Model):
    installer_choices = (
        ("1", _("Beginner")),
        ("2", _("Medium")),
        ("3", _("Advanced")),
        ("4", _("Super Hacker")),
    )
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)
    event_user = models.ForeignKey(
        EventUser,
        verbose_name=_("Event User"),
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    level = models.CharField(
        _("Level"),
        choices=installer_choices,
        max_length=200,
        help_text=_("Knowledge level for an installation"),
    )

    class Meta:
        verbose_name = _("Installer")
        verbose_name_plural = _("Installers")

    def __str__(self):
        return str(self.event_user)


class Software(models.Model):
    software_choices = (
        ("OS", _("Operative System")),
        ("AP", _("Application")),
        ("SU", _("Support and Problem Fixing")),
        ("OT", _("Other")),
    )
    name = models.CharField(_("Name"), max_length=200)
    type = models.CharField(_("Type"), choices=software_choices, max_length=200)

    def __str__(self):
        return "{} - {}".format(self.type, self.name)


class Hardware(models.Model):
    hardware_choices = (
        ("MOB", _("Mobile")),
        ("NOTE", _("Notebook")),
        ("NET", _("Netbook")),
        ("TAB", _("Tablet")),
        ("DES", _("Desktop")),
        ("OTH", _("Other")),
    )
    type = models.CharField(_("Type"), choices=hardware_choices, max_length=200)
    manufacturer = models.CharField(
        _("Manufacturer"), max_length=200, blank=True, null=True
    )
    model = models.CharField(_("Model"), max_length=200, blank=True, null=True)

    def __str__(self):
        return "{}, {}, {}".format(self.type, self.manufacturer, self.model)


class Room(models.Model):
    event = models.ForeignKey(
        Event,
        verbose_name=_noop("Event"),
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    name = models.CharField(
        _("Name"), max_length=200, help_text=_("i.e. Classroom 256")
    )

    def __str__(self):
        return "{} - {}".format(self.event, self.name)

    class Meta:
        verbose_name = _("Room")
        verbose_name_plural = _("Rooms")
        ordering = ["name"]


class ActivityType(models.Model):
    """User created type of activities"""

    name = models.CharField(max_length=60, help_text=_("Kind of activity"))

    def __str__(self):
        return self.name


class Activity(models.Model):
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)
    event = models.ForeignKey(Event, verbose_name=_("Event"), on_delete=models.CASCADE)
    owner = models.ForeignKey(
        EventUser,
        help_text=_("Speaker or the person in charge of the activity"),
        on_delete=models.CASCADE,
    )
    title = models.CharField(_("Title"), max_length=100, blank=False, null=False)
    long_description = models.TextField(_("Long Description"))
    abstract = models.TextField(
        _("Abstract"), help_text=_("Short idea of the talk (Two or three sentences)")
    )
    justification = models.TextField(
        _("Justification"),
        blank=True,
        null=True,
        help_text=_("Why do you reject this proposal?"),
    )
    room = models.ForeignKey(
        Room, verbose_name=_("Room"), blank=True, null=True, on_delete=models.CASCADE
    )
    start_date = models.DateTimeField(_("Start Time"), blank=True, null=True)
    end_date = models.DateTimeField(_("End Time"), blank=True, null=True)
    activity_type = models.ForeignKey(
        ActivityType, verbose_name=_("Activity Type"), on_delete=models.CASCADE
    )
    speakers_names = models.CharField(
        _("Speakers Names"),
        max_length=600,
        help_text=_("Comma separated speaker names"),
    )
    speaker_bio = models.TextField(
        _("Speaker Bio"),
        null=True,
        help_text=_('Tell us about you (we will use it as your "bio" in our website)'),
    )
    labels = models.CharField(
        _("Labels"),
        max_length=200,
        help_text=_(
            "Comma separated tags. i.e. Linux, \
                                          Free Software, Devuan"
        ),
    )
    presentation = models.FileField(
        _("Presentation"),
        upload_to="talks",
        blank=True,
        null=True,
        help_text=_(
            "Material you are going to use \
                                                for the talk (optional, but recommended)"
        ),
    )
    level_choices = (
        ("1", _("Beginner")),
        ("2", _("Medium")),
        ("3", _("Advanced")),
    )
    level = models.CharField(
        _("Level"),
        choices=level_choices,
        max_length=100,
        help_text=_("Talk's Technical level"),
    )
    additional_info = models.TextField(
        _("Additional Info"),
        blank=True,
        null=True,
        help_text=_(
            "Info you consider relevant \
                                                   to the organizer, special \
                                                   activity requirements, etc."
        ),
    )

    status_choices = (
        ("1", _("Proposal")),
        ("2", _("Accepted")),
        ("3", _("Rejected")),
    )

    status = models.CharField(
        _("Status"),
        choices=status_choices,
        max_length=20,
        help_text=_("Activity proposal status"),
    )

    is_dummy = models.BooleanField(
        _("Is a dummy Activity?"),
        default=False,
        help_text=_(
            "A dummy activity is used for example for coffee \
                                               breaks. We use this to exclude it from the index \
                                               page and other places"
        ),
    )

    def __str__(self):
        return "{} - {}".format(self.event, self.title)

    class Meta:
        ordering = ["title"]
        verbose_name = _("Activity")
        verbose_name_plural = _("Activities")


class Installation(models.Model):
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)
    hardware = models.ForeignKey(
        Hardware,
        verbose_name=_("Hardware"),
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    software = models.ForeignKey(
        Software,
        verbose_name=_("Software"),
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    attendee = models.ForeignKey(
        Attendee,
        verbose_name=_("Attendee"),
        help_text=_("The owner of the installed hardware"),
        on_delete=models.CASCADE,
    )
    installer = models.ForeignKey(
        EventUser,
        verbose_name=_("Installer"),
        related_name="installed_by",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    notes = models.TextField(
        _("Notes"),
        blank=True,
        null=True,
        help_text=_(
            "Info or trouble you \
                                         consider relevant to document"
        ),
    )

    def __str__(self):
        return "{}, {}, {}".format(self.attendee, self.hardware, self.software)

    class Meta:
        verbose_name = _("Installation")
        verbose_name_plural = _("Installations")


class EventolSetting(models.Model):
    background = models.ImageField(
        null=True, blank=True, help_text=_("A image to show in the background of")
    )
    logo_header = models.ImageField(
        null=True,
        blank=True,
        help_text=_("This logo will be shown in the right corner of the page"),
    )
    logo_landing = models.ImageField(
        null=True, blank=True, help_text=_("Logo to show in the center of the page")
    )
    message = models.TextField(
        max_length=280,
        null=True,
        blank=True,
        help_text=_("A message to show in the center of the page"),
    )

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return "eventol configuration"

    class Meta:
        verbose_name = _("eventol setting")
        verbose_name_plural = _("eventol settings")
