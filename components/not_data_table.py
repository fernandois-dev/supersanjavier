import flet as ft

class NotDataTableHeader(ft.Container):
    def __init__(self, data, model, is_chk_column_enabled = True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_chk_column_enabled = is_chk_column_enabled
        self.content= None
        self.bgcolor=ft.Colors.with_opacity(1, ft.Colors.SECONDARY_CONTAINER)
        self.height=45
        self._dict = {}
        
        self.bg_color_prin = ft.Colors.with_opacity(1, ft.Colors.SECONDARY_CONTAINER)
        self.bg_color_sec = ft.Colors.with_opacity(0.1, ft.Colors.SECONDARY)
        self.on_click_column = None
        self.handle_all_row_selected = None
        self._data = data
        self._model = model
        
        self.chk_column = ft.Checkbox(label="", value=False, width=40, tristate=True, on_change=lambda e: self.handle_all_row_selected(e))
    
    def build_header(self):
        list_header_row = []
            # HEADERS
        if not list_header_row:
            if self.is_chk_column_enabled: list_header_row.append(self.chk_column)
            for col in self._model._meta.fields:
                sort = getattr(col, "is_sortable", False)
                if not col.hidden:
                    order_col = ""
                    for key in self._dict:
                        if key == col.name:
                            order_col = f'{key}-{self._dict[key]}'
                        
                    # HEADER ALIGMENT    
                    if "BooleanField" in type(col).__name__:
                        header_aligment = ft.MainAxisAlignment.CENTER
                    elif "IntegerField" in type(col).__name__ :
                        header_aligment = ft.MainAxisAlignment.END
                    else:
                        header_aligment = ft.MainAxisAlignment.START
                        
                           
                    if sort:
                        if "desc" in order_col:
                            icon = ft.Icon("arrow_drop_down")
                        else:
                            icon = ft.Icon("arrow_drop_up")
                        
                        text_header = ft.Container(content=
                                            ft.Row(controls=[
                                                ft.Text(col.verbose_name, weight="bold", expand=True), 
                                                icon
                                            ], 
                                            alignment=header_aligment), 
                                            margin=ft.margin.symmetric(horizontal=5)
                                        )
                    else:
                        text_header = ft.Container(content=
                                        ft.Row(controls=[
                                            ft.Text(col.verbose_name, weight="bold"),                                       
                                        ],
                                        alignment=header_aligment
                                        ),
                                    margin=ft.margin.symmetric(horizontal=5),
                                    expand=True,
                                    
                                    )
                        
                    
                    if "BooleanField" in type(col).__name__:
                        list_header_row.append(ft.Container(text_header, 
                                                            expand=1, alignment=ft.alignment.center, 
                                                            on_hover= (lambda e: on_hover(e)) if sort else None,
                                                            on_click= (lambda e: on_click(e)) if sort else None,
                                                            data=col.name,
                                                            bgcolor= self.bg_color_sec if col.name in order_col else self.bg_color_prin,
                                                            ))
                    elif "IntegerField" in type(col).__name__ :
                        list_header_row.append(ft.Container(text_header, 
                                                            on_hover= (lambda e: on_hover(e)) if sort else None,
                                                            on_click= (lambda e: on_click(e)) if sort else None,
                                                            expand=1, 
                                                            data=col.name,
                                                            alignment=ft.alignment.center_right,
                                                            bgcolor= self.bg_color_sec if col.name in order_col else self.bg_color_prin,
                                                            ))
                    else:
                        list_header_row.append(ft.Container(text_header, 
                                                            on_hover= (lambda e: on_hover(e)) if sort else None,
                                                            on_click= (lambda e: on_click(e)) if sort else None,
                                                            expand=1,
                                                            data=col.name,
                                                            padding=ft.padding.symmetric(horizontal=5),
                                                            alignment=ft.alignment.center_left,
                                                            bgcolor= self.bg_color_sec if col.name in order_col else self.bg_color_prin,
                                                            ))
    
        self.content= ft.Row(controls=list_header_row)

        
        def on_hover(e):
            else_color = None
            if e.control.data in self._dict:
                else_color= ft.Colors.with_opacity(0.1, ft.Colors.SECONDARY)
            else:
                else_color= ft.Colors.with_opacity(1, ft.Colors.SECONDARY_CONTAINER)
                
            e.control.bgcolor = ft.Colors.with_opacity(0.1, ft.Colors.SECONDARY) if e.data == "true" else else_color
            e.control.update()
                
        def on_click(e):
            if e.control.data in self._dict:
                if self._dict[e.control.data] == "asc":
                    self._dict[e.control.data] = "desc"
                else:
                    self._dict[e.control.data] = "asc"
            else:
                self._dict = {}
                self._dict[e.control.data] = "desc"
            self.build_header()
            self.update()
            if self.on_click_column:
                self.on_click_column(self._dict)
                
    def manage_chk_header(self, len_list_rows_selected, len_rows):
        if(len_list_rows_selected == len_rows):
                self.chk_column.value = True
        elif(len_list_rows_selected == 0):
            self.chk_column.value = False
        else:
            self.chk_column.value = None
        self.chk_column.update()
                

class NotDataTable(ft.Column):
    def __init__(self, is_chk_column_enabled = True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expand = True
        self.headers = []
        self.rows = []
        self.spacing=0
        self._data = None
        self._model = None
        self.is_chk_column_enabled = is_chk_column_enabled
        self.on_row_selected = None
        self.on_long_press = None
        self.on_click_column = None
        self.controls = []
        self.dict_order = {}
        
        self.not_headers= None
        self.chk_column = None
        
        self.component_header = None
        self.component_body = ft.Column(controls=[], spacing=0)
        
    def set_data(self, data):
        self._data = data
        
    def set_model(self, model):
        self._model = model
        
    def build_header(self):
        self.component_header = NotDataTableHeader(is_chk_column_enabled=self.is_chk_column_enabled, data=self._data, model=self._model)
        self.component_header.on_click_column = self.on_click_column
        self.component_header.handle_all_row_selected = self.handle_all_row_selected
        self.component_header.build_header()
    
    def build_body(self):
        self.rows = []
        list_data_row = []
        for idx, obj in enumerate(self._data):
            list_data_row.append(self.make_row(idx, obj))
        self.component_body.controls=list_data_row
        
    def update_body(self):
        self.component_body.update()
        
    def create_table(self):
        self.build_header()
        self.build_body()
        self.controls = [self.component_header, self.component_body]
            
    def make_row(self, idx, obj):
        list_data_cell = []
        self.chk_column = ft.Checkbox(value= False, width=40, on_change=lambda e: handle_row_selected(e), data=obj)
        if self.is_chk_column_enabled: list_data_cell.append(self.chk_column)
        for col in obj._meta.fields:
            value = getattr(obj, col.name)
            if not col.hidden:
                if "BooleanField" in type(col).__name__:
                    list_data_cell.append(ft.Container(content=ft.Checkbox(value= value, disabled=True), expand=1, alignment=ft.alignment.center))
                elif "IntegerField" in type(col).__name__ :
                    list_data_cell.append(
                        ft.Container(ft.Text("{:,}".format(value).replace(",", ".") if value is not None else ""), expand=1, alignment=ft.alignment.center_right))
                else:
                    list_data_cell.append(ft.Container(ft.Text(value), expand=1, alignment=ft.alignment.center_left))
                        
        self.rows.append(list_data_cell)
            
        def handle_row_selected(e):
            list_rows_selected = self.list_rows_selected()
            self.component_header.manage_chk_header(len(list_rows_selected), len(self.rows))
        
            if self.on_row_selected:
                self.on_row_selected(list_rows_selected)
                
            e.control.update()
        
        row_container = ft.Container(content= ft.Row(controls=list_data_cell ),
            height=40,
            border = ft.border.only(bottom=ft.border.BorderSide(1, ft.Colors.with_opacity(0.2 , ft.Colors.ON_SURFACE_VARIANT))),
            bgcolor=ft.Colors.with_opacity(0.0 if idx%2 == 0 else 0.3  , ft.Colors.SECONDARY_CONTAINER),
            key=idx,
            on_long_press= lambda e: self.handle_long_press(obj),
            data=obj.id)
        def on_hover(e):
            row_container.bgcolor =  ft.Colors.with_opacity(0.8, ft.Colors.SECONDARY_CONTAINER) if e.data == "true" else ft.Colors.with_opacity(0.1 if e.control.key%2 == 0 else 0.4  , ft.Colors.SECONDARY_CONTAINER)
            row_container.update()
        row_container.on_hover = lambda e: on_hover(e)      
        
        return row_container
    
    def list_rows_selected(self):
        return [row[0].data for row in self.rows if row[0].value]
        
    def get_container_header (self, controls):
        header_row = ft.Container(
            content= ft.Row(controls=controls),
            bgcolor=ft.Colors.with_opacity(1, ft.Colors.SECONDARY_CONTAINER),
            height=45,
        )
        return header_row
    
    def get_container_body (self, controls):
        header_row = ft.Container(
            content= ft.Row(controls=controls),
            bgcolor=ft.Colors.with_opacity(1, ft.Colors.SECONDARY_CONTAINER),
            height=40,
        )
        return header_row
        
    def handle_all_row_selected(self, e):
        if e.control.value == None:
            e.control.value = False
            e.control.update()
            
        if e.control.value:
            for row in self.rows:
                row[0].value = True
                row[0].update()
        else:
            for row in self.rows:
                row[0].value = False
                row[0].update()
                
        list_rows_selected = self.list_rows_selected()
        if self.on_row_selected:
            self.on_row_selected(list_rows_selected)
        
    def handle_long_press(self, obj):
        if self.on_long_press:
            self.on_long_press(obj)
        
    def clean_selection(self):
        for row in self.rows:
            row[0].value = False
        self.update()