import re
from collections import defaultdict

from django.db import models
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.images import get_image_model
from wagtail.fields import RichTextField
from wagtail.models import Orderable, Page, ClusterableModel

ImageModel = get_image_model()


class PhotoGalTag(TaggedItemBase):
    content_object = ParentalKey('photogal.PhotoGal', on_delete=models.CASCADE, related_name='gal_photo_tags')


class PhotoGal(Page):

    gallery_image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.SET_NULL, related_name='+', null=True
    )
    intro = RichTextField(blank=True)
    detail = RichTextField(blank=True)

    photo_tags = ClusterTaggableManager(through=PhotoGalTag, blank=True)
    photo_name_re = models.CharField(max_length=250, blank=True, null=True)

    def get_context(self, request):
        context = super().get_context(request)

        # print(self.photo_tags.all())

        tag_ids = [tag.id for tag in self.photo_tags.all()]
        images = self._dedup(ImageModel.objects.filter(tags__in=tag_ids))
        if self.photo_name_re:
            photo_name_re = re.compile(self.photo_name_re)
            images = [img for img in images if photo_name_re.match(img.title)]
            images = self._dedup(ImageModel.objects.filter(tags__in=tag_ids))

        photo_rows = self._group(images)
        # print(photo_rows)
        context["photo_rows"] = photo_rows

        return context

    def _dedup(self, images) -> list:
        d = {image.id: image for image in images}
        return list(d.values())

    def _group(self, images: list) -> list[tuple, str, str]:
        groupped_images = []
        dates = []
        captions = []
        img_count = 0
        for row in self.gallery_row.all():
            title_re = re.compile(row.title_re)
            row_images = [img for img in images if title_re.match(img.title)]
            row_images = sorted(row_images, key=lambda img: img.title)
            groupped_images.append(row_images)
            img_count = max(img_count, len(row_images))
            dates.append(row.date)
            captions.append(row.caption)
        fill = [None] * img_count
        groupped_images = [tuple((row_images + fill)[:img_count]) for row_images in groupped_images]
        return list(zip(groupped_images, captions, dates))


    content_panels = Page.content_panels + [
        FieldPanel('gallery_image'),
        FieldPanel('intro'),
        FieldPanel('detail'),
        MultiFieldPanel([
            FieldPanel('photo_tags'),
            FieldPanel('photo_name_re'),
        ]),
        InlinePanel('gallery_row', label="Gallery photos"),
    ]


class PhotoGalRow(Orderable):
    page = ParentalKey(PhotoGal, on_delete=models.CASCADE, related_name='gallery_row')
    title_re = models.CharField(blank=True, max_length=127)
    caption = RichTextField(blank=True)
    date = models.CharField(blank=True, max_length=127)

    panels = [
        FieldPanel('title_re'),
        FieldPanel('caption'),
        FieldPanel('date'),
    ]

class PhotoGalIndex(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro')
    ]
