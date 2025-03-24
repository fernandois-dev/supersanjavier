class Conditions:
    def __init__(self, fields=None, fields_excluded=None, fields_readonly=None, overrides_input_type=None, overrides_view_type=None, 
                 filter=None, related_objects=None, fields_order=None, fields_expand=None, fields_calculations=None):
        self.fields = fields or []
        self.fields_excluded = fields_excluded or []
        self.fields_readonly = fields_readonly or []
        self.fields_order = fields_order or []
        self.fields_expand = fields_expand or {}
        self.overrides_input_type = overrides_input_type or {}
        self.overrides_view_type = overrides_view_type or {}
        self.filter = filter or []
        self.related_objects = related_objects or {}
        self.fields_calculations = fields_calculations or {}

    def init_from_dict(self, data):
        self.fields = data.get('fields', [])
        self.fields_excluded = data.get('fields_excluded', [])
        self.fields_readonly = data.get('fields_readonly', [])
        self.fields_order = data.get('fields_order', [])
        self.fields_expand = data.get('fields_expand', {})
        self.overrides_input_type = data.get('overrides_input_type', {})
        self.overrides_view_type = data.get('overrides_view_type', {})
        self.display_mode = data.get('display_mode', {})
        self.filter = data.get('filter', [])
        self.related_objects = data.get('related_objects', {})
        self.fields_calculations = data.get('fields_calculations', {})
        
    # def to_dict(self):
    #     return {
    #         'fields': self.fields,
    #         'fields_excluded': self.fields_excluded,
    #         'fields_readonly': self.fields_readonly,
    #         'fields_order': self.fields_order,
    #         'fields_expand': self.fields_expand,
    #         'display_mode': self.display_mode,
    #         'filter': self.filter,
    #         'related_objects': self.related_objects
    #     }