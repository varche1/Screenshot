Ext.define('Screener.controller.Screens', {
    extend: 'Ext.app.Controller',
    
    views: [
        'screen.List'
    ],
    
    refs: [{
        ref: 'screenList',
        selector: 'screenlist'
    }],
    
    tpl: Ext.create('Ext.XTemplate',
        '<tpl for="ready">',
            '<div class="screenshot {browser} {system}" id="{_id}">',
                '<span><b class="browser browser-{browser}">{version}</b></span>',
                '<span>{resolution}</span>',
                '<a href="{imageUrl}" target="_blank">',
                    '<img src="{thumbUrl}" />',
                '</a>',
            '</div>',
        '</tpl>',
        '<tpl for="wait">',
            '<div class="screenshot {browser} {system}" id="{_id}">',
                '<span><b class="browser browser-{browser}">{version}</b></span>',
                '<span>{resolution}</span>',
                '<img src="{thumbUrl}" />',
            '</div>',
        '</tpl>',
        '<tpl for="update">',
            '<span><b class="browser browser-{browser}">{version}</b></span>',
            '<span>{resolution}</span>',
            '<a href="{imageUrl}" target="_blank">',
                '<img src="{thumbUrl}" />',
            '</a>',
        '</tpl>'
    ),
    
    init: function() {
        this.control({
            'screenlist button[action=filter-os]': {
                click: this.filterScreens
            },
            'screenlist button[action=filter-browser]': {
                click: this.filterScreens
            },
        });
        
        this.application.on({
            screenload: this.onScreensLoad,
            screenUpdate: this.onScreensUpdate,
            scope: this
        });
    },
    
    filterScreens: function(button) {
        var list = Ext.DomQuery.select('.'+button.value);
        var action = !button.pressed ? 'show' : 'hide' ;
        for (i=0,m=list.length; i<m; i++)
            Ext.get(list[i]).setVisibilityMode(2)[action]();
    },
    
    onScreensLoad: function(page) {
        if (!page || !page.get('_id'))
            return;
        
        var self = this;
        Ext.Ajax.request({
            method: 'GET',
            url: '/screen',
            params: { page: page.get('_id') },
            success: function(response){
                (function(){
                    this.updateScreens(Ext.decode(response.responseText));
                }).call(self)
            }
        });
    },
    
    onScreensUpdate: function(data) {
        if (typeof(data) != 'object')
            return;
        
        data = this.prepareData({results: [data]})
        var self = this;
        var view = this.getScreenList();
        Ext.Object.each(data.ready, function(key, value) {
            var screen = Ext.DomQuery.select('#'+value._id);
            if (screen.length)
                self.tpl.overwrite(screen[0], {'update':value});
        });
    },
    
    prepareData: function(data)
    {
        var result = {'wait': [], 'ready': []};
        Ext.each(data.results, function(value, key) {
            value.resolution = value.resolution.replace('_', '*');
            value.imageUrl   = '/image?screen=%s%&type=medium&%rh%'.replace('%s%', value._id).replace('%rh%', value.random_hex);
            value.thumbUrl   = '/image?screen=%s%&type=thumbnail&%rh%'.replace('%s%', value._id).replace('%rh%', value.random_hex);
            
            if (value.ready)
                result.ready.push(value);
            else
                result.wait.push(value);
        });
        return result;
    },
    
    updateScreens: function(data)
    {
        data = this.prepareData(data)
        var self = this;
        var view = this.getScreenList();
        self.tpl.overwrite(view.body, data);
    }
});
