class BootstrapFormMixin:
    def bootstrapfy_fields(self, fields):
        for field in fields:
            class_attr = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = ("form-control " + class_attr).strip()

    def invalid_field(self, field):
        field.widget.attrs["class"] += " is-invalid"

    def valid_field(self, field):
        field.widget.attrs["class"] += " is-valid"
