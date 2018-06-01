from django.db import models


class GDB(models.Model):
    def __str__(self):
        return "%s" % self.base_name

    class Meta:
        ordering = ('workspace_type',)
        app_label = 'cloudSync'

    base_name = models.CharField(max_length=255)

    catalog_path = models.CharField(max_length=255, unique=True)

    workspace_type = models.CharField(max_length=25)

    workspace_factory_prog_ID = models.CharField(max_length=255)

    release = models.CharField(max_length=255)

    current_release = models.BooleanField()

    connection_string = models.CharField(max_length=255)


class DomainValues(models.Model):
    def __str__(self):
        return "%s::%s::%s" % (self.name, self.code, self.description)

    class Meta:
        ordering = ('code', 'description')
        app_label = 'cloudSync'

    gdb = models.ForeignKey(
        GDB,
        on_delete=models.CASCADE,
        null=True
    )

    name = models.CharField(max_length=100)

    code = models.CharField(max_length=255)

    description = models.CharField(max_length=255)


class FeatureDataset(models.Model):
    def __str__(self):
        return "%s" % self.base_name

    class Meta:
        ordering = ('base_name',)
        app_label = 'cloudSync'

    gdb = models.ForeignKey(
        GDB,
        on_delete=models.CASCADE,
        null=True
    )

    base_name = models.CharField(max_length=50, unique=True)

    change_tracked = models.BooleanField()

    dataset_type = models.CharField(max_length=25)

    is_versioned = models.BooleanField()

    spatial_reference = models.CharField(max_length=255)

    xy_resolution = models.FloatField()

    z_resolution = models.FloatField()

    pcs_name = models.CharField(max_length=255)

    pcs_code = models.CharField(max_length=100, null=True)

    gcs_code = models.CharField(max_length=100, null=True)

    gcs_name = models.CharField(max_length=255, null=True)


class FeatureClass(models.Model):

    def __str__(self):
        return "%s" % self.base_name

    class Meta:
        ordering = ('base_name', )
        app_label = 'cloudSync'

    feature_dataset = models.ForeignKey(
        FeatureDataset,
        on_delete=models.CASCADE,
        null=True
    )

    catalog_path = models.CharField(max_length=255, unique=True)

    base_name = models.CharField(max_length=255)

    count = models.IntegerField(null=True)

    feature_type = models.CharField(max_length=25)

    hasM = models.BooleanField()

    hasZ = models.BooleanField()

    has_spatial_index = models.BooleanField()

    shape_field_name = models.CharField(max_length=25)

    shape_type = models.CharField(max_length=25)


class FieldObject(models.Model):
    def __str__(self):
        return "%s" % self.name

    class Meta:
        ordering = ('name',)
        app_label = 'cloudSync'

    feature_class = models.ForeignKey(
        FeatureClass,
        on_delete=models.CASCADE,
        null=True
    )

    domain = models.ForeignKey(
        DomainValues,
        on_delete=models.CASCADE,
        null=True
    )

    name = models.CharField(max_length=100, unique=True)

    alias_name = models.CharField(max_length=100)

    base_name = models.CharField(max_length=100)

    percent = models.FloatField()

    default_value = models.CharField(max_length=100, null=True)

    editable = models.BooleanField()

    is_nullable = models.BooleanField()

    length = models.IntegerField()

    precision = models.FloatField()

    required = models.BooleanField()

    scale = models.FloatField()

    type = models.CharField(max_length=50)


class FeatureLayer(models.Model):
    def __str__(self):
        return "%s" % self.name

    class Meta:
        ordering = ('layer_id', 'name',)
        app_label = 'cloudSync'

    current_version = models.CharField(max_length=10)

    layer_id = models.IntegerField()

    name = models.CharField(max_length=100)

    type = models.CharField(max_length=255)

    service_item_id = models.CharField(max_length=255)

    is_view = models.BooleanField()

    is_updatetable_view = models.BooleanField()

    source_schema_changes_allowed = models.BooleanField()

    display_field = models.CharField(max_length=255)

    geometry_type = models.CharField(max_length=100)

    min_scale = models.IntegerField()

    max_scale = models.IntegerField()

    x_min = models.FloatField()

    y_min = models.FloatField()

    x_max = models.FloatField()

    y_max = models.FloatField()

    wkid = models.IntegerField()

    description = models.CharField(max_length=255)

    default_visibility = models.BooleanField()

    supports_append = models.BooleanField()

    supports_calculate = models.BooleanField()

    supports_truncate = models.BooleanField()

    supports_attachments_by_upload_id = models.BooleanField()

    supports_rollback_on_failure = models.BooleanField()

    supports_statistics = models.BooleanField()

    supports_advanced_queries = models.BooleanField()

    supports_validate_sql = models.BooleanField()

    supports_coordinates_quantization = models.BooleanField()

    supports_apply_edits_with_guids = models.BooleanField()

    supports_multi_scale_geo = models.BooleanField()

    has_geo_updates = models.BooleanField()


class WebMap(models.Model):

    def __str__(self):
        return "%s" % self.name

    class Meta:
        ordering = ('name',)
        app_label = 'cloudSync'

    name = models.CharField(max_length=100)

    item_id = models.IntegerField()

    layers = models.ForeignKey(
        FeatureLayer,
        on_delete=models.CASCADE,
        null=True
    )


class PublisherLog(models.Model):
    def __str__(self):
        return "%s" % self.feature_layer

    class Meta:
        ordering = ('feature_layer',)
        app_label = 'cloudSync'

    feature_layer = models.OneToOneField(
        FeatureLayer,
        on_delete=models.CASCADE,
        null=True
    )

    feature_class = models.OneToOneField(
        FeatureClass,
        on_delete=models.CASCADE,
        null=True
    )

    folder = models.CharField(max_length=25)

    timestamp = models.DateField(auto_now=True)


